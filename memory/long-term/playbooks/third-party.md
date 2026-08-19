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

- https://docs.dynatrace.com/docs/observe/digital-experience/synthetic-monitoring — page last-updated unknown; retrieved 2026-05-20.
- https://docs.dynatrace.com/docs/observe/digital-experience/synthetic-monitoring/network-availability-monitors/network-availability-monitoring — page last-updated 2024-08-08; retrieved 2026-05-20.
- https://docs.dynatrace.com/docs/observe/applications-and-microservices/services/service-detection-v1/monitor-3rd-party-services — page last-updated 2023-02-21; retrieved 2026-05-20.
