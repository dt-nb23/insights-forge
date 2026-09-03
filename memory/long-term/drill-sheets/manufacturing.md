---
vertical: Manufacturing
status: draft — validate with a practitioner who works this vertical
---

# Manufacturing drill sheet

Ask in this order, in one message, after Phase B. Prune per the capability dependency column and the engagement's exclusions.

| # | Consultant-facing question | Client-facing phrasing | Capability dependency | Phase 1 hook |
|---|---|---|---|---|
| 1 | Where is the boundary between the systems Dynatrace sees (ERP, MES front ends, supplier portals, e-commerce) and the plant-floor systems it does not (SCADA, PLC, OT networks)? Which problems cross that line? | "When a line stops, does the cause usually sit in a system you can see, or one you can't?" | Full-Stack Monitoring / Infrastructure Monitoring; OneAgent coverage | Sets the scope boundary; problems that originate in OT are instrumentation gaps by design, not hypotheses |
| 2 | Which order-to-cash or plan-to-produce transactions does leadership track — order entry, scheduling, shipment confirmation, invoicing — and what does a delay in each cost? | "Which business transaction, if it stalls for a day, shows up in the quarter?" | APM; Business Analytics if present | Transaction latency and failure ↔ order cycle time, on-time delivery, days sales outstanding |
| 3 | When are the planned downtime windows and change freezes, and has an unplanned outage ever landed inside a freeze? | "When are you allowed to change things, and when did a change bite you anyway?" | Deployment / SDLC events; Davis AI | Deploy-correlation playbook; change-window discipline ↔ unplanned downtime |
| 4 | Which supplier, logistics, or EDI integrations carry the risk, and which has produced a stuck order or a duplicate shipment before? | "Which partner connection has caused a mess in the last year?" | APM outbound spans; Log Management for EDI processing | Third-party and log playbooks; integration failure ↔ on-time-in-full and expedite cost |
| 5 | Where does application latency actually cost money on the floor — scan-and-pick systems, label printing, handheld devices, quality checks — and is that experience measured at the device? | "Where do people on the floor wait on a screen, and does anyone measure that wait?" | RUM — Mobile, or synthetic checks on floor apps | Device-side latency ↔ pick rate, line throughput, overtime; typically an instrumentation gap |

**KPI vocabulary to listen for:** OEE, planned vs. unplanned downtime, order cycle time, on-time-in-full, expedite cost, scrap and rework, line throughput.

**Pruning notes:** if no RUM exists on floor applications, Q5 becomes a gap to name rather than a hypothesis to investigate. If deployment events are not ingested, Q3's correlation is anecdotal; record it that way.
