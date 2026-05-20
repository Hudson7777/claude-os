# The Alpha Hunter Framework

> Finding technology investment opportunities before they become consensus.

Most investment research suffers from a timing problem: by the time a thesis appears in mainstream financial media, the Alpha has already been extracted. The investors who profited read the same data earlier — from different sources, through different lenses.

This framework is a systematic attempt to solve that problem.

---

## The 5-Stage Technology Lifecycle

Every technology investment theme passes through a predictable sequence of awareness expansion. Identifying the current stage determines whether Alpha is still available.

### Stage 0 — Technical Necessity (awareness <5%)

Visible only to insiders: domain engineers, academic researchers, specialty analysts covering the precise vertical.

**Signals:** Academic papers and conference proceedings. Zero financial media coverage. No sell-side initiation reports. CEO complaints about supply constraints emerging — not yet picked up by analysts.

**Investability:** Highest theoretical Alpha, but also highest technical-validation risk. Size positions to reflect uncertainty.

### Stage 1 — Industry Consensus Forming (awareness 5–15%)

Specialist research outlets begin publishing deep analyses. Supply-chain data starts showing anomalies.

**Signals:** SemiAnalysis / The Information / DigiTimes have 1–2 deep dives. TrendForce shows price anomalies. 1–2 sell-side analysts have quietly upgraded category leaders. Mainstream financial media NOT yet focused on it.

**Investability:** Best risk/reward zone. Technical uncertainty resolved, market hasn't priced it. This is where conviction sizing should happen.

### Stage 2 — Smart Money Building (awareness 15–40%)

Specialist hedge funds and sector PMs visibly building positions. Multiple sell-side initiations.

**Signals:** 13F filings show specialist funds adding. Multiple sell-side reports with measured tone. Stocks show structural uptrends with high volatility.

**Investability:** Still good if you have differentiated view on magnitude or speed of adoption. Sizing should be more conservative than Stage 1.

### Stage 3 — Mainstream Awareness (awareness 40–70%)

Topic appears in general business media. Non-specialist institutional funds entering.

**Signals:** Bloomberg / WSJ / FT coverage. CNBC segments. Generalist fund managers mentioning it. Retail interest rising.

**Investability:** Alpha largely extracted. Can still trade momentum, but risk/reward has deteriorated. Thesis must now include "how long does this last" rather than "will this happen."

### Stage 4 — Crowded Trade / Peak Hype (awareness >70%)

Topic is consensus. Everyone knows about it.

**Signals:** Main topic of every earnings call in the sector. Retail FOMO visible. New ETFs launched to capture the theme. Magazine covers.

**Investability:** Fade, not buy. Look for the next Stage 0–1 within the same supply chain.

---

## The Three-Layer Translation

A common failure mode in tech investing: understanding the technology but not the investment implications. The three-layer translation forces rigorous connection between the technical and the financial.

**Layer 1: Technical** — What is actually happening?  
Describe the engineering constraint, breakthrough, or adoption driver without financial language.  
*Example: "CoWoS advanced packaging has a 12-18 month lead time at TSMC. The bottleneck is the redistribution layer deposition step."*

**Layer 2: Engineering / Supply Chain** — Who feels this first?  
Which companies sit at the constraint? Who benefits from the bottleneck? Who suffers?  
*Example: "TSMC CoWoS capacity is the binding constraint on H100/H200 shipment volume. NVIDIA is capacity-constrained, not demand-constrained. TSMC has pricing power."*

**Layer 3: Economic / Financial** — What does the market not yet know?  
Where does the current consensus mis-price the supply chain implication?  
*Example: "Consensus models TSMC revenue based on node mix. CoWoS advanced packaging is priced at a significant premium per wafer equivalent and is not yet breaking out in consensus models. When it does, TSMC gross margin estimates will be revised upward."*

A thesis that cannot complete all three layers is not ready to act on.

---

## Cognitive Discipline

The frameworks above are worthless without the mental discipline to apply them honestly. These are the failure modes that destroy returns:

**Confirmation bias in signal collection:** Only reading sources that agree with your existing thesis. Counter: actively seek out the best bear case before sizing up.

**Stage mis-identification:** Calling Stage 2 a Stage 1 because you want higher position size. Counter: use the awareness percentage as an objective anchor, not a feeling.

**Narrative substitution:** The thesis evolves from "supply chain inflection" to "AI is eating the world" — a true but useless claim that can justify any price. Counter: falsifiability. Write down exactly what evidence would prove you wrong.

**Recency bias in stage assessment:** A theme that was Stage 1 six months ago might be Stage 3 today. Counter: reassess stage at every periodic review, don't anchor to initial classification.

---

## Using Alpha Hunter with Claude Code

The `alpha-hunter` skill operationalizes this framework. Configure your information sources and investment profile in `config/`, then use natural language to:

- Capture a signal: *"新信号：Broadcom CEO 提到 XPU 定制化需求超预期"*
- Assess stage: *"液冷现在到 Stage 几了？"*
- Deep dive a theme: *"deep dive on 800V DC power architecture"*
- Log a prediction: *"记录预测：TSMC CoWoS 产能 2025Q2 开始去瓶颈"*
- Run periodic review: *"monthly review of tracked themes"*

---

## Further Reading

The frameworks referenced in this essay are fully documented in the `frameworks/` directory:

- [5-stage-lifecycle.md](./frameworks/5-stage-lifecycle.md) — full stage definitions with awareness %, signal checklists, and position-sizing guidance
- [cognitive-discipline.md](./frameworks/cognitive-discipline.md) — the complete anti-bias toolkit: confirmation bias, narrative substitution, reflexivity
- [signal-sources.md](./frameworks/signal-sources.md) — tiered signal source catalog (Tier 1–4) with reliability assessments
- [variant-perception.md](./frameworks/variant-perception.md) — how to develop differentiated views that diverge from consensus
- [physical-constraints.md](./frameworks/physical-constraints.md) — why physical/engineering limits are the highest-conviction signal source
- [bottleneck-migration.md](./frameworks/bottleneck-migration.md) — how to track Alpha as a bottleneck resolves and migrates to the next constraint
- [reflexivity.md](./frameworks/reflexivity.md) — when market attention itself changes the investment thesis
