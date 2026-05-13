# Dynatrace Investigation Playbooks

Client-agnostic procedural patterns for using Dynatrace to investigate common problem shapes. **These describe the workflow, not the configuration** — no specific Management Zone names, service names, or environment IDs appear here. Org-specific behavior (which Smartscape views the team trusts, which synthetic tests are load-bearing, which Davis problem types get auto-actioned) lives in `domain-knowledge.md`.

## How to use this file

- **Phase 1 (hypothesis generation)** — when a hypothesis names a problem shape (latency, errors, UX, etc.), the agent pulls the matching playbook's investigation sequence into the "validation approach" field and the playbook's "confirmed" / "ruled out" criteria into exit criteria.
- **Phase 2 (action plan)** — the playbook seeds the investigation-action rows. Each step becomes a candidate action with the playbook's source URL carried through as the citation.
- **Phase 3 (one-pager and deck)** — the playbook's "what good evidence looks like" anchors the "Top findings" framing so the deliverable matches what the team actually observed.

Playbook content is sourced from `docs.dynatrace.com` on 2026-05-12 unless noted otherwise. Re-verify before relying on a procedural detail in a deliverable; product surfaces evolve.

## Playbook index

| Problem shape | Playbook |
|---|---|
| Latency degradation on a backend service | [Latency on a backend service](#latency-on-a-backend-service) |
| Error rate / failure spike on a service | [Service failure spike](#service-failure-spike) |
| User-visible slowness or errors in the browser/app | [Frontend / UX regression in RUM](#frontend--ux-regression-in-rum) |
| Anomalous behavior in logs (volume, errors, content) | [Log investigation in Grail](#log-investigation-in-grail) |
| SLO at risk or breached | [SLO breach / error-budget burn](#slo-breach--error-budget-burn) |
| Regression correlated with a deploy | [Deploy / release correlation](#deploy--release-correlation) |
| Third-party dependency suspected | [Third-party dependency investigation](#third-party-dependency-investigation) |
| Triage starting from an open Davis problem | [Reading a Davis problem](#reading-a-davis-problem) |

---

## Latency on a backend service

### When this applies

A hypothesis names elevated p95/p99 latency on a specific service or call path. Symptoms include rising tail latency, slow page loads tracing back to a backend call, or a Davis problem with "response time degradation" framing.

### Investigation sequence

1. Open the **Services app** for the suspected service and review the response-time chart against the prior baseline window.
2. From the service overview, under **Understand dependencies**, select **View service flow** to see the call topology and where time is being spent across downstream calls.
3. In **Distributed Tracing**, open the slow traces in the affected window and read the **waterfall** to find the span(s) that account for the regression — DB call, downstream service, internal compute, or external dependency.
4. Switch the trace view to **Spans**, filter for internal spans, and group by **Service** and **Span name** to surface the consistently long-running spans across the population (not just one trace).
5. Cross-check against `Smartscape` horizontal topology around the focused service to identify upstream callers (who is feeling it) and downstream callees (who is causing it).

### What "confirmed" looks like

- A specific span name or downstream call accounts for the majority of the added time in the affected window, and the elevation persists across multiple traces (not a single outlier).
- The latency rise is concentrated on a specific call path or endpoint, not spread uniformly across the service's surface area.

### What "ruled out" looks like

- p50/p95/p99 are all flat on the service across the affected window, and trace samples show no consistent slow span — the latency reported elsewhere is not originating in this service.

### Common dead-ends

- Looking only at the service's aggregate response time. A 200ms median is fine; a p99 of 12s is the story. Always pull the percentiles.
- Reading one slow trace and generalizing. One trace is an anecdote; the **Spans** view grouped by service + span name is the population.

### Source

- https://docs.dynatrace.com/docs/observe/application-observability/distributed-traces/analysis/get-started — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/observe/application-observability/distributed-tracing/use-traces-and-dql-to-spot-patterns — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/observe/application-observability/services/services-app — retrieved 2026-05-12.

---

## Service failure spike

### When this applies

A hypothesis names elevated error rate (5xx, gRPC errors, span-status errors, or unhandled exceptions) on a specific service or call path.

### Investigation sequence

1. Open **Failure Analysis** for the suspected service. Dynatrace detects failed states based on **HTTP/gRPC response codes, span status, and the presence of exceptions within traces** — read all three.
2. In the failed-trace list, drill down to **service failure causes**. Group by exception type or HTTP status code to see whether one root error dominates or whether the failure is broad.
3. Open **Exception Analysis** for the dominant exception. Errors are captured as span attributes with type, message, stack trace, and timestamp — read the stack trace, not just the message.
4. Use the **Spans** view filtered to failed spans and grouped by **Service** and **Endpoint** to confirm whether the failure is endpoint-scoped or service-wide.
5. Confirm against any open **Davis problem** for the same window — Davis correlates events with the same root cause into a single problem, so the problem record may already name the originating entity.

### What "confirmed" looks like

- A specific exception type or HTTP status code accounts for the failure spike, with a recognizable stack trace, and the same signature appears across the failing traces.
- The endpoint or call path producing the failures is identifiable, not spread uniformly across the service.

### What "ruled out" looks like

- The service's failure rate is steady across the affected window and Failure Analysis shows no new exception types, no new failing endpoints, and no Davis problem.

### Common dead-ends

- Reading the exception **message** without the stack trace. Messages are often generic ("connection refused"); the stack trace says where in the code path the failure originated.
- Treating 4xx and 5xx the same. 4xx usually points upstream (bad input, client/protocol issue); 5xx usually points to the service itself. Investigate them separately.

### Source

- https://docs.dynatrace.com/docs/observe/application-observability/services/failure-analysis — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/observe/application-observability/distributed-tracing/exception-analysis — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/analyze-explore-automate/distributed-traces/use-cases/error-analysis — retrieved 2026-05-12.

---

## Frontend / UX regression in RUM

### When this applies

A hypothesis names a user-visible problem — page slowness, abandoned flows, browser/device-specific errors, regional regressions, route-transition failures.

### Investigation sequence

1. Open **Users & Sessions** in the **New RUM Experience** for the affected application and the affected time window.
2. **Filter sessions** by duration, frontend, browser, browser window width, and location to find the segment that is regressed. The filter axes most often load-bearing are **browser/OS** (for client-side regressions), **location/region** (for CDN or network), and **route/view** (for page-scoped regressions).
3. **Sort by navigation count** to isolate the longest, most-deeply-engaged sessions and review the per-event timing — domain lookup, connection time, request duration, DOM processing — to identify which phase regressed.
4. Open **Error Inspector** to see the JS errors and HTTP failures grouped by frontend and route. Cross-check with the RUM-side failure list — RUM JS errors are independent of backend 5xx and often reveal client-side regressions that backend telemetry will miss.
5. If frontend timing isolates the regression to backend latency (e.g., long request duration), hand off to the [Latency on a backend service](#latency-on-a-backend-service) playbook using the named endpoint.

### What "confirmed" looks like

- A specific segment (browser/OS, region, route) shows the regression and an adjacent segment does not.
- The regressed timing phase is identified (lookup vs connect vs request vs DOM) — not a vague "page is slower".

### What "ruled out" looks like

- Session distributions, timing phases, and Error Inspector counts are flat across the affected window when sliced by the candidate segmentation axes.

### Common dead-ends

- Looking at aggregate RUM dashboards before filtering. The whole-app view almost always looks fine when the regression is segment-specific.
- Ignoring browser/OS and region. These are the highest-signal segmentation axes for frontend regressions and the first place to look.

### Source

- https://docs.dynatrace.com/docs/observe/digital-experience/new-rum-experience/users-and-sessions — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/observe/digital-experience/new-rum-experience/error-inspector — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/observe/digital-experience/rum-concepts/rum-overview — retrieved 2026-05-12.

---

## Log investigation in Grail

### When this applies

A hypothesis depends on log evidence — error volume in a window, specific error messages, log-derived metrics, parsed fields not exposed elsewhere.

### Investigation sequence

1. Frame the question as a **DQL pipeline shape** before opening any UI: `fetch <data> → filter <predicate> → summarize <aggregation>`. The agent describes this pipeline to the team in plain English; **the team writes the DQL** (per CLAUDE.md).
2. Specify the **data source** for `fetch` — logs, events, business events, security data, spans, or metrics — and the time window (`from:` parameter).
3. Specify the **filter** predicates needed: field operators (`==`, `!=`), substring matching (`contains`, `endsWith`), and any field extraction patterns required (DPL — Dynatrace Pattern Language — with elements like `LD:` for line data and typed fields like `INT:httpstatus`).
4. Specify the **aggregation** needed in `summarize` — count, distinct, percentile, time-bucketed series — and the group-by dimensions.
5. Hand the pipeline shape to the team alongside the hypothesis. The team validates the query and shares the result back as evidence on the hypothesis row.

### What "confirmed" looks like

- The team's executed query returns the expected pattern (volume, rate, distribution) and the shape matches the hypothesis's expected signal.

### What "ruled out" looks like

- The query executes against the right window and returns flat or absent signal where the hypothesis predicted a change.

### Common dead-ends

- Asking the team to "look at the logs". Logs without a query are archaeological. Always specify the pipeline shape.
- Forgetting the **time window**. DQL queries default to a UI-selected window; the hypothesis specifies what window is meaningful — pass it through.
- Querying without a parsing strategy when the field is unstructured. If the relevant data is inside a free-text message, the team will need a `parse` step with a DPL pattern; flag this up front.

### Source

- https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/dql-guide — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/commands/filtering-commands — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/commands/aggregation-commands — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language/commands/extraction-and-parsing-commands — retrieved 2026-05-12.

---

## SLO breach / error-budget burn

### When this applies

A hypothesis depends on the state of an SLO — is the SLO at risk, is the error budget burning fast, is a recent change pushing burn rate up?

### Investigation sequence

1. Identify the SLO that protects the affected user experience or service. Confirm its **threshold** (target), its **evaluation period**, and the SLI it tracks.
2. Read the **error budget** as the difference between current SLO status and SLO threshold. A positive error budget means the SLO is currently compliant; a negative one means it is breached.
3. Pull the **burn rate** over the last hour. Fast-burn alerts in Dynatrace use a **-1h look-back window**; a static threshold of **10–14** is the documented starting point for fast-burn detection.
4. If the burn rate is elevated, correlate the burn window against deploy events, traffic shifts, and any open Davis problem — burn rate by itself is the symptom, not the cause.
5. If the SLO is breached but burn is now flat, the breach is historical — confirm whether the underlying SLI has recovered and the SLO is now compliant going forward.

### What "confirmed" looks like

- Burn rate is sustained above the fast-burn threshold over the look-back window, with an identifiable cause in the same window (deploy, dependency regression, traffic shift).

### What "ruled out" looks like

- Burn rate is within normal bounds across the affected window and the error budget is intact, even if the underlying signal looks visually concerning. The SLO is the contract; absent burn-rate signal, the SLO is not at risk.

### Common dead-ends

- Reading the SLO status snapshot without the burn rate. A compliant SLO with rapidly burning budget will breach tomorrow; treat burn rate as the leading indicator.
- Using a too-short look-back window for slow-burn problems. Slow-burn alerts use a longer look-back than the -1h fast-burn window; pick the window that matches the failure mode.

### Source

- https://docs.dynatrace.com/docs/deliver/service-level-objectives/service-level-objective-basics — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/deliver/service-level-objectives — retrieved 2026-05-12.

---

## Deploy / release correlation

### When this applies

A hypothesis names a deploy, release, or configuration change as the suspected cause — typically a step-function regression timestamped close to a known change event.

### Investigation sequence

1. Pull **deployment events** and **SDLC events** for the suspected service(s) in the affected window. Dynatrace shows process restart events and deployment events; SDLC events represent release, deploy, and quality-gate transitions emitted by CI/CD pipelines.
2. Confirm the **version detection** is reliable for the service — process version, package version, or container image tag — so the "before/after" comparison is clean.
3. Overlay the deploy timestamp on the affected metric (latency, error rate, RUM signal). A **step-function change at the deploy timestamp** is a strong signal; a slow drift starting before the deploy is not.
4. Read Dynatrace's **event correlation** for the same window — Davis correlates deployment events with downstream symptoms when the topology supports it. The correlation may already name the originating change.
5. Confirm against the team's change log / release notes for the deployed version. Without that confirmation, the correlation is suggestive, not proven.

### What "confirmed" looks like

- A clean step-function change in the affected SLI at the deployment timestamp, persisting through the post-deploy window, with a named version delta and a plausible mechanism in the change set.

### What "ruled out" looks like

- The metric was already trending before the deploy timestamp, **or** other instances on the same version are unaffected, **or** rolling back the version does not restore the SLI.

### Common dead-ends

- Treating temporal correlation as causation. A deploy and a CDN config change in the same hour are equally suspect until the change set is read.
- Trusting version detection silently. If the service's version label is stale or missing, the before/after comparison is unreliable — verify the version detection strategy first.

### Source

- https://docs.dynatrace.com/docs/deliver/release-monitoring/monitor-releases-with-dynatrace — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/deliver/release-monitoring/version-detection-strategies — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/deliver/pipeline-observability-sdlc-events — retrieved 2026-05-12.

---

## Third-party dependency investigation

### When this applies

A hypothesis names an external dependency — payment processor, identity provider, CDN, third-party API — as the suspected cause.

### Investigation sequence

1. Confirm whether the dependency is monitored. **Synthetic monitoring** is the primary lens for third-party availability: single-URL browser monitors, browser clickpaths, HTTP monitors, and Network Availability Monitoring (ICMP ping, TCP port check, DNS).
2. Pull the synthetic results for the dependency in the affected window. Treat synthetic failure or latency as **direct evidence** the dependency is misbehaving; treat synthetic success as evidence the dependency is reachable from the synthetic location (which may not match the customer's location).
3. If the dependency emits third-party synthetic data via the **Third-Party Synthetic API**, pull those results too — they may have richer coverage than Dynatrace-run synthetics.
4. Cross-check service-side calls to the dependency in **Distributed Tracing** — look for spans whose target is the third-party endpoint and read their latency and failure rate. A backend service that depends on a third party will show the symptom on outbound spans.
5. If the dependency is behind a CDN or load balancer, segment by **region** in RUM and synthetic to confirm whether the symptom is geographic.

### What "confirmed" looks like

- Synthetic monitors against the dependency endpoint show elevated latency or failure in the affected window, AND service-side outbound spans to the same endpoint show the corresponding pattern.

### What "ruled out" looks like

- Synthetic and outbound-span signal are both clean across the affected window, even though the team's intuition pointed to the dependency. Look upstream of the dependency call instead.

### Common dead-ends

- Treating synthetic success from one location as proof the dependency is healthy globally. Synthetic coverage is location-specific; user impact may be in a region the synthetic does not cover.
- Ignoring outbound spans. Dependency problems usually manifest as elevated outbound-span latency or failures inside the calling service's traces; that view is often clearer than the dependency's own monitor.

### Source

- https://docs.dynatrace.com/docs/observe/digital-experience/synthetic-monitoring — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/observe/digital-experience/synthetic-monitoring/network-availability-monitors/network-availability-monitoring — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/observe/applications-and-microservices/services/service-detection-v1/monitor-3rd-party-services — retrieved 2026-05-12.

---

## Reading a Davis problem

### When this applies

The investigation starts from an open Davis problem (the team was paged, the Problems app surfaced an issue) rather than from a hypothesis. The agent's job is to extract the problem's structure before generating hypotheses.

### Investigation sequence

1. Open the **Problems app** and select the problem. Read the problem title, severity, and time window first.
2. Read the **root cause entity** — Davis marks one entity with a red mark as the suggested starting point. Treat this as Davis's hypothesis, not as truth; it is a starting point for investigation.
3. Scan the **Affected entities** section to see the blast radius — entity types and event counts. A problem with a single affected service is a different shape from one with 40 affected services and a shared dependency.
4. Read the **events timeline** within the problem. Davis correlates events that share a root cause into a single problem; the timeline shows the sequence in which symptoms appeared.
5. Use the root cause entity and event sequence to seed Phase 1 hypotheses — typically the matching playbook ([Latency on a backend service](#latency-on-a-backend-service), [Service failure spike](#service-failure-spike), [Deploy / release correlation](#deploy--release-correlation), etc.) — rather than restarting from scratch.

### What "confirmed" looks like

- The Davis-suggested root cause entity, when investigated with the matching playbook, produces a coherent story for the entire affected-entity list.

### What "ruled out" looks like

- The Davis-suggested root cause does not explain the observed symptoms when investigated, **or** affected entities exist that have no causal path from the suggested root.

### Common dead-ends

- Treating Davis's root cause as the answer. Davis's job is to propose; the team's job is to verify. The red-mark entity is where to *start*, not where to *stop*.
- Ignoring the affected-entity list. The blast radius shape (one service vs many services on a shared dependency) usually picks the playbook for you.

### Source

- https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/root-cause-analysis/davis-problems-app — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/platform/davis-ai/problem-and-root-cause — retrieved 2026-05-12.
- https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/root-cause-analysis/concepts/events — retrieved 2026-05-12.

---

## What this file deliberately does NOT contain

- **Executable DQL.** The agent describes the pipeline shape (`fetch → filter → summarize`) in plain English. The team writes and runs the query.
- **Specific Management Zone names, service names, or environment IDs.** Those are client/team-specific and live in `domain-knowledge.md` brackets.
- **UI click paths past one level of detail.** Dynatrace UI evolves faster than the conceptual workflow. The playbooks name the *artifact* (Services app, Failure Analysis, Users & Sessions) and let the team click into it.
- **Recommendations on whether to use Classic vs new Apps.** Where both exist, the playbook names the concept and lets the team pick the surface their environment runs.
- **Configuration guidance.** This file is for *how to investigate*, not *how to set up*. SLO configuration, failure-detection rules, and synthetic test creation are out of scope here.
