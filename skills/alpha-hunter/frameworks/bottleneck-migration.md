# Framework: Bottleneck Migration

The single most powerful generator of AI Alpha themes is the **bottleneck migration law**: in any complex distributed system, removing one bottleneck always reveals the next. The progression is roughly predictable, and identifying which bottleneck is *about to* become binding is the central skill of Alpha hunting in AI infrastructure.

## The Law

Performance of an AI training/inference system is gated by the slowest of N interdependent components. Ranking, roughly: compute → memory bandwidth → memory capacity → network bandwidth → network latency → power delivery → cooling → space → grid capacity → upstream raw materials.

When the system removes the current bottleneck (more compute, more memory, faster network), the next-most-constrained component becomes the binding one. The supply chain of *that next* component then experiences an order-of-magnitude demand shock.

## Historical Migration Trajectory

| Period | Binding bottleneck | Resolution | Beneficiary supply chain |
|--------|---------------------|------------|--------------------------|
| 2017–2020 | Algorithm + data | Transformer + internet-scale data | (Pre-investment phase) |
| 2020–2022 | Compute (FLOPs) | A100 / H100 ramp | NVIDIA, TSMC |
| 2022–2024 | HBM capacity & bandwidth | HBM3 → HBM3E ramp | SK Hynix, Samsung, Micron, advanced packaging |
| 2023–2024 | Advanced packaging capacity (CoWoS) | TSMC capacity expansion | Substrate makers, AMAT, packaging equipment |
| 2024–2025 | Optical interconnect | Higher-speed pluggables, CPO | 中际旭创, Coherent, Lumentum, silicon photonics |
| 2024–2025 | High-speed PCB / CCL | M8/M9 materials | TTM, 建滔, Shengyi, ITEQ |
| 2024–2025 | Power capacity | Hyperscaler power deals | Vistra, Constellation, AEP, NextEra |
| 2025–2026 | Cooling — air → liquid | Liquid cooling scale-up | Vertiv, Boyd, Jetcool, CDU specialists |
| 2025–2026 | Grid capacity, transformers | Multi-year backlog forming | GE Vernova, Eaton, Siemens Energy, Hitachi Energy |

## Where Bottlenecks Are Forming Next (as of 2026Q2)

Listed in rough order of emergent visibility. **These are framework-driven candidates, not buy lists.** Use them as starting points for deep-dive research; do not treat as recommendations.

1. **Power delivery — 800V DC architecture**: As single-rack power crosses 1MW, 48V DC distribution loses on copper losses. 800V DC (and even higher) is becoming necessary. Beneficiaries: SiC/GaN power electronics, solid-state transformers, high-voltage power shelves.

2. **Liquid cooling subsystem productization**: Liquid cooling is no longer experimental but the supply chain remains fragmented. Whoever standardizes CDU+manifold+plate at hyperscale wins.

3. **Inference-specific silicon**: Training is locked up by NVIDIA, but inference workload characteristics differ (more memory bandwidth-bound, more latency-sensitive, more power-constrained per query). Custom silicon and near-memory compute architectures may carve out share.

4. **HBM4 and 3D DRAM transition**: HBM3E is Stage 3-4. The next architectural transition (HBM4, hybrid bonding, 3D DRAM) is Stage 0-1. Whoever solves the thermal/yield issues first gets disproportionate share.

5. **AI-native storage**: KV cache, vector databases, training data loaders all stress storage in ways traditional SSDs were not optimized for. New architectures (computational storage, near-storage compute, specialized NAND) are beginning to emerge.

6. **Robotics / physical AI supply chain**: If embodied AI scales in 2026-2027, the bill of materials (precision actuators, force sensors, vision SoCs, simulation platforms) becomes a multi-decade supply chain with low current penetration in mainstream investment narratives.

7. **Energy supply at the data center level**: Beyond grid capacity, distributed generation (gas turbines on-site, SMR-ready sites, fuel cells) starts becoming a real supply chain rather than a press release theme.

8. **Networking beyond NVLink/InfiniBand**: As cluster sizes cross 100k GPUs, the topology and protocol limits become real. UALink, Ultra Ethernet, and the optical replacement of copper inside the rack are all upstream Alpha sources.

## How to Use This Framework

1. **For each tracked theme**: Identify which bottleneck on the migration ladder it sits on.
2. **For each bottleneck**: Identify the order in the supply chain (一阶 → 二阶 → 三阶受益者). Three orders down the supply chain typically have 6–12 months of awareness lag relative to the first order.
3. **Ask quarterly**: Has the binding bottleneck shifted? If yes, what does that imply for theme priority?

## Cognitive trap to avoid

Confusing **the theme that is currently working** with **the theme to be positioned in**. Stocks in the current bottleneck (e.g., 光模块 in 2025) are visible, validated, and rallying — the easy thesis to feel right about. Stocks in the *next* bottleneck (still Stage 0/1) feel uncertain and unrewarding for 6–12 months. The discipline is to allocate research time disproportionately to the next bottleneck, not the current one.

## Connection to other frameworks

- Use with `5-stage-lifecycle.md`: A bottleneck that is binding *now* is at Stage 3-4 in awareness; a bottleneck about to become binding is at Stage 0-1. The two frameworks together let you triangulate.
- Use with `physical-constraints.md`: The most reliable next-bottleneck candidates are those backed by hard physical limits (cooling thermodynamics, copper resistivity, transformer iron core saturation).
