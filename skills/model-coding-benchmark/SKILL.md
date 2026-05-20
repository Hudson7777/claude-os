---
name: model-coding-benchmark
description: 评测大语言模型的编程能力。对多个模型运行标准化编程任务（代码生成/工具调用/Debug/代码理解/重构/综合实战），自动计时，多模型盲评聚合打分，输出排名报告。触发词：评测模型编程能力、模型编程对比、编程能力评测、model coding benchmark、coding benchmark、哪个模型写代码更强。不用于：代码性能分析、非编程类模型评测（写作/数学）。支持分层任务（核心6题必做保证可比性 + 可选扩展题）和3盲评聚合。
argument-hint: <model1> <model2> [model3...] [--evaluators kimi,gpt-5.4,sonnet] [--timeout 600]
---

# 模型编程能力评测

## 何时使用

- 用户想评测或对比多个模型的编程能力
- 用户提到 "benchmark"、"评测模型"、"模型对比"、"编程能力"
- 新模型上线后需要评估

## 不应触发

- 单纯询问模型能力（非对比评测）
- 非编程类评测（数学、写作等）

## 前置条件

- 已安装 `claude` CLI（或通过 `CLAUDE_CLI` 环境变量指定路径）
- Python 3.9+
- 足够 token 额度：6题 × N模型（agent 模式，每题消耗远高于 --print 模式）+ N次盲评
- 注意：agent 模式下单题耗时 2-20 分钟，总评测时间约 1-3 小时

## 参数解析

从用户输入提取：

| 参数 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| models | 是 | - | 2个以上模型名，如 glm-5.1 sonnet gpt-5.4 |
| --evaluators | 否 | kimi,gpt-5.4,sonnet | 盲评模型列表，逗号分隔，至少1个 |
| --timeout | 否 | 600 | 单任务超时秒数 |
| --output | 否 | /tmp/model-benchmark-{YYMMDD-HHMM} | 输出目录 |

## 工作流程

按以下步骤严格执行，每步完成后再进入下一步。

### Step 1: 初始化

1. 创建输出目录 `OUTPUT_DIR`
2. 读取 `references/tasks-core.md`，将每个任务的 prompt 写入 `OUTPUT_DIR/prompts/T{n}.txt`
3. 每个任务 prompt 前加前缀：`请直接执行所有步骤，不要问我任何问题，不要等待确认。`
4. 每个任务 prompt 后加后缀：`完成后运行验证。`
5. 复制 `references/workspace/` 下的源文件到各模型工作区
   - T2 工作区额外复制 `verify_t2.py`
   - T3 工作区额外复制 `verify_t3.py`
   - T5 工作区额外复制 `verify_t5.py`
   - T6 工作区额外复制 `verify_t6.py`
6. 生成随机匿名映射（X/Y/Z/A/B/C...），记录到 `OUTPUT_DIR/mapping.txt`
   - 映射必须随机，不要按模型名字母序

### Step 2: 执行核心任务

对每个模型执行6个核心任务。**可并行不同模型，同模型内串行**。

每个任务的执行方式（agent 模式）：

```bash
python3 scripts/run_task.py \
  --model {model} \
  --task-n {n} \
  --workspace OUTPUT_DIR/ws_{model}_{n} \
  --output OUTPUT_DIR/results/{model}__T{n}.txt \
  --output-dir OUTPUT_DIR \
  --timeout {timeout}
```

`run_task.py` 会自动：
1. 将任务说明写入工作区的 `TASK.md`
2. 以 agent 模式启动 `${CLAUDE_CLI:-claude} --code`（无 `--print`），模型真实执行工具调用
3. 通过三信号联合判断任务完成：
   - **信号1（最高优先级）**：进程自然退出 → 立即记录完成
   - **信号2+3（联合）**：工作区文件稳定窗口已满（T1/T4=60s，T2/T3/T5=90s，T6=120s）**且** 进程 CPU 连续3次采样 < 5% → kill 进程，记录 `OK-idle`
   - **超时兜底**：总耗时超过 `--timeout` → kill 进程，记录 `TIMEOUT`
   - **热身保护**：启动后前 30s 不触发稳定判断
4. 将耗时和状态追加到 `OUTPUT_DIR/results/timing.log`

工作区预置内容：
- 任务相关源文件（从 `references/workspace/` 复制）
- `TASK.md`（自动写入，包含任务说明）
- T2/T3/T5/T6 工作区额外放入对应 verify 脚本，供模型自主运行验证

**T4 特殊说明**：T4 为纯文字回答，模型将答案写入 `T4_answer.md`，只依赖进程退出信号，不做文件稳定判断。

### Step 3: 收集结果与计时

1. 读取 `OUTPUT_DIR/results/` 下所有结果文件
2. 读取各工作区的生成代码文件
3. 从文件修改时间戳或 timing.log 计算各任务耗时
4. 标记每个任务的成功/失败/超时状态
5. **运行 ground truth 验证脚本**（T2/T3/T5/T6 有对应脚本）：

```bash
# T2
python3 references/workspace/verify_t2.py OUTPUT_DIR/ws_{model}_2/buggy_sort.py

# T3
python3 references/workspace/verify_t3.py OUTPUT_DIR/ws_{model}_3/api_server.py

# T5
python3 references/workspace/verify_t5.py OUTPUT_DIR/ws_{model}_5/buggy_sort.py

# T6
python3 references/workspace/verify_t6.py OUTPUT_DIR/ws_{model}_6/blog_api.py
```

将 verify 结果（PASS/FAIL/ERROR）写入 `OUTPUT_DIR/verify_results.txt`，格式：

```
{model}__T2: VERIFY PASS
{model}__T3: VERIFY FAIL (2/4 tests passed)
{model}__T5: VERIFY FAIL (8/12 tests passed)
{model}__T6: VERIFY PASS
```

6. 写入 `OUTPUT_DIR/timing_data.txt`，格式：

```
| Task | ModelA | ModelB | ModelC |
|------|--------|--------|--------|
| T1   | 2min OK| 1min OK| 4min OK|
| T2   | 4min OK(r1)| 8min OK(r2)| TIMEOUT|
| T3   | 4min OK| TIMEOUT| 17min OK|
```

T2 的 round 信息从 timing.log 读取（r1=一轮通过，r2=二轮通过）。

7. 写入成功率统计

### Step 4: 生成盲评 Prompt

按 `references/eval-methodology.md` 的规范生成盲评 prompt。

关键要求：
- 用匿名标识（X/Y/Z）替换所有真实模型名
- 包含每个任务的：代码、输出、耗时、成功状态
- 包含评分标准（从 `references/rubric.md` 引用）
- 要求评测者按统一表格打分
- 不泄露任何可推断模型身份的信息

写入 `OUTPUT_DIR/eval_prompt.txt`

### Step 5: 执行盲评

对每个评测模型运行盲评（**可并行**）：

```bash
cat OUTPUT_DIR/eval_prompt.txt | ${CLAUDE_CLI:-claude} --code --model {evaluator} --dangerously-skip-permissions --print > OUTPUT_DIR/eval_{evaluator}.txt 2>&1
```

等待所有盲评完成。如果某个评测模型超时或失败，跳过并记录。

### Step 6: 聚合与输出

1. 读取所有盲评结果
2. 从各结果中提取分数表格
3. 计算各模型在每个任务上的**跨评测者平均分**
4. 计算总分和最终排名
4b. 计算评测者间 Spearman 相关系数矩阵，输出到报告：
    - 两两评测者之间的排名相关性（基于各模型总分排名）
    - 平均一致性：>0.7 为可信，0.5-0.7 需注意，<0.5 需警惕
5. 揭晓匿名映射
6. 输出最终报告，包含：

```
## 评测结果

### 各评测者打分
（完整输出每个评测者的评分表）

### 聚合排名（跨评测者平均）
| 排名 | 模型 | 平均总分 | 特点 |
|------|------|----------|------|

### 映射揭晓
X = ..., Y = ..., Z = ...
```

## 核心任务（必做，保证历史可比性）

详见 `references/tasks-core.md`：
- T1 代码生成：csv_stats.py
- T2 工具调用：buggy_sort.py 修 bug
- T3 Debug：api_server.py 中间件穿透
- T4 代码理解：api_server.py 分析
- T5 代码重构：buggy_sort.py 原地排序
- T6 综合实战：blog_api.py

核心6题分数可跨次对比。

## 扩展任务（可选，不计入核心分）

详见 `references/tasks-extended.md`。用户说"跑扩展题"时执行，单独计分，不影响核心排名。

**防污染轮换机制**：每季度可从扩展题（E1-E6）中选一道替换核心题，防止模型对固定题目产生训练数据记忆。
- 替换前：确认新题有 verify 脚本或客观评分标准
- 替换时：更新 tasks-core.md，将被替换的核心题移入 tasks-extended.md
- 核心6题总数保持不变，历史可比性由题目 ID（T1-T6）和版本日期维护

## 效率评分标准

效率维度满分 5 分 = 速度分（0-4）+ 成功率分（0-1）。

**速度分按任务难度分档：**

| 任务 | 速度分4 | 速度分3 | 速度分2 | 速度分1 | 速度分0 |
|------|---------|---------|---------|---------|---------|
| T1 代码生成 | <2min | 2-4min | 4-7min | 7-15min | >15min或TIMEOUT |
| T4 代码理解 | <2min | 2-4min | 4-7min | 7-15min | >15min或TIMEOUT |
| T2 工具调用 | <5min | 5-8min | 8-12min | 12-20min | >20min或TIMEOUT |
| T3 Debug | <5min | 5-8min | 8-12min | 12-20min | >20min或TIMEOUT |
| T5 重构 | <5min | 5-8min | 8-12min | 12-20min | >20min或TIMEOUT |
| T6 综合实战 | <8min | 8-12min | 12-18min | 18-25min | >25min或TIMEOUT |

**成功率分：**

| 结果状态 | 成功率分 |
|----------|----------|
| 完全成功 | 1 |
| 部分成功（功能完成但有瑕疵） | 0.5 |
| 失败但有输出 / TIMEOUT | 0 |

## 注意事项

- macOS 无 `timeout` 命令，用 Python subprocess timeout 或后台进程+sleep+kill
- agent 模式下任务通过 TASK.md 下发，run_task.py 自动处理，无需手动加前缀
- 效率分档表的时间基准基于 v1（--print 模式）设计，agent 模式首次跑完后需根据实际数据重新校准
- 并行运行多模型时注意资源竞争，GLM 在复杂任务并行时容易超时
- 盲评映射每次随机生成，防止评测者跨次记忆
- 评测 prompt 不要超过 50K 字符，过长会截断
