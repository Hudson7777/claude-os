# evening-brief

**Level:** configure — fill in `config/sources.template.md`, set optional notification

Generates a daily evening recap. Four sections:

- **Today's News** — top stories of the day
- **Deep Dive** — one story analyzed in depth
- **Knowledge Boost** — one non-obvious insight (science, history, tech)
- **Human Moment** — a cultural or personal reflection piece

Output: local HTML file or optional webhook push.

## Dependencies

Requires `openclaw-feeds`:
```bash
claude plugin install github:nesdeq/openclaw-feeds
```

## Setup

1. Copy `config/sources.template.md` → `config/sources.md` and fill in your preferences
2. (Optional) Set `BRIEF_WEBHOOK_URL` — see `config/notification.template.md`

## Usage

Say: "晚报" / "evening brief"

## Installation

```bash
cp -r evening-brief ~/.claude/skills/
```
