# Issue Tree — Hannah's Bread Company

## Root problem

> "Why can't Hannah's currently detect, diagnose, and prevent performance failures in their mission-critical applications and digital channels before they impact customers or operations?"

**Axis of decomposition:** Observability domain — each branch represents a distinct monitoring and visibility problem space across Hannah's technology stack.

**Cross-cutting constraint (not a branch):** The DataDog → Dynatrace migration creates a dual-stack period during which each branch below has an additional risk layer — metric inconsistency, coverage gaps, and uncertain system-of-record. This constraint is addressed in Phase 2 action planning, not as a problem-space branch.

---

## Branches

Each branch is a problem space, not a solution. Each carries a "what we'd see" line that seeds Phase 1 hypothesis generation.

### Branch 1 — Customer-facing digital experience

**Scope:** Visibility into what end users experience across web and mobile channels. Cross-channel session continuity, device/browser/geo performance consistency, UX-to-business KPI linkage.

- **What we'd see if this is the gap:** Session abandonment on mobile that doesn't appear on web; geo-specific latency spikes visible only by filtering RUM sessions; device- or browser-specific JS errors; mobile app crashes with no corresponding server-side alert; cross-channel conversion discrepancies with no telemetry to explain them.

---

### Branch 2 — Application transaction and dependency performance

**Scope:** Internal behavior of breadSHIP and breadSAIL — transaction latency, endpoint error rates, dependency call performance, service-to-service interaction health.

- **What we'd see if this is the gap:** Elevated transaction latency on distribution queries or yard-management operations with no trace data to locate the slow span; unhandled exceptions in breadSHIP with no stack trace visibility; downstream dependency calls (databases, internal APIs) timing out without surfacing in any monitor; errors discovered by users or facility staff before the IT team is alerted.

---

### Branch 3 — Infrastructure and host health

**Scope:** Server and host performance across 30 U.S. and Canada facilities — CPU, memory, disk, process-level resource saturation. Facility-level availability and capacity posture.

- **What we'd see if this is the gap:** A facility host reaching CPU saturation with no alert; memory pressure causing process restarts with no incident ticket created; disk I/O throttling on a distribution-center host degrading breadSHIP query performance; host unavailability at a remote facility going undetected until a logistics operation fails.

---

### Branch 4 — Network and inter-facility connectivity

**Scope:** Network performance between the 30 facilities, between facilities and cloud/data-center endpoints, and between users and the web/mobile application layer. Includes DNS, routing, latency, and packet loss.

- **What we'd see if this is the gap:** Elevated latency between a specific facility and the breadSHIP data center that causes distribution queries to time out; DNS resolution failures on the mobile app API at a specific geographic location; routing changes causing degraded egress from a facility without a corresponding host-level alert; synthetic monitors failing at a single location while passing globally.

---

### Branch 5 — Anomaly and synthetic visibility gaps

**Scope:** Whether anomalous behavior is detected automatically before users notice it, and whether proactive synthetic checks are in place to catch availability failures without waiting for real user impact.

- **What we'd see if this is the gap:** A performance regression discovered by a facility operator or customer complaint rather than by an alert; alert thresholds in DataDog set to static values that no longer match current traffic patterns (false negatives or alert storms); no synthetic test on the mobile ordering app API — so a regional outage is not detected until the first customer order fails; mean time to detect (MTTD) measured in hours rather than minutes.

---

### Branch 6 — Business metric instrumentation and correlation

**Scope:** Whether application and infrastructure performance signals are connected to business KPIs — order completions, conversion rates, fulfillment throughput, and expansion readiness indicators — so leadership can see the business impact of a technical event.

- **What we'd see if this is the gap:** An outage in breadSAIL that the IT team closes as "resolved" while logistics leadership has no data on how many orders were delayed or lost; a mobile app performance degradation with no correlated conversion drop visible to the CTO; expansion to a new facility with no readiness dashboard to validate that monitoring coverage, availability SLOs, and synthetic tests are in place before go-live.

---

## MECE check

- **Reviewed on:** 2026-05-28
- **Overlaps flagged:**
  - Branches 2 and 3 originally shared database/disk I/O problems (transaction latency and I/O saturation claiming the same root cause). Resolved by clarifying Branch 2 as application-layer transaction behavior and Branch 3 as host-level resource saturation — different monitoring instruments (APM traces vs. host metrics).
  - Branches 2 and 6 (original draft) both touched instrumentation gaps — resolved by promoting instrumentation coverage to Branch 5 (detection) and keeping business KPI linkage in Branch 6. The DataDog/migration gap was moved to a cross-cutting constraint, not a branch.
- **Gaps flagged:** Network and inter-facility connectivity was missing entirely. Added as Branch 4.
- **Abstraction issues flagged:** Original Branch 4 ("Proactive detection and alerting") was a capability branch ("what should exist"), not a problem space. Rephrased as "Anomaly and synthetic visibility gaps" — a problem space that can be confirmed or ruled out.
- **Phrasing issues flagged:** Original Branch 6 ("Monitoring coverage continuity — migration risk") was conclusion-shaped. Demoted to a cross-cutting constraint; replaced by "Business metric instrumentation and correlation" as Branch 6.
- **Resolution:** All four issues addressed. Tree revised to 6 problem-space branches on the observability-domain axis. Migration risk captured as a cross-cutting constraint.

---

## Version history

- **2026-05-28 v1:** Initial draft with 6 branches on observability-domain axis. MECE lens run; 4 issues found and resolved (network branch added, abstraction and phrasing rephrased, migration risk demoted to cross-cutting constraint, instrumentation overlap resolved).
