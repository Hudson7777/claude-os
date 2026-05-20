# 早报 HTML 输出规范

## 文件路径

```
~/Desktop/morning-brief-YYYY-MM-DD.html
```

目录按需自动创建，写入前执行 `Path(out_path).parent.mkdir(parents=True, exist_ok=True)`。

Obsidian users: set `OBSIDIAN_VAULT_PATH` env var to write into `{OBSIDIAN_VAULT_PATH}/日报/YYYY/MM/DD/morning.html` instead.

---

## HTML 生成方式（必须遵守）

**禁止用 `str.replace()` 填充内容**。字符串替换对换行/空格极度敏感，静默失败时内容为空但不报错。

**必须用 BeautifulSoup 直接注入**：

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(template_html, 'html.parser')

# 示例：注入标题
soup.find(class_='section-title').string = "实际标题文字"

# 示例：注入多段正文
container = soup.find(class_='depth-block')
for p in container.find_all('p', recursive=False):
    p.decompose()  # 清空占位符
for text in paragraphs:
    new_p = soup.new_tag('p')
    new_p.string = text
    container.append(new_p)

# 写入文件
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(str(soup), encoding='utf-8')
```

**验证步骤（每次生成后必做）**：用 BeautifulSoup 重新读取生成文件，检查每个板块的 `p` 标签数量 > 0，标题不等于占位符字符串。任何板块为空立即报错重试，不允许静默失败。

---

## HTML 模板文件

HTML 设计模板存放于：`references/html-template-morning.html`

**每次生成时必须读取该文件作为基础模板**，不要自己重写 CSS/HTML 结构。

---

## 内容规范

### 板块一：AI & 科技前沿（8-9条）
- 国外信源 >80%
- 每条 3 段正文：发生了什么 / 背景与技术细节 / 为什么重要
- 覆盖多个细分方向，避免全部集中在同一主题
- 有数据的尽量精确

### 板块二：宏观财经（6条）
- 覆盖：货币政策、地缘/能源、全球市场、中美贸易、产业政策
- 每条 3 段，含具体数据和传导分析

### 板块三：今日深度（约2000字）
- 1个议题，不限话题
- 结构：引子（1段）+ 核心分析（4-5段）+ 观点追问（1段）

---

## HTML 生成（BS4 注入，禁止 str.replace 填内容）

```python
from bs4 import BeautifulSoup
from pathlib import Path
import datetime, os

date = datetime.date.today()
y, m, d = date.strftime('%Y'), date.strftime('%m'), date.strftime('%d')
date_str = date.strftime('%Y-%m-%d')

vault = os.environ.get('OBSIDIAN_VAULT_PATH')
if vault:
    out_path = Path(vault) / '日报' / y / m / d / 'morning.html'
else:
    out_path = Path.home() / 'Desktop' / f'morning-brief-{date_str}.html'

out_path.parent.mkdir(parents=True, exist_ok=True)

tmpl = Path("~/.claude/skills/morning-brief/references/html-template-morning.html").expanduser().read_text()

# 元数据替换（简单变量，str.replace 可以）
html = tmpl.replace('{{DATE_DISPLAY}}', f'{date.year}年{date.month}月{date.day}日')
html = html.replace('{{WEEKDAY}}', ['星期一','星期二','星期三','星期四','星期五','星期六','星期日'][date.weekday()])
html = html.replace('{{GEN_TIME}}', datetime.datetime.now().strftime('%H:%M'))
html = html.replace('{{HERO_HEADLINE}}', hero_headline)
html = html.replace('{{HERO_HEADLINE_EM}}', hero_em)
html = html.replace('{{HERO_SUB}}', hero_sub)

soup = BeautifulSoup(html, 'html.parser')

# AI 板块：清空占位符，逐条注入
ai_section = soup.find(id='ai')
for el in ai_section.find_all(class_='article-item'):
    el.decompose()
for art in ai_articles:  # list of {headline, headline_en, source, paragraphs, body_en}
    item = soup.new_tag('div', attrs={'class': 'article-item'})
    h = soup.new_tag('div', attrs={'class': 'article-headline'}); h.string = art['headline']; item.append(h)
    if art.get('headline_en'):
        hen = soup.new_tag('div', attrs={'class': 'article-headline-en'}); hen.string = art['headline_en']; item.append(hen)
    s = soup.new_tag('div', attrs={'class': 'article-source'}); s.string = art['source']; item.append(s)
    for i, text in enumerate(art['paragraphs']):
        p = soup.new_tag('p'); p.string = text; item.append(p)
        if i == 0 and art.get('body_en'):
            pen = soup.new_tag('p', attrs={'class': 'article-en'}); pen.string = art['body_en']; item.append(pen)
    ai_section.append(item)

# 宏观板块：同上
macro_section = soup.find(id='macro')
for el in macro_section.find_all(class_='article-item'):
    el.decompose()
for art in macro_articles:
    item = soup.new_tag('div', attrs={'class': 'article-item'})
    h = soup.new_tag('div', attrs={'class': 'article-headline'}); h.string = art['headline']; item.append(h)
    if art.get('headline_en'):
        hen = soup.new_tag('div', attrs={'class': 'article-headline-en'}); hen.string = art['headline_en']; item.append(hen)
    s = soup.new_tag('div', attrs={'class': 'article-source'}); s.string = art['source']; item.append(s)
    for i, text in enumerate(art['paragraphs']):
        p = soup.new_tag('p'); p.string = text; item.append(p)
        if i == 0 and art.get('body_en'):
            pen = soup.new_tag('p', attrs={'class': 'article-en'}); pen.string = art['body_en']; item.append(pen)
    macro_section.append(item)

# 深度板块
db = soup.find(class_='depth-block')
db.find(class_='depth-title').string = depth_title
for p in db.find_all('p', recursive=False):
    p.decompose()
opinion = db.find(class_='depth-opinion')
opinion.string = depth_opinion
for text in depth_paragraphs:
    p = soup.new_tag('p'); p.string = text
    opinion.insert_before(p)

out_path.write_text(str(soup), encoding='utf-8')
```

**生成后验证（必做，任何板块为空立即报错）**：

```python
check = BeautifulSoup(out_path.read_text(), 'html.parser')
assert len(check.find(id='ai').find_all(class_='article-item')) >= 8, "AI板块不足8条"
assert len(check.find(id='macro').find_all(class_='article-item')) >= 6, "宏观板块不足6条"
assert len(check.find(class_='depth-block').find_all('p')) >= 4, "深度板块段落不足"
```

---

## Obsidian md 摘要规范（optional）

If `OBSIDIAN_VAULT_PATH` is set, also write a companion `.md` file:

```markdown
---
date: YYYY-MM-DD
type: morning-brief
topics: [从深度议题和AI新闻中提取 3-5 个关键词]
html-path: "{OBSIDIAN_VAULT_PATH}/日报/YYYY/MM/DD/morning.html"
---

## AI & 科技前沿
- [标题1]（来源）
- ...（共8-9条）

## 宏观财经
- [宏观事件1]
- ...（共6条）

## 今日深度
**议题**：[议题标题]
[2-3句话摘要深度分析的核心观点]
```
