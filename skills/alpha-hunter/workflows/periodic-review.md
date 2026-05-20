# Workflow: Periodic Review (Weekly / Monthly)

## When to use
Triggered by:
- "周回顾 / weekly review"
- "月报 / monthly review"
- "review my themes"
- Or proactively after capturing 10+ signals without a review

This workflow aggregates state across all tracked themes and forces the user to act on what's accumulated.

## Operating principle
A cognitive system without periodic forcing functions accumulates entropy. This review is the forcing function: it surfaces stale themes, overdue predictions, and patterns the user may have missed.

## Steps

### Step 1 — Snapshot the state
```bash
python3 scripts/query.py themes
python3 scripts/query.py signals --since <today minus review window>
python3 scripts/query.py predictions --pending
python3 scripts/query.py predictions --overdue
python3 scripts/query.py calibration
```

For monthly review, also run:
```bash
# All themes that haven't been touched in 30+ days
sqlite3 data/alpha.db "SELECT slug, name_cn, status, julianday('now') - julianday(updated_at) AS days_stale FROM themes ORDER BY days_stale DESC"
```

### Step 2 — Walk through 5 review questions

Ask the user to answer each. Don't move on until they do.

**Q1 — Overdue predictions (CRITICAL)**
For every prediction past its deadline that is still 'pending':
- Did it come true? Partially? Wrong?
- Close it out via `scripts/log_prediction.py --close <id> --outcome <correct|wrong|partial>`
- Force a `--lessons` entry. No skipping.

**Q2 — Stale themes**
For every theme not updated in 30+ days:
- Is it still worth tracking?
- If yes, what's the next signal that would change your mind?
- If no, mark it `--status killed` or `--status exited` with a one-line reason.

**Q3 — High-importance signals nobody acted on**
Look at signals with importance ≥ 4 from the past period. For each:
- Did this lead to a research task or a position change?
- If not, why not? (Was the signal not actually that important? Or was it dropped on the floor?)

**Q4 — Stage transitions**
Compare current stage assessment vs assessment from start of period.
- Any theme that moved up a stage: did position size change?
- Any theme that's been at the same stage for 6+ months: is the thesis stuck or am I underestimating it?
- Any theme that should have moved up but didn't: re-evaluate.

**Q5 — Bottleneck migration check**
Re-load `frameworks/bottleneck-migration.md`. Ask:
- What was the dominant bottleneck 6 months ago?
- What's the dominant bottleneck now?
- What is likely to be the dominant bottleneck 6–12 months from now?
- Are my themes positioned for the next bottleneck, or for the current one?

### Step 3 — Calibration check
```bash
python3 scripts/query.py calibration
```
This shows the hit rate by confidence bucket. Read the output with the user:
- If 0.7-confidence predictions hit 50% of the time → you're systematically overconfident
- If 0.5-confidence predictions hit 80% of the time → you're systematically underconfident; bigger conviction is warranted
- Adjust how you set future confidence values accordingly

### Step 4 — Persist the review
Save a snapshot to `data/reviews/<YYYY-MM-DD>-review.md` using `templates/review.md`. The snapshot captures:
- State at this date
- Decisions made (themes killed, stages updated, predictions closed)
- New research tasks committed to for next period

The persistence is the discipline. Without writing it down, "review" becomes "vibes check."

### Step 5 — Set 3 concrete tasks for next period
End the review by having the user commit to **at most 3 specific, time-bound research tasks** for the next period. Examples:
- "Research the SiC supply chain deep dive by next monthly review"
- "Reverse-engineer the铀矿 case to extract patterns by month-end"
- "Test current themes against the bottleneck-migration framework"

3 max. If they say 5, push back: "Which 2 are you actually going to deprioritize?"

## Cadence guidance

- **Weekly review (light)**: Just Q1 (overdue) and Q3 (high-importance signals). 15–20 min.
- **Monthly review (full)**: All 5 questions + calibration + 3 tasks. 60–90 min.
- **Quarterly review (deep)**: Monthly review + reverse-engineer 1 historical case + write a forward-looking memo. Half a day.

## Anti-patterns

- **Don't skip overdue predictions.** This is the calibration loop. If the user keeps deferring, the entire skill loses its value.
- **Don't review without writing.** The output is a markdown file; if it's not saved, it didn't happen.
- **Don't review too often.** Daily reviews destroy long-term thinking. Weekly minimum, monthly is the sweet spot.
