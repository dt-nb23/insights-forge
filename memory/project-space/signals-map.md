# Signals Map

The chain from technical signals to user-visible outcomes to business KPIs. The agent fills this in during Phase 1 and references it heavily in Phases 2 and 3 to keep deliverables grounded in business impact rather than raw telemetry.

## SLIs / SLOs (technical signals being watched)

| SLI / SLO | Service or surface | Current value | Target | Notes |
|---|---|---|---|---|
| [Service p95 latency] | [cart-service] | [...] | [<300ms] | [Linked to which hypotheses; instrumentation source] |
| [Error rate] | [payment-service] | [...] | [<0.1%] | [...] |
| [Availability] | [checkout flow end-to-end] | [...] | [99.95%] | [...] |
| [...] | [...] | [...] | [...] | [...] |

## UX outcomes (how tech signals translate to what users feel)

| UX outcome | Driven by which SLIs | How users experience it | How we measure it |
|---|---|---|---|
| [Page load speed on payment screen] | [Service p95 latency; CDN TTFB; client render time] | [Visible wait, spinner, or abandonment before page paints] | [RUM page load p75 / p95; perceived performance via INP / LCP] |
| [Checkout completion friction] | [Form error rate; step-level latency; payment SDK errors] | [Repeated attempts, dropped sessions, support tickets] | [Funnel step conversion; session replay; CSAT after checkout] |
| [...] | [...] | [...] | [...] |

## Business KPIs (how UX outcomes translate to business impact)

| Business KPI | UX outcomes that drive it | Current value | Target / baseline | Owner |
|---|---|---|---|---|
| [Checkout conversion rate] | [Page load speed; checkout completion friction] | [...] | [...] | [Head of Growth] |
| [Revenue at risk per percentage-point conversion drop] | [...] | [$ per pp] | [...] | [Finance partner] |
| [Customer churn following failed checkout] | [...] | [...] | [...] | [VP of Product] |
| [...] | [...] | [...] | [...] | [...] |

## Instrumentation gaps

Places where the chain breaks — we cannot currently measure what we would need to validate a hypothesis or confirm an outcome. Each gap is a candidate work item in the action plan.

| Gap | What we'd need to measure | Why it matters now | Estimated cost to close |
|---|---|---|---|
| [No SDK version segmentation in RUM] | [JS error rate by payment SDK version] | [Blocks H-01 validation — cannot attribute errors to a specific SDK version] | [~1 week of frontend platform work] |
| [No region-level breakdown of payment gateway success rate] | [Payment gateway success/error rate by region] | [Blocks H-03 validation — cannot confirm geographic concentration] | [Coordinate with payment vendor for region-tagged events] |
| [...] | [...] | [...] | [...] |
