# Terminology

Glossary of recurring terms used across investigations. Two-line definitions each — enough to anchor the meaning, short enough to scan. The team will extend this over time. Updated only on explicit user approval.

## Analytical frameworks

- **MECE** — Mutually Exclusive, Collectively Exhaustive. A decomposition discipline where every cause fits in exactly one branch and no real cause is missing from the set. The backbone of the issue tree in Phase 1.
- **ICE** — Impact × Confidence / Effort. A 1–10-per-dimension scoring formula for ranking hypotheses or actions. Higher ICE = higher priority; calibration matters more than absolute numbers.
- **Issue tree** — A hierarchical, MECE decomposition of a problem into branches that represent possible causes. The artifact produced by `skills/mece-decomposition`.
- **Hypothesis** — A specific, testable claim about what is happening inside one branch of the issue tree. Must specify expected signals and exit criteria.
- **Signal** — A measurable change in a metric or dataset that confirms or refutes a hypothesis. Must be specific enough that the team can recognize it when they see it.
- **Exit criteria** — Pre-agreed conditions under which a hypothesis is declared confirmed, ruled out, or inconclusive. Set before the investigation starts so the result is not adjudicated after the fact.

## Observability

- **SLI (Service Level Indicator)** — A quantitative measure of service behavior, such as p95 latency or error rate. The raw number; the SLO is its target.
- **SLO (Service Level Objective)** — A target value or range for an SLI over a stated time window. Internal commitment, distinct from a contractual SLA.
- **RUM (Real User Monitoring)** — Telemetry collected from actual user sessions in the browser or app. Measures what users actually experience, complementary to server-side monitoring.
- **APM (Application Performance Monitoring)** — Server-side telemetry on application behavior: latency, throughput, errors, transaction traces. Dynatrace, New Relic, Datadog APM, similar tools.
- **Error budget** — The inverse of an SLO. The amount of unreliability the team has "allowance" for in a given window before SLO compliance is at risk.
- **Trace** — A request-scoped record that follows a single user action through every service it touches. Distributed tracing is the foundation of multi-service diagnosis.

## Workflow

- **Phase gate** — The approval point at the end of each phase where the user must approve, redirect, or iterate before the agent proceeds.
- **Lens** — A specialized sub-agent that critiques a draft along one specific dimension (MECE, Optimist, ICE, Consultative, Customer, Skeptic). Invoked on demand, not on every artifact.
- **Project space** — `memory/project-space/`. The live investigation memory. Read and written every session; reset between investigations.
- **Long-term memory** — `memory/long-term/`. Durable knowledge that persists across investigations. Read freely; written only on explicit user approval.
