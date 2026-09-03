---
vertical: Logistics / Supply Chain
status: draft — validate with a practitioner who works this vertical
---

# Logistics / Supply Chain drill sheet

Ask in this order, in one message, after Phase B. Prune per the capability dependency column and the engagement's exclusions.

| # | Consultant-facing question | Client-facing phrasing | Capability dependency | Phase 1 hook |
|---|---|---|---|---|
| 1 | Which steps of the fulfillment critical path — order intake, allocation, pick, pack, ship, track, deliver — run through instrumented systems, and where does the trail go dark between WMS, TMS, and ERP? | "Follow one order from the moment it arrives to the moment it's delivered. Where can your team see it, and where does it vanish?" | APM / Full-Stack; Log Management for handoffs | Handoff latency and failure ↔ order cycle time and on-time-in-full; the dark stretches are instrumentation gaps by definition |
| 2 | Which carrier and partner integrations — rate shopping, label generation, tracking, customs, marketplace feeds — have failed or degraded in the last two quarters, and how was it noticed? | "Which partner's API has ruined a shipping day, and who noticed first — you or the customer?" | APM outbound spans; Synthetic Monitoring | Third-party playbook; integration error rate ↔ exception rate and expedite cost |
| 3 | What is the experience on warehouse handhelds and driver devices — scanner apps, mobile pick lists, proof-of-delivery — and is it measured at the device or inferred from throughput? | "Do the people holding the scanners wait on the screen, and would you know if they did?" | RUM — Mobile; synthetic checks on device apps | Device-side latency ↔ pick rate and dock-to-stock time; usually an instrumentation gap |
| 4 | When are the peak volume windows — seasonal, promotional, end-of-quarter — and what capacity or integration incident happened during the last one? | "What was the worst day on the dock last year, and what caused the backlog?" | Full-Stack / Infrastructure Monitoring; Davis AI | Saturation and queue-depth patterns; sets the urgency window for Phase 2 |
| 5 | When a shipment is late or lost, how long does root cause take across WMS, TMS, and ERP, and which of those systems is outside Dynatrace's view? | "When something goes wrong with an order, how many systems does someone open before they find out why?" | Full-Stack; OneAgent coverage; Davis AI | MTTR across systems ↔ exception handling cost; cross-system blind spots become instrumentation gaps |

**KPI vocabulary to listen for:** on-time-in-full, order cycle time, pick rate, exception rate, dock-to-stock time, tracking accuracy, cost per shipment, expedite spend.

**Pruning notes:** if no mobile RUM exists, Q3 is a gap to name rather than a hypothesis to investigate. If TMS or WMS is a SaaS product outside the tenant, Q1 and Q5 anchor on the integration edges only.
