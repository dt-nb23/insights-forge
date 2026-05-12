# Stakeholder Profiles

One profile per leader the agent regularly produces outputs for. The agent reads the matching profile before drafting any Phase 3 deliverable so the tone, depth, and emphasis match what that leader actually wants. Updated only on explicit user approval.

## How to use this file

When a Phase 3 one-pager or deck is intended for a specific named leader, read the relevant profile here first. If no profile exists for the named reader, fall back to the closest archetype (VP of Engineering, Director of Reliability, Head of Data Analytics) and ask the user whether to create a new profile.

## Profile template

Each profile carries the same fields. Keep entries short and concrete — "they ignore vendor logos in the appendix" is more useful than "they value clarity".

---

## VP of Engineering

- **Name / role**: [Name], VP of Engineering
- **What they care about**: [Time-to-resolution, engineering team capacity, what blocks the roadmap, ownership clarity. Wants to know who is doing what by when.]
- **What they ignore**: [Detailed query syntax, vendor-specific UI screenshots, anything that reads like a status update without a decision attached.]
- **Preferred level of detail**: [One page maximum. Three bullets of findings, three bullets of actions, one paragraph of business impact. Appendix tolerated only if explicitly requested.]
- **Typical questions they ask**: [
  - "What does this cost in engineering weeks?"
  - "Whose roadmap does this disrupt?"
  - "What's the decision I need to make right now?"
  - "What happens if we do nothing?"
]
- **Decisions they own**: [Cross-team prioritization; engineering headcount allocation; go/no-go on disruptive remediations like rollbacks, hot-fixes, or roadmap reshuffles.]
- **Tone notes**: [Direct. No hedging. Tradeoffs surfaced in the same paragraph as recommendations. Vendor-neutral unless the vendor specifically matters.]

---

## Director of Reliability

- **Name / role**: [Name], Director of Reliability / Director of SRE
- **What they care about**: [SLO health, error budget burn, incident patterns, instrumentation maturity, blameless retrospective culture. Wants the data to be defensible.]
- **What they ignore**: [Recommendations that don't tie back to a specific SLI, SLO, or error budget. Hype language.]
- **Preferred level of detail**: [Higher tolerance for technical depth than the VP. Will follow trace IDs and dashboard links if they support the argument. One-pager + technical appendix is welcome.]
- **Typical questions they ask**: [
  - "Which SLO did this affect, and how much error budget did it burn?"
  - "Is this a recurring pattern, or a one-off?"
  - "What instrumentation gap let this hide for as long as it did?"
  - "What's the long-term fix vs the immediate fix?"
]
- **Decisions they own**: [SLO definition and revision; on-call practice changes; observability platform investment; reliability roadmap.]
- **Tone notes**: [Technical precision matters. SLI/SLO terminology must be used correctly. Treat error-budget framing as load-bearing language.]

---

## Head of Data Analytics

- **Name / role**: [Name], Head of Data Analytics / VP of Analytics
- **What they care about**: [Data quality, instrumentation coverage, the integrity of the metrics being cited, whether the conclusion is statistically defensible, whether the funnel attribution holds up.]
- **What they ignore**: [Backend-only framing; tech findings stated without their business KPI translation; conclusions that don't acknowledge confidence intervals.]
- **Preferred level of detail**: [Wants the numbers, the time windows, the segments. Will push back on anything stated as a single point estimate without context. Appendix with methodology is welcome.]
- **Typical questions they ask**: [
  - "What's the confidence interval on that number?"
  - "How did we segment the population?"
  - "Are we comparing like to like in the before/after window?"
  - "Which KPI does this actually move, and by how much?"
]
- **Decisions they own**: [Metrics definition; experiment readouts; analytics roadmap; data team prioritization.]
- **Tone notes**: [Cite the source telemetry; name the time window; acknowledge confounders. Translate technical signals into KPI deltas with explicit math.]

---

## [Add new profiles below as needed. Maintain the same field structure.]
