# Framework: Cognitive Discipline — Tools from Forecasting Research

The actionable habits of superforecasters and decision researchers, adapted for tech investment thesis-building. These are general-purpose cognitive tools — load this framework whenever a workflow asks for rigorous thinking.

## The Five Disciplines

### 1. Beliefs as Hypotheses, Not Treasures
Tetlock's most concise prescription: **"For superforecasters, beliefs are hypotheses to be tested, not treasures to be guarded."**

In practice, this means:
- When you build conviction in a theme, immediately list the evidence that would falsify it
- When new evidence appears, ask "does this update my view?" — and if not, why not?
- Don't get attached to past predictions; update willingly when reality demands it
- Distinguish "I changed my view because new info arrived" (good) from "I changed my view because the price moved" (bad)

The opposite — **belief preservation** — is the single most common failure mode of investors. Symptoms: dismissing disconfirming evidence, finding excuses for missed predictions, getting defensive when challenged.

### 2. Outside View Before Inside View (Base Rates)

For any specific thesis, before building the inside-view case ("here's why THIS will work"), force the outside-view case ("of past examples that look like this, what % worked?").

For tech investment theses, useful base-rate categories:
- **New bottleneck theses**: Of historical "next bottleneck" predictions, what % actually became binding within 18 months? (My estimate: ~40%, but track your own data.)
- **Technology-replacement theses** (X will replace Y): What's the historical hit rate? Lower than people expect — incumbents adapt more often than they're displaced.
- **Capacity expansion theses**: What's the historical relationship between capex announcements and supplier revenue, with what lag?
- **Stage transition theses** (Stage 1 → 2): Historical base rate ~50-70% within 12 months, depending on type.

If you don't have base rates, **build them via post-mortems** (`workflows/reverse-engineer.md`). After 5-10 cases, you'll have rough priors.

The Tetlock rule: **"Anchor on the outside view, then adjust based on inside view."** Inside view alone produces overconfidence; outside view alone produces under-conviction. The sequence matters.

### 3. Pre-Mortem (Inversion)

A bear case is "the case against." A pre-mortem is structurally different and stronger.

**Pre-mortem prompt**: "Imagine it is 18 months from now, and this thesis has failed catastrophically. The thesis is dead. Tell me the story of how it died, in specific causal sequence."

Why this works:
- Bear cases are debate-style ("here are the counterarguments"); pre-mortems are narrative ("here's the failure path")
- Pre-mortems force concrete causal chains, not abstract risks
- They surface failure modes the bull case implicitly assumed away
- They produce specific signals to watch (which become kill criteria)

**Process**:
1. State the thesis cleanly
2. Set the failure timeline (12-18 months works best)
3. Write 3 distinct failure stories — different causal mechanisms, not variations of one
4. For each, identify the earliest observable signal that the failure path is unfolding
5. Those signals become entries in the kill criteria list

After pre-mortem, your conviction should either drop (if the failure stories are compelling) or strengthen (if they're each easy to dismiss). Either outcome is informative.

### 4. Probability Decomposition

Most theses are conjunctive: they require multiple things to all be true. Yet investors often state confidence at the conjunctive level ("I'm 80% on this") without decomposing.

**Decomposition method**:
1. Break the thesis into 3-5 sub-conditions, each independently observable and time-bound
2. Estimate probability for each
3. Multiply (with consideration of correlations)
4. Compare the product to your gut conviction

Example for "800V DC architecture will benefit specialty power suppliers within 18 months":
- P(at least one major hyperscaler publicly commits to 800V DC by month 12) = 0.70
- P(commitment translates to actual orders by month 18 | commitment) = 0.80
- P(orders flow disproportionately to 2-3 specialty suppliers | orders happen) = 0.60
- Multiplied (assuming independence — questionable): 0.70 × 0.80 × 0.60 = **0.336**

If your gut says "I'm 70% on this," decomposition reveals the gut is wrong (or the sub-probabilities are wrong). Either way, the discipline forces engagement with the chain.

This is why a single confidence number on a complex thesis is almost always overconfident: humans systematically underestimate how much conjunction erodes probability.

### 5. Active Open-Mindedness

Tetlock's phrase for the habit of **looking for evidence that disconfirms your existing view, with the same energy as evidence that confirms it.**

Practical implementations:
- Before declaring conviction, spend 30 minutes specifically looking for disconfirming evidence (Twitter accounts that disagree, sell-side analysts who are bearish, alternative explanations for the data you're citing)
- For each piece of confirming evidence, ask "what would the strongest alternative explanation be?"
- Periodically read the strongest skeptic of your thesis; if you can't name one, find one
- When you receive disconfirming evidence, your default should be to take it seriously, not to immediately rebut

The mental shift: confirming evidence makes you marginally more right; disconfirming evidence is more informative because it carries new information. Pay it more attention, not less.

## Cognitive Biases Specifically Relevant to Tech Investing

These biases are everywhere; flag them in your own thinking when you notice them:

- **Narrative bias**: Compelling stories feel like compelling investments. They aren't always.
- **Recency bias**: Recent winners feel like permanent winners. Rotation happens.
- **Authority bias**: Just because a respected person is bullish doesn't make you right. Their incentives may differ from yours.
- **Sunk-cost bias**: Hours of research on a thesis don't make the thesis correct. Walk away when evidence demands it.
- **Confirmation bias**: You will naturally notice supporting evidence and ignore disconfirming. Counter with active open-mindedness.
- **Hindsight bias**: After a theme works, you'll remember "I knew it." You probably didn't. Use post-mortems against this.
- **Survivorship bias**: We study NVIDIA but not the dozens of also-rans. The strategy that produced NVIDIA might also have produced losers; need to look at the full distribution, not just winners.
- **Overprecision**: "I think there's a 73% chance" implies more granularity than you can support. Round to 0.1 increments at most.
- **Affect heuristic**: When you like a company / management, you under-weight risks. Notice this and counter.

## A Simple Pre-Decision Checklist

Before sizing a position based on a thesis, run through:

- [ ] **Variant perception articulated**: I can state consensus, my view, and the gap.
- [ ] **Base rate consulted**: I know roughly how often theses of this type have worked historically.
- [ ] **Pre-mortem complete**: I've written 3 failure stories with specific kill signals.
- [ ] **Probability decomposed**: I've broken the thesis into ≥3 conjunctive sub-conditions and multiplied.
- [ ] **Disconfirming evidence sought**: I've actively looked for the strongest opposing view.
- [ ] **Reflexivity flagged**: I've identified whether the theme is in a self-reinforcing loop and where in the loop.
- [ ] **Catalyst identified**: I know what specific event(s) would force consensus to update.
- [ ] **Time horizon explicit**: I know how long this thesis needs to play out and whether that fits my capital.

If any unchecked, more work is needed before sizing. **The checklist is the discipline.**

## Connection to Calibration

These cognitive disciplines are inputs to better forecasts; calibration tracking (in `scripts/query.py calibration`) is the output measure. Over 10-20 closed predictions, you'll see whether the disciplines are improving your hit rate. If they aren't, either you're not actually applying them, or your inside view (technical understanding) needs strengthening.
