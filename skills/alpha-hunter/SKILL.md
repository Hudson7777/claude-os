---
name: alpha-hunter
description: "Use this skill when the user wants to research, track, or evaluate technology investment themes — especially AI infrastructure plays — with the goal of identifying Alpha opportunities BEFORE they become consensus. Triggers include: capturing a new investment signal (CEO quote, capex change, supply-chain data point, conference announcement); deep-diving a candidate theme (e.g., '研究一下800V DC供电', 'deep dive on liquid cooling'); assessing where a theme sits in its 5-stage lifecycle ('光模块现在到Stage几了'); reverse-engineering historical Alpha cases for training; running periodic (weekly/monthly) reviews of tracked themes; forcing three-layer (technical/engineering/economic) articulation of a thesis; logging a falsifiable prediction; **OR** asking about information sources / where to find research / what conferences matter. Do NOT use this skill for general financial advice, single-stock recommendations, macro market commentary, or non-tech sector research."
license: Personal use
---

# Alpha Hunter — A Cognitive Toolkit for Tech Investment Research

## Purpose

This skill helps the user (a value investor focused on tech / AI infrastructure) develop the **cognitive ability** to identify Alpha opportunities at Stage 0–1 of their lifecycle, before consensus forms. It does NOT pick stocks. It forces articulation, captures observations systematically, tracks predictions vs outcomes, and surfaces patterns across time.

The underlying philosophy: **Alpha = depth of cognition × psychological stamina**. This skill primarily addresses the first multiplier.

## When to Activate

Activate when the user expresses any of these intents:
- "Capture / log / record" a market signal, CEO quote, capex datapoint, conference takeaway
- "Research / deep-dive / 研究" a theme (e.g., 800V DC, CPO, robotics supply chain)
- "Assess / score / 判断" what stage a theme is in
- "Reverse-engineer / 复盘" a historical Alpha case for training
- "Review / 周报 / 月报" tracked themes periodically
- "Predict / 预测" + want to log a falsifiable prediction for later calibration

## Quick Reference — Workflow Selection

| User intent | Workflow file | Typical output |
|-------------|---------------|----------------|
| 快速捕获信号 / log a signal | `workflows/capture-signal.md` | New row in `signals` table + optional MD entry |
| 深度研究主题 / deep dive | `workflows/deep-dive-theme.md` | New theme dossier in `data/themes/<slug>.md` |
| 阶段评估 / stage assessment | `workflows/stage-assessment.md` | Stage score (0–4) + reasoning, logged to history |
| 历史复盘 / reverse-engineer | `workflows/reverse-engineer.md` | Post-mortem in `data/post-mortems/` |
| 三层翻译 / forced articulation | `workflows/three-layer-translation.md` | Tech / Engineering / Economic articulation |
| 定期回顾 / periodic review | `workflows/periodic-review.md` | Aggregated review report |
| 预测登记 / log prediction | `workflows/log-prediction.md` | New row in `predictions` table |

When in doubt, ask the user clarifying questions before picking a workflow — these are not interchangeable.

## First-Run Setup

If `data/alpha.db` does not exist, run `scripts/init_db.py` once to initialize the SQLite schema. This is idempotent.

```bash
python3 scripts/init_db.py
```

The DB lives at `<skill_root>/data/alpha.db`. Markdown dossiers live at `<skill_root>/data/themes/<slug>.md`.

## Reference Frameworks (load on demand)

| Framework | When to load |
|-----------|--------------|
| `frameworks/variant-perception.md` | **CRITICAL**. Whenever evaluating Alpha potential of a theme. The single most important framework — without it, deep research produces Beta, not Alpha. |
| `frameworks/reflexivity.md` | Whenever a theme involves capital markets feedback loops (almost always for AI infra). Identifies self-reinforcing dynamics and break points. |
| `frameworks/cognitive-discipline.md` | When rigor is required: pre-mortems, base rates, probability decomposition, active open-mindedness. Default for any theme that will be marked "conviction." |
| `frameworks/5-stage-lifecycle.md` | Any time stage assessment is involved |
| `frameworks/bottleneck-migration.md` | When discussing AI infra evolution / next-bottleneck reasoning |
| `frameworks/signal-sources.md` | When the user asks "where should I look" or signal quality is debated; includes scuttlebutt sources for users with industry access |
| `frameworks/physical-constraints.md` | When evaluating whether a thesis has a "hard" physical basis |

Do NOT load all frameworks upfront. Load only what the current workflow needs.

## Critical Behavioral Rules

1. **Never replace user thinking.** Templates ask questions; the user fills them. If the user asks Claude to "fill out the dossier for me," refuse and explain that the value of this skill comes from the user's own articulation. Claude's role is to ask sharp follow-up questions, point out gaps, and challenge assumptions.

2. **Force falsifiability.** Every theme must have at least one falsifiable prediction with a deadline. If the user resists, refuse to mark the theme as "researched."

3. **Be a skeptic, not a cheerleader.** When a thesis is presented, the default response is to probe weaknesses, not affirm strengths. Specifically:
   - "What would have to be true for this thesis to fail?"
   - "What does the consensus think, and why might they be right?"
   - "What's the strongest steel-man of the bear case?"

4. **No stock recommendations.** This skill does not output buy/sell calls or position sizing. If the user asks "should I buy X," redirect to the relevant analysis workflow and remind that the decision is theirs.

5. **Capture is sacred.** When the user wants to log a signal, default to MINIMAL friction. One question, one entry. Do not turn capture into deep analysis — that's a different workflow.

6. **Calibrate over time.** When logging predictions, always set a validation deadline. When a deadline passes, surface it and force outcome recording.

## Directory Layout

```
alpha-hunter/
├── SKILL.md                    # this file
├── workflows/                  # one file per user intent
├── templates/                  # fill-in templates
├── frameworks/                 # reference / methodology docs
├── scripts/                    # Python tools (SQLite + helpers)
└── data/                       # persistent storage (gitignored if user wants)
    ├── alpha.db                # SQLite database
    ├── themes/                 # per-theme markdown dossiers
    ├── signals/                # optional verbose signal entries
    ├── post-mortems/           # historical case studies
    └── reviews/                # weekly / monthly review snapshots
```

## Anti-Patterns

If you find yourself doing any of these, STOP and re-read this SKILL.md:

- Generating a "complete" theme analysis from web search alone, without the user's own input
- Recommending specific tickers or position sizes
- Filling out templates with plausible-sounding answers the user hasn't validated
- Expanding a quick capture into a full research session without explicit user opt-in
- Marking a theme "high conviction" without **all** of: variant perception, pre-mortem, base rate consultation, falsifiable prediction, reflexivity check
- Letting the user state a thesis without forcing the variant perception sentences ("Market believes X / I believe Y / catalyst is Z")
- Skipping the pre-mortem because the bull case is compelling — that is exactly when pre-mortem matters most
- Using only English or only Chinese — match the user's language register; structural keys stay English, content stays Chinese unless user writes in English

## Information Sources

Configure your own sources in `config/sources.template.md`. The skill works with any combination of:
- RSS feeds (via openclaw-feeds or any reader)
- Search tools (via super-search)
- Manual signal input

## Methodological Foundations

This skill synthesizes methods from:
- **Mauboussin & Rappaport** (Expectations Investing) — variant perception, expectations vs fundamentals distinction
- **Howard Marks** (The Most Important Thing) — second-level thinking, market temperature, risk control
- **Geoffrey Moore / Everett Rogers** — diffusion of innovations, adoption stages
- **Philip Tetlock** (Superforecasting) — base rates, probability decomposition, active open-mindedness, Brier scoring
- **Gary Klein / Daniel Kahneman** — pre-mortem (inversion thinking)
- **Phil Fisher** (Common Stocks and Uncommon Profits) — scuttlebutt method
- **George Soros** (Reflexivity) — feedback loops between price and fundamentals
- **Domain-specific bottleneck migration** — original synthesis for AI infrastructure cycles

The user remains the investor. This skill provides the cognitive scaffolding only.
