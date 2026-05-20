# Framework: Physical Constraint Identification

The strongest investment theses are anchored on **hard physical constraints** — laws of physics, chemistry, or thermodynamics that no amount of capital or engineering can overcome on a short timeframe. Themes anchored on physical constraints are inevitable in the medium term; themes anchored on "trends" or "preferences" can reverse without warning.

## Why this matters for Alpha

Soft constraints (consumer preferences, regulatory regimes, fashion) are unpredictable and reversible. Hard constraints are predictable and one-directional. Theses anchored on hard constraints have:
- Higher conviction floors (the constraint won't disappear)
- More predictable timing (the constraint becomes binding when scaling reaches a known threshold)
- Lower competitive risk (you can't capital-spend your way around physics)

## A working list of hard constraints in AI infrastructure

**These are the constraints I most often see drive Alpha cases. The list is not exhaustive.**

### Compute & memory
- **Moore's Law slowdown**: Sub-3nm transistor scaling now driven by structural innovations (GAA, CFET) more than dimensional shrink. This makes process leadership a harder moat.
- **Memory wall**: DRAM bandwidth scales much slower than compute FLOPs (~2x per node vs ~5x). Inevitable: more aggressive memory architectures (HBM, 3D DRAM, near-memory compute).
- **DRAM cell scaling**: Capacitor miniaturization has well-known refresh / leakage limits. Limits to single-die capacity force 3D stacking.

### Networking & interconnect
- **Copper signal integrity**: Above ~112 Gb/s per lane, copper PCB traces lose to dielectric / skin-effect losses over even short distances. Inevitable: optical interconnect penetration, CPO, etc.
- **NIC bandwidth ceiling**: NICs cannot scale arbitrarily — they share PCIe lanes and physical pin count constrains aggregate bandwidth at the package level.
- **Latency floor**: Speed of light in fiber is ~2/3 of c; real systems add switching, serialization, and queueing delays that don't shrink with capital.

### Power & cooling (thermodynamics — the hardest constraints)
- **Heat flux per area**: Silicon heat fluxes >100 W/cm² exceed what air convection can remove at any reasonable airflow velocity. Inevitable: liquid cooling.
- **Coefficient of performance for cooling**: The energy needed to remove heat is a function of temperature gradient — colder facility air requires disproportionately more energy. Inevitable: heat reuse, warmer-water cooling, heat-recovery economics.
- **Copper resistivity & I²R losses**: For high-current power distribution, doubling current quadruples I²R losses. Inevitable: voltage rises (12V → 48V → 800V DC).
- **Transformer iron-core saturation**: Existing distribution transformers cannot be infinitely loaded; replacing them is a multi-year supply chain.

### Materials & manufacturing
- **EUV photon flux**: ASML can only push wafer throughput so far given source power constraints. Hyper-NA EUV requires entirely new optics paths — 5+ year lead time.
- **Substrate aspect ratios**: ABF substrate stacking is constrained by warpage physics.
- **Yield vs die-size scaling**: Defect density × die area = expected defects per die; very large dies (chiplets aside) are mathematically impossible without yield collapse.

### Energy & infrastructure
- **Grid connection lead-times**: New grid interconnects in the US currently take 4–7 years from queue entry to energization. This is a regulatory + physical constraint compounded.
- **Cooling water availability**: Many candidate data center sites are water-constrained; this drives architectural shifts toward dry / hybrid cooling.

## How to use this framework when evaluating a thesis

For any theme being researched, ask:

1. **What physical/thermodynamic/economic constraint is being approached?**
   - If you can name a quantitative threshold (e.g., "above X W/cm² air cooling fails"), the thesis has hard backing.
   - If you can only describe a "trend," the thesis is soft.

2. **What is the current trajectory toward the constraint?**
   - If the constraint becomes binding in 1–2 years at current scaling rates, the theme is at Stage 0–1.
   - If it's already binding, the theme is at Stage 2+.
   - If it's >5 years away, the theme is too early to be actionable (but still worth tracking).

3. **What is the engineering response to the constraint?**
   - Is there a single dominant solution? (Higher conviction; concentrated supply chain.)
   - Are there multiple competing solutions? (Lower conviction per name; need to handicap winners.)
   - Is the response a known technology being scaled, or a new technology needing invention? (The former is more bankable; the latter has higher upside but execution risk.)

## The "necessity test"

A useful tactical filter: write down the thesis as "if X happens, then Y is inevitable because of Z constraint."

If you cannot fill in Z with a specific physical/economic constraint, the thesis lacks hard backing — and your conviction ceiling should be capped.

Examples:

✓ "If single-rack power crosses 1MW, **then** 800V DC distribution becomes mandatory **because** copper I²R losses scale with current squared and 48V cannot deliver 1MW without prohibitive losses."

✗ "If AI keeps growing, **then** liquid cooling will be huge **because** cooling matters." (No physical constraint named; thesis is soft.)

## Connection to other frameworks

- Theses with hard physical backing ≈ better candidates for Stage 0/1 conviction sizing per `5-stage-lifecycle.md`
- Each entry in `bottleneck-migration.md` should ideally be backed by at least one constraint here. If a candidate bottleneck has no physical backing, treat it as speculative.
