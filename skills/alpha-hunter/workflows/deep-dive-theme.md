# Workflow: Deep-Dive Theme

## When to use
The user wants to seriously research a candidate Alpha theme — not just log a signal. Triggers:
- "深度研究 / deep dive on <theme>"
- "我想认真研究一下 <theme>"
- "帮我把 <theme> 这个主题做完整的 dossier"
- "分析下 <theme> 现在值不值得跟踪"

This workflow produces a **theme dossier**: a markdown file at `data/themes/<slug>.md` and a corresponding row in the `themes` table.

## Operating principle
**Force the user to articulate, don't articulate for them.** Claude's job here is to be a relentless interviewer. If the user says "you fill it in," refuse — the act of filling in is the training.

The dossier is built incrementally through 9 sections. After each section, summarize what the user said in their own words (not yours), confirm, then move on. **Do not skip sections to be agreeable.** The sections that feel hardest (variant perception, pre-mortem, base rate) are the most important.

## Sections (in order)

### 1. One-line thesis
Force a single sentence: "If X happens within Y timeframe, then Z technology will become a structural bottleneck, benefiting [type of company]."

If the user can't write this in one sentence, the thesis isn't clear enough yet. Stay on this until they can.

**Bad**: "AI需要更多电力" (vague)
**Good**: "未来18个月内单rack功耗突破1MW，48V直流配电的电流损耗成为物理瓶颈，受益方为800V DC固态变压器、SiC功率器件供应商"

### 2. Bottleneck identification
What specific bottleneck does this theme address? Cross-reference with `frameworks/bottleneck-migration.md`. Probe:
- Is this bottleneck downstream of an already-known bottleneck (i.e., 二阶受益者)?
- Or is it a net-new bottleneck (i.e., Stage 0)?
- What is the **physical or economic constraint** that makes this bottleneck inevitable, not just probable? Reference `frameworks/physical-constraints.md`.

If the user can't name a hard constraint, this is a "soft" thesis — flag it.

### 3. Five forces of validation
For each, ask the user to provide at least one concrete piece of evidence:

a. **CEO抱怨提取**: Who, in the last 4 quarters, has publicly complained about this bottleneck? Cite specific calls/interviews.
b. **Capex拆解**: What capex structural shift is consistent with this thesis? (Not just total capex up — which line item is shifting?)
c. **Roadmap溯源**: Whose published roadmap (TSMC, NVIDIA, ASML, etc.) implies this trajectory?
d. **Physical / Engineering Evidence**: Peer-reviewed paper, ISSCC presentation, OCP submission, IEEE disclosure?
e. **Supply chain anomaly**: Abnormal pricing, lead-time, or order behavior that the bottleneck would explain?

f. (Optional but valuable, for users with industry access) **Scuttlebutt**: Direct conversations with customers, suppliers, ex-employees, or competitors. See `frameworks/signal-sources.md`.

If <3 validated, **Stage 0** (technical necessity, high uncertainty).
If 3-4, **Stage 1** (industry consensus forming).
If all 5+ with named primary sources, **Stage 2+** (Alpha is partially priced in).

### 4. Three-layer translation
Run `workflows/three-layer-translation.md` as a sub-workflow. The user must articulate Tech / Engineering / Economic layers, with self-graded confidence.

### 5. Variant Perception (CRITICAL — most often skipped)

**Load `frameworks/variant-perception.md` before this section.** This is the section that distinguishes Alpha-targeting research from generic theme research.

Force three explicit sentences:

a. **"The market currently believes ___."**
   - What does sell-side currently say?
   - What multiples are category leaders trading at vs historical range?
   - What is mainstream financial media saying about this theme?
   - What's the retail / 雪球 / Twitter sentiment?

b. **"I believe ___, which differs because ___."**
   - On which specific dimension is your view different? (Magnitude / timing / probability / beneficiary identity / mechanism)
   - Quantify the gap if possible.

c. **"The market will be forced to update its view when ___ happens by ___."**
   - Specific catalyst with date.
   - Without an identifiable catalyst, the gap may not close in your investable timeframe — flag this risk.

**If the user's view is identical to consensus, there is no Alpha. Stop the dossier and tell them so directly.** Mark the theme as "watching" rather than "researching" until variant perception is articulable.

### 6. Reflexivity Check

**Load `frameworks/reflexivity.md` before this section.** AI infrastructure themes are highly reflexive; ignoring this leads to late-cycle entries.

For this theme, identify:
- **Reflexivity strength**: low / medium / high
- **Underlying real trend**: what's the fundamental part?
- **Embedded misconception**: what's the part the market is exaggerating?
- **Loop phase**: 1 (latent) / 2 (acceleration) / 3 (test) / 4 (twilight) / 5 (reversal)
- **Loop-breaker**: specific event(s) that would expose the misconception

**If theme is in Phase 4-5, conviction sizing should be reduced regardless of fundamental quality.** If in Phase 1-2, the same fundamental thesis can be sized larger.

### 7. Pre-mortem (Inversion)

**Load `frameworks/cognitive-discipline.md` (Section 3) for context.**

This is structurally different from a bear case. Force this prompt:

> "Imagine it is 18 months from now, and this thesis has failed catastrophically. Tell me three distinct stories of how it died, in specific causal sequence."

Three failure stories — not three variations of one story. Each story should:
- Have a specific causal trigger (an event, not a "trend")
- Identify the earliest observable signal that the path is unfolding
- Be plausible enough that a smart skeptic would consider it worth attention

The earliest signals from each story become **kill criteria** in the dossier.

### 8. Base Rate / Outside View

**Load `frameworks/cognitive-discipline.md` (Section 2) for context.**

Before the user becomes confident in their inside-view case, force the outside-view question:

> "Of past investment theses that look like this — same general shape, similar setup — what fraction historically played out as expected within the predicted timeframe?"

If the user has done post-mortems via `workflows/reverse-engineer.md`, use those as base rates. If not, suggest doing 1-2 reverse-engineerings before locking in conviction.

Anchor on the base rate, then adjust based on inside-view specifics. If the user's confidence is far above the base rate, ask: "What about THIS theme makes it different from the historical reference class?"

### 9. Falsifiable predictions (with decomposition)

**Load `frameworks/cognitive-discipline.md` (Section 4) for context.**

The dossier is NOT considered complete until at least one falsifiable prediction is logged.

For complex theses, encourage **probability decomposition**:
- Break thesis into 3-5 sub-conditions, each independently observable and time-bound
- Assign probability to each
- Multiply for the joint probability
- Compare to gut conviction

Run `workflows/log-prediction.md` for each sub-prediction or for the consolidated joint prediction.

## After all sections

1. Save the markdown to `data/themes/<slug>.md` using `templates/theme-dossier.md`.
2. Insert/update the theme in the DB via `scripts/add_theme.py`.
3. Run a stage assessment via `workflows/stage-assessment.md` and persist the result.
4. Confirm with the user, then stop.

## Pre-Decision Checklist (before user marks theme as "conviction")

Before any theme moves from `researching` to `conviction` status, all of the following must be true:

- [ ] Variant perception articulated (consensus / my view / gap / catalyst)
- [ ] Base rate consulted (or post-mortem done)
- [ ] Pre-mortem complete (3 failure stories + signals)
- [ ] Probability decomposed (joint probability calculated)
- [ ] Reflexivity flagged (loop phase identified)
- [ ] Catalyst dated
- [ ] Time horizon explicit
- [ ] At least one falsifiable prediction logged

If any unchecked, status stays at `researching`. **No exceptions, including for themes the user is excited about — especially for those.**

## What NOT to do

- Do NOT do extensive web search to "fill in" the dossier yourself. The user does the synthesis.
- Do NOT recommend specific tickers. The dossier is about the thesis, not stock picks.
- Do NOT skip variant perception, pre-mortem, or base rate sections to be agreeable.
- Do NOT use bullet points to fake completeness when the user gave you a one-line answer.
- Do NOT accept "I have a feeling" — push for articulation.
