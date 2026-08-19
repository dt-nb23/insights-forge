## SRE / Reliability Engineer

- **Typical titles**: Site Reliability Engineer, Reliability Engineer, Director of SRE, Director of Reliability, Platform Reliability Lead
- **What they care about**: SLO health, error budget burn, incident patterns, instrumentation maturity, and blameless retrospective culture. Wants the data to be defensible and the exit criteria to be pre-agreed.
- **What they ignore**: Recommendations that don't tie back to a specific SLI, SLO, or error budget. Hype language. Findings stated without supporting telemetry.
- **Preferred level of detail**: High tolerance for technical depth. Will follow trace IDs, dashboard links, and DQL references if they support the argument. One-pager plus technical appendix is welcome.
- **Typical questions they ask**:
  - "Which SLO did this affect and how much error budget did it burn?"
  - "Is this a recurring pattern or a one-off?"
  - "What instrumentation gap let this hide for as long as it did?"
  - "What's the long-term fix versus the immediate mitigation?"
- **Decisions they own**: SLO definition and revision; on-call practice changes; observability platform investment; reliability roadmap; instrumentation standards.
- **Tone notes**: Technical precision matters. SLI/SLO terminology must be used correctly. Treat error-budget framing as load-bearing language. Cite the telemetry source for every finding.

---

## Director of Reliability → overlay on SRE / Reliability Engineer

- **Name / role**: [Name], Director of Reliability / Director of SRE
- **Overrides preferred level of detail**: Higher tolerance for technical depth than a VP-level reader. Will follow trace IDs and dashboard links if they support the argument. One-pager plus technical appendix is welcome.
- **Overrides typical questions**:
  - "Which SLO did this affect, and how much error budget did it burn?"
  - "Is this a recurring pattern, or a one-off?"
  - "What instrumentation gap let this hide for as long as it did?"
  - "What's the long-term fix vs the immediate fix?"
- **Overrides decisions they own**: SLO definition and revision; on-call practice changes; observability platform investment; reliability roadmap.
- **Overrides tone notes**: Otherwise use SRE / Reliability Engineer defaults.
