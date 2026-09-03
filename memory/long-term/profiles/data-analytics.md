## Data / Analytics Lead

- **Typical titles**: Head of Data Analytics, VP of Analytics, Director of Business Intelligence, Chief Data Officer, Analytics Engineering Manager
- **What they care about**: Data quality, instrumentation coverage, the integrity of the metrics being cited, whether the conclusion is statistically defensible, and whether funnel attribution holds up under scrutiny.
- **What they ignore**: Backend-only framing without a business KPI translation. Conclusions stated without confidence intervals or methodology. Single-point estimates presented as ground truth.
- **Preferred level of detail**: High. Wants the numbers, the time windows, the segments, and the methodology. Will push back on anything stated without context. Appendix with methodology is welcome and expected.
- **Typical questions they ask**:
  - "What's the confidence interval on that number?"
  - "How did we segment the population?"
  - "Are we comparing like to like in the before/after window?"
  - "Which KPI does this actually move, and by how much?"
- **Decisions they own**: Metrics definition; experiment readouts; analytics roadmap; data team prioritization; instrumentation requirements for business events.
- **Tone notes**: Cite the source telemetry; name the time window; acknowledge confounders. Translate technical signals into KPI deltas with explicit math. Never present a single number without its denominator and time window.

---

## Head of Data Analytics → overlay on Data / Analytics Lead

- **Name / role**: [Name], Head of Data Analytics / VP of Analytics
- **Overrides what they ignore**: Backend-only framing; tech findings stated without their business KPI translation; conclusions that don't acknowledge confidence intervals.
- **Overrides preferred level of detail**: Wants the numbers, the time windows, the segments. Will push back on anything stated as a single point estimate without context. Appendix with methodology is welcome.
- **Overrides typical questions**:
  - "What's the confidence interval on that number?"
  - "How did we segment the population?"
  - "Are we comparing like to like in the before/after window?"
  - "Which KPI does this actually move, and by how much?"
- **Overrides decisions they own**: Metrics definition; experiment readouts; analytics roadmap; data team prioritization.
- **Overrides tone notes**: Otherwise use Data / Analytics Lead defaults.
