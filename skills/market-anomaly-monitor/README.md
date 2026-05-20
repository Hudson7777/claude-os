# market-anomaly-monitor

**Level:** configure — optional webhook for notifications

Detects price anomalies across global markets (US stocks, HK stocks, crypto, macro indicators) and automatically searches for triggering events (policy, earnings, geopolitical). Outputs: price change + event attribution + impact analysis.

## What it monitors

- US equities (S&P 500, NASDAQ, key tech names)
- HK equities
- Crypto (BTC, ETH)
- Macro indicators (VIX, DXY, yields)

## Output

Writes a markdown report to `/tmp/market-anomaly-{date}.md`. Optional webhook push (Slack / Telegram / Discord / 钉钉).

## Configuration

```bash
# Optional: set webhook for push notifications
export ANOMALY_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

## Usage

Trigger: "股市异动" / "today's market anomalies" / "market monitor"

Run automatically via cron: set a Claude Code cron task to trigger this skill daily at market close.

## Installation

```bash
cp -r market-anomaly-monitor ~/.claude/skills/
```
