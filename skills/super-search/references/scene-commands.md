# Super Search — 场景详细命令参考

---

## 场景 A：微信公众号文章（有链接）

微信有严格反爬，直接转交 web-access，不在此处处理。

```bash
# 转交 web-access skill 处理
```

---

## 场景 B：已知 URL 内容提取（非微信）

优先级：`web_fetch` → Firecrawl → 转交 web-access

**B-1：web_fetch（首选，完全免费）**

直接使用内置 `web_fetch` 工具传入 URL。
判断成功：返回内容 > 500 字符且包含正文 → 成功；否则降级到 B-2。

**B-2：Firecrawl scrape（1cr/页）**

```bash
curl -s --max-time 20 \
  -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"<URL>","formats":["markdown"],"onlyMainContent":true}'
```

**B-3：转交 web-access（终极兜底）**

内网/登录态页面直接跳到此步。

---

## 场景 C：通用 Web 搜索

### C-1：Serper（首选，Google 结果，2500次一次性）

```bash
curl -s --max-time 10 \
  -X POST "https://google.serper.dev/search" \
  -H "X-API-KEY: $SERPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"<查询词>","num":10}'

# 中文查询加语言参数
curl -s --max-time 10 \
  -X POST "https://google.serper.dev/search" \
  -H "X-API-KEY: $SERPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"<查询词>","num":10,"gl":"cn","hl":"zh-cn"}'

# 新闻搜索
curl -s --max-time 10 \
  -X POST "https://google.serper.dev/news" \
  -H "X-API-KEY: $SERPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"<查询词>","num":10}'
```

### C-1.5：LangSearch（1000次/天，中文首选）

```bash
# 中文话题优先用这个（混合关键词+向量搜索，中文效果强）
curl -s --max-time 15 \
  -X POST "https://api.langsearch.com/v1/web-search" \
  -H "Authorization: Bearer $LANGSEARCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<查询词>","freshness":"noLimit","summary":false,"count":10}'

# 时效性查询（最近一周）
curl -s --max-time 15 \
  -X POST "https://api.langsearch.com/v1/web-search" \
  -H "Authorization: Bearer $LANGSEARCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<查询词>","freshness":"Week","summary":false,"count":10}'

# 带摘要（summary:true 让 LangSearch 自动总结每条结果）
curl -s --max-time 20 \
  -X POST "https://api.langsearch.com/v1/web-search" \
  -H "Authorization: Bearer $LANGSEARCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<查询词>","freshness":"noLimit","summary":true,"count":5}'
```

### C-1.6：AnySearch（无限额，英文主力）

> 当前完全免费，无限额。`ANYSEARCH_FREE = true`
> 收费后改为 false，路由退化为 Bing HTML 抓取主力 + AnySearch 作为 fallback。

```bash
# 通用英文搜索（标准用量）
curl -s --max-time 15 \
  -X POST "https://api.anysearch.com/v1/search" \
  -H "Authorization: Bearer $ANYSEARCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<查询词>","max_results":12,"content_types":["web","news"]}'

# 时效性新闻（近3天）
curl -s --max-time 15 \
  -X POST "https://api.anysearch.com/v1/search" \
  -H "Authorization: Bearer $ANYSEARCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<查询词>","max_results":12,"content_types":["news"],"constraint":{"freshness":"day"}}'

# 近一周
curl -s --max-time 15 \
  -X POST "https://api.anysearch.com/v1/search" \
  -H "Authorization: Bearer $ANYSEARCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<查询词>","max_results":12,"content_types":["news","web"],"constraint":{"freshness":"week"}}'

# 近一个月
curl -s --max-time 15 \
  -X POST "https://api.anysearch.com/v1/search" \
  -H "Authorization: Bearer $ANYSEARCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<查询词>","max_results":12,"content_types":["news","web"],"constraint":{"freshness":"month"}}'

# 技术/学术（domains 过滤）
curl -s --max-time 15 \
  -X POST "https://api.anysearch.com/v1/search" \
  -H "Authorization: Bearer $ANYSEARCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<查询词>","max_results":12,"domains":["tech","academic"],"content_types":["web","doc","academic"]}'

# 中文内容补充（zone=cn 时）
curl -s --max-time 15 \
  -X POST "https://api.anysearch.com/v1/search" \
  -H "Authorization: Bearer $ANYSEARCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<查询词>","max_results":12,"zone":"cn","language":"zh-CN"}'

# 降级单独执行时（并行对端失败），取更多条数保证覆盖
curl -s --max-time 15 \
  -X POST "https://api.anysearch.com/v1/search" \
  -H "Authorization: Bearer $ANYSEARCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<查询词>","max_results":20,"content_types":["web","news"]}'
```

判断成功：返回 `code: 0` 且 `results` 数组非空 → 成功；`code` 非 0 或空数组 → 降级。

---

### C-1.8：Bing HTML 抓取（无需 key，无限制，fallback 用）

> ⚠️ scraping，不稳定，HTML 结构可能随 Bing 改版变化。作为 API 额度耗尽时的 fallback。

```bash
# 英文查询（cn.bing.com，实测 9-10 条结果稳定）
python3 -c "
import urllib.request, urllib.parse, re, json, sys

def bing_search(query, count=10):
    url = f'https://cn.bing.com/search?q={urllib.parse.quote(query)}&count={count}'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='replace')
    items = re.findall(r'<li class=\"b_algo\".*?</li>', html, re.DOTALL)
    results = []
    for item in items:
        # 跳过 r.bing.com CSS/资源链接，找真实目标 URL
        hrefs = re.findall(r'href=\"(https?://[^\"]+)\"', item)
        real_urls = [h for h in hrefs if 'r.bing.com' not in h and 'bing.com' not in h]
        title_m = re.search(r'<h2[^>]*>.*?<a[^>]*>(.*?)</a>', item, re.DOTALL)
        desc_m = re.search(r'<p[^>]*>(.*?)</p>', item, re.DOTALL)
        if title_m and real_urls:
            results.append({
                'title': re.sub('<[^>]+>', '', title_m.group(1)).strip(),
                'url': real_urls[0],
                'desc': re.sub('<[^>]+>', '', desc_m.group(1)).strip()[:120] if desc_m else ''
            })
    return results

results = bing_search('<查询词>')
for r in results:
    print(r['title'])
    print(' ', r['url'])
    print(' ', r['desc'])
    print()
"
```

判断失效：返回结果数 < 3 或全部 URL 含 bing.com → Bing HTML 结构已变，换其他工具。

### C-2：Tavily（月度额度，时效性强）

```bash
curl -s --max-time 15 \
  -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$TAVILY_API_KEY\",\"query\":\"<查询词>\",\"max_results\":5}"

# 时效性查询加时间范围
curl -s --max-time 15 \
  -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$TAVILY_API_KEY\",\"query\":\"<查询词>\",\"max_results\":5,\"days\":3}"
```

### C-3：Exa（1000次/月，语义搜索）

```bash
# 通用搜索
curl -s --max-time 15 \
  -X POST "https://api.exa.ai/search" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<查询词>","type":"auto","num_results":5}'

# 代码/技术问题（比普通搜索便宜7倍）
curl -s --max-time 15 \
  -X POST "https://api.exa.ai/search" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<技术问题>","type":"auto","num_results":5,"contents":{"highlights":{"max_characters":2000}}}'
```

> ⚠️ Exa 偶发超时（约1/3概率），超时立即重试一次，仍失败换 Serper。
> EXA_API_KEY = b506452f-f005-4d95-bd65-1828ffbdb314

### C-4：Linkup（€5/月，深度搜索）

```bash
# 标准搜索
curl -s --max-time 20 \
  -X POST "https://api.linkup.so/v1/search" \
  -H "Authorization: Bearer $LINKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"<查询词>","depth":"standard","outputType":"searchResults","numResults":5}'

# 深度搜索（更贵，用于复杂研究）
curl -s --max-time 30 \
  -X POST "https://api.linkup.so/v1/search" \
  -H "Authorization: Bearer $LINKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"<查询词>","depth":"deep","outputType":"searchResults","numResults":5}'
```

### C-5：Firecrawl Search（~500cr一次性）

```bash
curl -s --max-time 15 \
  -X POST "https://api.firecrawl.dev/v1/search" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<查询词>","limit":5}'
```

---

## 场景 D：GitHub 搜索（完全免费）

```bash
# 仓库搜索
gh search repos "<查询词>" --sort stars --limit 10 --json name,stargazersCount,description,url

# 代码搜索
gh search code "<查询词>" --language <语言> --limit 10

# Issue 搜索
gh issue list -R <owner>/<repo> --state open --search "<关键词>"

# 查看仓库详情
gh repo view <owner>/<repo>

# gh 不可用时降级
curl -s --max-time 10 \
  -X POST "https://google.serper.dev/search" \
  -H "X-API-KEY: $SERPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"<查询词> site:github.com","num":10}'
```

---

## 场景 E：微信公众号关键词搜索

```bash
# 搜狗微信搜索（curl）
curl -s --max-time 10 \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
  -H "Accept-Language: zh-CN,zh;q=0.9" \
  "https://weixin.sogou.com/weixin?type=2&query=<URL编码的关键词>"

# 备选：Exa 搜索微信公众号域名
curl -s --max-time 15 \
  -X POST "https://api.exa.ai/search" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<关键词>","type":"auto","num_results":5,"includeDomains":["mp.weixin.qq.com"]}'

# 获取到 URL 后转交 web-access 读取全文
```

---

## 场景 F：视频内容（YouTube/B站）

```bash
# YouTube 字幕提取
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" \
  --skip-download -o "/tmp/%(id)s" "<YouTube URL>"
cat /tmp/<video_id>.zh-Hans.vtt 2>/dev/null || cat /tmp/<video_id>.en.vtt

# YouTube 搜索（免费）
yt-dlp --dump-json "ytsearch5:<查询词>"

# B站视频字幕
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh" \
  --convert-subs vtt --skip-download -o "/tmp/%(id)s" "<B站URL>"

# B站搜索 API（无需key）
curl -s --max-time 10 \
  "https://api.bilibili.com/x/web-interface/search/all/v2?keyword=<关键词>&page=1" \
  -H "User-Agent: Mozilla/5.0" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for item_type in d.get('data',{}).get('result',[]):
    if item_type.get('result_type')=='video':
        for v in item_type.get('data',[])[:5]:
            print(v.get('title','')[:60],'|',v.get('author',''),'|',v.get('play',''),'plays')
"
```

---

## 场景 G：小红书搜索

```bash
# 通过 mcporter 调用
mcporter call 'xiaohongshu.search_feeds(keyword: "<关键词>")'

# 读取具体笔记
mcporter call 'xiaohongshu.get_feed_detail(feed_id: "<id>", xsec_token: "<token>")'

# mcporter 不可用时降级
curl -s --max-time 10 \
  -X POST "https://google.serper.dev/search" \
  -H "X-API-KEY: $SERPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"<关键词> site:xiaohongshu.com","num":5}'
```

---

## 场景 H：学术论文搜索

```bash
# arXiv（无需key，论文预印本权威）
curl -s --max-time 10 \
  "https://export.arxiv.org/api/query?search_query=all:<关键词>&start=0&max_results=5" | \
  python3 -c "
import sys,xml.etree.ElementTree as ET
ns={'a':'http://www.w3.org/2005/Atom'}
root=ET.fromstring(sys.stdin.read())
for e in root.findall('a:entry',ns)[:5]:
    print(e.find('a:title',ns).text.strip()[:70])
    print('  ',e.find('a:id',ns).text)
"

# Semantic Scholar（无需key）
curl -s --max-time 10 \
  "https://api.semanticscholar.org/graph/v1/paper/search?query=<关键词>&fields=title,year,authors,url&limit=5"

# OpenAlex（无需key，最全学术图谱）
curl -s --max-time 10 \
  "https://api.openalex.org/works?search=<关键词>&per-page=5&select=title,publication_year,doi" | \
  python3 -c "
import sys,json
d=json.load(sys.stdin)
for w in d.get('results',[]):
    print(w.get('title','')[:70],'(',w.get('publication_year',''),')')
"

# PubMed（无需key，医学/生命科学）
curl -s --max-time 10 \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<关键词>&retmax=5&retmode=json" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print('IDs:', d.get('esearchresult',{}).get('idlist',[]))"

# CrossRef（无需key，DOI元数据）
curl -s --max-time 10 \
  "https://api.crossref.org/works?query=<关键词>&rows=5" | \
  python3 -c "
import sys,json
d=json.load(sys.stdin)
for item in d.get('message',{}).get('items',[])[:5]:
    title=item.get('title',[''])[0][:70]
    year=item.get('published',{}).get('date-parts',[['']])[0][0]
    print(title,'(',year,')')
"

# Exa 语义学术搜索
curl -s --max-time 15 \
  -X POST "https://api.exa.ai/search" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<关键词>","type":"auto","num_results":5,"includeDomains":["arxiv.org","scholar.google.com","semanticscholar.org"]}'
```

---

## 场景 I：技术社区搜索

```bash
# HN Algolia（无需key，无限制）
curl -s --max-time 10 \
  "https://hn.algolia.com/api/v1/search?query=<关键词>&hitsPerPage=10&tags=story" | \
  python3 -c "
import sys,json
d=json.load(sys.stdin)
print('hits:', d.get('nbHits',0))
for h in d.get('hits',[])[:5]:
    print(' -', h.get('title','')[:70])
    print('   ', h.get('url','')[:70])
"

# Stack Overflow（无需key，10000次/天）
curl -s --max-time 10 \
  "https://api.stackexchange.com/2.3/search/advanced?q=<关键词>&site=stackoverflow&pagesize=5&order=desc&sort=relevance" | \
  python3 -c "
import sys,json
d=json.load(sys.stdin)
print('quota_remaining:', d.get('quota_remaining','?'))
for item in d.get('items',[])[:5]:
    print(' -', item.get('title','')[:70])
    print('   score:', item.get('score',0), '| answers:', item.get('answer_count',0))
    print('   ', item.get('link',''))
"

# npm 包搜索（无需key，无限制）
curl -s --max-time 10 \
  "https://registry.npmjs.org/-/v1/search?text=<关键词>&size=5" | \
  python3 -c "
import sys,json
d=json.load(sys.stdin)
for obj in d.get('objects',[])[:5]:
    p=obj.get('package',{})
    print(p.get('name',''),'|',p.get('description','')[:60])
"

# Dev.to 技术文章（无需key）
curl -s --max-time 10 \
  "https://dev.to/api/articles?tag=<tag>&per_page=5" | \
  python3 -c "
import sys,json
for a in json.load(sys.stdin)[:5]:
    print(a.get('title','')[:70])
    print('  ', a.get('url',''))
"
```

---

## 场景 J：新闻资讯搜索

```bash
# GNews（100次/天，多语言）
curl -s --max-time 10 \
  "https://gnews.io/api/v4/search?q=<关键词>&token=$GNEWS_API_KEY&lang=zh&max=5"

# 英文新闻
curl -s --max-time 10 \
  "https://gnews.io/api/v4/search?q=<关键词>&token=$GNEWS_API_KEY&lang=en&max=5"

# TheNewsAPI（100次/天）
curl -s --max-time 10 \
  "https://api.thenewsapi.com/v1/news/all?api_token=$THE_NEWS_API_KEY&search=<关键词>&language=zh&limit=5"

# Tavily 时效性新闻（月度额度，1cr/次）
curl -s --max-time 15 \
  -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$TAVILY_API_KEY\",\"query\":\"<关键词>\",\"max_results\":5,\"days\":3}"

# Serper 新闻搜索（2500次一次性）
curl -s --max-time 10 \
  -X POST "https://google.serper.dev/news" \
  -H "X-API-KEY: $SERPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"<关键词>","num":5}'
```

---

## 场景 K：RSS 订阅源

```bash
# feedparser（无需key，无限制）
python3 -c "
import feedparser
feed = feedparser.parse('<RSS_URL>')
print('entries:', len(feed.entries))
for e in feed.entries[:5]:
    print(' -', e.get('title','')[:70])
    print('   ', e.get('link',''))
"

# 常用 RSS 源示例
# HN: https://feeds.feedburner.com/TheHackersNews
# TechCrunch: https://techcrunch.com/feed/
# ArsTechnica: https://feeds.arstechnica.com/arstechnica/index
```

---

## 场景 L：知识图谱查询

```bash
# Wikipedia（无需key，概念解释）
curl -s --max-time 10 \
  "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=<关键词>&format=json&srlimit=5" | \
  python3 -c "
import sys,json
d=json.load(sys.stdin)
for h in d.get('query',{}).get('search',[])[:5]:
    print(h.get('title','')[:60])
    import re; print(' ', re.sub('<[^>]+>','',h.get('snippet',''))[:100])
"

# Wikidata SPARQL（无需key，结构化数据）
curl -s --max-time 15 \
  "https://query.wikidata.org/sparql?query=<SPARQL>&format=json" \
  -H "Accept: application/json"

# Google Books（无需key）
curl -s --max-time 10 \
  "https://www.googleapis.com/books/v1/volumes?q=<关键词>&maxResults=5" | \
  python3 -c "
import sys,json
d=json.load(sys.stdin)
print('total:', d.get('totalItems',0))
for item in d.get('items',[])[:5]:
    info=item.get('volumeInfo',{})
    print(info.get('title','')[:60],'|',', '.join(info.get('authors',[])))
"
```

---

## 场景 M：深度研究（多工具并行）

```bash
# 并行启动多个 subagent，每个用不同工具搜索同一话题：
# Agent 1: Serper（通用）
# Agent 2: Exa（语义/技术）
# Agent 3: Tavily（时效性）
# Agent 4: arXiv / OpenAlex（学术）
# 汇总结果去重后输出

# 单次深度搜索（Linkup deep）
curl -s --max-time 30 \
  -X POST "https://api.linkup.so/v1/search" \
  -H "Authorization: Bearer $LINKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"<详细问题描述>","depth":"deep","outputType":"searchResults","numResults":10}'
```

---

## API Key 速查

| 变量名 | 用途 |
|--------|------|
| `$ANYSEARCH_API_KEY` | AnySearch 英文搜索（当前免费无限额，as_sk_fe14300e0421c6fa1e3df243b1f2af61） |
| `$LANGSEARCH_API_KEY` | LangSearch 中文搜索（1000次/天） |
| `$GNEWS_API_KEY` | GNews 新闻（100次/天日重置） |
| `$THE_NEWS_API_KEY` | TheNewsAPI 新闻（100次/天日重置） |
| `$TAVILY_API_KEY` | Tavily AI 搜索（~950次/月） |
| `$EXA_API_KEY` | Exa 语义搜索（b506452f-f005-4d95-bd65-1828ffbdb314，1000次/月） |
| `$LINKUP_API_KEY` | Linkup 深度搜索（€5/月） |
| `$SERPER_API_KEY` | Serper Google 搜索（2500次一次性，终极保底） |
| `$FIRECRAWL_API_KEY` | Firecrawl 搜索+抓取（fc-bb5e282bdde24961889dff961f03e809，~500cr一次性） |
| `$BOCHA_API_KEY` | 博查 AI（暂无余额，保留备用）|
