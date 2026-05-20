---
name: evening-brief
description: 生成每日晚报，覆盖今日要闻、今日深度、知识充电站（亮点板块）、人文关怀四大板块，以及明日天气。生成本地 HTML 文件和 Obsidian md 摘要。当用户或自动化任务提到以下任意场景时立即激活，无需确认：晚报、evening brief、今日晚报、生成晚报、发晚报、每日晚报、定时晚报任务触发。
---

# Evening Brief — 每日晚报

## 执行前：cases.md 检查

读取 `references/cases.md`，检查是否有「验证次数 ≥2 且未升入 SKILL.md：否」的条目。

- **用户手动触发**：有则提示用户"发现 N 个待固化的改进建议，建议先更新 skill 再执行。"，等待用户确认后再继续。
- **自动化任务触发**（消息包含"定时晚报任务触发"/"automation"）：检查照常执行，但不等待确认，直接继续执行。

---

## 执行模式判断

- **自动化任务触发**（消息包含"定时晚报任务触发"/"automation"）→ **串行模式**
- **用户手动触发** → **并行模式**，使用 subagent 四轨并行采集

---

## 🚀 并行模式（手动触发）

### 第一步：确定今日知识领域

读取 `references/knowledge-domains.md`，用 `(当天日期的"日") % 12` 计算领域编号，记录：
- 领域名称
- 该领域的深度搜索关键词（用于 Subagent 2 的 prompt）
- 该领域推荐的信息来源

### 第二步：四轨并行采集

在同一 tool call batch 中同时启动以下 4 个 subagent。
**完整 prompt 见 `references/subagent-prompts.md`，启动前必读，替换所有占位符。**

- **Subagent 1（新闻采集）**：今日 20 条新闻，国内 8 条 + 国际 12 条
- **Subagent 2（知识充电站）**：今日领域深度内容，质量优先于速度
- **Subagent 3（天气采集）**：明日北京望京天气预报
- **Subagent 4（今日深度 + 人文关怀）**：深度议题素材 + 历史上的今天 + 今日一句话

四轨汇总后进入第三步。

---

### 第三步：生成晚报内容

读取 `references/report-template.md` 中的 HTML 模板，将四轨内容填入。**生成前必读该文件。**

**今日要闻**（20条）：
- 国内 8 条 / 国际 12 条，严格按比例
- 国际新闻来源必须是英文一手媒体（Reuters, AP, BBC, Guardian, FT, Bloomberg, NYT, WSJ 等）
- 每条必须包含「为什么重要」1-2句
- **国际12条使用中英双语 HTML 结构**：`news-headline-en`（英文原标题）+ `news-en`（英文原文关键句1-2句），中文内容照常生成

**今日深度**（约2000字）：
- 议题不限：AI/科技/宏观/地缘/社会均可，选当天全球最值得深想的话题
- 结构：引子（1段）+ 核心分析（4-5段，有数据、有争议、有多方视角）+ 观点追问（1段）

**知识充电站**（晚报最重要板块，约2000字，质量标准最高）：
- 选定「一个极其具体的问题或现象」，而非宽泛领域——不是「量子力学」而是「为什么量子力学有十几种互相矛盾的诠释，物理学家真正在争什么」
- 目标读者感受：读完后说「原来如此，我以前理解错了」或「这个我从没想过」——科普入门级内容直接不合格
- **内容硬标准**（缺任何一项则重新采集）：
  1. 有具体的研究/实验/数据（年份、机构、数字），不接受泛泛陈述
  2. 有真实争议或反直觉之处——该领域专家们真正分歧在哪里
  3. 有具体人物或案例——某个科学家的发现、某次实验的转折、某个历史节点
  4. 有认知升级价值——读完后对某个问题的理解层次提升了
- 结构：引子（用一个具体故事/现象切入）→ 核心内容（3-4段，每段推进一层）→ 高亮反直觉核心发现 → 延伸（与其他领域的意外联系）
- **质量红线**：subagent 采集素材不满足上述4项硬标准时，主 agent 必须用 super-search skill 追加搜索并读取原文全文（article-reader skill），不接受摘要凑数

**人文关怀**：
- 历史事件：有深度，说清为什么值得记住，100-150字/条
- 今日一句话：有思想张力，含出处
- 晚安收尾：温暖但不套话，呼应今天的某个内容（新闻/知识点均可）

---

### 第四步：生成 HTML 和 md 文件

1. **HTML 文件**（主输出）：
   路径：`~/Documents/Obsidian Vault/日报/YYYY/MM/DD/evening.html`
   写入前先 `mkdir -p` 创建目录（Python: `Path(out).parent.mkdir(parents=True, exist_ok=True)`）

2. **Obsidian md 摘要**：
   路径：`~/Documents/Obsidian Vault/日报/YYYY/MM/DD/evening.md`
   按 report-template.md 中的 md 摘要规范生成

---

### 第五步：系统通知 + cases.md 更新

**发送 macOS 系统通知**：

```python
import subprocess, datetime
date_str = datetime.date.today().strftime('%Y-%m-%d')
y, m, d = date_str.split('-')
html_path = f"~/Documents/Obsidian Vault/日报/{y}/{m}/{d}/evening.html"
msg = f"每日晚报 {date_str} 已生成 → {html_path}"
subprocess.run(
    ['osascript', '-e', f'display notification "{msg}" with title "晚报"'],
    capture_output=True, text=True
)
```

**cases.md 更新**（发现以下情况时自动追加，不等用户提问）：
- RSS 拉取失败或返回空
- super-search skill 搜索返回结果 <3 条
- article-reader skill 读取失败
- 知识充电站素材质量不足（判断：读到的原文不足 800 字，或内容偏向科普入门）
- 某板块 subagent 超时失败

追加格式（写入 `references/cases.md`）：
```
## [今日日期] [evening]
- 问题：[一句话描述]
- 分类：信源失效 / 工具失败 / 内容质量差
- 验证次数：1
- 是否已升入 SKILL.md：否
- 建议改动：（如有）
```

---

## 🐢 串行模式（自动化触发）

目标总耗时 ≤ 10 分钟。

**串行模式强制约束**：
1. 禁止使用 web_search 工具（全局禁用）
2. 禁止使用 Jina Reader（网络封锁）
3. 禁止启动 subagent（沙盒会拦截）
4. 每步超时立即用已有内容继续，不等待

### 串行第一步：确定今日知识领域（30秒）

读取 `references/knowledge-domains.md`，用 `(当天日期的"日") % 12` 计算领域编号。

### 串行第二步：天气采集（1分钟内）

通过 super-search skill 搜索"北京朝阳区望京 明日天气 [明日日期]"。
超时则写"天气信息暂时无法获取"，继续下一步。

### 串行第三步：人文关怀采集（1分钟内）

在同一 tool call batch 中同时调用 super-search skill：
- "历史上的今天 [月份]月[日期]日 重要事件"
- "[Month] [Day] history on this day"

### 串行第四步：新闻采集（3分钟内）

第一批（同一 tool call batch 并发）：
```bash
python3 ~/.claude/skills/openclaw-feeds/scripts/feeds.py --category news
python3 ~/.claude/skills/openclaw-feeds/scripts/feeds.py --category finance
```

第二批（同一 tool call batch 并发，通过 super-search skill）：
- "中国政治外交经济新闻 [当日日期]"
- "global news today [英文日期]"

### 串行第五步：知识充电站采集（3分钟内）

**知识充电站是晚报质量最高的板块，给它充足的时间预算。**

1. 先从 RSS 筛选 Quanta/Aeon/Nautilus 等深度来源中与今日领域相关的文章
2. 调用 super-search skill 搜索 2-3 次（含"[领域] counterintuitive surprising"等带争议性的关键词）
3. 找到候选文章后，**必须用 article-reader skill 读取完整原文**（不能只用摘要）
4. 对照4项标准自查（有具体数据/有真实争议/有具体案例/有认知升级），不满足则换主题重搜

时间预算耗尽时：宁可只有1条深度内容而不是3条浅内容；若确实质量不足，在 cases.md 中记录原因。

### 串行第六步：今日深度素材（1分钟内）

根据新闻采集结果选定议题，通过 super-search skill 搜索 1-2 次补充背景。

### 串行第七步：生成内容 + 输出文件

**不要在此步骤前输出任何汇总或中间总结。前六步采集结束后，直接进入本步骤，不停顿。**

按 report-template.md 生成 HTML 和 md，写入文件，发送系统通知，更新 cases.md（同并行模式第三、四、五步）。

---

## 参考文件

| 文件 | 内容 | 何时读取 |
|------|------|----------|
| `references/report-template.md` | HTML 模板和 md 摘要规范 | **生成内容前必读** |
| `references/knowledge-domains.md` | 12 个知识领域轮换表 | **确定今日领域时必读** |
| `references/subagent-prompts.md` | 四个 subagent 的完整 prompt 模板 | **并行模式启动 subagent 前必读** |
| `references/cases.md` | 异常记录 | **执行前检查，执行后按需追加** |
| `config/sources.template.md` | 推荐信息源清单 | 采集时参考 |
