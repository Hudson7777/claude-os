# Morning Brief — Notification Configuration

## Output (choose one)

### Option A: Local HTML file (default, no setup needed)
Output path: ~/Desktop/morning-brief-{date}.html
Auto-open in browser: yes

### Option B: Webhook push (Slack / Telegram / Discord / 钉钉)
Set env var:
  export BRIEF_WEBHOOK_URL="https://hooks.slack.com/services/..."

The skill will POST a plain-text summary (≤4000 chars) to this URL.

### Option C: Obsidian note
Set env var:
  export OBSIDIAN_VAULT_PATH="/Users/you/ObsidianVault"

The skill will write a .md file to {OBSIDIAN_VAULT_PATH}/Briefs/morning-{date}.md
