# Current Context — Hannah's Bread Company

**Phase:** 0 — Context Framing
**Date:** 2026-05-28
**Consultant role:** Business Insights Analyst

---

## Customer

**Name:** Hannah's Bread Company
**Business:** One of the world's largest producers and marketers of high-quality fresh bread, bagels, and pastries. Operations in the U.S. and Canada. 700+ total users across 30 facilities.
**Size:** 700+ application users / 30 facilities (U.S. and Canada)

---

## Vertical

**Food Manufacturing / Logistics & Supply Chain**

Relevant KPI vocabulary for this vertical: availability/uptime, order fulfillment rates, distribution throughput, conversion (direct-to-consumer e-commerce), customer experience consistency, national expansion readiness.

---

## Engagement Framing (C.S.I.R.)

### C — Context
New logo. Customer is excited about Dynatrace and eager to get started. Currently running DataDog (with Synthetic and RUM equivalents active) and also using QM; migrating away from DataDog. Consultant is a Business Insights Analyst. Relationship is at the start — no prior Dynatrace engagement history.

### S — Specific Information
- **Mission-critical applications:**
  - **breadSHIP** — equipment and product tracking; distribution management from Hannah's bakeries to U.S. distribution centers
  - **breadSAIL** — yard management system; container tracking, dispatching, and port management at yard and terminal facilities
- **New mobile app** — recently launched for direct customer ordering; adoption is growing rapidly
- **Cross-channel challenge** — delivering consistent service levels across the mobile app and the website is increasingly difficult as adoption grows
- **IT monitoring need** — accurate monitoring of both application performance and server performance across 30 facilities
- **Current state** — Greenfield Dynatrace (nothing implemented); DataDog active with Synthetics and RUM equivalents; migrating off DataDog ASAP
- **Scale** — 700+ users, 30 facilities, U.S. and Canada

### I — Intent
Hannah's needs to monitor cross-channel performance (web + mobile) and map it to relevant business metrics. Consistency across devices, browsers, and geographies is essential given mobile app growth. Consultant's goal: make the migration as smooth and fast as possible and accelerate time to value. Customer's expected outcome: a Dynatrace environment that gives them better visibility than DataDog, especially for cross-channel UX and business metric linkage. Note: "fast migration" must be bounded with specific milestones (e.g., "RUM visibility within 30 days; full APM coverage within 90 days") before being stated to leadership — an open-ended "fast" promise against a greenfield, 30-facility implementation sets undefendable expectations.

### R — Response Format
- **Slide deck** — for the broader Hannah's leadership team
- **One-pager** — for the Executive leadership sponsors (CTO, VP of IT, VP of Operations)
- Tone: executive-ready, business-outcome-first; no raw technical detail at the leadership level

---

## Tenant Type

**SaaS**

---

## Active Capabilities

**Greenfield — no Dynatrace capabilities active yet.** Hannah's is a new customer. Nothing is implemented.

Current DataDog capabilities (in use, being migrated away from):
- Synthetic monitoring equivalent
- Real User Monitoring equivalent (web; mobile status in DataDog unknown)

Target Dynatrace capability set to design toward (derived from engagement intent):
- Full-Stack Monitoring (OneAgent) — for breadSHIP, breadSAIL, and server performance
- Real User Monitoring — Web
- Real User Monitoring — Mobile
- Synthetic Monitoring (geographically distributed)
- Davis AI (problem detection)
- Grail (data lakehouse)
- Log Management (Grail)
- Business Analytics / Business Events — for conversion and UX KPI mapping
- Dashboards & Notebooks — red/green availability views for the technical team

---

## RUM Status

**Not yet active in Dynatrace.** DataDog RUM equivalent is in use (web; mobile scope uncertain in DataDog). This is a **MUST-HAVE capability** to implement given the engagement's UX and cross-channel focus. Both Web RUM and Mobile RUM are required to deliver the cross-channel consistency story.

---

## Consulting Objective

Position Dynatrace as the superior cross-channel observability platform for Hannah's — a new SaaS customer migrating from DataDog — by designing a monitoring architecture that covers Web RUM, Mobile RUM, Synthetic Monitoring, Full-Stack APM for breadSHIP and breadSAIL, and business metric mapping. Deliver a leadership deck and an executive one-pager that demonstrate measurable, near-term time-to-value for a CTO, VP of IT, and VP of Operations audience focused on availability, national expansion readiness, and conversion growth.

---

## Leadership Priorities (Named KPIs)

- **Availability** — uptime and reliability of applications and infrastructure across 30 facilities
- **National Expansion** — operational and monitoring readiness to support geographic growth
- **Customer Experience KPIs** — cross-channel consistency across devices, browsers, and geographies; mobile app performance
- **Increased Conversions** — direct-to-consumer e-commerce conversion rate tied to app and web performance

---

## Technical Team Priorities

- **Ease of use** — top priority; the team wants a platform they can operate without deep configuration overhead
- **Red/green availability dashboards** — simple, visual status at a glance
- **Fast alerting (MTTD)** — mean time to detect must be low; want to know about problems before customers do
- **Extremely change-averse** — implementation and configuration changes must be minimized and sequenced carefully; do not disrupt what is working in DataDog while migration is underway

---

## Engagement Trigger

**Contract signing.** Timing pressure is immediate — moving off DataDog creates urgency to accelerate time to value in Dynatrace. Every week without Dynatrace coverage is a week running blind (or running dual-stack DataDog + Dynatrace, which adds operational overhead).

---

## Orientation Hypotheses

Pre-scoring candidates — not findings. These will be formally scored in Phase 1. Confidence levels are provisional pending DataDog baseline data.

1. **Davis AI automatic baselining is expected to compress MTTD vs DataDog's manual threshold configuration.** Davis learns normal behavior without requiring engineers to set alert thresholds. *Acceptance criteria to define in Phase 1: target MTTD category (e.g., application errors, host saturation) and the DataDog baseline MTTD to compare against. Do not present as a proven advantage until pilot data exists.*

2. **Unified Web + Mobile RUM may surface cross-channel session continuity gaps that DataDog's siloed views obscured.** Dynatrace's single-platform RUM model enables device/browser/geo comparisons across channels in ways a separate-tool setup may not. *Must validate against DataDog RUM configuration before asserting gaps to leadership — gaps are expected, not confirmed.*

3. **Geographically distributed Synthetic monitoring will provide proactive availability coverage** for the website and mobile app API layer — the red/green signal the technical team wants and a readiness indicator for national expansion. *Requires expansion plan input (facilities count, timeline, geographies) from VP of Operations before Synthetic coverage can be positioned as expansion-ready.*

4. **Business Events mapped to order completions and conversions will establish the tech → business KPI linkage leadership needs.** *Conditional: requires validation that conversion events are already instrumented in the application layer. If not, application code changes are required — a potential blocker for the change-averse team.*

5. **Full-Stack OneAgent on breadSHIP and breadSAIL will deliver unified application + server performance visibility in a single pane.** *High-risk dependency: instrumentation-readiness of both applications (runtime, OS, deployment model, access rights) is unknown. Phased rollout starting in a non-production environment is recommended before any leadership commitment.*

---

## Capability Gaps

All gaps are greenfield — nothing is yet implemented in Dynatrace:

- **No RUM** — Web RUM and Mobile RUM not yet active; cross-channel UX story is unavailable until implemented
- **No Synthetic monitoring** — no proactive availability monitoring in Dynatrace yet; DataDog synthetics are the only safety net during migration
- **No Full-Stack instrumentation** — breadSHIP and breadSAIL not yet monitored; instrumentation-readiness unknown
- **No Business Events** — no conversion or order-completion events tracked in Dynatrace; depends on existing app-layer event instrumentation
- **No SLOs defined** — no formal availability or performance contracts in Dynatrace
- **No Davis AI tuning** — baseline anomaly detection not yet configured; no DataDog MTTD baseline to compare against
- **No red/green dashboards** — technical team's primary operational view does not yet exist in Dynatrace
- **No mobile conversion baseline** — if the mobile app is too new to have stable conversion data, "increased conversions" as a leadership KPI is premature; reframe as "establish conversion visibility" until a baseline exists

Migration risks:
- **Dual-stack metric inconsistency** — DataDog and Dynatrace will report different numbers for the same signals during the overlap; define which system is authoritative per metric per migration phase before the deck is drafted
- **Change-averse team → OneAgent installation blocker** — Full-Stack instrumentation on production breadSHIP/breadSAIL is the foundational dependency for hypotheses 1 and 5; a phased rollout (non-production first) must be designed before this is committed to in leadership materials
- **DataDog contract end-date unknown** — if there is a hard contract termination date, migration sequencing is dictated by that deadline, not by ideal architecture order

---

## Stakeholder Role Archetypes

**Primary audience (one-pager):** Executive Sponsor × 3
- **CTO** → Executive Sponsor archetype. Cares about technology strategy, risk, ROI, and what happens if nothing is done.
- **VP of IT** → Executive Sponsor archetype (IT operations lens). Cares about infrastructure stability, team capacity, and monitoring tool ROI.
- **VP of Operations** → Executive Sponsor archetype (operational continuity lens). Cares about uptime, distribution reliability, and readiness for national expansion.

**Secondary audience (deck):** Broader leadership team — blend of Executive Sponsor and IT Operations Manager archetypes. Apply Executive Sponsor tone as the baseline; keep technical depth light.

No named-leader overlays exist yet. Flag: run `skills/stakeholder-overlay/SKILL.md` after the Phase 0 gate if specific leaders are named for the deck or one-pager.

---

## Open Questions (Skeptic lens — raised 2026-05-28)

The following questions must be answered before Phase 1 architecture hypotheses can be committed to leadership materials. Prioritized by severity.

**High priority — potential Phase 1 blockers:**
- What is the DataDog contract end date and any renewal window? Migration sequencing depends on this more than capability gaps do.
- Who is Hannah's customer-side technical DRI (infra lead, platform engineer, or DevOps contact)? Without this, all architecture decisions are unvalidated.
- What are the runtime environments, deployment models, and host OS for breadSHIP and breadSAIL? OneAgent suitability cannot be assumed.
- Does Hannah's have DataDog dashboard exports, alert history, and synthetic check configurations available? Comparative claims (Davis AI MTTD, cross-channel gaps) require a DataDog baseline to be defensible.
- What is the DataDog current MTTD for the failure categories the team cares about most?

**Medium priority — needed before Phase 3 deliverables:**
- What is the mobile ordering app's current conversion rate (or is the app too new to have a stable baseline)? "Increased conversions" as a KPI cannot be stated without a denominator.
- What are the planned new facilities, timelines, and geographies for national expansion? Synthetic "expansion readiness" requires this data.
- What is the mobile app's platform (iOS/Android/both) and release cadence? Mobile RUM instrumentation timeline depends on it.
- Are conversion/order-completion events currently instrumented in the application layer (web or mobile)? Business Events mapping assumes this.
- What is the network topology at the 30 facilities — direct internet egress or corporate proxy? OneAgent and Synthetic connectivity depend on this.

**Low priority — clarify before any deliverable is finalized:**
- What is "QM"? If it is a digital experience tool (e.g., Quantum Metric), Session Replay scope and licensing need to be confirmed.
- Does "700+ users" refer to Hannah's employees using the operations applications, or to the mobile app's end customers? The number appears in different contexts with different implications.

---

## Prior Engagement Reference

None — first engagement with Hannah's Bread Company.

---

## Scope

**In scope:**
- Dynatrace monitoring architecture design for Hannah's cross-channel observability needs
- Web RUM + Mobile RUM implementation positioning
- Synthetic monitoring for availability and geo coverage
- Full-Stack OneAgent positioning for breadSHIP, breadSAIL, and server performance
- Business metric mapping (availability → conversion → expansion)
- Leadership deck (broader leadership team)
- Executive one-pager (CTO, VP of IT, VP of Operations)

**Out of scope:**
- Live Dynatrace data analysis (not yet available — greenfield)
- DataDog configuration specifics or DataDog-side tuning
- Network/firewall/infrastructure configuration detail
- Raw DQL queries or executable monitoring syntax

---

## Gate Decision

**Approved — 2026-05-28.** User requested Skeptic lens iteration; 16 findings incorporated. Framing approved after revision. Proceeding to Phase 1.
