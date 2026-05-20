# Domain Knowledge

Reference notes on observability, common signal patterns, and the mappings between technical signals and business outcomes. Updated only on explicit user approval.

## Observability concepts

- **SLI (Service Level Indicator)** — a quantitative measure of some aspect of service behavior. Examples: request success rate, p95 request latency, availability percentage, error rate. An SLI is a number; an SLO is a target for that number.
- **SLO (Service Level Objective)** — a target value or range for an SLI over a stated time window. Example: "p95 latency for the checkout-service shall be below 300ms over any rolling 30-day window."
- **SLA (Service Level Agreement)** — a contractual commitment derived from one or more SLOs, with consequences attached. SLOs are internal; SLAs are external.
- **Error budget** — the inverse of an SLO. If the SLO is 99.9% availability over 30 days, the error budget is 0.1% of that window — roughly 43 minutes of downtime per month. Burn rate tracks how quickly the budget is being consumed.
- **RUM (Real User Monitoring)** — telemetry collected from actual user sessions in the browser or app. Measures what users actually experience: page load times, JS errors, route transitions, INP, LCP. Complements server-side and synthetic monitoring.
- **APM (Application Performance Monitoring)** — server-side telemetry on application behavior: request latency, throughput, error rate, transaction traces, dependency calls. Dynatrace, New Relic, Datadog APM, and similar tools.
- **Traces** — request-scoped records that follow a single user action through every service it touches. A trace makes it possible to see that a 2s page load is 1.7s of database query inside `payment-service` and 200ms of everything else. Distributed tracing requires consistent context propagation across services.
- **Logs** — discrete, timestamped events emitted by services. Structured logs (JSON) are queryable; unstructured logs are archaeological. Logs are the third pillar of observability alongside metrics and traces.
- **Metrics** — numeric measurements aggregated over time. Cheap to store, fast to query, lossy by construction. Use metrics for SLIs and dashboards; use traces and logs for diagnosis.

## Common signal patterns

Patterns the team recognizes from prior investigations. Each pattern names what the signal typically indicates so the agent does not have to re-derive it every time.

- **Latency degradation** — p95/p99 latency rises while p50 stays flat. Typically indicates a long-tail problem: a slow dependency, GC pauses, lock contention, or a small population of pathological requests. If p50 also rises, the cause is more pervasive (saturation, broad regression).
- **Step-function latency change at a deploy timestamp** — strong signal of a code or configuration change introduced in that deploy. Confirm against the deploy log and the change set.
- **Error rate spikes** — sustained rise in 5xx (server errors) usually indicates the service itself is failing; sustained rise in 4xx (client errors) usually indicates upstream or input changes. Short transient spikes correlated with deploys usually self-resolve.
- **Throughput drops** — request volume drops while error rate is steady. Usually indicates an upstream issue (CDN, DNS, load balancer, client-side problem) rather than the service itself. Check upstream layers first.
- **Saturation** — resource utilization (CPU, memory, thread pool, connection pool) approaches limits. Typically a precursor to latency degradation and error rate spikes. USE method (Utilization, Saturation, Errors) is a useful checklist.
- **Cache hit-rate collapse** — sudden drop in cache hit rate, often correlated with latency rise and downstream load increase. Usually points to a cache invalidation event, a config change, or a deploy that changed cache keys.
- **Funnel-step abandonment correlated with technical signal** — when a specific step in a user funnel shows elevated abandonment in lockstep with a technical regression on the same step, the linkage is strong. Look for the timestamp coincidence.

## Tech → UX → business linkages

Standard mappings the agent uses to translate technical findings into business impact. These are starting points — every investigation should validate the mapping against the specific product and user base.

| Technical signal | UX outcome | Business KPI |
|---|---|---|
| Backend p95 latency on a key endpoint | Page load time / time-to-interactive | Conversion rate; bounce rate; session depth |
| Mobile crash rate | App stability, perceived reliability | App store rating; retention; uninstall rate |
| API error rate (5xx) on a critical path | Failed actions, broken workflows | Funnel completion; support ticket volume; churn |
| CDN cache hit rate | Time-to-first-byte; geographic consistency | Conversion in distant regions; bounce rate by region |
| Auth latency or error rate | Login friction, lockouts | Sign-in success rate; new-user activation |
| Search latency | Search abandonment, query reformulation | Search-to-conversion rate; revenue per search |
| Payment SDK error rate | Failed checkout, repeated attempts | Checkout conversion; cart abandonment rate; revenue at risk |

## Dynatrace-specific concepts

Originally seeded from `docs.dynatrace.com` on 2026-05-12; baseline page-last-updated values for every citation were captured on 2026-05-20 by the `doc-freshness-checker` sub-agent (see `skills/external-research/SKILL.md`). The vendor-authoritative definition lives here; org-specific behavior (which MZs the team runs, which synthetic tests are load-bearing, the team's OneAgent vs OpenTelemetry mix) is captured in the `[team to note ...]` brackets and should be filled in by the team. When a doc-sourced fact is updated below, bump both the page-last-updated and the retrieval date.

- **DPS (Dynatrace Platform Subscription)** — Licensing model that covers all Dynatrace capabilities under one agreement, typically 1–3 years with a minimum annual commit. Usage is recorded as Billing Usage Events (BUEs) in Grail; on-demand usage above the commit is billed monthly at the same rates as pre-paid consumption. *(Source: https://docs.dynatrace.com/docs/manage/dynatrace-platform-subscription — page last-updated 2025-09-03; retrieved 2026-05-20.)* [Team to note: which capabilities are in our DPS rate card and which months have run hot on-demand.]
- **Grail** — Dynatrace's observability and security data lakehouse — unified storage for logs, metrics, traces, events, and topology with an MPP query engine and no upfront schema. Read via DQL; the agent references Grail as the data substrate, not as something to query directly. *(Source: https://docs.dynatrace.com/docs/platform/grail/dynatrace-grail — page last-updated 2026-01-28; retrieved 2026-05-20.)* [Team to note: our Grail retention windows per data type and any tables we have explicitly disabled.]
- **DQL (Dynatrace Query Language)** — Read-only, pipeline-style query language for Grail. Queries chain commands (`fetch`, `filter`, `summarize`, etc.) with `|`. The agent describes what data a hypothesis needs in plain English; **the team writes the DQL**. *(Source: https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language — page last-updated 2026-01-28; retrieved 2026-05-20.)* [Team to note: our internal DQL style conventions and any vetted query snippets that should be linked from action plans.]
- **Smartscape** — Auto-discovered, near real-time topology of entities (services, processes, hosts, data centers) and dependencies. Vertical view = full-stack dependencies for one entity; horizontal view = upstream callers / downstream callees around a focused node. Smartscape on Grail is the Grail-native variant. *(Source: https://docs.dynatrace.com/docs/platform/smartscape — page last-updated unknown; retrieved 2026-05-20.)* [Team to note: which Smartscape views we consider load-bearing for cross-team triage.]
- **Davis AI** — Causation-based AI engine that traverses the Smartscape causal topology, correlates related events into a single problem, and identifies a root-cause entity. Davis grouping is deliberate — treat alert consolidation as a feature when reasoning about volume. *(Source: https://docs.dynatrace.com/docs/platform/davis-ai — page last-updated 2026-01-28; retrieved 2026-05-20.)* [Team to note: which Davis problem types we trust without human review and which we always sanity-check.]
- **Management Zones (MZ)** — Information-partitioning mechanism that scopes both views and access. Rules define which entities and dimensional data belong to a zone; a role granted at MZ scope acts as a security filter on that group's view. *(Source: https://docs.dynatrace.com/docs/manage/identity-access-management/permission-management/management-zones — page last-updated unknown; retrieved 2026-05-20.)* [Team to note: our MZ taxonomy — by product line, by team, or by environment — and any zones that intentionally overlap.]
- **Service-flow** — [Team to note how service-flow views support investigation in our environment, and whether the action plan should usually open with a service-flow screenshot when the problem is cross-service.]
- **Synthetic monitoring** — [Team to note which synthetic tests are load-bearing for which SLOs — i.e., which tests, if red, are sufficient to declare an SLO breach without further evidence.]
- **OneAgent** — Host-level agent; one per host collects process, service, and infrastructure data across containers, VMs, and cloud hosts. Modes include Full-Stack and Infrastructure Observability; Full-Stack is recommended for business-critical applications. *(Source: https://docs.dynatrace.com/docs/ingest-from/dynatrace-oneagent — page last-updated unknown; retrieved 2026-05-20.)* [Team to note: our OneAgent vs OpenTelemetry split — which services are exclusively on each and any known instrumentation gaps at the boundary.]
- **RUM session / user action** — A RUM session is a "user visit"; a user action is a click, tap, or app start that triggers a web request. Session-per-application-per-hour is the DPS unit of measure for RUM consumption. *(Source: https://docs.dynatrace.com/docs/observe/digital-experience/rum-concepts/rum-overview — page last-updated 2023-10-20; retrieved 2026-05-20.)* [Team to note: which applications we have RUM enabled on and whether session-replay is on for any of them.]

When a Dynatrace concept is unclear, ambiguous, or missing from this section, the agent consults the **authoritative external references** below via `skills/external-research/SKILL.md` rather than guessing. Findings land in the active phase artifact with a citation, and durable additions to this file require explicit user approval.

## Authoritative external references

The agent treats the sources below as the canonical lookup path for Dynatrace concepts and known issues. The list is an allowlist: the agent fetches from these domains and asks before fetching from anything else. The procedure for using them lives in `skills/external-research/SKILL.md`.

| Source | URL root | What it is good for | Confidence weight |
|---|---|---|---|
| Dynatrace product documentation | `https://docs.dynatrace.com/` | Feature behavior, defaults, supported configuration, concept definitions, deprecation timelines, quota limits. | Vendor-authoritative. |
| Dynatrace Community | `https://community.dynatrace.com/` | Practitioner discussion, known-issue corroboration, workarounds, migration nuance. | Practitioner reporting — corroborate before treating as ground truth. |

**Citation rule.** Every fact pulled from these sources lands in the phase artifact with its URL, the page's own "Last updated" date, and the retrieval date — e.g., *"Source: https://docs.dynatrace.com/… — page last-updated 2026-04-30; retrieved 2026-05-12"*. Capturing both dates is what makes the freshness sub-agent work: the page-last-updated value is the comparison point for drift detection. If a page does not advertise a last-updated date, write `page last-updated unknown`.

**Freshness rule.** Citations older than 7 days are presumed stale and must be re-validated before reuse in any phase artifact. The `doc-freshness-checker` sub-agent (defined in `.claude/agents/doc-freshness-checker.md`) is dispatched as a Haiku background task at the start of every Phase 0 — it re-checks every cited URL while the consultant answers Q1–Q9 and writes findings to `memory/long-term/freshness-report.md`. The sub-agent writes only to the report — it never edits this file or `dynatrace-playbooks.md` directly. The main agent surfaces drifted or unreachable citations at the Phase 0 gate so the team can approve memory updates inline. The full procedure lives in `skills/external-research/SKILL.md`.

**Reserved for future integration** (do not invoke without user approval and a configured tool):

- Internal Slack channels — practitioner discussion, incident retros, oncall handoffs.
- Salesforce — customer tickets, account-specific context, support history.

When the team is ready to add an internal source, propose it as a row in this table at the next gate. The agent does not silently expand the allowlist.
