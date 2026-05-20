---
name: wechat-article-save
description: Use when the user pastes any mp.weixin.qq.com URL in their message, with or without additional instructions. Triggers automatically — no explicit request to "save" or "record" is needed.
---

# WeChat Article Save

收到微信公众号链接时，自动执行完整的三步知识库工作流。**不需要用户额外说明，看到链接直接开始。**

## 触发条件

URL 包含 `mp.weixin.qq.com` → 立即启动本流程，不等用户说"保存"或"记录"。

## 浏览器约束（重要）

Playwright MCP 是**单浏览器单 tab**，所有 navigate 共享同一个实例。多篇文章**必须串行**，否则后来的 navigate 会覆盖前面的，导致读到错误页面写入错误内容。

**绝对不能并行启动多个 subagent 各自 navigate。**

## 三步工作流（每篇重复）

### Step 1：读取并验证

```
mcp__playwright__browser_navigate → url
等待 2 秒
mcp__playwright__browser_evaluate → 提取标题 + 正文
```

提取字段：
- 标题：`#activity-name` > `h1` > `document.title`
- 公众号名：`#js_name` > `.rich_media_meta_text`（取第一个）
- 正文：`#js_content` > `.rich_media_content` > `document.body.innerText`

**读取后必须验证**：检查提取到的 title 是否与预期文章匹配（不是"微信公众平台"空页，不是上一篇的标题残留）。验证通过再进行 Step 2，否则重新 navigate 一次。

失效检测：title 为"微信公众平台"且正文 < 50 字 → 标记"已删除"，跳过 Step 2/3，继续下一篇。

### Step 2：写 Obsidian 笔记

路径：`$HOME/Documents/Obsidian Vault/阅读/优秀文章/公众号文章/<文章标题>.md`

文件名：用文章标题，去掉特殊字符，控制在 20 字以内。

格式：

```markdown
---
title: 文章标题
source: 原文链接
author: 公众号名
date: YYYY-MM-DD
tags:
  - 标签1
  - 标签2

**Tag 命名规则：tag 不能包含空格，多词 tag 用连字符连接（如 Claude-Code、AI-Agent、Vibe-Coding）**
---

## 一句话主旨

xxx

## 核心观点

1. **观点标题**：内容
2. ...

## 原文金句

> 引用1
```

### Step 3：更新索引

文件：`$HOME/Documents/Obsidian Vault/阅读/优秀文章/公众号文章/_索引.md`

在表格末尾追加一行：

```
| YYYY-MM-DD | 公众号名 | ⭐ 或空 | 标签1, 标签2 | 一句话主旨 | [[笔记文件名]] | [链接](原文URL) |
```

星标公众号列表（填 ⭐，其余留空）：海外独角兽、晚点LatePost

## Step 0：重复检测（每次执行前必做）

在读取任何文章之前，先对所有待处理 URL 做重复检测：

```bash
# 读取索引文件内容
Read $HOME/Documents/Obsidian Vault/阅读/优秀文章/公众号文章/_索引.md
```

对每个 URL，检查两项：
1. **URL 重复**：索引中是否已有完全相同的链接
2. **标题重复**：先从 URL 导航获取标题，再检查索引中是否已有相同或高度相似的标题（覆盖"同文章不同链接"的情况）

检测结果分三类：
- **全部新文章** → 直接执行，无需提示
- **部分重复** → 告知用户哪些已存在（附索引中的记录行），询问是否跳过还是覆盖，等用户确认后再继续
- **全部重复** → 告知用户，不执行保存，结束流程

> 注意：标题检测需要先 navigate 获取标题，这一步同样受浏览器串行约束，必须逐篇检查。

## 执行顺序

Step 0（重复检测）→ Step 1（含验证）→ Step 2 → Step 3 → 下一篇 → ... → **所有篇完成后**才向用户展示汇总摘要。

不要在任何中间步骤停下来输出——完成全部文章后一次性汇报（重复检测发现冲突时除外，此时必须中断并询问用户）。

## 多链接处理方式

派**单个 subagent** 串行处理所有链接，逐篇执行完整三步后再处理下一篇。

subagent prompt 模板要点：
- 明确列出所有 URL 及处理顺序
- 强调每篇 navigate 后必须验证 title
- 每篇完成后输出一行进度：`[N/总数] 标题 | 状态`
- 全部完成后按下方格式输出结构化汇报

## Subagent 结构化汇报格式

subagent 完成所有文章后，**必须**按以下格式输出（主 agent 用此格式做异常检测）：

```
SUMMARY
total: N
success: N
deleted: N
error: N

RESULTS
- url: <原始URL>
  title: <读取到的标题>
  file: <写入的文件名>
  status: success | deleted | error
  anomaly: none | <异常描述>

- url: ...
```

anomaly 字段填写规则：
- `none`：一切正常
- `title_mismatch`：读取到的标题与上一篇相同（疑似缓存污染）
- `retry_required`：第一次 navigate 验证失败，重试后成功
- `write_failed`：文件写入失败
- `index_failed`：索引更新失败
- 其他自由描述异常原因

## 主 Agent 收到汇报后的处理

subagent 返回后，主 agent 执行以下检查：

**1. 扫描异常**

检查所有条目的 `anomaly` 字段，以及 `error` 计数：
- 全部 `none` 且 `error: 0` → 正常完成，向用户展示摘要
- 有任何非 `none` 的 anomaly → 进入异常处理流程

**2. 异常处理流程**

对每个有异常的条目：
- `title_mismatch`：说明浏览器缓存污染，受影响文章需要重新读取
- `retry_required`：记录但不需要修复，说明当前验证机制有效
- `write_failed` / `index_failed`：立即补救（重新写文件或更新索引）

**3. 自动写 cases.md**

发现任何异常后，**不等用户提问**，自动在 `~/.claude/skills/wechat-article-save/cases.md` 追加记录：

```
## YYYY-MM-DD [任务描述，如"保存5篇文章"]
- 规模：N 篇文章
- 发现：[一句话描述异常]
- 分类：平台约束 / 行为模式（问题）/ 行为模式（成功）
- 验证次数：1
- 是否已升入 SKILL.md：否
- 建议改动：[如有]
```

写完后告知用户："发现 1 个异常，已记录到 cases.md，待下次复现后评估是否更新 skill。"

**4. cases.md 升级检查**

每次执行前，检查 `~/.claude/skills/wechat-article-save/cases.md` 是否存在"验证次数 ≥2 且未升入 SKILL.md"的条目。有则在执行前提示用户，建议先更新 skill 再执行。
