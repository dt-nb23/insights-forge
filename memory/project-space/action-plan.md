# Action Plan — Hannah's Bread Company

**Phase:** 2 — Solution
**Date:** 2026-05-28
**Context:** Greenfield Dynatrace SaaS deployment migrating from DataDog. All hypotheses are currently blocked on instrumentation. Actions are sequenced in waves; Waves 2 and 3 are deliberately serialized to prevent simultaneous instrumentation tracks on a change-averse team.

---

## Pre-deployment actions (Days 1–5, no Dynatrace deployment required)

These actions unblock every downstream wave and can begin immediately.

| ID | Action | Who's involved | Exit criteria: done | Target |
|---|---|---|---|---|
| IA-01 | Export DataDog alert history (90 days) and complete synthetic test inventory. **Critical path: must be completed before the DataDog contract lapses.** | Hannah's DataDog admin / IT team + consultant | Alert history delivered with timestamps, service name, resolution status, and MTTD per incident; synthetic test inventory lists every monitored endpoint with pass/fail history. | Day 3 |
| IA-02 | Compile facility host inventory from IT asset register or CMDB. Flag if the register is known to be out of date — a stale inventory turns Wave 2 into a rework cycle. | Hannah's IT ops | List delivered: facility name, host count, OS, application role per host. If register is stale, a physical discovery or site-walk should be scoped as a parallel track. | Day 3 |
| IA-03 | SLO target workshop — define availability % and latency thresholds for breadSHIP, breadSAIL, and the mobile ordering app. Requires sign-off from VP of IT, application owners, and VP of Operations — not VP of IT alone. | Consultant + Hannah's VP of IT + application owners + VP of Operations | Written SLO targets agreed for all three applications, with a named review date (e.g., tighten after 30-day baseline). | Day 5 |
| IA-04 | Compile mission-critical endpoint list for Synthetic monitoring. Identify breadSHIP, breadSAIL, mobile app API, and website endpoints, including expected HTTP response codes and acceptable latency thresholds. | Hannah's technical DRI (to be named) + consultant | Signed-off endpoint list with: URL, method, expected response, geo coverage requirement, SLO linkage. |  Day 5 |
| IA-05 | Identify and confirm Hannah's customer-side technical DRI. This person owns: OneAgent production deployment approval, rollback plans for breadSHIP and breadSAIL, and web team coordination for RUM tag injection. **Wave 2 does not start without this name.** | Hannah's IT leadership + consultant | Named DRI confirmed with explicit scope of authority (production deployment approval, rollback plan ownership). | Day 3 |
| IA-06 | Confirm mobile ordering app release cadence, platform (iOS/Android/both), and mobile engineering contact. **Wave 3 start date is TBD until this is confirmed.** | Hannah's CTO or mobile lead + consultant | Mobile engineering contact named; build pipeline access confirmed; release cadence documented (e.g., bi-weekly builds). | Day 5 |

---

## Wave 1 — Foundation monitoring (Weeks 1–3)

Highest-ICE items. Directly delivers the technical team's top priorities: red/green availability dashboards, fast alerting, and formal SLO tracking. Low disruption — no application code changes or host agent installations.

| ID | Action | Addresses | Owner | Timeline | Exit criteria: done | Risk | Mitigation |
|---|---|---|---|---|---|---|---|
| RA-01 | Deploy Dynatrace Synthetic monitors on all endpoints from IA-04, including geo-distributed locations matching key facility clusters. | H5-B, H4-A, H1-B | Consultant + Hannah's IT ops (IA-05 DRI must be named first) | Weeks 1–2 | Synthetic monitors running; alert fires within 5 minutes of a simulated endpoint failure; results visible in availability dashboard. | DataDog and Dynatrace synthetics may overlap during migration — both will fire alerts for the same endpoint. | Coordinate cutover per endpoint: DataDog synthetic muted after Dynatrace equivalent is confirmed green for 48h. |
| RA-02 | Configure SLOs and red/green availability dashboards in Dynatrace using SLO targets from IA-03. | H6-C | Consultant + Hannah's VP of IT | Weeks 1–2 (after IA-03) | SLOs live for breadSHIP, breadSAIL, and mobile app; error-budget burn rate visible on dashboard; technical team confirms dashboard meets their "red/green" requirement. | SLO targets may be set too tight for a first baseline, causing immediate "breach" state that panics the team. | Start at a discoverable, achievable level (e.g., 99.0%); plan a formal SLO review after 30 days of data. |
| RA-03 | Inject Dynatrace Web RUM JavaScript tag on Hannah's website. Requires named web team contact — this is not a self-service task without one. | H1-B, H1-C | Consultant + Hannah's web team contact (to be named in IA-05) | Week 1–2 | RUM sessions appearing in Dynatrace; page load timing, JS errors, and geo segmentation visible; CSP headers confirmed not blocking Dynatrace domains. | Web governance model unknown; CSP or tag manager restrictions may add delay. | Confirm tag deployment process with web team before scheduling — do not assume direct access. |

---

## Wave 2 — Core APM (Weeks 3–8)

Full-Stack OneAgent deployment on breadSHIP and breadSAIL. **Prerequisite: IA-05 (named technical DRI) must be confirmed before Wave 2 begins.** Serialized with Wave 3 — do not run simultaneously to avoid overwhelming a change-averse team.

| ID | Action | Addresses | Owner | Timeline | Exit criteria: done | Risk | Mitigation |
|---|---|---|---|---|---|---|---|
| RA-04 | Deploy OneAgent on breadSHIP hosts — **non-production environment first**, then production with a formal change window. Document rollback procedure before production deployment begins. | H2-A, H2-C, H3-A, H3-B | Hannah's technical DRI (named in IA-05) + consultant | Weeks 3–5: non-production. Weeks 5–8: production rollout. | OneAgent reporting service metrics, host metrics, and distributed traces for breadSHIP in Dynatrace. Non-production pilot runs cleanly for 5 business days before production approval is sought. | Production deployment on a mission-critical distribution system will trigger the change-averse team's highest anxiety. | Non-production pilot data is the proof point that earns production approval; do not ask for production access without pilot evidence. Also: instrument OneAgent in Infrastructure Observability mode first if Full-Stack mode meets resistance — upgrade later. |
| RA-05 | Deploy OneAgent on breadSAIL hosts — same non-production first approach as RA-04. Parallel track, but production approvals are separate change windows. | H2-B, H2-C, H3-A, H3-B | Hannah's technical DRI + consultant | Weeks 3–8 (parallel with RA-04 in non-production; production windows staggered by 1 week) | OneAgent reporting for breadSAIL; non-production pilot clean for 5 days before production request. | Simultaneous production deployments to both mission-critical apps in the same week is high risk for a change-averse team. | Stagger production windows by at least one week; confirm with DRI before scheduling. |
| RA-06 | Validate host coverage across all 30 facilities against IA-02 inventory. Flag any facility with zero or partial OneAgent coverage. | H3-B | Consultant + Hannah's IT ops | Week 8 (after RA-04/05 production deployments) | Host entity count in Dynatrace matches IA-02 inventory; zero facilities with no coverage; any gaps have a named remediation timeline. | IA-02 inventory may be stale — discrepancies between expected and discovered hosts must be resolved before claiming full coverage to leadership. | Compare discovered hosts against the inventory during rollout, not after; flag gaps early rather than at the completion milestone. |

---

## Wave 3 — Mobile and business intelligence (Weeks 9–16)

Begins only after Wave 2 (breadSHIP/breadSAIL OneAgent) is stable in production. This is deliberate — the change-averse team should not be asked to manage three simultaneous instrumentation tracks.

| ID | Action | Addresses | Owner | Timeline | Exit criteria: done | Risk | Mitigation |
|---|---|---|---|---|---|---|---|
| RA-07 | Deploy Dynatrace Mobile RUM SDK into the mobile ordering app. Timeline is TBD until IA-06 (mobile engineering contact and release cadence) is confirmed. | H1-A, H1-C, H4-B | Hannah's mobile engineering team + consultant | Weeks 9–12 (TBD pending IA-06) | Mobile RUM sessions appearing in Dynatrace; action latency, crash rate, and geo segmentation visible; cross-channel comparison with web RUM (RA-03) functional. | Mobile app is new with unknown release cadence — schedule fiction until IA-06 is confirmed. | Do not commit this timeline to leadership until IA-06 is resolved. |
| RA-08 | Configure Business Events for mobile conversion funnel (order-placed, cart-completed) and establish the join key between RUM session ID and commerce order ID. | H6-B | Hannah's mobile engineering + commerce team + consultant | Weeks 11–16 | Business Events firing for every order completion on the mobile app; conversion funnel visible in Dynatrace with drop-off by step; session-to-order join key operational. | Highest coordination effort of any Wave 3 action: requires mobile, commerce, and IT teams simultaneously. | Scope the join key design before committing to the implementation timeline; confirm commerce team availability in advance. |
| RA-09 | Configure Business Events for logistics outcomes on breadSHIP/breadSAIL (order creation, distribution dispatch trigger, exception events). | H6-A | Hannah's application developers (breadSHIP/breadSAIL) + consultant | Weeks 12–18 | Business Events firing for distribution dispatch; order volume and exception rate visible in Dynatrace dashboards; IT can correlate an application incident to a logistics outcome. | Requires application-layer code changes on mission-critical logistics systems — the highest-anxiety action for the change-averse team. | Phase it: start with the lowest-risk event type (e.g., a read-only order status check) before instrumenting dispatch triggers. Named application developer DRI required before scoping begins. |

---

## Wave 4 — Davis AI baseline and MTTD validation (Week 12+)

Begins after OneAgent coverage is sufficient to produce meaningful anomaly detection signal.

| ID | Action | Addresses | Owner | Timeline | Exit criteria: done | Risk | Mitigation |
|---|---|---|---|---|---|---|---|
| RA-10 | Allow Davis AI 30-day baselining period; compare MTTD vs DataDog baseline from IA-01. | H5-A | Consultant + Hannah's IT ops | Weeks 12–16 (30 days after OneAgent production coverage established) | Davis AI MTTD measured for at least 10 real incidents; comparison against IA-01 DataDog baseline shows directional improvement; false-positive rate documented. | Meaningful comparison requires IA-01 DataDog export to be complete and structured — if DataDog access is reduced before IA-01 is done, the before-and-after claim is anecdotal. | IA-01 is the first pre-deployment action precisely because of this risk; escalate if DataDog export is blocked. |

---

## Decision asks for leadership

The following decisions must be made by a named leader before the corresponding wave can proceed. Framed as asks, not updates.

| Ask | Decision needed | Owner | Required before | Blocker if not resolved |
|---|---|---|---|---|
| DA-01 | Approve export of DataDog alert history, synthetic test inventory, and all relevant monitoring data before the DataDog contract lapses. | VP of IT | Day 1 | Without this, the MTTD improvement claim in the business case has no defensible before-and-after comparison. |
| DA-02 | Approve greenlight for the full Dynatrace implementation scope — Synthetic monitors, Web RUM, Mobile RUM, OneAgent on breadSHIP and breadSAIL, Business Events, SLOs. | CTO | Day 5 | Entire implementation is blocked. |
| DA-03 | Name a customer-side technical DRI with production deployment authority for breadSHIP and breadSAIL (including rollback plan sign-off). | VP of IT | Day 3 (before Wave 2) | Wave 2 cannot begin without an accountable internal owner. A production deployment on mission-critical logistics systems with no named internal owner is an unacceptable risk. |
| DA-04 | Approve agreed SLO targets for breadSHIP, breadSAIL, and the mobile ordering app — signed off by VP of IT, application owners, and VP of Operations. | VP of IT + VP of Operations | Day 5 (before Wave 1) | SLO dashboard and error-budget burn alerting cannot be configured without targets. |
| DA-05 | Provide national expansion plan (facility count, timeline, geographies) so Synthetic monitoring geo coverage can be designed to prove expansion readiness from Day 1. | VP of Operations | Day 5 | National expansion readiness is a leadership KPI with no concrete target to instrument without this input. |
| DA-06 | Confirm mobile app release cadence and assign a mobile engineering contact for Mobile RUM SDK injection. **Wave 3 start date is TBD until this is resolved.** | CTO or mobile engineering lead | Day 5 | RA-07 and RA-08 timelines are schedule fiction without this. Do not present a Wave 3 timeline to leadership until this decision is made. |
| DA-07 | Approve OneAgent production deployment on breadSHIP — including change window, rollback procedure, and pilot success criteria. Decision required after non-production pilot runs cleanly for 5 business days. | VP of IT (with named DRI from DA-03) | Week 5 | Wave 2 production rollout is blocked. |
| DA-08 | Approve OneAgent production deployment on breadSAIL — same criteria as DA-07; staggered by at least 1 week from DA-07. | VP of IT (with named DRI from DA-03) | Week 6 | Wave 2 production rollout is blocked. |

---

## Risks and tradeoffs

| Risk | Severity | Mitigation |
|---|---|---|
| **DataDog contract lapses before export is complete (IA-01)** — the MTTD improvement baseline disappears if DataDog access is revoked mid-migration. | High | IA-01 is Day 1 action. Escalate immediately if DataDog admin access is restricted. Export everything — alerts, synthetics, dashboards — not just the MTTD data. |
| **No named technical DRI blocks Wave 2 indefinitely** — without an internally accountable owner, production OneAgent deployment on breadSHIP/breadSAIL cannot proceed. | High | DA-03 is a pre-condition for Wave 2. Surface this explicitly at the leadership kickoff — frame it as a risk to the migration timeline, not a consultant ask. |
| **Simultaneous instrumentation tracks overwhelm the change-averse team** — if Wave 2 (OneAgent) and Wave 3 (Mobile RUM) overlap, the team's instinct will be to stop everything. | High | Waves are serialized: Wave 3 does not start until Wave 2 is stable in production. Non-negotiable. |
| **IT asset register is stale, making coverage validation in RA-06 unreliable** — a gap in the host inventory becomes a gap in the leadership "full coverage" claim. | Medium | Validate IA-02 against discovered hosts during Wave 2 rollout — flag discrepancies immediately, not at the completion milestone. |
| **Mobile app release cadence is incompatible with a 4-week SDK injection timeline** — if the app ships quarterly, Wave 3 could slip 8–12 weeks from current assumptions. | Medium | IA-06 must be resolved by Day 5. If cadence is quarterly, re-plan Wave 3 around the next release window and communicate the slip to leadership immediately. |
| **SLO targets set too tight cause an immediate breach state, eroding trust in Dynatrace** — a red dashboard on Day 1 will be blamed on the new tool, not the existing performance gap. | Medium | Start at 99.0% for all three applications; tighten after a 30-day data baseline. Communicate this explicitly in the SLO workshop (IA-03). |
| **Business Events on breadSHIP/breadSAIL (RA-09) requires code changes to production logistics systems** — the highest-anxiety action for the change-averse team; likely to be delayed or deprioritized. | Medium | Scope RA-09 as a named future wave, not a committed timeline item. Name a specific application developer DRI and an initial event type (lowest-risk) before scheduling. |
| **DataDog and Dynatrace Synthetic monitors firing simultaneously during overlap** — dual alerting causes operational confusion and may cause the team to dismiss Dynatrace alerts as noise. | Low | Coordinate a per-endpoint muting procedure: mute DataDog synthetic for an endpoint only after Dynatrace equivalent is confirmed green for 48 consecutive hours. Document the procedure before Wave 1 begins. |
| **Web RUM tag blocked by CSP or tag manager restrictions (RA-03)** — unknown web governance model could add days to weeks of delay. | Low | Confirm tag deployment process with named web team contact before scheduling. Do not assume direct tag manager access. |
