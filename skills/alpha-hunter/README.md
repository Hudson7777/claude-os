# alpha-hunter

**Level:** 📐 template — configure `config/sources.md` and `config/investment-profile.md`

A systematic framework for identifying technology investment opportunities before they reach consensus. Built around three original analytical tools: the 5-stage technology lifecycle model, the three-layer translation method, and a cognitive discipline framework.

→ **Read the full framework:** [FRAMEWORK.md](./FRAMEWORK.md)

## What it does

- **Signal capture:** When you encounter a data point (CEO quote, supply-chain anomaly, paper), the skill structures it into the framework automatically
- **Stage assessment:** Ask where a theme sits in the lifecycle; get a structured analysis
- **Deep dive:** Full lifecycle + three-layer analysis of any tech theme
- **Prediction logging:** Falsifiable predictions with timestamps and evidence requirements
- **Periodic review:** Weekly/monthly structured review of tracked themes

## Setup

```bash
# 1. Copy and fill in your configuration
cp config/sources.template.md config/sources.md
cp config/investment-profile.template.md config/investment-profile.md
# Edit both files with your own focus areas

# 2. Install the skill
cp -r alpha-hunter ~/.claude/skills/
```

## Usage examples

```
"新信号：Broadcom CEO mentioned XPU custom silicon demand exceeding expectations"
"Where is liquid cooling in the lifecycle? 液冷现在到 Stage 几了？"
"Deep dive on 800V DC power architecture for AI data centers"
"Log prediction: TSMC CoWoS capacity constraint resolves in 2025Q3"
"Monthly review of my tracked themes"
```
