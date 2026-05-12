# Issue Tree

The MECE decomposition of the current problem. The agent updates this file in Phase 1 and any time the user redirects the framing.

## Root problem

> [The reframed problem from `current-context.md`, stated as a question. Example: "Why has checkout conversion declined 8% week-over-week on iOS while remaining flat on web?"]

## Branches

Each branch represents a problem space, not a solution. Each branch carries a one-line note describing **what we would see if this branch is the cause** — this is the seed of the hypotheses generated in Phase 1.

### Client

- **What we'd see if this is the cause**: [e.g., elevated client-side errors, JS exceptions, frontend latency, render failures, increased crash rate on a specific OS version or device class.]

### Network

- **What we'd see if this is the cause**: [e.g., elevated TTFB regionally, packet loss on specific ASNs, CDN edge anomalies, DNS resolution failures.]

### Backend (application)

- **What we'd see if this is the cause**: [e.g., elevated p95/p99 service latency, increased 5xx rate, thread pool saturation, GC pauses, deploy-correlated regressions.]

### Data (storage and pipelines)

- **What we'd see if this is the cause**: [e.g., query latency regressions, replica lag, cache miss rate spike, schema migration timing, stale or missing analytics events.]

### Third-party dependencies

- **What we'd see if this is the cause**: [e.g., elevated latency or error rate from a named upstream vendor — payment gateway, auth provider, geocoding, analytics SDK.]

### Business process / configuration

- **What we'd see if this is the cause**: [e.g., recent pricing change, promotion configuration, feature flag rollout, geographic gating, A/B test in flight.]

### Instrumentation gaps

- **What we'd see if this is the cause**: [the cause is genuine but invisible — note which data we would need to instrument to confirm or rule out. Listed as a branch because it changes how the investigation proceeds.]

## MECE check

Notes from the most recent MECE lens review. Capture what was flagged and how it was resolved.

- **Reviewed on**: [YYYY-MM-DD]
- **Overlaps flagged**: [...]
- **Gaps flagged**: [...]
- **Abstraction issues flagged**: [...]
- **Resolution**: [what was changed; what was kept as-is and why]

## Version history

Date-stamped revisions. Append a new entry whenever the tree changes.

- **YYYY-MM-DD**: Initial draft. [Brief note on the starting structure.]
- **YYYY-MM-DD**: [What changed and why — e.g., "added third-party branch after MECE lens flagged missing dependency on payment gateway".]
