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

- https://docs.dynatrace.com/docs/observe/application-observability/distributed-traces/analysis/get-started — page last-updated 2024-08-13; retrieved 2026-05-20.
- https://docs.dynatrace.com/docs/observe/application-observability/distributed-tracing/use-traces-and-dql-to-spot-patterns — page last-updated 2025-11-20; retrieved 2026-05-20.
- https://docs.dynatrace.com/docs/observe/application-observability/services/services-app — page last-updated 2026-05-19; retrieved 2026-05-20.
