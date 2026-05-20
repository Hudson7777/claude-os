# wechat-article-save

**Level:** plug-in — works immediately after installation  
**Trigger:** Paste any `mp.weixin.qq.com` URL into the chat

Automatically detects WeChat article URLs and saves the full content — no explicit command needed. Just paste the link.

## What it does

- Detects `mp.weixin.qq.com` URLs on paste
- Fetches full article content via browser automation
- Saves to a local markdown file

## Installation

Copy the `wechat-article-save/` directory into `~/.claude/skills/`:

```bash
cp -r wechat-article-save ~/.claude/skills/
```

## Usage

Paste a WeChat article URL anywhere in your Claude Code chat. The skill triggers automatically.
