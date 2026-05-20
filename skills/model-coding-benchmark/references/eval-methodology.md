# 盲评方法论

## 核心原则

1. **匿名性**：评测者不知道 X/Y/Z 对应哪个模型
2. **随机映射**：每次评测随机生成映射，防止跨次记忆
3. **多评测者**：默认3个不同模型评测，取平均分
4. **统一标准**：所有评测者使用相同的评分标准和表格格式

## 匿名映射生成

```
1. 收集所有待评模型名
2. 生成随机排列（用 Python random.shuffle）
3. 按排列顺序分配 X, Y, Z, A, B, C... 标识
4. 将映射记录到 OUTPUT_DIR/mapping.txt（不放入盲评 prompt）
```

映射示例：
```
X = gpt-5.4
Y = glm-5.1
Z = sonnet-4.6
```

## 盲评 Prompt 结构

```
# 编程能力盲评

你是编程能力评测专家。以下有 N 个模型的编程任务输出，标识为 X/Y/Z。
你不知道它们对应哪个模型，请客观评分。

## 评分标准

（插入 references/rubric.md 的评分标准）

## 任务输出

### T1 代码生成：csv_stats.py

#### Model X
耗时：4min | 状态：成功

代码：
（插入代码）

输出：
（插入运行输出）

#### Model Y
耗时：1min | 状态：成功

代码：
（插入代码）

...（每个模型每个任务都如此展示）

## 评分要求

请对每个任务的每个模型按5个维度打分（0-10）：
1. 正确性
2. 代码质量
3. 完整性
4. 工具使用
5. 效率（综合速度和成功率）

输出格式：

### T1 代码生成
| 维度 | Model X | Model Y | Model Z |
|------|---------|---------|---------|
| 正确性 | ? | ? | ? |
| 代码质量 | ? | ? | ? |
| 完整性 | ? | ? | ? |
| 工具使用 | ? | ? | ? |
| 效率 | ? | ? | ? |
| **总分** | **?** | **?** | **?** |

（每题一段评语，指出各模型的关键优缺点）

### 最终汇总
| Task | Model X | Model Y | Model Z |
|------|---------|---------|---------|
| T1 | ? | ? | ? |
| ... | ... | ... | ... |
| **总计** | **?** | **?** | **?** |

### 综合排名与评语
```

## 信息脱敏检查清单

在生成盲评 prompt 前，确认以下信息已脱敏：

- [ ] 模型名（如 glm-5.1、sonnet-4.6、gpt-5.4）→ 替换为 X/Y/Z
- [ ] 文件名中的模型标识（如 ws_glm_csv_stats.py → ws_Y_csv_stats.py）
- [ ] 代码注释中的模型特征（如 "我是 GPT" 之类）
- [ ] 运行输出的模型标识信息
- [ ] timing_data.txt 中的真实模型名 → 替换为 X/Y/Z

## 评测者选择

默认3个评测模型：kimi, gpt-5.4, sonnet

原则：
- 盲评下评测者不知道 X/Y/Z 对应谁，无需排除被评模型
- 所有评测者平等参与，不跳过任何人
- 至少需要2个有效评测结果才能聚合
- 脱敏质量是公平性的保障，而非排除规则

## 聚合方法

```
对于每个(任务, 维度, 模型)组合：
  final_score = mean(所有有效评测者的打分)

对于每个(任务, 模型)组合：
  task_score = sum(5个维度的final_score)

对于每个模型：
  total_score = sum(6个任务的task_score)
```

## 评测结果输出

最终报告应包含：

1. **各评测者完整结果**（原文输出，不做修改）
2. **聚合分数表**（跨评测者平均）
3. **最终排名**
4. **映射揭晓**

## 评测者间一致性量化

### Spearman 相关系数矩阵

在最终报告中输出评测者两两之间的 Spearman 排名相关系数：

```
评测者间 Spearman 相关系数：
           评测者A  评测者B  评测者C
评测者A      1.0     0.82    0.71
评测者B      0.82    1.0     0.78
评测者C      0.71    0.78    1.0

平均一致性: 0.77
```

### 一致性阈值

| 平均相关系数 | 解读 |
|-------------|------|
| > 0.7 | 可信，评测者理解一致 |
| 0.5 - 0.7 | 需注意，存在分歧 |
| < 0.5 | 需警惕，评分标准理解不一致 |

### 计算方法

基于各模型总分的排名（不是原始分）计算 Spearman 相关系数：

```python
from scipy.stats import spearmanr
import numpy as np

# scores[evaluator] = {model: total_score}
def compute_spearman_matrix(scores: dict) -> dict:
    evaluators = list(scores.keys())
    models = list(scores[evaluators[0]].keys())
    
    rankings = {}
    for ev in evaluators:
        model_scores = [scores[ev][m] for m in models]
        rankings[ev] = model_scores  # spearmanr handles ranking internally
    
    matrix = {}
    for i, ev1 in enumerate(evaluators):
        matrix[ev1] = {}
        for j, ev2 in enumerate(evaluators):
            if i == j:
                matrix[ev1][ev2] = 1.0
            else:
                corr, _ = spearmanr(rankings[ev1], rankings[ev2])
                matrix[ev1][ev2] = round(corr, 2)
    
    pairs = [(i, j) for i in range(len(evaluators)) 
             for j in range(i+1, len(evaluators))]
    avg = np.mean([matrix[evaluators[i]][evaluators[j]] for i, j in pairs])
    
    return matrix, round(float(avg), 2)
```

如果只有2个评测者，直接输出两者相关系数即可，无需矩阵。
