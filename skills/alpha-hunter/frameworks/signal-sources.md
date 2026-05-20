# Framework: Signal Sources by Stage

A theme is only as good as the information sources you have access to. This framework maps source types to the stages of theme detection they're best suited for.

## Source Hierarchy by Lead-Time

### Tier 1 — Stage 0 sources (lead-time: 6–24 months)
**Where the technical necessity is first visible.**

- **Academic**: arXiv (cs.AR for hardware, cs.LG for ML), ACL, NeurIPS, ICML, conference proceedings
- **Industry-academic conferences**: Hot Chips, ISSCC, IEDM, SIGGRAPH, MICRO, ASPLOS
- **Vendor technical conferences**: NVIDIA GTC, Intel Innovation, ASML/AMAT/LAM tech days
- **Vendor roadmaps**: TSMC roadmap (March symposium + Q&A), NVIDIA architecture announcements, Samsung Memory Tech Day, ASML Investor Day
- **OCP (Open Compute Project) submissions**: Especially valuable — hyperscalers reveal future infrastructure requirements 12–18 months early
- **Standards bodies**: JEDEC (memory), PCI-SIG, OIF (optical), Ultra Ethernet Consortium

Use these to spot **technical necessities** before any financial analyst has noticed.

### Tier 2 — Stage 0/1 sources (lead-time: 3–12 months)
**Specialty research that connects technology to supply chain.**

- **SemiAnalysis** (Dylan Patel): Unmatched for HPC / semiconductor / AI infrastructure depth
- **The Information**: Hyperscaler decisions, supply-chain leaks, executive movements
- **Stratechery** (Ben Thompson): Strategic and structural analysis (longer-term, less near-term Alpha)
- **Asianometry** (YouTube): Free, very high quality on East Asian supply chain
- **TrendForce / DRAMeXchange**: Memory & display contract pricing — critical for spotting cycle inflections
- **DigiTimes**: Taiwanese supply-chain reporting; subscription required
- **Counterpoint Research / Omdia / IDC / Canalys**: Quantitative shipment / pricing data
- **SEMI**: Equipment and materials data, capacity forecasts
- **SIA (Semiconductor Industry Association)**: Monthly billings, government policy

Use these to **validate** Tier 1 signals with supply-chain evidence.

### Tier 3 — Stage 1/2 sources (lead-time: 1–6 months)
**Earnings call transcripts and primary management commentary.**

- **Earnings call transcripts** (Seeking Alpha, [earningscall.biz](https://earningscall.biz), motley-fool.com): Q&A is where the real signal is, not the prepared remarks. Track 10–15 key vendors quarterly.
- **Investor day presentations**: TSMC, NVIDIA, AMD, Intel, ASML, AMAT, LAM, Samsung, SK Hynix, Micron — at minimum
- **10-K / 20-F / Annual Reports**: Risk factors section often reveals concerns 6+ months before they become news
- **Wind 调研纪要**: Mainland-China market visit notes from analysts
- **Bernstein, Morgan Stanley, Goldman, JPMorgan electronics teams**: Best-of-class sell-side research with multi-quarter lead time

Use these to **confirm** that thesis catalysts are materializing as expected.

### Tier 4 — Stage 2 sources (lead-time: 0–3 months)
**Specialist Twitter / X accounts and niche newsletters.**

Curated list (illustrative, verify currency before relying):
- **Semiconductors**: @dylan522p, @SemiVision, @chiakokhua, @SKundojjala
- **Korean supply chain**: @Jukanlosreve
- **AI infrastructure**: @_arohan_, @soumithchintala (research side)
- **Networking / optical**: @FibeReality, @CloudOptics
- **Power / energy**: @TylerNorris, @gridstrategies

Twitter has high signal-to-noise variability. Curate aggressively. Mute accounts that pivot from analysis to advocacy.

### Tier 5 — Stage 3 sources (lead-time: 0–1 month)
**Mainstream financial media, retail discussion forums.**

By the time these are talking about a theme, structural Alpha is gone. Useful for confirming consensus has formed (i.e., a theme is at Stage 3) but not for finding it.

- Bloomberg, Reuters, WSJ, FT
- 华尔街见闻, 36Kr
- CNBC

### Tier 6 — Stage 4 sources (lead-time: NEGATIVE)
**Retail social media.**

By the time a theme is here, it's typically a sell signal, not a buy signal.

- 雪球热帖
- WallStreetBets
- TikTok / 小红书 finance influencers
- 出租车司机

### Tier 0 — Scuttlebutt (Phil Fisher tradition; lead-time variable)
**Direct human conversations with people who interact with the company / industry.**

Phil Fisher's original method, still underrated. For tech themes, especially valuable for users with industry access. Categories:

- **Customers**: What are they actually buying / planning to buy in the next 12 months? What problems are they prioritizing? What do they wish their suppliers did better?
- **Suppliers** (one level upstream of the company you're researching): What's their order book look like? Whose orders are growing fastest? Whose are slowing?
- **Competitors**: What do they think of the leader? Where do they see vulnerabilities? Fisher's favorite question to executives: **"What are you doing that your competitors aren't doing yet?"** (Pose this through any access channel you have.)
- **Ex-employees**: Often the most candid view. LinkedIn alumni networks are gold for tech companies. Ex-employees from 1-2 years ago strike the best balance of recent knowledge and willingness to speak.
- **Research professionals & engineers**: Domain experts at universities, national labs, standards bodies, OEMs. They often see technology directionality before financial markets do.
- **Sales & support people**: Often have the best ground-truth picture of demand patterns at any moment.

**For users with industry access (engineers in big tech, supply chain, hardware OEMs)**: Scuttlebutt is your structural advantage over generalist financial analysts. Use it. Even casual conversations at conferences, lunches with colleagues, or LinkedIn outreach to ex-vendors can reveal Stage 0/1 signals that no public source contains.

**Practical tactics**:
- Maintain a private list of 10-30 industry contacts you trust, organized by sub-domain
- Schedule "industry coffees" 2-4x per quarter — purpose is information, not networking per se
- Post-conversation, immediately log the signal via `workflows/capture-signal.md` with `--source-type other` and tag the source generically (don't include identifying info if confidential)
- Cross-validate: if 3 independent contacts say the same thing, that's strong signal; if 1 says it, hypothesis only

**Caveats**:
- Material non-public information — never use it. Scuttlebutt is for color and qualitative judgment, not earnings preview.
- Subjects of conversations have biases (e.g., a salesperson is bullish on their own product). Always ask "what's their incentive to tell me this?"
- Outdated info: people who left a company 3+ years ago often have stale views, especially in fast-moving tech.

## Information Diet Composition

A balanced research diet looks roughly like:
- **5-15%** Tier 0 (scuttlebutt) — irreplaceable for users with industry access; treat as Alpha multiplier when available
- **25-30%** Tier 1 (academic / conference / roadmap) — Stage 0 generators
- **20-25%** Tier 2 (specialty research) — Stage 0/1 validators
- **20-25%** Tier 3 (earnings + sell-side) — Stage 1/2 confirmers
- **10-15%** Tier 4 (Twitter specialists) — Stage 2 sentiment
- **5%** Tier 5/6 (mainstream/retail) — only as anti-signals

If your information diet is dominated by Tier 5/6 sources, you are systematically late. The discipline is to **shift consumption upstream**.

## Anti-patterns

- **Source consumption without source filtering**: subscribing to 50 newsletters and skimming all is worse than reading 5 deeply.
- **Conflating volume with depth**: 100 tweets ≠ 1 deep technical paper.
- **Recency bias on sources**: a SemiAnalysis post from 6 months ago about a Stage 0 theme may be more valuable today than yesterday's hot take.
- **Avoiding paid sources to save money**: Tier 2 paid research (SemiAnalysis Pro, The Information, specialty consultancies) often pays for itself many times over if you actually use them.
