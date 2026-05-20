# Workflow: Three-Layer Translation

## When to use
Triggered explicitly ("帮我做三层翻译", "let me articulate this in three layers") or as a sub-step of `deep-dive-theme.md`. The goal is to force the user to articulate a thesis at three independent levels of abstraction:

1. **Tech layer** — the underlying technical / physical / algorithmic necessity
2. **Engineering layer** — what it takes to mass-produce, who has the Know-how
3. **Economic layer** — TAM, gross margin, competitive structure, key timing

A thesis with all three layers articulated is robust. A thesis with only one layer is fragile — and identifying which layer is missing tells you exactly what research to do next.

## Operating principle
The user is a strong technologist (ML/CV background, Python+frontend+backend) but probably weaker on engineering supply chain and competitive economics. **Push hardest on the layer they're weakest at**. Their tech-layer answers should not get a free pass — but their engineering and economic answers need much more interrogation.

## Steps

### Step 1 — Tech Layer
Ask:
1. What is the **physical or algorithmic necessity** that makes this technology required, not just nice-to-have?
2. What is the **scaling law** at play? (e.g., "GPU power scales with transistor count, but cooling efficiency scales with surface area, so beyond X density, traditional cooling fails")
3. What **alternative paths** exist, and why are they worse?

Acceptance criteria: The user should be able to draw a chart or explain in 3 sentences why this technology is **inevitable** under physical/economic laws, not just "popular."

Common failure: User is enthusiastic about a technology because it's clever, but can't articulate why incumbents/alternatives can't simply close the gap. Push: "Why can't the existing approach just be optimized further?"

### Step 2 — Engineering Layer
Ask:
1. What are the **hardest 2–3 engineering problems** to actually mass-produce this?
2. Who, **specifically by name**, has solved these problems at scale? (Not "Chinese companies" — names.)
3. What is the **defensibility** of those companies? Patents? Process Know-how? Capital intensity? Customer lock-in? Trade secrets?
4. How long would a well-resourced new entrant need to catch up? (1 year → low moat; 5+ years → high moat)

Acceptance criteria: User can name 3–5 specific companies/research groups solving the hardest engineering problems, and articulate a moat that is verifiable, not vibes.

Common failure: User assumes "TSMC has it / Samsung has it / 海力士 has it" without specifying which subsystem. Push: "Within HBM, which specific layer is hardest? Is it the through-silicon via process? The thermo-compression bonding? The known-good die testing? Different companies lead in different subsystems."

### Step 3 — Economic Layer
Ask:
1. **Unit economics**: What does a single unit (chip, module, system) sell for? What's the gross margin? How does that compare to incumbents?
2. **TAM**: What's the addressable market in 3 years? Show a path from current revenue to projected revenue with explicit assumptions (price × volume).
3. **Competitive structure**: Is this a 1-winner market, 2–3 winner oligopoly, or fragmented? What's the historical margin profile of similar structures?
4. **Catalysts and timing**: What specific events in the next 12 months would re-rate the multiple? (Product announcements, design wins, capacity ramps, regulatory.)

Acceptance criteria: User can write a back-of-envelope DCF or comparable valuation that they actually believe, with assumptions they can defend.

Common failure: User skips this because it feels "soft." Push hard: "Without a price target you're tracking, you cannot have conviction on entry, sizing, or exit. Walk me through a multiple framework."

### Step 4 — Self-assessment

After all three layers, ask the user to grade themselves on each:
- A: I can teach this layer to someone else
- B: I understand it but couldn't defend it under pushback
- C: I'm guessing
- D: I haven't researched this yet

If any layer is C or D, **that is the next research task**. Tell them so explicitly. Don't let them mark the theme as "researched" until all layers are at least B.

### Step 5 — Persist

Append the three-layer articulation as a section in the theme dossier (`data/themes/<slug>.md`). Do NOT add it to the SQLite themes table — full text belongs in markdown, not in DB rows.

## Output format

```markdown
## Three-Layer Translation — <date>

### Tech Layer (grade: <A/B/C/D>)
<user's articulation>

### Engineering Layer (grade: <A/B/C/D>)
<user's articulation>

### Economic Layer (grade: <A/B/C/D>)
<user's articulation>

### Weakest layer & next research task
<which layer needs work, and what specifically to research>
```

## Anti-patterns

- Don't accept "AI demand is huge" as economic-layer analysis. Push for unit economics.
- Don't accept "TSMC dominates" as engineering-layer analysis. Push for specific subsystems.
- Don't accept "this is more efficient" as tech-layer analysis. Push for the physical scaling law.
- Don't fill in the layers yourself when the user gets stuck. Stuck = the skill is working. Tell them what to research and end the session.
