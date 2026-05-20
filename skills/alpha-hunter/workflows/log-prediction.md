# Workflow: Log Prediction

## When to use
The user wants to register a falsifiable prediction tied to a theme. Triggers:
- "我赌一个：<prediction>"
- "log a prediction: <prediction>"
- As mandatory final step of `deep-dive-theme.md`
- When the user says something that sounds confident: "I think X will happen by Y" — gently ask if they want to log it.

## Operating principle
The point of logged predictions is **calibration over time**. Predictions without deadlines are wishes; predictions without confidence levels are noise; predictions without observable validation signals are unfalsifiable. This workflow enforces all three.

## Steps

### Step 1 — Force falsifiability
The prediction MUST be:
- **Specific**: Not "AI infra will keep being important." Yes "≥1 hyperscaler will publicly announce 800V DC deployment."
- **Observable**: Tied to a publicly verifiable signal (announcement, financial filing, market price level, government report).
- **Time-bound**: Has a specific deadline date, not "eventually" or "next year-ish."

If the user proposes a prediction that fails any of these, push back until they tighten it. Examples of pushback:

| User's first attempt | What's wrong | Pushback |
|----------------------|--------------|----------|
| "光模块还会涨" | Not specific, not falsifiable | "By when, and how much? What price level would prove you wrong?" |
| "存储周期会反转" | Not observable in a hard sense | "What metric tells you it reverted? DRAM contract price level? Inventory weeks? Memory company gross margins?" |
| "电力会成为瓶颈" | Not time-bound | "By what date? And what specific event would confirm it became 'the' bottleneck?" |

### Step 2 — Articulate validation signals
Beyond the prediction itself, ask the user to list 1–3 specific signals that, if observed, would confirm the prediction. Examples:
- "OCP公开submit 800V DC architecture spec"
- "Microsoft / Meta / Google任一财报会议明确提及800V DC部署"
- "Vertiv / Delta / Eaton任一公司财报中800V DC相关营收单独披露"

The validation signals serve as the user's "tripwire list" — they tell you what to watch for in news/research between now and the deadline.

### Step 3 — Calibrate confidence
Force a 0.0–1.0 number. Common framings to help the user:
- 0.5 = coin flip; should not be logged unless tied to a major theme as a "watch this"
- 0.6–0.7 = "I lean this way"
- 0.7–0.8 = "I'd be willing to size this in my portfolio based on this view"
- 0.8–0.9 = "I'd be surprised and would seek to understand my error if this is wrong"
- 0.9+ = "Near-certain in my view"; reserve for rare cases

If the user keeps saying 0.9 or 0.95, that's a calibration warning sign — they're likely overconfident. After 5+ closed predictions, the calibration query will show whether their confidence is well-calibrated.

### Step 4 — Set a deadline
The deadline should be:
- **Long enough** that the prediction is meaningful (typically 3–18 months)
- **Short enough** that you'll actually check (rarely > 24 months — predictions that far out are usually too vague to be falsifiable)

If the prediction is "this will eventually happen but I don't know when," it's not a prediction yet — it's a thesis. Push the user to either (a) tighten the timing or (b) reformulate as a thesis statement instead.

### Step 5 — Log

```bash
cd <skill_root>
python3 scripts/log_prediction.py \
    --theme <slug> \
    --prediction "<prediction>" \
    --signals "<signal 1>\n<signal 2>\n<signal 3>" \
    --confidence <0.0-1.0> \
    --deadline <YYYY-MM-DD>
```

Confirm the logged prediction back to the user with the id, then stop.

## Closing predictions

When the deadline passes (surfaced via `query.py predictions --overdue` during periodic review), use:

```bash
python3 scripts/log_prediction.py --close <id> \
    --outcome <correct|wrong|partial> \
    --notes "<what happened>" \
    --lessons "<what I learned>"
```

The `--lessons` field is mandatory. No skipping. The whole point is to extract a transferable lesson, especially from wrong predictions.

## Anti-patterns

- **Don't accept vague predictions.** "AI will be big" is not a prediction. Reject it firmly.
- **Don't accept "I'm 100% sure."** No one is. Push for 0.85–0.9 max.
- **Don't predict when the user hasn't done the underlying research.** Logging a prediction is a downstream artifact of a thesis. If the thesis is half-baked, the prediction will be too. Suggest deep-dive-theme first.
- **Don't auto-close predictions.** The user must actively decide outcome — that's the calibration training.
