# <Theme Name CN> / <Theme Name EN>

> **slug**: `<slug>`
> **layer**: <compute|memory|network|power|cooling|software|robotics|sensor|materials|other>
> **status**: <watching|researching|conviction|exited|killed>
> **created**: <YYYY-MM-DD>
> **last updated**: <YYYY-MM-DD>

---

## 1. One-Line Thesis

> If <X> happens within <timeframe>, then <Z technology / supply-chain segment> becomes a structural bottleneck, benefiting <type of company>.

<Write the single sentence here. If you cannot, the thesis is not yet clear.>

## 2. Bottleneck Identified

**Which bottleneck does this address?**
<Reference frameworks/bottleneck-migration.md. Is this 一阶 / 二阶 / 三阶?>

**What is the hard physical or economic constraint?**
<The "why is this inevitable" — not just "why is this likely.">

**Stage 0 origin signal** — earliest knowable indicator:
<Date + source + what was said/seen>

## 3. Five Forces of Validation

### 3a. CEO抱怨提取
| Date | Who | Forum | Quote / Paraphrase |
|------|-----|-------|--------------------|
|      |     |       |                    |

### 3b. Capex 结构变化
<Which line item is shifting? Reference financial filings. Don't just cite total capex.>

### 3c. Roadmap 溯源
<TSMC / NVIDIA / ASML / SK Hynix / etc. — whose roadmap implies this?>

### 3d. Physical / Engineering Evidence
<Papers, ISSCC presentations, OCP submissions, IEEE disclosures.>

### 3e. Supply-Chain Anomaly
<Pricing, lead-times, order behavior. Sources: TrendForce, DigiTimes, IC Insights, Counterpoint, SEMI.>

**Forces validated**: <count out of 5>

## 5. Variant Perception (THE Alpha test)

### What does the market currently believe?
<One paragraph capturing consensus: sell-side tone, multiples vs history, mainstream media framing, retail sentiment.>

### What do I believe — specifically?
<My view, with the dimension of difference made explicit (magnitude / timing / probability / beneficiary identity / mechanism).>

### The gap
<How wide is the gap? Why does it exist? Why am I not the one who's wrong?>

### Catalyst
<Specific event(s) by specific date(s) that will force consensus to update.>

**If consensus = my view, this is Beta, not Alpha. Stop here.**

## 6. Reflexivity Check

| Aspect | Assessment |
|--------|------------|
| Reflexivity strength | low / medium / high |
| Underlying real trend | <the fundamental part> |
| Embedded misconception | <what the market is exaggerating> |
| Loop phase | 1 latent / 2 acceleration / 3 test / 4 twilight / 5 reversal |
| Loop-breaker | <specific event(s) that would expose the misconception> |
| Implication for sizing | <Phase 1-2: can size larger; Phase 4-5: reduce or exit> |

## 7. Three-Layer Translation

### Tech Layer (grade: <A/B/C/D>)
<Physical/algorithmic necessity. Scaling law. Why alternatives fail.>

### Engineering Layer (grade: <A/B/C/D>)
<Hardest 2-3 engineering problems. WHO solves them — by name. Defensibility.>

### Economic Layer (grade: <A/B/C/D>)
<Unit economics. TAM. Competitive structure. Multiple framework. **What expectations are already in the price?**>

### Weakest layer & next research task
<Which letter grade is lowest? That's your next research item.>

## 8. Pre-Mortem (3 distinct failure stories)

> "It is 18 months from now. This thesis has failed catastrophically. Here are three stories of how it died."

### Failure story 1: <Causal trigger>
<Specific causal sequence. Earliest observable signal: ___>

### Failure story 2: <Different causal trigger>
<Specific causal sequence. Earliest observable signal: ___>

### Failure story 3: <Different causal trigger>
<Specific causal sequence. Earliest observable signal: ___>

### Kill criteria (derived from earliest signals above)
1. <Kill criterion 1>
2. <Kill criterion 2>
3. <Kill criterion 3>

## 9. Base Rate / Outside View

### Reference class
<Of past investment theses that look like this — same general shape — what fraction historically played out as expected within the predicted timeframe?>

**Estimated base rate**: <X%>

**Source of base rate**: <post-mortems / general history / informed estimate>

### Why is THIS theme above (or below) the base rate?
<What makes this case different from the historical reference class? Be specific.>

## 10. Stage Assessment

**Current stage**: <0–4>
**Confidence**: <0.0–1.0>
**Reasoning**: <One paragraph; reference indicators from frameworks/5-stage-lifecycle.md>

History (auto-populated from stage_history table; see `query.py stage-history --theme <slug>`).

## 11. Falsifiable Predictions

(Logged via `scripts/log_prediction.py`. Auto-queryable via `query.py predictions --theme <slug>`.)

If thesis is compound, decompose via `scripts/decompose_thesis.py` and log the joint probability as well as 2-3 sub-predictions.

## 12. Beneficiary Map (Optional)

<Specific companies that benefit, organized by sub-segment of the supply chain. NOT a buy list. Just a map of "if the thesis plays out, here's who's exposed to it.">

| Sub-segment | Companies | Why exposed | Quality of moat (H/M/L) |
|-------------|-----------|-------------|-------------------------|
|             |           |             |                         |

## 13. Open Questions

<Questions you have NOT yet answered. These become the next research backlog.>

- [ ] Open question 1
- [ ] Open question 2

## 14. Signal Log

(Auto-aggregated from signals table; see `query.py signals --theme <slug>`.)

---

*This dossier is a living document. Update on every meaningful new signal. Re-grade three layers and re-check variant perception quarterly.*
