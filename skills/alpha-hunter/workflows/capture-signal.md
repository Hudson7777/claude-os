# Workflow: Capture Signal

## When to use
The user wants to log a single observation: a CEO quote, a capex datapoint, a price move, a conference announcement, a research paper, etc. The defining trigger is **brevity** — the user is dropping a data point, not asking for analysis.

Examples:
- "刚看了Nadella访谈，他说现在缺的不是芯片是电"
- "记一下：海力士Q1电话会暗示HBM4良率改善"
- "@dylan522p 发了一条 800V DC的推，存一下"
- "Capture this: Microsoft capex指引上调到800亿"

## Operating principle
**Friction is the enemy of capture.** If the user has to think hard before logging, they won't log. Default to logging in ≤2 turns.

## Steps

### Step 1 — Parse what you have
From the user's message, try to extract:
- `signal_type`: ceo_quote | capex | roadmap | price | order | conference | paper | filing | other
- `source`: who/where (e.g., "NVIDIA Q3 2026 earnings call", "Bloomberg article 2026-04-15")
- `content`: the actual quote / data / observation
- `observed_at`: when the source published (default = today)
- `theme_slug` (if user mentioned a theme they're already tracking; otherwise leave NULL)

### Step 2 — Ask AT MOST one clarifying question
Only ask if you literally cannot fill the required fields (`signal_type`, `source`, `content`). Do NOT ask about interpretation, importance, or theme attachment — these are all optional.

If the user provided enough to log, **just log it**. Confirm the entry and stop.

### Step 3 — Run the script
```bash
cd <skill_root>
python3 scripts/add_signal.py \
    --type <signal_type> \
    --source "<source>" \
    --source-type <source_type> \
    --content "<content>" \
    --observed <YYYY-MM-DD> \
    [--theme <slug>] \
    [--importance <1-5>]
```

For multi-line content, prefer the `--json` form to avoid shell quoting issues:
```bash
python3 scripts/add_signal.py --json '{"signal_type":"ceo_quote", ...}'
```

### Step 4 — Confirm and stop
After the script runs, output:
- The signal id assigned
- One line acknowledging what was captured
- IF the signal feels high-importance (importance ≥ 4) AND it's not yet attached to a theme, ASK ONCE whether to create/attach a theme. Don't push.

**Do not** start a deep-dive in the same turn unless the user explicitly asks. Capture = capture.

## Importance heuristic (for setting --importance default)

| Importance | Heuristic |
|------------|-----------|
| 5 | CEO/CTO of category leader directly naming a new bottleneck (Stage 0 signal) |
| 4 | Capex structural shift / named roadmap change / supply-chain price anomaly |
| 3 | Notable but not novel; reinforces existing thesis |
| 2 | General industry color |
| 1 | Tangential / archive only |

If unclear, default to 3.

## After capture
Do NOT automatically:
- Search the web for more context
- Suggest related themes to research
- Re-state your earlier methodology

If the user wants more, they'll ask.
