# Workflow: Stage Assessment

## When to use
The user wants to evaluate where a theme sits in its 5-stage lifecycle. Triggers:
- "光模块现在到Stage几了"
- "帮我评估一下 <theme> 的成熟度"
- "<theme> 还能买吗" — translate this internally to "What stage is it at?"

The 5-stage framework is in `frameworks/5-stage-lifecycle.md`. **Load it before running this workflow.**

## Operating principle
Stage assessment is judgment under uncertainty. The output is a stage (0–4) PLUS a confidence level (0.0–1.0) PLUS reasoning. Never give a stage without all three. Never give a stage without checking the user's own reasoning first — your role is to challenge, not to declare.

## Steps

### Step 1 — Confirm the theme exists
```bash
python3 scripts/query.py themes --json | grep <slug>
```
If not, the user needs to create it first via deep-dive-theme.

### Step 2 — Walk the 5-stage diagnostic checklist
Ask the user to answer (don't answer for them; they assess, you probe):

**Stage 0 indicators (Technical Necessity, awareness <5%)**
- [ ] Only mentioned in academic papers, conference talks, or insider technical blogs?
- [ ] Zero or near-zero coverage in mainstream financial media?
- [ ] No sell-side analyst initiation reports?
- [ ] CEO抱怨提取信号刚出现，且尚未被市场广泛解读?

**Stage 1 indicators (Industry Consensus Forming, awareness 5–15%)**
- [ ] Specialty research outlets (SemiAnalysis, The Information) have published deep dives?
- [ ] Supply-chain price/order anomalies showing up in TrendForce/DigiTimes?
- [ ] Top vendors' earnings Q&A sections beginning to address the topic directly?
- [ ] One or two sell-side analysts have quietly upgraded category leaders?
- [ ] But: still NOT a top-of-mind topic on Twitter / 雪球 / mainstream channels?

**Stage 2 indicators (Smart Money Building Positions, 15–40%)**
- [ ] Specialist hedge funds and sector PMs visibly building positions (13F, fund letters)?
- [ ] Multiple sell-side initiations with positive-but-cautious tone?
- [ ] Stock prices showing structural uptrends but with sharp drawdowns (high vol)?
- [ ] Theme has a name now (e.g., "AI power", "光互联")?

**Stage 3 indicators (Sell-Side Consensus, 40–70%)**
- [ ] All major sell-side houses have it as top pick / overweight?
- [ ] Mutual funds significantly overweight vs benchmark?
- [ ] Mainstream financial media (Bloomberg/CNBC/华尔街见闻) doing weekly coverage?
- [ ] Multiple expansion (P/E, P/S) into top quartile of historical range?

**Stage 4 indicators (Mass Awareness, >70%)**
- [ ] 雪球热帖 / Twitter retail / TikTok / 出租车司机讨论?
- [ ] IPO窗口打开，新公司争相用此主题做包装?
- [ ] Multiple expansion已超过历史顶部?
- [ ] 出现"这次不一样"叙事?

### Step 3 — Stage decision rule

The user's stage is determined by the HIGHEST stage where they can check ≥60% of the indicators. If they can check Stage 2 indicators but also Stage 3 indicators, the theme is at Stage 2/3 transition — typical for themes that are "ripening fast."

**Confidence calibration:**
- 0.8–1.0: Most indicators of one specific stage check, very few of adjacent stages
- 0.5–0.8: Theme spans two stages, evidence ambiguous
- <0.5: User has too few data points; the assessment is more guess than judgment — push them to gather more data before logging

### Step 4 — Compare with prior assessment
```bash
python3 scripts/query.py stage-history --theme <slug>
```

If a prior assessment exists, ask: "What changed since [last assessed_at] that justifies this new stage?" If the answer is "nothing new, I just feel different about it," that's a red flag — don't update the stage on vibes.

### Step 5 — Log the assessment
Update the theme record AND append to stage_history:
```bash
python3 scripts/add_theme.py --slug <slug> --name-cn "<name>" --stage <0-4> --stage-confidence <0.0-1.0>
```
(`add_theme.py` automatically appends to stage_history when --stage is provided.)

For a more detailed stage_history entry with reasoning, use a direct SQL insert:
```bash
sqlite3 data/alpha.db "INSERT INTO stage_history (theme_slug, stage, confidence, reasoning) VALUES ('<slug>', <stage>, <conf>, '<reasoning>')"
```

### Step 6 — Output

Format:
```
Theme: <name_cn> (<slug>)
Stage: <0-4>  (confidence: <0.0-1.0>)
Reasoning: <one paragraph>
Implication: <Alpha left? Stage 0-2 = yes, Stage 3 = mostly Beta, Stage 4 = exit signal>
Next action: <what data point would change the assessment>
```

## Anti-patterns

- **Don't anchor on price action.** A theme with strong fundamentals can be at Stage 1 even after a 50% drawdown; conversely, a Stage 4 theme can keep going up. Stage is about awareness, not price.
- **Don't conflate sector with theme.** "AI" is not a theme. "光模块" is also too broad now. Themes should be specific enough that you can list 5–10 specific companies that benefit.
- **Don't skip the indicator checklist.** "I think it's Stage 2" without going through indicators is exactly the cognitive shortcut this skill exists to prevent.
