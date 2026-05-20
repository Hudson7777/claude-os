# Workflow: Reverse-Engineer (Historical Post-Mortem)

## When to use
The user wants to study a past Alpha case to learn pattern recognition. Triggers:
- "复盘一下HBM"
- "Reverse-engineer optical modules 2024"
- "我想分析一下当年英伟达是怎么涨起来的"

This workflow is **training**, not investing. The output is a post-mortem at `data/post-mortems/<slug>.md` and a row in the `post_mortems` table.

## Operating principle
The point is not "what was this story" — the point is "what signals existed at what time, that I would have needed to see in order to have caught this BEFORE consensus formed." Walk the timeline backward from peak euphoria to earliest leading indicator.

The user does the reasoning. Claude is the timeline keeper and the question-asker.

## Steps

### Step 1 — Define the case period
Pin down:
- **Theme name** (e.g., "HBM 2023-2024", "Optical modules 2023-2025")
- **Stage 4 peak** (when did awareness become mass-market? Define this with a specific event: e.g., "雪球热搜 / CNBC头条 / 出租车司机讨论了")
- **Stage 0 origin** (when was the technical/physical necessity first observable? Usually a paper, conference talk, or roadmap announcement)

Force specificity. "It was hot in 2024" is not enough. "Peak euphoria was June 2024 when [specific event]" is.

### Step 2 — Reconstruct the signal timeline
Ask the user to reconstruct, in order:

| Date | Stage | Signal | Source | Was this knowable in real time? |
|------|-------|--------|--------|--------------------------------|

Walk from earliest signal forward. For each signal, ask:
- Where would the user have seen this signal at the time?
- What was the dominant narrative at that moment? (i.e., what was the market focused on instead?)
- How long after this signal did consensus form?

This timeline is the most valuable training artifact. **Make sure 5–10 entries minimum.**

### Step 3 — Counterfactual analysis
For each Stage 0/1 signal:
- Was this signal in your information diet at the time?
- If yes: why did you NOT act on it?
- If no: what part of your information diet would have included it?

The diagnosis matters more than the regret. Common failure modes:
- "I saw the signal but dismissed it because [pattern X]"
- "I didn't see it because I wasn't reading [source Y]"
- "I saw it but didn't have the technical depth to evaluate it"

### Step 4 — Pattern extraction
Have the user write 2–4 transferable lessons in the form: **"Next time I see <pattern>, I should <action>."**

Examples (illustrative, not for the user to copy):
- "Next time the largest customer of a category publicly says 'this is now my biggest constraint,' put the supply chain on watch immediately."
- "Next time TSMC capex on a specific advanced packaging line jumps >2x, deeply research downstream substrate suppliers within 30 days."

These pattern rules should be specific enough to act on, not generic ("pay more attention").

### Step 5 — Persist

```bash
sqlite3 data/alpha.db <<EOF
INSERT INTO post_mortems (slug, name_cn, case_period, earliest_signal, consensus_signal, lessons)
VALUES ('<slug>', '<name>', '<period>', '<earliest signal>', '<consensus signal>', '<lessons text>');
EOF
```

And save the full timeline + counterfactual + lessons to `data/post-mortems/<slug>.md` using `templates/post-mortem.md`.

### Step 6 — Connect forward
The most powerful training move: ask the user to **identify whether any signal pattern from the post-mortem is currently appearing in another theme they track**.

Run:
```bash
python3 scripts/query.py themes
```

For each tracked theme, ask: "Does the early signal pattern from <post-mortem> match anything you're seeing here?" If yes, that's a high-priority research task.

## Anti-patterns

- **Don't let the user write a hagiography.** "I knew it all along" is useless. The whole value is in the moments where the signal was visible but ignored or misread.
- **Don't summarize the case from web search.** The reconstruction must come from the user's own memory, supplemented by primary sources where available. If the user genuinely doesn't remember, that's also a useful data point: "Why was this case not in my memory?"
- **Don't accept generic lessons.** "Read more research" is not actionable. "Subscribe to TrendForce monthly DRAM contract price report and check on day 1 of every month" is.

## Recommended cases to reverse-engineer (priority order, illustrative only)
1. NVIDIA 2022→2024 (the foundational AI Alpha case)
2. HBM (海力士) 2023→2024
3. CoWoS (TSMC先进封装) 2023→2024
4. 光模块 (中际旭创等) 2024→2025
5. AI电力 (Vistra, Constellation) 2024→2025
6. 铀矿 (Cameco etc.) 2024→2025
7. PCB高速材料 2024→2025

Doing 5+ reverse-engineerings before doing forward-prediction is HIGHLY recommended for calibration.
