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

Placeholder section — the team should populate this with the Dynatrace-specific terminology, dashboards, and conventions relevant to their environment. Suggested entries to fill in:

- **DPS (Dynatrace Platform Subscription)** — [team to note licensing model and any reporting implications].
- **Grail** — [team to note query model, retention windows, and which data sources land in Grail].
- **DQL (Dynatrace Query Language)** — [team to note style conventions; remember the agent does not generate DQL, but references it].
- **Smartscape** — [team to note when Smartscape topology is the right view].
- **Davis AI** — [team to note what Davis does well, what it surfaces, what to treat with caution].
- **Management Zones** — [team to note their org's MZ structure].
- **Service-flow** — [team to note how service-flow views support investigation].
- **Synthetic monitoring** — [team to note which synthetic tests are load-bearing for which SLOs].
- **OneAgent vs OpenTelemetry ingest** — [team to note their mix].
