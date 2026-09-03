---
vertical: Public Sector
status: draft — validate with a practitioner who works this vertical
---

# Public Sector drill sheet

Ask in this order, in one message, after Phase B. Prune per the capability dependency column and the engagement's exclusions.

| # | Consultant-facing question | Client-facing phrasing | Capability dependency | Phase 1 hook |
|---|---|---|---|---|
| 1 | Which citizen- or constituent-facing services carry a statutory deadline or a predictable surge — tax filing, benefits enrollment, permits, registrations — and when is the next one? | "Which service has a date on the calendar when everyone shows up at once, and how did the last one go?" | RUM — Web; Synthetic Monitoring; Full-Stack | Surge saturation ↔ service completion rate and backlog; sets the urgency window |
| 2 | What accessibility, privacy, and records-retention obligations shape what may be captured and how long it may be kept? | "What rules govern what you can record about a citizen's visit, and for how long?" | Applies to RUM, Session Replay, Log Management | Defines the exclusion list; retention limits bound the historical baselines Phase 1 can use |
| 3 | Which legacy or mainframe integrations sit behind the modern front ends, and which has caused a visible outage or a queue in the last year? | "What old system is the new website secretly waiting on?" | APM; Infrastructure Monitoring; OneAgent coverage at the boundary | Backend latency ↔ front-end completion; third-party / legacy dependency playbook; gaps where OneAgent cannot reach |
| 4 | What procurement, budget-cycle, or policy constraints limit which recommendations are actionable this year — a new capability may be out of reach until the next cycle? | "If we found something worth fixing that needed money, when could that money exist?" | None (planning constraint) | Bounds the Phase 2 ambition ceiling and timeframes; feeds decision asks with realistic dates |
| 5 | What published availability commitments or performance reporting obligations exist, and how is compliance evidenced today? | "When someone asks whether the service met its promise last month, what do you show them?" | Defined SLOs; Dashboards & Notebooks | Availability SLO ↔ published commitment; a missing evidence trail is an instrumentation gap |

**KPI vocabulary to listen for:** service completion rate, queue or backlog time, published uptime commitment, cost per transaction, call-center deflection, citizen satisfaction score.

**Pruning notes:** many public-sector tenants are Managed rather than SaaS (Q4 of the closed block) — check capability availability before assuming Grail-native features in the Phase 1 hooks. If Session Replay is excluded, anchor the UX story on RUM timings and synthetic journeys.
