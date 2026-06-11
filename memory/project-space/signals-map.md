# Signals Map — Hannah's Bread Company

The chain from technical signals to user-visible outcomes to business KPIs. This map is built for a **greenfield Dynatrace deployment** — current values are either unknown or sourced from DataDog. Target values are provisional until SLOs are formally defined with the IT team.

---

## SLIs / SLOs (technical signals to be established in Dynatrace)

| SLI / SLO | Service or surface | Current value | Target | Linked hypotheses | Notes |
|---|---|---|---|---|---|
| Application availability | breadSHIP | Unknown — no SLO defined | TBD (verbal commitment exists) | H6-C, H3-B | Must be derived from DataDog availability history; formal SLO to be defined as part of migration |
| Application availability | breadSAIL | Unknown — no SLO defined | TBD | H6-C, H2-B | Same as breadSHIP — DataDog baseline export needed |
| Application availability | Mobile ordering app | Unknown | TBD | H6-C, H1-A | New app; baseline period may be too short for reliable SLO |
| Service p95/p99 latency | breadSHIP distribution queries | Unknown (stated to be elevated) | TBD | H2-A | No APM instrumentation yet; Dynatrace OneAgent required |
| Service p95/p99 latency | breadSAIL yard-management operations | Unknown | TBD | H2-B | Same — OneAgent required |
| Service error rate | breadSHIP | Unknown | <1% (provisional) | H2-A, H2-C | No APM instrumentation; baseline from DataDog export |
| Service error rate | breadSAIL | Unknown | <1% (provisional) | H2-B, H2-C | Same |
| Host CPU/memory utilization | 30-facility servers (breadSHIP/breadSAIL hosts) | Unknown — no unified host monitoring | <80% sustained | H3-A, H3-B | OneAgent host monitoring not yet deployed |
| Synthetic availability (uptime check) | breadSHIP endpoint | Not configured | 99.9% (provisional) | H5-B | No Dynatrace Synthetic; DataDog synthetic coverage scope unknown |
| Synthetic availability (uptime check) | breadSAIL endpoint | Not configured | 99.9% (provisional) | H5-B | Same |
| Synthetic availability (uptime check) | Mobile ordering app API | Not configured | 99.9% (provisional) | H5-B, H4-B | Mobile API endpoint must be confirmed |
| Synthetic TTFB by geo location | breadSHIP/breadSAIL endpoints from 30 facility locations | Not configured | Baseline to establish | H4-A, H1-B | Needs Synthetic location coverage mapped to facility geography |
| RUM page load / action duration | Mobile ordering app (by device OS, geo, app version) | Unknown — no Dynatrace Mobile RUM | Baseline to establish | H1-A, H1-C, H4-B | Mobile RUM SDK not yet deployed |
| RUM session completion rate | Mobile ordering app funnel (browse → cart → order placed) | Unknown | Baseline to establish | H6-B | Requires Business Events for conversion step capture |
| RUM page load / action duration | Hannah's website (by browser, geo) | Unknown — no Dynatrace Web RUM | Baseline to establish | H1-B, H1-C | Web RUM not yet deployed |
| Davis AI mean time to detect (MTTD) | All monitored services | Unknown — DataDog static thresholds | Target: MTTD < 5 min (provisional) | H5-A, H5-B | Measurable only after Davis AI is live and a 30-day baseline accumulates |
| Business event: order created | breadSHIP | Not instrumented | Baseline to establish | H6-A | Requires application-layer event hook |
| Business event: distribution dispatch triggered | breadSHIP | Not instrumented | Baseline to establish | H6-A | Same |
| Business event: order placed | Mobile ordering app | Not instrumented | Baseline to establish | H6-B | Requires mobile SDK business event configuration |
| SLO error budget burn rate | breadSHIP, breadSAIL, mobile app | Not configured | <10× burn rate (fast-burn threshold per DT docs) | H6-C | SLOs must be defined before burn rate is measurable |

---

## UX outcomes (how technical signals translate to what users feel)

| UX outcome | Driven by which SLIs | How users/operators experience it | How we measure it in Dynatrace |
|---|---|---|---|
| Mobile app ordering slowness or failure | Mobile RUM action duration; mobile app error rate; mobile API synthetic availability | Customer waits for the app to respond during product browse or checkout; order fails silently; customer abandons app and calls in | Mobile RUM session data filtered by device OS, geo, app version; Mobile RUM error inspector |
| Inconsistent experience across web and mobile | Web RUM timing vs. Mobile RUM timing for the same journey step; cross-channel session stitching gap | Customer who uses the website expects the same speed and reliability on the app — they notice when the app is slower or shows a different error behavior | Cross-channel RUM session comparison; user session funnel by channel |
| Geographic performance inconsistency | Synthetic TTFB by location; RUM session timing by geo segment | Facility staff or remote customers experience sluggish or failed application responses that headquarters users do not | Synthetic results by geographic location; RUM sessions filtered by user location/ISP |
| breadSHIP distribution operations delayed | Service p95 latency on distribution queries; error rate; host CPU saturation | Logistics operators wait for distribution queries to return or see error screens during peak dispatch windows; physical shipments are delayed | APM service latency by endpoint; Failure Analysis; host utilization correlation |
| breadSAIL yard-management failures | Service error rate during peak operational windows; exception stack traces | Yard staff cannot process container check-in/out or dispatch; yard operations stall; staff escalate to IT verbally | APM Failure Analysis; Davis problem detection; exception analysis |
| Undetected outage (reactive discovery) | Synthetic availability; Davis AI problem detection; MTTD measurement | IT team learns of an outage from a facility staff phone call or customer complaint — not from an alert | MTTD from alert-to-incident timeline; Synthetic monitor failure history |
| Leadership blind to business impact of technical events | Business event absence; no SLO dashboard | CTO/VP of Operations learns that breadSHIP was down for 2 hours only from a logistics report; cannot correlate to order delays or revenue | Business event dashboards; SLO burn-rate reports; Davis problem with business context |

---

## Business KPIs (how UX outcomes translate to business impact)

| Business KPI | UX outcomes that drive it | Current value | Target / baseline | Owner (archetype) |
|---|---|---|---|---|
| Application availability (uptime %) | Undetected outages; reactive discovery; host health failures | Unknown — must derive from DataDog history | TBD — verbal commitment exists; formal SLO not yet defined | VP of IT → Executive Sponsor |
| Order conversion rate (mobile app) | Mobile app ordering slowness; cross-channel inconsistency; geo performance gaps | Unknown — no current instrumentation connecting performance to orders | Baseline to establish post-RUM deployment | CTO → Executive Sponsor |
| Distribution order fulfillment throughput | breadSHIP distribution operations delayed; breadSAIL yard failures | Unknown — lives in logistics reports, not monitoring tools | TBD — define with VP of Operations | VP of Operations → Executive Sponsor |
| Mean time to detect (MTTD) — operational performance | Undetected outages; reactive discovery | Unknown — no DataDog MTTD baseline captured | Target: MTTD < 5 minutes (provisional; to validate against DataDog alert history) | VP of IT → IT Operations Manager archetype |
| National expansion readiness | Geographic performance inconsistency; facility host coverage gaps; Synthetic geo coverage | No readiness indicator currently exists | New facility go-live gated on: Synthetic coverage confirmed + SLO baseline established + OneAgent deployed | VP of Operations → Executive Sponsor |
| Customer experience quality (NPS/CSAT proxy) | Mobile app ordering slowness; inconsistent cross-channel experience | Unknown | TBD — no current CX metric linked to app performance | CTO → Executive Sponsor |

*Note: All current values are unknown or sourced from DataDog (pending export). Quantitative linkages between performance signals and KPI changes (e.g., "every 100ms of mobile load time corresponds to X% conversion drop") are not available and should not be stated to leadership until a measurement baseline is established.*

---

## Instrumentation gaps

Every item below is a break in the signal → UX → KPI chain. Each gap is a candidate work item in the Phase 2 action plan.

| Gap | What we'd need to measure | Why it matters now | Linked hypotheses | Estimated effort to close |
|---|---|---|---|---|
| No Dynatrace OneAgent on breadSHIP hosts | APM traces, service latency, error rate, host utilization for breadSHIP | Blocks all breadSHIP APM hypotheses; mission-critical application is a black box | H2-A, H2-B, H2-C, H3-A, H3-B | Requires application inventory (runtime, OS, deployment model); likely 2–4 weeks depending on access rights and change-approval process |
| No Dynatrace OneAgent on breadSAIL hosts | APM traces, service latency, error rate for breadSAIL | Same as above for breadSAIL | H2-B, H2-C, H3-A, H3-B | Same as breadSHIP; can be parallelized |
| No Dynatrace Mobile RUM SDK | Mobile session data, action duration, crash rate, conversion funnel by device/geo | Blocks all mobile UX hypotheses; the mobile ordering app is the growth KPI driver with no current Dynatrace visibility | H1-A, H1-C, H4-B, H6-B | Mobile engineering contact required; SDK injection into app build pipeline; 1–3 weeks depending on release cadence |
| No Dynatrace Web RUM | Web session data, page load timing, JS errors, cross-channel baseline | Blocks cross-channel comparison; without web RUM, mobile performance cannot be compared to the web baseline | H1-B, H1-C | Dynatrace RUM JavaScript tag injection; typically 1–3 days for initial setup; configuration tuning adds time |
| No Dynatrace Synthetic monitors | Proactive availability and latency checks on mission-critical endpoints | Primary gap against the technical team's MTTD requirement; reactive-only discovery is the current state | H5-B, H4-A, H1-B | Requires endpoint inventory, SLO targets, and stakeholder alignment; 1–2 weeks to deploy first set of monitors |
| No Business Events on breadSHIP/breadSAIL | Order creation, dispatch trigger, exception events as business-context signals | Without this, technical events cannot be connected to logistics outcomes; leadership KPI chain is broken | H6-A | Application-layer event hooks required; logistics team and application developer coordination; 3–6 weeks |
| No Business Events on mobile ordering app | Order-placed, cart-completed events as RUM business events | Blocks conversion funnel instrumentation; "increased conversions" KPI is unmeasurable | H6-B | Mobile SDK business event configuration; commerce team coordination for join key (session ID ↔ order ID); 3–6 weeks |
| No SLOs defined or configured | Availability SLO, error-budget burn rate, fast-burn alerting | Without SLOs, availability is a verbal commitment with no formal tracking; breach events are invisible | H6-C | SLO target definition with IT/leadership; Dynatrace SLO configuration; 1–2 weeks once targets are agreed |
| No DataDog alert history export | Historical MTTD baseline and false-positive rate for comparison with Davis AI | H5-A validation requires this as the pre-migration baseline; without it, Davis AI improvement claim is anecdotal | H5-A | DataDog admin export; typically hours to produce if access is available |
| No DataDog synthetic inventory | Confirmed list of endpoints currently covered by DataDog synthetic monitoring | Without this, the scope of the coverage gap (H5-B) cannot be precisely quantified | H5-B | DataDog admin review; hours to days |
| No mobile app conversion baseline | Current mobile order conversion rate, by time window | "Increased conversions" is a leadership KPI that cannot be measured or claimed without this baseline | H6-B | Commerce system query or dashboard; requires commerce team; days to produce |
| No facility host inventory | Expected host count per facility for OneAgent coverage validation | Without this, H3-B (coverage gaps) cannot be confirmed — we don't know what to compare the Dynatrace entity map against | H3-B | IT asset register or CMDB query; hours to produce if documentation exists |
| No national expansion plan data | Planned new facilities, timelines, geographies | "National expansion readiness" is a leadership KPI with no concrete target to instrument against | H1-B, H4-A | VP of Operations conversation; qualitative input |
