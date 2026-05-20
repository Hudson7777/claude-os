# 晚报 HTML 输出规范

## 文件路径

```
~/Documents/Obsidian Vault/日报/YYYY/MM/DD/evening.html
~/Documents/Obsidian Vault/日报/YYYY/MM/DD/evening.md
```

目录按年/月/日三级自动创建，写入前执行 `Path(out_path).parent.mkdir(parents=True, exist_ok=True)`。

---

## HTML 生成方式（必须遵守）

**禁止用 `str.replace()` 填充内容**。字符串替换对换行/空格极度敏感，静默失败时内容为空但不报错。

**必须用 BeautifulSoup 直接注入**：

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(template_html, 'html.parser')

# 日期/元数据：直接替换字符串（简单变量用 replace 可以）
html = template_html.replace('{{DATE_DISPLAY}}', '2026年5月11日')
soup = BeautifulSoup(html, 'html.parser')

# 内容注入：必须用 BS4，禁止 str.replace
# 标题
soup.find(class_='depth-title').string = depth_title

# 多段正文（先清空占位符，再逐段插入）
block = soup.find(class_='depth-block')
for p in block.find_all('p', recursive=False):
    p.decompose()
for text in depth_paragraphs:
    new_p = soup.new_tag('p')
    new_p.string = text
    block.find(class_='depth-opinion').insert_before(new_p)

# 知识充电站高亮块
hl = soup.find(class_='knowledge-highlight')
hl.find('p').string = highlight_text

# 写入
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(str(soup), encoding='utf-8')
```

**生成后验证（每次必做，发现空板块立即终止并重试）**：

```python
check = BeautifulSoup(out_path.read_text(), 'html.parser')
checks = {
    'news':      len(check.find_all(class_='news-item')),
    'depth_p':   len(check.find(class_='depth-block').find_all('p')),
    'know_p':    len(check.find(class_='knowledge-block').find_all('p')),
    'hum_items': len(check.find_all(class_='history-item')),
}
for k, v in checks.items():
    if v == 0:
        raise RuntimeError(f"板块为空: {k}，中止，请检查内容提取逻辑")
print("验证通过:", checks)
```

---

## HTML 结构模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>每日晚报 · {{DATE_DISPLAY}}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,300;1,8..60,400&family=Space+Mono:wght@400;700&display=swap');

:root {
  --bg:           #F5F7F5;
  --fg:           #1C2B1E;
  --card:         rgba(255,255,255,0.88);
  --accent:       #8BA888;
  --accent-deep:  #5a7a57;
  --muted:        #EEF3EE;
  --muted-fg:     #6B7D6C;
  --border:       #DDE8DD;
  --apricot:      #F5E6D3;
  --lavender:     #E8E0F0;
  --mist:         #D6EAF2;
  --ember:        #8B3A1A;
  --ember-light:  #c0522a;
  --radius:       10px;
  --shadow:       0 2px 12px rgba(28,43,30,0.06), 0 1px 3px rgba(28,43,30,0.04);
  --shadow-hover: 0 8px 28px rgba(28,43,30,0.10), 0 2px 6px rgba(28,43,30,0.06);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }

body {
  font-family: 'Source Serif 4', Georgia, serif;
  font-weight: 300;
  font-size: 30px;
  line-height: 1.8;
  color: var(--fg);
  background-color: var(--bg);
  /* Monet multi-source light halos */
  background-image:
    radial-gradient(ellipse 70% 50% at 12% 5%,  rgba(245,230,211,0.22) 0%, transparent 60%),
    radial-gradient(ellipse 55% 40% at 88% 10%, rgba(214,234,242,0.16) 0%, transparent 50%),
    radial-gradient(ellipse 60% 45% at 72% 45%, rgba(232,224,240,0.12) 0%, transparent 55%),
    radial-gradient(ellipse 65% 50% at 15% 80%, rgba(139,168,136,0.13) 0%, transparent 52%),
    radial-gradient(ellipse 50% 40% at 85% 85%, rgba(245,230,211,0.10) 0%, transparent 45%);
  background-attachment: fixed;
  min-height: 100vh;
}

/* Canvas grain — painterly texture */
body::after {
  content: '';
  position: fixed;
  inset: 0;
  z-index: 9999;
  pointer-events: none;
  opacity: 0.028;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 200px 200px;
}

/* ─── MASTHEAD ───────────────────────────────────────────────── */
.masthead {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(245,247,245,0.92);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--border);
  padding: 0 48px;
  height: 56px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.masthead-brand {
  font-family: 'Lora', Georgia, serif;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--accent-deep);
  letter-spacing: 0.04em;
}

.masthead-sep {
  width: 1px;
  height: 16px;
  background: var(--border);
}

.masthead-date {
  font-family: 'Space Mono', monospace;
  font-size: 0.68rem;
  color: var(--muted-fg);
  letter-spacing: 0.06em;
}

.masthead-nav {
  margin-left: auto;
  display: flex;
  gap: 24px;
}

.masthead-nav a {
  font-family: 'Space Mono', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted-fg);
  text-decoration: none;
  transition: color 0.2s;
}

.masthead-nav a:hover { color: var(--accent-deep); }

/* ─── LAYOUT ─────────────────────────────────────────────────── */
.container {
  max-width: 1748px;
  margin: 0 auto;
  padding: 0 40px;
}

@media (max-width: 680px) {
  .masthead { padding: 0 20px; }
  .masthead-nav { display: none; }
  .container { padding: 0 20px; }
}

/* ─── HERO ───────────────────────────────────────────────────── */
.hero {
  padding: 72px 0 60px;
  display: grid;
  grid-template-columns: 1fr 220px;
  gap: 48px;
  align-items: start;
  border-bottom: 1px solid var(--border);
  opacity: 0;
  animation: fadeUp 0.6s ease 0.05s forwards;
}

.hero-eyebrow {
  font-family: 'Space Mono', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 14px;
}

.hero-title {
  font-family: 'Lora', Georgia, serif;
  font-size: clamp(2.9rem, 4.5vw, 4.6rem);
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.015em;
  color: var(--fg);
}

.hero-title em {
  font-style: italic;
  color: var(--accent-deep);
}

.hero-sub {
  margin-top: 16px;
  font-size: 1.26rem;
  color: var(--muted-fg);
  line-height: 1.65;
  max-width: 600px;
}

/* ─── WEATHER CARD ───────────────────────────────────────────── */
.weather-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px 22px;
  box-shadow: var(--shadow);
  margin-top: 4px;
}

.weather-temp {
  font-family: 'Lora', Georgia, serif;
  font-size: 2.6rem;
  font-weight: 700;
  color: var(--fg);
  line-height: 1;
}

.weather-desc {
  font-family: 'Space Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted-fg);
  margin-top: 5px;
}

.weather-detail {
  margin-top: 10px;
  font-size: 0.78rem;
  color: var(--muted-fg);
  line-height: 1.5;
}

.weather-tip {
  margin-top: 8px;
  font-size: 0.75rem;
  color: var(--accent-deep);
  font-style: italic;
}

@media (max-width: 680px) {
  .hero { grid-template-columns: 1fr; padding: 40px 20px 36px; }
}

/* ─── SECTION WRAPPER ────────────────────────────────────────── */
.section-wrap {
  padding: 56px 0;
  border-bottom: 1px solid var(--border);
  opacity: 0;
  transform: translateY(20px);
}

.section-wrap.visible {
  animation: fadeUp 0.55s ease forwards;
}

.section-eyebrow {
  font-family: 'Space Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-eyebrow::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}

.section-heading {
  font-family: 'Lora', Georgia, serif;
  font-size: 2.4rem;
  font-weight: 700;
  color: var(--fg);
  margin-bottom: 36px;
  line-height: 1.25;
}

/* ─── REGION DIVIDER ─────────────────────────────────────────── */
.region-divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 32px 0 24px;
  font-family: 'Space Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--muted-fg);
}

.region-divider::before, .region-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}

/* ─── NEWS ITEMS ─────────────────────────────────────────────── */
.news-item {
  display: grid;
  grid-template-columns: 32px 1fr;
  gap: 0 16px;
  padding: 22px 0;
  border-bottom: 1px solid var(--muted);
  position: relative;
  transition: background 0.15s;
}

.news-item:last-child { border-bottom: none; }

/* Sage left-bar hover */
.news-item::before {
  content: '';
  position: absolute;
  left: -2px;
  bottom: 0;
  width: 2px;
  height: 0%;
  background: var(--accent);
  border-radius: 2px;
  transition: height 0.3s ease-out;
}

.news-item:hover::before { height: 100%; }
.news-item:hover { background: rgba(139,168,136,0.04); }

.news-num {
  font-family: 'Space Mono', monospace;
  font-size: 0.6rem;
  color: var(--accent);
  padding-top: 2px;
  letter-spacing: 0.05em;
}

.news-headline {
  font-family: 'Lora', Georgia, serif;
  font-size: 1.44rem;
  font-weight: 600;
  color: var(--fg);
  line-height: 1.35;
  margin-bottom: 3px;
}

.news-source {
  font-family: 'Space Mono', monospace;
  font-size: 0.58rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted-fg);
  opacity: 0.7;
  margin-bottom: 9px;
}

.news-body p {
  font-size: 1.2rem;
  color: #3d4d3e;
  line-height: 1.75;
  margin-bottom: 8px;
}

.news-why {
  margin-top: 8px;
  padding: 8px 0 0 12px;
  border-left: 2px solid var(--accent);
  font-size: 1.1rem;
  font-style: italic;
  color: var(--muted-fg);
  line-height: 1.6;
}

/* ─── DEPTH BLOCK ────────────────────────────────────────────── */
.depth-block {
  background: var(--apricot);
  border: 1px solid rgba(139,58,26,0.15);
  border-radius: var(--radius);
  padding: 48px 52px;
  margin: 56px 0;
  position: relative;
  opacity: 0;
  transform: translateY(20px);
}

.depth-block.visible {
  animation: fadeUp 0.6s ease forwards;
}

.depth-block::before {
  content: 'DEPTH';
  position: absolute;
  top: 24px;
  right: 32px;
  font-family: 'Space Mono', monospace;
  font-size: 0.52rem;
  letter-spacing: 0.35em;
  color: rgba(139,58,26,0.3);
}

.depth-eyebrow {
  font-family: 'Space Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--ember);
  margin-bottom: 14px;
}

.depth-title {
  font-family: 'Lora', Georgia, serif;
  font-size: clamp(1.8rem, 2.8vw, 2.4rem);
  font-weight: 700;
  font-style: italic;
  color: var(--ember);
  line-height: 1.3;
  margin-bottom: 28px;
}

.depth-block p {
  font-size: 1.26rem;
  color: #3a2510;
  line-height: 1.85;
  margin-bottom: 18px;
}

.depth-opinion {
  margin-top: 28px;
  padding: 18px 22px;
  background: rgba(139,58,26,0.07);
  border-left: 3px solid var(--ember-light);
  border-radius: 0 6px 6px 0;
  font-size: 1.2rem;
  font-style: italic;
  color: #5a3018;
  line-height: 1.7;
}

@media (max-width: 680px) {
  .depth-block { padding: 32px 24px; }
}

/* ─── KNOWLEDGE BLOCK ────────────────────────────────────────── */
.knowledge-block {
  background: var(--mist);
  border: 1px solid rgba(100,150,180,0.2);
  border-radius: var(--radius);
  padding: 48px 52px;
  margin: 56px 0;
  position: relative;
  opacity: 0;
  transform: translateY(20px);
}

.knowledge-block.visible {
  animation: fadeUp 0.6s ease 0.1s forwards;
}

/* Corner accents */
.knowledge-block::before,
.knowledge-block::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  border-color: rgba(100,150,180,0.35);
  border-style: solid;
}

.knowledge-block::before {
  top: -1px; left: -1px;
  border-width: 2px 0 0 2px;
  border-radius: var(--radius) 0 0 0;
}

.knowledge-block::after {
  bottom: -1px; right: -1px;
  border-width: 0 2px 2px 0;
  border-radius: 0 0 var(--radius) 0;
}

.knowledge-eyebrow {
  font-family: 'Space Mono', monospace;
  font-size: 0.58rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: #3a6080;
  opacity: 0.75;
  margin-bottom: 6px;
}

.knowledge-title {
  font-family: 'Lora', Georgia, serif;
  font-size: clamp(1.8rem, 2.8vw, 2.52rem);
  font-weight: 700;
  color: #1a3a52;
  line-height: 1.25;
  margin-bottom: 32px;
}

.knowledge-block p {
  font-size: 1.26rem;
  color: #1e3a4a;
  line-height: 1.85;
  margin-bottom: 18px;
}

.knowledge-highlight {
  margin: 24px 0;
  padding: 18px 22px;
  background: rgba(255,255,255,0.55);
  border-left: 3px solid #5090b8;
  border-radius: 0 6px 6px 0;
}

.knowledge-highlight p {
  font-size: 1.22rem;
  color: #1a3a52;
  font-style: italic;
  line-height: 1.75;
  margin: 0;
}

@media (max-width: 680px) {
  .knowledge-block { padding: 32px 24px; }
}

/* ─── HUMANITIES BLOCK ───────────────────────────────────────── */
.humanities-block {
  background: var(--lavender);
  border: 1px solid rgba(160,140,200,0.2);
  border-radius: var(--radius);
  padding: 48px 52px;
  margin: 56px 0 0;
  opacity: 0;
  transform: translateY(20px);
}

.humanities-block.visible {
  animation: fadeUp 0.6s ease 0.15s forwards;
}

.humanities-eyebrow {
  font-family: 'Space Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: #5a4878;
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.humanities-eyebrow::after {
  content: '';
  flex: 1;
  height: 1px;
  background: rgba(160,140,200,0.3);
}

.history-item {
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px dashed rgba(160,140,200,0.3);
}

.history-item:last-of-type { border-bottom: none; }

.history-title {
  font-family: 'Lora', Georgia, serif;
  font-size: 1.38rem;
  font-weight: 600;
  color: #2d2040;
  margin-bottom: 8px;
  line-height: 1.35;
}

.history-item p {
  font-size: 1.2rem;
  color: #4a3860;
  line-height: 1.75;
}

.quote-block {
  margin: 28px 0 24px;
  padding: 0 0 0 18px;
  border-left: 3px solid rgba(160,140,200,0.5);
  font-family: 'Lora', Georgia, serif;
  font-size: 1.44rem;
  font-style: italic;
  color: #2d2040;
  line-height: 1.65;
}

.quote-attr {
  display: block;
  margin-top: 7px;
  font-family: 'Space Mono', monospace;
  font-size: 0.6rem;
  font-style: normal;
  letter-spacing: 0.1em;
  color: #6a5488;
}

.goodnight {
  margin-top: 28px;
  padding-top: 24px;
  border-top: 1px solid rgba(160,140,200,0.25);
  font-size: 1.26rem;
  color: #3a2c52;
  line-height: 1.8;
  font-style: italic;
}

@media (max-width: 680px) {
  .humanities-block { padding: 32px 24px; }
}

/* ─── FOOTER ─────────────────────────────────────────────────── */
.site-footer {
  padding: 36px 40px;
  font-family: 'Space Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 0.1em;
  color: var(--muted-fg);
  text-align: center;
  border-top: 1px solid var(--border);
  opacity: 0.6;
}

/* ─── ANIMATIONS ─────────────────────────────────────────────── */
@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}

/* ─── BILINGUAL (国际新闻中英双语) ──────────────────────────── */
.news-headline-en {
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 0.88rem;
  font-weight: 400;
  font-style: italic;
  color: var(--muted-fg);
  line-height: 1.4;
  margin-bottom: 8px;
  opacity: 0.75;
}

.news-en {
  font-size: 0.9rem !important;
  color: var(--muted-fg) !important;
  line-height: 1.65 !important;
  font-style: italic;
  opacity: 0.8;
  border-left: 2px solid var(--border);
  padding-left: 10px;
  margin-top: 2px !important;
  margin-bottom: 4px !important;
}
</style>
</head>
<body>

<!-- MASTHEAD -->
<header class="masthead">
  <div class="masthead-brand">每日晚报</div>
  <div class="masthead-sep"></div>
  <div class="masthead-date">{{DATE_DISPLAY}} · 星期X · HH:MM</div>
  <nav class="masthead-nav">
    <a href="#news">要闻</a>
    <a href="#depth">深度</a>
    <a href="#knowledge">知识</a>
    <a href="#humanities">人文</a>
  </nav>
</header>

<!-- HERO -->
<div class="container">
  <div class="hero">
    <div>
      <div class="hero-eyebrow">{{DATE_DISPLAY}} · 今日晚报</div>
      <h1 class="hero-title">[深度议题主标题]<br/><em>[深度议题副标题]</em></h1>
      <p class="hero-sub">[1-2句话概括今日最重要的深度议题，作为 hero 导语]</p>
    </div>
    <div class="weather-card">
      <div class="weather-temp">[最高温]°</div>
      <div class="weather-desc">[天气状况] · 最低[最低温]°</div>
      <div class="weather-detail">[风向风力]<br/>[AQI描述]</div>
      <div class="weather-tip">[出行提示]</div>
    </div>
  </div>
</div>

<!-- NEWS -->
<div class="container">
  <section class="section-wrap" id="news">
    <div class="section-eyebrow">今日要闻</div>
    <h2 class="section-heading">20条 · 国内8条 + 国际12条</h2>

    <div class="region-divider">🇨🇳 国内要闻 01—08</div>

    <article class="news-item">
      <div class="news-num">01</div>
      <div class="news-body">
        <div class="news-headline">[新闻标题]</div>
        <div class="news-source">来源：[媒体名] · [时间]</div>
        <p>[第1段：发生了什么，注明时间地点人物]</p>
        <p>[第2段：背景与意义]</p>
        <div class="news-why">为什么重要：[1-2句话，说明这件事的影响范围或深层含义]</div>
      </div>
    </article>

    <!-- 重复 news-item，国内共 8 条 -->

    <div class="region-divider">🌐 国际要闻 09—20</div>

    <!-- 国际新闻 12 条，中英双语结构 -->
    <!-- 每条必须包含 news-headline-en（英文原标题）和 news-en（英文原文关键句） -->

  </section>
</div>

<!-- DEPTH -->
<div class="container">
  <div class="depth-block" id="depth">
    <div class="depth-eyebrow">今日深度</div>
    <h2 class="depth-title">[深度议题标题]</h2>
    <p>[引子：1段，具体现象或数据]</p>
    <p>[核心分析：4-5段，约2000字，有数据、有争议、有多方视角]</p>
    <div class="depth-opinion">
      [观点/结论：这件事对你意味着什么，值得追问的下一个问题]
    </div>
  </div>
</div>

<!-- KNOWLEDGE -->
<div class="container">
  <div class="knowledge-block" id="knowledge">
    <div class="knowledge-eyebrow">知识充电站 · [领域名称]</div>
    <h2 class="knowledge-title">[今日主题：一个具体问题，而非宽泛领域名]</h2>
    <p>[引子：1段，具体故事或现象]</p>
    <p>[核心内容：3-4段，有研究数据、案例、逻辑]</p>
    <div class="knowledge-highlight">
      <p>[最反直觉或最有价值的核心发现，加高亮]</p>
    </div>
    <p>[延伸：与其他领域的联系或对日常生活的启示]</p>
  </div>
</div>

<!-- HUMANITIES -->
<div class="container">
  <div class="humanities-block" id="humanities">
    <div class="humanities-eyebrow">人文关怀 · 历史上的今天</div>

    <div class="history-item">
      <div class="history-title">[历史事件标题]</div>
      <p>[150字，先说事件，再说为什么值得记住，或它对今天的意义]</p>
    </div>

    <!-- 可选第二个历史事件，同结构 -->

    <div class="quote-block">
      [一句有思想张力的话]
      <span class="quote-attr">——[署名]</span>
    </div>

    <div class="goodnight">晚安，浩然。[2-3句温暖收尾，呼应今天的某个内容]</div>
  </div>
</div>

<footer class="site-footer">
  每日晚报 · {{DATE_DISPLAY}} · HH:MM
</footer>

<script>
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.06 });

document.querySelectorAll('.section-wrap, .depth-block, .knowledge-block, .humanities-block')
  .forEach(el => observer.observe(el));
</script>

</body>
</html>
```

---

## Obsidian md 摘要规范

```markdown
---
date: YYYY-MM-DD
type: evening-brief
knowledge-domain: [今日领域名称]
depth-topic: [深度议题关键词]
html-path: "~/Documents/Obsidian Vault/日报/YYYY/MM/DD/evening.html"
---

🌙 [在浏览器中打开晚报]($HOME/Documents/Obsidian%20Vault/日报/YYYY/MM/DD/evening.html)

## 今日要闻（精选）
- [国内1]（来源）
- [国内2]（来源）
- [国际1]（来源）
- [国际2]（来源）
- [国际3]（来源）

## 今日深度
**议题**：[标题]
[2-3句核心观点摘要]

## 知识充电站
**领域**：[领域名称] / **主题**：[具体问题]
[2-3句核心发现摘要]

## 人文关怀
> [今日一句话]
```

---

## 系统通知

```python
import subprocess, datetime
date_str = datetime.date.today().strftime('%Y-%m-%d')
y, m, d = date_str.split('-')
msg = f"每日晚报 {date_str} 已生成 → ~/Documents/Obsidian Vault/日报/{y}/{m}/{d}/evening.html"
subprocess.run(
    ['osascript', '-e', f'display notification "{msg}" with title "晚报"'],
    capture_output=True, text=True
)
```
