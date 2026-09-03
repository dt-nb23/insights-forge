---
vertical: Telco / Media
status: draft — validate with a practitioner who works this vertical
---

# Telco / Media drill sheet

Ask in this order, in one message, after Phase B. Prune per the capability dependency column and the engagement's exclusions.

| # | Consultant-facing question | Client-facing phrasing | Capability dependency | Phase 1 hook |
|---|---|---|---|---|
| 1 | Which customer-facing flows carry revenue or churn risk — activation, provisioning, billing and payment, plan changes, the self-service app — and which are instrumented as user journeys rather than only as backend services? | "Where do customers sign up, pay, or change something, and which of those journeys can your team watch end to end?" | RUM — Web and/or Mobile; Business Analytics if present | Journey-step failure ↔ activation rate, self-service containment, churn |
| 2 | For streaming or content delivery: what quality-of-experience signals exist (start time, rebuffer ratio, bitrate drops), and which CDN or origin dependencies sit behind them? | "When playback stutters, can you tell whether it was you, your CDN, or the customer's connection?" | RUM (player instrumentation); Synthetic Monitoring; APM for origin services | QoE ↔ session length and churn; CDN cache hit rate ↔ regional consistency; third-party playbook |
| 3 | What are the peak events — launches, live broadcasts, billing cycles, promotional windows — and what failed during the last one? | "What was your worst day in the last year, and what caused it?" | Full-Stack / APM; Davis AI | Saturation and step-function patterns; sets the urgency window for Phase 2 |
| 4 | How does order orchestration fail — partial orders, fallout queues, manual rework — and is fallout measured as a rate or discovered by the back office? | "How many orders need a human to finish them, and how do you find out?" | APM; Log Management for orchestration logs; Business Analytics | Order fallout rate ↔ cost to serve and time to activate; log-investigation playbook |
| 5 | Where is the boundary between what Dynatrace sees (applications, BSS/OSS, digital channels) and what the NOC tools see (network elements, RAN, core), and where do incidents get lost between them? | "When something breaks, how long does it take to know whether it's the network or the app?" | Full-Stack Monitoring; OneAgent coverage; Davis AI | Scope boundary; cross-boundary incidents become instrumentation gaps, not hypotheses |

**KPI vocabulary to listen for:** activation success rate and time, order fallout rate, ARPU, churn, self-service containment rate, rebuffer ratio, MTTR by domain.

**Pruning notes:** if the customer is telco-only (no media), drop Q2 and note it. If the self-service app has no mobile RUM, Q1 becomes partially an instrumentation gap.
