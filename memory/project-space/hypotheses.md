# Hypotheses

Ranked candidate hypotheses for the current investigation. Each row maps to a branch in `issue-tree.md`. The agent updates this file in Phase 1 (initial drafting and ICE scoring) and keeps the **Status** column current as evidence comes in from the team.

## Status legend

- **open** — not yet investigated.
- **validating** — investigation in progress; evidence is being gathered.
- **confirmed** — exit criteria met; this is a real cause.
- **ruled out** — exit criteria met; this is not the cause.

## Hypothesis table

| ID | Hypothesis | Branch | Expected signals | Validation approach | Required metrics (not queries) | Impact | Confidence | Effort | ICE | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| H-01 | iOS checkout conversion decline is driven by elevated client-side JS exceptions in the payment SDK after the 4.12 SDK update. | Client | Spike in JS exception rate on iOS Safari starting around SDK rollout date; concentrated on payment screen route; absent on web. | Compare client error rate by OS and route before and after rollout; segment by SDK version where available. | RUM JS error rate, segmented by OS and route; SDK version distribution; checkout funnel step conversion. | 8 | 6 | 3 | 16.0 | validating |
| H-02 | A backend p95 latency regression in the cart-service after the 2026-05-04 deploy is causing a measurable share of users to abandon checkout. | Backend | p95 latency on cart-service rises step-function-like after deploy; abandonment rate at cart→payment step rises in lockstep. | Compare cart-service p95 latency seven days before vs seven days after deploy; correlate with step-level funnel conversion. | Service p95/p99 latency over time; deploy timestamps; funnel step conversion; user session duration on cart route. | 7 | 7 | 4 | 12.25 | open |
| H-03 | A third-party payment gateway has elevated error rate from a specific region (e.g., LATAM), and iOS traffic is disproportionately routed there. | Third-party | Payment gateway error rate elevated for affected region; iOS traffic share in that region higher than baseline; conversion impact concentrated geographically. | Compare payment gateway success rate by region and platform; cross-reference with iOS traffic distribution. | Payment gateway success/error rate by region; iOS vs web traffic distribution by region; checkout completion by region and platform. | 6 | 4 | 5 | 4.8 | open |

## Notes on the table

- **Expected signals** must be specific enough that the team can recognize the signal when they see it. "Latency goes up" is not a signal. "p95 latency on cart-service rises step-function-like after deploy" is a signal.
- **Required metrics (not queries)** lists the *kinds* of data needed. The agent does not generate raw DQL. The team writes the queries.
- **ICE** scores follow the calibration in `memory/long-term/frameworks.md`. Re-score whenever new evidence shifts Confidence materially.
- Add rows as new hypotheses emerge. Do not delete ruled-out rows — they are part of the audit trail.
