# Evening Brief — Notification Configuration

## Output (choose one)

### Option A: Local HTML file (default, no setup needed)
Output path: ~/Desktop/evening-brief-{date}.html
Auto-open in browser: yes

### Option B: Webhook push (Slack / Telegram / Discord / 钉钉)
Set env var:
  export BRIEF_WEBHOOK_URL="https://hooks.slack.com/services/..."

### Option C: Obsidian note
Set env var:
  export OBSIDIAN_VAULT_PATH="/Users/you/ObsidianVault"
