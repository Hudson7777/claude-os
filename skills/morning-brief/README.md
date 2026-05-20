# morning-brief

**Level:** configure — fill in `config/sources.template.md`, set optional notification

Generates a daily AI + markets digest. Three sections:

- **AI & Tech** — model releases, infra developments, research papers
- **Finance** — macro indicators, your watchlist names, sector moves  
- **Deep Dive** — one story with 3-layer analysis (what happened / implications / signal strength)

Output: local HTML file (beautiful, date-stamped) or optional webhook push.

## Dependencies

Requires `openclaw-feeds` for RSS aggregation (public skill):

```bash
claude plugin install github:nesdeq/openclaw-feeds
```

## Setup

1. Copy `config/sources.template.md` to `config/sources.md` and fill in your focus areas
2. (Optional) Set `BRIEF_WEBHOOK_URL` for push notification — see `config/notification.template.md`

## Usage

Say: "早报" / "morning brief" / "generate morning brief"

Or automate with Claude Code cron: runs every weekday at 7am.

## Installation

```bash
cp -r morning-brief ~/.claude/skills/
```
