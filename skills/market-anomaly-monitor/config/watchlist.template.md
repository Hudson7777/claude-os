# Market Anomaly Monitor — Configuration

## Notification

```bash
# Optional: webhook URL for push notifications
# Supports Slack, Telegram, Discord, 钉钉, or any HTTP endpoint
export ANOMALY_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

If not set, the report is written to `/tmp/market-anomaly-{date}.md`.

## Watchlist (optional customization)

The skill monitors a default set of global markets. To customize, edit the
watchlist in `scripts/fetch_prices.py`. Default coverage:

**US equities (indices + key names):**
- S&P 500 (^GSPC), NASDAQ (^IXIC), QQQ
- NVDA, MSFT, AAPL, AMZN, META, GOOG, AMD

**HK equities:**
- Hang Seng Index (^HSI)
- 0700.HK (Tencent), 9988.HK (Alibaba)

**Crypto:**
- BTC-USD, ETH-USD

**Macro indicators:**
- VIX (^VIX), DXY (DX-Y.NYB), US10Y (^TNX)

## Anomaly detection thresholds

Default: flag any move > ±3% intraday or > ±5% over 5 days.
To customize, set env vars:

```bash
export ANOMALY_INTRADAY_PCT=3.0   # default: 3.0
export ANOMALY_5DAY_PCT=5.0       # default: 5.0
```
