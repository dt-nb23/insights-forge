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

## Dynatrace platform

Definitions originally seeded from `docs.dynatrace.com` on 2026-05-12; baseline page-last-updated values for every citation were captured on 2026-05-20 by the `doc-freshness-checker` sub-agent (see `skills/external-research/SKILL.md`). Citation format is `(Source: URL — page last-updated YYYY-MM-DD; retrieved YYYY-MM-DD)`; the sub-agent re-validates these citations at the start of every Phase 0. Org-specific behavior (which Management Zones the team runs, which Smartscape views are load-bearing) lives in `domain-knowledge.md`, not here.

- **Grail** — Dynatrace's data lakehouse for observability and security data; unified storage for logs, metrics, traces, events, and entity topology with a massively parallel processing query engine and no required indexes. *(Source: https://docs.dynatrace.com/docs/platform/grail/dynatrace-grail — page last-updated 2026-01-28; retrieved 2026-05-20.)*
- **DQL (Dynatrace Query Language)** — Read-only, pipeline-style query language for data in Grail. Commands are chained with `|` and there is no upfront schema requirement. The agent does not generate DQL — it references the *kinds of data* a hypothesis needs and lets the team write the query. *(Source: https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language — page last-updated 2026-01-28; retrieved 2026-05-20.)*
- **Smartscape** — Near real-time auto-discovered topology of entities (services, processes, hosts, data centers) and their dependencies. Vertical view shows full-stack dependencies; horizontal view shows upstream/downstream calls around a focused node. Smartscape on Grail is the Grail-native variant. *(Source: https://docs.dynatrace.com/docs/platform/smartscape — page last-updated unknown; retrieved 2026-05-20.)*
- **Davis AI** — Dynatrace's causation-based AI engine. Traverses the Smartscape causal topology to correlate related events into a single problem and identify a root-cause entity. Treat single-problem grouping as a feature, not a bug, when reasoning about alert volume. *(Source: https://docs.dynatrace.com/docs/platform/davis-ai — page last-updated 2026-01-28; retrieved 2026-05-20.)*
- **OneAgent** — Dynatrace's host-level agent. One agent per host collects all monitoring data (processes, services, infrastructure) across containers, VMs, and cloud hosts. Monitoring modes include Full-Stack and Infrastructure Observability. *(Source: https://docs.dynatrace.com/docs/ingest-from/dynatrace-oneagent — page last-updated unknown; retrieved 2026-05-20.)*
- **Management Zone (MZ)** — An information-partitioning mechanism that scopes both views and access. MZ rules define which entities and dimensional data (logs, metrics) belong to the zone; when a role is granted at MZ scope, the zone acts as a security filter on that group's view. *(Source: https://docs.dynatrace.com/docs/manage/identity-access-management/permission-management/management-zones — page last-updated unknown; retrieved 2026-05-20.)*
- **DPS (Dynatrace Platform Subscription)** — The licensing model for all Dynatrace capabilities. Typically a 1–3 year agreement with a minimum annual commitment; usage is recorded as Billing Usage Events (BUEs) in Grail and on-demand usage above the commit is billed monthly at the same rates. *(Source: https://docs.dynatrace.com/docs/manage/dynatrace-platform-subscription — page last-updated 2025-09-03; retrieved 2026-05-20.)*
- **RUM session / user action** — A RUM session is a "user visit" in a web, mobile, or custom application; a user action is a click, tap, or app start that triggers a web request (page load, route transition). Session-per-application-per-hour is the DPS unit of measure for RUM consumption. *(Source: https://docs.dynatrace.com/docs/observe/digital-experience/rum-concepts/rum-overview — page last-updated 2023-10-20; retrieved 2026-05-20.)*
