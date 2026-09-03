---
vertical: Healthcare / Life Sciences
status: draft — validate with a practitioner who works this vertical
---

# Healthcare / Life Sciences drill sheet

Ask in this order, in one message, after Phase B. Prune per the capability dependency column and the engagement's exclusions. Like FSI, Q1 usually produces exclusions — record them first.

| # | Consultant-facing question | Client-facing phrasing | Capability dependency | Phase 1 hook |
|---|---|---|---|---|
| 1 | What compliance constraints (HIPAA / PHI, GDPR, regional health-data rules) govern what RUM, Session Replay, and logs may capture, and what is already masked or disabled? | "What patient or member information must never appear in monitoring data, and how do you enforce that today?" | Applies to RUM, Session Replay, Log Management | Defines the exclusion list; an unmasked field found later is a compliance finding |
| 2 | Which patient- or member-facing flows matter most — portal login, scheduling, telehealth, e-prescribing, claims status — and which of them are instrumented end to end? | "Where does a patient touch you digitally, and which of those moments can your team see?" | RUM — Web and/or Mobile | Flow-step failure ↔ appointment completion, portal adoption, call-center volume |
| 3 | Which systems are clinical versus administrative, and who gets paged when each degrades — because the SLO that matters is whichever protects care delivery? | "If two systems are slow at once, which one gets fixed first, and why?" | Davis AI problem detection; defined SLOs or Site Reliability Guardian if present | Sets Impact calibration for ICE; clinical-path SLO burn outranks administrative latency |
| 4 | Which integration surfaces carry the risk — EHR interfaces, HL7 / FHIR, lab, pharmacy, imaging, payer connections — and which has failed in the last two quarters? | "Which connection to another system, if it dropped, would stop someone from getting care or getting paid?" | APM outbound spans; Log Management for interface engines | Third-party and log playbooks; interface error rate ↔ order turnaround and claim cycle time |
| 5 | What availability or reporting commitments carry a regulatory or contractual deadline, and how would the team prove compliance from telemetry today? | "When someone asks you to prove the system was up, what do you hand them?" | Defined SLOs; Dashboards & Notebooks | Availability SLO ↔ contractual penalty exposure; a missing evidence trail is an instrumentation gap |

**KPI vocabulary to listen for:** appointment completion rate, portal adoption, claim turnaround, interface error rate, patient-reported wait time, audit findings.

**Pruning notes:** if PHI rules exclude Session Replay, keep the UX story on RUM timings, error rates, and synthetic journeys. If only administrative systems are in the tenant, drop the clinical half of Q3 and say so at the gate.
