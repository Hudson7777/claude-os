---
name: morning-brief
description: 生成 AI 财经早报，覆盖 AI&科技前沿、宏观财经、今日深度三大板块，生成本地 HTML 文件和 Obsidian md 摘要。当用户或自动化任务提到以下任意场景时立即激活，无需确认：早报、AI财经早报、morning brief、今日早报、生成早报、发早报、AI日报、定时早报任务触发。
---

# Morning Brief — AI 财经早报

## 执行前：cases.md 检查

读取 `references/cases.md`，检查是否有「验证次数 ≥2 且未升入 SKILL.md：否」的条目。

- **用户手动触发**：有则提示用户"发现 N 个待固化的改进建议，建议先更新 skill 再执行。"，等待用户确认后再继续。
- **自动化任务触发**（消息包含"定时早报任务触发"/"automation"）：检查照常执行，但不等待确认，直接继续执行。

---

## 执行模式判断

- **自动化任务触发**（消息包含"定时早报任务触发"/"automation"）→ **串行模式**，不启动 subagent
- **用户手动触发** → **并行模式**，使用 subagent 三轨并行采集

---

## 🚀 并行模式（手动触发）

### 第一步：三轨并行采集

在同一 tool call batch 中同时启动以下 3 个 subagent：

**Subagent A（AI & 科技前沿）**：

```
采集今日 AI 与科技前沿新闻，8-9 条，国外信源占比 >80%。

⚠️ 搜索工具约束（必须遵守）：
- 禁止使用 web_search 工具（全局禁用，始终返回空）
- 禁止使用 Jina Reader（r.jina.ai，网络封锁）
- 所有搜索调用 super-search skill
- URL 全文读取调用 article-reader skill

采集策略（按顺序）：
1. 运行 RSS：python3 ~/.claude/skills/openclaw-feeds/scripts/feeds.py --category news
   # openclaw-feeds is a public skill: install from https://github.com/nesdeq/openclaw-feeds
   从 RSS 结果中筛选 TechCrunch AI、The Verge AI、Ars Technica、Wired、MIT Technology Review、OpenAI Blog、HuggingFace Blog、VentureBeat、New Scientist 等来源的 AI/科技条目
   目标从 RSS 筛出至少 5-6 条候选
2. 不足时调用 super-search skill 补充（使用 [intl] 前缀，每次独立调用）：
   - "[intl] AI artificial intelligence news today [英文日期]"
   - "[intl] NVIDIA OpenAI Anthropic Google DeepMind AI latest [英文日期]"
   - "[intl] semiconductor AI chip robotics news [英文日期]"
   - "[intl] cybersecurity AI tech policy news [英文日期]"
   super-search 自动走 AnySearch + Tavily + GNews/TheNewsAPI 三轨并行，目标候选池 ≥ 12 条。
   GNews/TheNewsAPI 结果约占最终 8-9 条中的 20%（≈2条），确保来源多样性。
3. 找到值得深读的文章 URL 后，调用 article-reader skill 读取全文

返回：8-9 条，每条包含：
- 中文标题 + 英文原始标题（headline_en，直接取原文，不翻译）
- 来源/媒体（英文优先）
- 3段中文正文（发生了什么/背景细节/为什么重要）
- 英文原文关键句（body_en，1-2句，≤80词，直接摘自原文）
```

**Subagent B（宏观财经）**：

```
采集今日宏观财经新闻，6 条，覆盖：货币政策、地缘/大宗商品、全球市场、产业政策。

⚠️ 搜索工具约束（必须遵守）：
- 禁止使用 web_search 工具（全局禁用，始终返回空）
- 禁止使用 Jina Reader（r.jina.ai，网络封锁）
- 所有搜索调用 super-search skill
- URL 全文读取调用 article-reader skill

采集策略：
1. 运行 RSS：python3 ~/.claude/skills/openclaw-feeds/scripts/feeds.py --category finance
   从 Bloomberg、WSJ、FT、Reuters、CNBC、The Economist、Nikkei Asia 等来源筛选宏观财经条目
   目标从 RSS 筛出至少 3-4 条候选
2. 不足时调用 super-search skill（使用 [intl] 前缀，每次独立调用）：
   - "[intl] Federal Reserve interest rate monetary policy [英文日期]"
   - "[intl] oil gold commodity geopolitical news [英文日期]"
   - "[intl] global stock market economy [英文日期]"
   - "[intl] China US trade tariff policy [英文日期]"
   super-search 自动走 AnySearch + Tavily + GNews/TheNewsAPI 三轨并行，目标候选池 ≥ 10 条。
   GNews/TheNewsAPI 结果约占最终 6 条中的 20%（≈1-2条），确保来源多样性。
3. 需要读全文时调用 article-reader skill

返回：6 条，每条包含：
- 中文标题 + 英文原始标题（headline_en）
- 来源/媒体
- 3段中文正文（含具体数据、背景、传导分析）
- 英文原文关键句（body_en，1-2句，≤80词）
```

**Subagent C（今日深度素材）**：

```
为今日早报的「今日深度」板块采集材料。

⚠️ 搜索工具约束（必须遵守）：
- 禁止使用 web_search 工具（全局禁用，始终返回空）
- 禁止使用 Jina Reader（r.jina.ai，网络封锁）
- 所有搜索调用 super-search skill
- URL 全文读取调用 article-reader skill

步骤：
1. 根据今日 AI/科技/宏观/地缘/社会新闻，判断哪个议题最值得深度分析（不限话题）
2. 调用 super-search skill 搜索该议题的深度报道：
   - "[议题关键词] analysis explained background"
   - "[议题关键词] 深度分析 背景"
3. 调用 article-reader skill 读取 2-3 篇长文

返回：议题标题 + 分点整理的素材（背景/多方视角/数据/争议点）
```

三轨汇总后进入第二步。

---

### 第二步：生成早报内容

按照 `references/report-template.md` 中的 HTML 模板生成内容。**生成前必读该文件。**

**板块一：AI & 科技前沿**（8-9条）
- 国外信源 >80%，每条 3 段正文（发生了什么 / 背景与技术细节 / 为什么重要）
- 有数据的尽量精确（发布日期、参数规格、市场份额等）
- 覆盖多个细分方向：大模型/AI产品、AI安全/政策、芯片/硬件、机器人/具身、科技公司动态
- **国际来源文章（>80%）使用双语 HTML 结构**：`article-headline-en`（英文原标题）+ `article-en`（英文原文关键句），中文内容照常生成

**板块二：宏观财经**（6条）
- 覆盖：货币政策/美联储、地缘/能源、全球市场行情、中美贸易、产业政策
- 每条 3 段，含具体数据和传导分析
- **国际来源文章同样使用双语 HTML 结构**（同板块一）

**板块三：今日深度**（1个议题，约2000字）
- 议题不限：AI/科技/宏观/地缘/社会均可，选当天最值得深想的话题
- 结构：引子（1段）+ 核心分析（4-5段，有数据、有争议、有多方视角）+ 观点追问（1段）
- 末尾一个开放性追问，引导读者继续思考

---

### 第三步：生成 HTML 文件

读取 `references/report-template.md` 中的 HTML 模板，将内容填入，生成文件：

**HTML 文件**（主输出）：

```python
import datetime, os
date = datetime.date.today()
date_str = date.strftime('%Y-%m-%d')

# Default: ~/Desktop/morning-brief-{date}.html
# Override: set OBSIDIAN_VAULT_PATH env var to write into your vault instead
vault = os.environ.get('OBSIDIAN_VAULT_PATH')
if vault:
    from pathlib import Path
    out_path = Path(vault) / '日报' / date.strftime('%Y') / date.strftime('%m') / date.strftime('%d') / 'morning.html'
else:
    from pathlib import Path
    out_path = Path.home() / 'Desktop' / f'morning-brief-{date_str}.html'

out_path.parent.mkdir(parents=True, exist_ok=True)
```

---

### 第四步：通知 + cases.md 更新

## Notification

If `BRIEF_WEBHOOK_URL` env var is set, POST the report summary to it.
Otherwise, save HTML to `~/Desktop/morning-brief-{date}.html` and open in browser.

```python
import os, subprocess, datetime
date_str = datetime.date.today().strftime('%Y-%m-%d')
webhook = os.environ.get('BRIEF_WEBHOOK_URL')
if webhook:
    import urllib.request, json
    summary = f"AI财经早报 {date_str} 已生成"
    data = json.dumps({"text": summary}).encode()
    req = urllib.request.Request(webhook, data=data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)
else:
    html_path = os.path.expanduser(f'~/Desktop/morning-brief-{date_str}.html')
    subprocess.run(['open', html_path])
```

**cases.md 更新**（执行过程中发现以下情况则自动追加，不等用户提问）：
- RSS 拉取失败或返回空
- super-search skill 搜索返回结果 <3 条
- article-reader skill 读取某 URL 失败
- 某板块内容严重不足（找不到足够高质量素材）

追加格式（写入 `references/cases.md`）：
```
## [今日日期] [morning]
- 问题：[一句话描述]
- 分类：信源失效 / 工具失败 / 内容质量差
- 验证次数：1
- 是否已升入 SKILL.md：否
- 建议改动：（如有）
```

---

## 🐢 串行模式（自动化触发）

串行模式在主线程中依次完成所有采集，目标总耗时 ≤ 8 分钟。

**串行模式强制约束**：
1. 禁止使用 web_search 工具（全局禁用）
2. 禁止使用 Jina Reader（网络封锁）
3. 禁止启动 subagent（沙盒会拦截）
4. 每步超时立即用已有内容继续，不等待

### 串行第一步：RSS 采集（2分钟内）

同一 tool call batch 中并发：
```bash
python3 ~/.claude/skills/openclaw-feeds/scripts/feeds.py --category news
python3 ~/.claude/skills/openclaw-feeds/scripts/feeds.py --category finance
```
从结果中筛选 AI/科技候选（目标 6-7 条）和财经/宏观候选（目标 4-5 条）。

### 串行第二步：补充搜索（2分钟内）

通过 super-search skill 补充 RSS 未覆盖的内容，在同一 tool call batch 中并发调用。
所有早报搜索均使用 [intl] 前缀（AI/宏观/国际话题均为英文权威领域），
super-search 自动走 AnySearch + Tavily + GNews/TheNewsAPI 三轨并行。
**GNews/TheNewsAPI 的结果应占每个板块最终条数的约 20%**，确保来源多样性。

- AI补充1："[intl] AI artificial intelligence news today [英文日期]"
- AI补充2："[intl] NVIDIA OpenAI Anthropic tech news [英文日期]"
- 宏观补充1："[intl] Federal Reserve global market economy [英文日期]"
- 宏观补充2："[intl] oil geopolitical trade policy [英文日期]"

目标：AI & 科技候选池 ≥ 12 条（筛出 8-9 条），宏观财经候选池 ≥ 10 条（筛出 6 条）。
GNews/TheNewsAPI 日额度耗尽时，对应槽位由 AnySearch 自动补足，不影响最终条数。

### 串行第三步：深度素材（2分钟内）

根据前两步采集到的新闻，选定深度议题，通过 super-search skill 搜索 2-3 个补充关键词。
如果找到高质量长文 URL，用 article-reader skill 读取全文。

### 串行第四步：生成内容 + 输出文件

**不要在此步骤前输出任何汇总或中间总结。前三步采集结束后，直接进入本步骤，不停顿。**

按 report-template.md 生成 HTML，写入文件，发送通知，更新 cases.md（同并行模式第三、四步）。

---

## 参考文件

| 文件 | 内容 | 何时读取 |
|------|------|----------|
| `references/report-template.md` | HTML 模板和 md 摘要规范 | **生成内容前必读** |
| `config/sources.template.md` | 推荐信息源清单（填写你的关注领域） | 采集时参考 |
| `references/cases.md` | 异常记录 | **执行前检查，执行后按需追加** |

See `config/sources.template.md` to configure your personal focus areas and preferred markets.
