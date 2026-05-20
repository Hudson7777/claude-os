---
name: super-search
description: >
  多平台搜索工具，负责「找信息」。按场景路由到最合适的工具，失败自动降级。

  适用场景：
  - 在线搜索：上网搜索、全网搜索、搜一下、帮我搜、web search、搜索新闻/论文/代码、
    查最新消息、查最新进展、有什么新闻、最新动态、时效性查询（含"最新""今天""目前"等词）
  - 平台专项搜索：GitHub搜索、搜推特、搜小红书、搜B站、搜微信、公众号搜索、搜索视频
  - 新闻/资讯聚合、学术论文、技术社区内容
  - 深度研究：深度研究、调研报告、全面了解某话题
  - 自动化任务（早报/晚报）中的所有搜索行为

  不适用场景（转交其他 skill）：
  - 本地代码/文件搜索 → 用 Grep/Glob
  - 普通公开网页/文章链接读取 → 优先用 article-reader（更轻量）
  - 需要登录态、页面交互、动态渲染的网页 → 用 web-access（CDP 浏览器）
  - 微信公众号/小红书/微博等反爬平台的内容读取 → 用 web-access（CDP 更可靠）
  - 需要点击/填表/截图/视频采帧等浏览器操作 → 用 web-access
  - 实时股票行情 → 用 stock-market-pro skill
  - Internal knowledge bases → add your own routing rules in `references/scene-commands.md` (see Configuration below)
---

# Super Search — 多平台搜索路由

核心原则：**按场景选工具，额度从多到少依次消耗，失败自动降级。**

> 详细命令见 [`references/scene-commands.md`](references/scene-commands.md)，执行时按需查阅。

---

## 与其他 skill 的分工

| 场景 | 用哪个 skill |
|------|------------|
| 关键词搜索、发现信息来源 | **super-search** |
| 时效性新闻/资讯查询 | **super-search** |
| 深度研究、多源聚合 | **super-search** |
| 自动化任务（早报/晚报）中的搜索 | **super-search** |
| 普通公开网页 URL 读取（无反爬） | **article-reader**（更轻量） |
| 微信公众号/小红书/微博等反爬平台 | **web-access**（CDP 直连） |
| 需要登录态/动态渲染/交互操作的页面 | **web-access** |
| GitHub 搜索/代码搜索 | **super-search**（gh CLI） |
| YouTube/B站字幕提取 | **super-search**（yt-dlp） |

---

## 工具速查

### 通用 Web 搜索

| 工具 | 额度 | 最适合 |
|------|------|-------|
| **AnySearch** | 无限制（当前免费） | 英文通用+新闻主力，返回完整正文 |
| **LangSearch** | 1000次/天日重置 | 中文查询首选 |
| **Tavily** | ~950次/月 | 时效性查询，与 AnySearch 并行补充 |
| **Exa** | 1000次/月 | 技术/学术/代码语义搜索 |
| **Linkup** | €5/月≈1000次 | 深度研究 |
| **Firecrawl** | ~500cr一次性 | 搜索同时需要正文 |
| **Bing HTML 抓取** | 无限制（scraping） | 第0层最后手段，不稳定 |
| **Serper** | 2500次一次性 | 终极保底，轻易不触发 |

### 专项平台（无需 key）

| 工具 | 适用 |
|------|------|
| **gh CLI** | GitHub 仓库/代码/Issue |
| **yt-dlp** | YouTube/B站视频字幕 |
| **bili CLI** | B站搜索/热门/排行 |
| **小红书 via mcporter** | 小红书内容 |
| **搜狗微信搜索** | 微信公众号文章 |
| **HN Algolia** | 技术社区讨论 |
| **Stack Overflow API** | 编程问题（10000次/天） |
| **feedparser** | RSS/Atom 订阅源 |

### 新闻专项（有 key，100次/天）

| 工具 | 特点 |
|------|------|
| **GNews** | 多语言新闻聚合 |
| **TheNewsAPI** | 12000+来源 |

### 学术专项（无需 key，无限制）

| 工具 | 适用 |
|------|------|
| **arXiv** | 论文预印本 |
| **OpenAlex** | 学术全图谱 390万+ |
| **PubMed** | 医学/生命科学 |
| **CrossRef** | DOI/引用元数据 |
| **Wikipedia** | 概念解释 |
| **Google Books** | 书籍搜索 |

---

## 搜索路由决策

### 第一步：能用免费专项工具解决吗？

先判断是否命中无限制的专项工具——这些工具不消耗配额，优先走：

| 意图 | 直接走 | 场景 |
|------|-------|------|
| GitHub 仓库/代码/Issue | `gh` CLI | D |
| YouTube/B站视频字幕 | `yt-dlp` | F |
| B站热门/搜索/排行 | `bili` CLI 或 Bilibili API | F |
| 微信公众号关键词 | 搜狗微信搜索 | E |
| 小红书内容 | `mcporter xiaohongshu` | G |
| 学术论文 | arXiv / OpenAlex / PubMed | H |
| 技术问答 | HN Algolia / Stack Overflow | I |
| RSS 订阅源内容 | feedparser | K |
| 书籍/应用/npm包 | Google Books / iTunes / npm | L |

→ 不命中，进入第二步

### 第二步：zone 判断——确定信息来源语言

进入工具选择前，先确定 `zone`。**查询语言 ≠ 期望结果语言**，必须区分。

**显式覆盖（优先级最高）**：query 前加前缀，跳过自动推断：
- `[cn] 查询词` → zone = cn
- `[intl] 查询词` → zone = intl
- `[both] 查询词` → zone = both

**自动推断（无前缀时）**：

```
query 纯英文 → zone = intl（永远不走 LangSearch）

query 含中文 → 判断话题领域：

  中文权威领域 → zone = cn
  （国内政策/法规/监管、中国公司国内动态、国内社会民生文化、
   A股/港股中文视角、国内平台生态如微博/抖音/微信）

  英文权威领域 → zone = intl
  （国际科技/AI/半导体、全球宏观/金融市场/大宗商品、
   地缘政治/国际外交、学术研究/科学发现、美股/全球科技公司动态）

  横跨中英文 → zone = both
  （如"中美贸易""国内AI公司+全球对比""中国宏观+全球市场"）

  无法判断 → zone = both（保守默认，不丢信息）
```

### 第三步：按 zone 选工具 + 多层 fallback

#### zone = intl（英文来源优先）

```
时效性新闻（含"最新/今天/刚刚/现在"）：
  并行：AnySearch(freshness=day/week, 取12条)
       + Tavily(days=3, 取5条)
       + GNews/TheNewsAPI(取3条)          ← 三轨并行，去重后目标 ≥ 15 条
  Tavily 402 → 取消，AnySearch 单独取 15 条 + GNews 取 5 条
  GNews/TheNewsAPI 日额度耗尽 → 取消，其余两轨正常
  AnySearch 故障 → Tavily(取12条) + GNews(取5条)
  全部失败 → Bing HTML 抓取 → Serper

技术/代码/学术：
  并行：Exa(取8条, 语义搜索)
       + AnySearch(domains=["tech","academic"], 取8条)  ← 去重后目标 ≥ 10 条
  Exa 402 → AnySearch 单独取 15 条
  AnySearch 故障 → Exa 单独取 10 条
  均失败 → Bing HTML 抓取 → Serper

通用英文查询：
  并行：AnySearch(取12条)
       + Tavily(取5条)
       + GNews/TheNewsAPI(取3条，仅新闻类查询)  ← 去重后目标 ≥ 12 条
  Tavily 402 → AnySearch 单独取 15 条
  AnySearch 故障 → Tavily(取10条) + Exa(取5条)
  均失败 → Bing HTML 抓取 → Serper

深度研究：
  Linkup deep 或多工具并行（不变，见场景 M）
```

#### zone = cn（中文来源优先）

```
并行：LangSearch(取10条)
     + AnySearch(zone="cn", language="zh-CN", 取5条)  ← 去重后目标 ≥ 10 条
LangSearch 失败 → AnySearch(zone=cn) 单独取 15 条
AnySearch 故障 → LangSearch 单独取 10 条
均失败 → Bing HTML 抓取（中文查询） → Serper(cn)

新闻类 cn：补充 GNews(lang=zh) / TheNewsAPI(language=zh)，取3条并入
```

#### zone = both（中英文并行）

```
并行三轨：
  LangSearch(取8条, 中文)
  + AnySearch(取12条, 英文)
  + GNews/TheNewsAPI(取4条, 中英文各半)
→ 合并去重，中文结果占比上限 40%，目标总量 ≥ 15 条

LangSearch 失败 → AnySearch(zone=cn) 补中文（取5条）
AnySearch 故障  → Tavily(取10条) 补英文
GNews 额度耗尽  → 取消该轨，其余两轨正常
均失败 → Bing HTML 抓取 → Serper
```

#### 全局 fallback（所有轨道均失败）

```
→ Bing HTML 抓取（无需 key，见场景 C-1.8）
→ Serper（终极保底，2500次一次性）
→ 仍失败 → 告知用户，建议用 web-access
```

### 自动化任务（早报/晚报）专用路由

> 自动化任务**不触发 Serper**，保留一次性额度给手动触发。

```
英文板块（AI/宏观/国际新闻）：
  并行：AnySearch(freshness=day/week, 取12条)
       + Tavily(取5条, 单次任务上限10cr)
       + GNews/TheNewsAPI(取4条)          ← 三轨并行，去重后目标 ≥ 15 条
  Tavily 402 → AnySearch 单独取 15 条 + GNews 取 5 条
  AnySearch 故障 → Tavily(取10条) + GNews(取5条)
  均失败 → Bing HTML 抓取（不触发 Serper）

中文板块（国内新闻）：
  并行：LangSearch(取10条)
       + AnySearch(zone=cn, 取5条)
       + GNews(lang=zh, 取3条)            ← 三轨并行，去重后目标 ≥ 12 条
  LangSearch 失败 → AnySearch(zone=cn) 单独取 15 条 + GNews 取 5 条
  均失败 → Bing HTML 抓取（不触发 Serper）
```

---

## 额度优先级

消耗顺序（从最不心疼到最心疼）：

**第 0 层：完全免费无限制（优先消耗）**
1. **专项工具**（gh/yt-dlp/bili/HN/SO/arXiv/Wikipedia/feedparser 等）
2. **AnySearch**（当前免费无限额，英文搜索主力）
3. **Bing HTML 抓取**（scraping，不稳定，第0层最后手段）

**第 1 层：日重置（每天自动恢复）**
4. **LangSearch**（1000次/天）— 中文主力
5. **GNews/TheNewsAPI**（各100次/天）— 新闻专用，早晚报必分配 20% 权重

**第 2 层：月度配额（每月恢复）**
6. **Tavily**（~950次/月）— 时效性，与 AnySearch 并行补充
7. **Exa**（1000次/月）— 技术/学术语义查询
8. **Linkup**（€5/月≈1000次）— 深度研究

**第 3 层：一次性配额（用完不补，终极保底）**
9. **Serper**（2500次，**轻易不触发，仅全链路失败时使用**）
10. **Firecrawl**（~500cr，仅在需要抓取正文且其他方式失败时用）

---

## AnySearch 收费应对机制

当 AnySearch 由免费变为收费时，在 `scene-commands.md` 顶部将 `ANYSEARCH_FREE` 改为 `false`。

路由变化：
- AnySearch 降为第 2 层（与 Tavily/Exa 并列），不再作为主力并行
- Bing HTML 抓取升为第 0 层英文主力（取更多条数）
- 并行模式退化为：Bing HTML(取15条) + Tavily(取5条) + GNews(取4条)
- AnySearch 作为 Tavily 的 fallback，不主动触发

---

## 搜索后读全文

```
步骤1：搜索获取 URL 列表（用上方任意搜索工具）

步骤2：读取全文
  → web_fetch 直抓（静态页面，完全免费）
  → 失败 → Firecrawl scrape（1cr/页，有正文提取）
  → 失败 → 转交 web-access
  → 多个 URL 时并发执行，不要串行
```

---

## 暂不可用工具（保留备用）

> 当前网络环境封锁，功能完整、未来可能恢复。

| 工具 | 状态 | 恢复条件 |
|------|------|---------|
| **Jina Reader** (`r.jina.ai`) | 网络封锁 HTTP 000 | 网络环境变化 |
| **DuckDuckGo API** | 网络封锁 HTTP 000 | 网络环境变化 |
| **SearXNG 公开实例** | 全部 HTTP 000 | 网络环境变化 |
| **Reddit JSON API** | 网络封锁 | 网络环境变化 |
| **Brave Search API** | 网络封锁 HTTP 000 | 网络环境变化 |
| **NewsAPI.org** | 网络封锁 HTTP 000 | 网络环境变化 |
| **V2EX API** | 网络封锁 HTTP 000 | 网络环境变化 |
| **Currents API** | 网络封锁 HTTP 000 | 网络环境变化 |

> 需要认证才能使用的工具：

| 工具 | 状态 | 恢复条件 |
|------|------|---------|
| **xreach（Twitter）** | 已安装，未认证 | `xreach auth extract --browser chrome` |
| **博查 AI** | key 无余额 | 充值或等免费额度 |

> 已永久停用：

| 工具 | 原因 |
|------|------|
| **Bing Web Search API** | 微软 2025年8月正式停用 |
| **Google CSE 全网搜索** | 2026年1月限制，不再支持全网 |

---

## Output Contract

每次搜索输出必须满足：
- 每条结论标注来源（URL 或"搜索工具名 + 查询词"）
- 不确定或无法验证的信息标注"需验证"
- 时效性信息标注发布/更新日期
- 操作建议必须是具体命令或链接，不是泛泛描述
