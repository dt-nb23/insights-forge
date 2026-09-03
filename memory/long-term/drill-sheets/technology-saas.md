---
vertical: Technology / SaaS
status: draft — validate with a practitioner who works this vertical
---

# Technology / SaaS drill sheet

Ask in this order, in one message, after Phase B. Prune per the capability dependency column and the engagement's exclusions.

| # | Consultant-facing question | Client-facing phrasing | Capability dependency | Phase 1 hook |
|---|---|---|---|---|
| 1 | What is the tenancy model, which customer segments or named tenants matter most to the business, and can telemetry be segmented by tenant today? | "If your biggest customer had a bad week, would you know it was them before they told you?" | APM with request attributes or tenant tagging; Business Analytics | Tenant-segmented latency and errors ↔ retention of top accounts; noisy-neighbor saturation patterns; a missing tenant dimension is an instrumentation gap |
| 2 | What is the deployment cadence, how are feature flags and canaries used, and what were the root causes of the last three customer-visible regressions? | "How often do you ship, and when a release hurt customers, how long until you knew?" | Deployment / SDLC events; Davis AI | Deploy-correlation playbook; change failure rate and MTTR; step-function regressions |
| 3 | Which steps of the product-led funnel — signup, activation, first value, retention, expansion — are instrumented, and which does the team argue about because nobody can measure it? | "Where do trial users disappear, and can you see the step where it happens?" | RUM — Web; Business Analytics | Funnel-step abandonment ↔ activation and expansion rates; uninstrumented steps become gaps |
| 4 | Which public or partner APIs carry contractual SLAs or error budgets, and which consumers complain first when they degrade? | "Who calls your API in anger when it slows down?" | APM; defined SLOs or Site Reliability Guardian | API error rate and latency ↔ SLA credits, partner churn; SLO-burn playbook |
| 5 | Where does cloud cost pressure collide with performance — right-sizing, autoscaling events, scale-to-zero — and who owns that trade-off? | "Have you ever made the product slower to make it cheaper, on purpose or by accident?" | Infrastructure Monitoring; Kubernetes / cloud metrics | Saturation ↔ latency; cost per tenant as a business KPI; informs the Phase 2 ambition ceiling |

**KPI vocabulary to listen for:** activation rate, DAU/WAU, net revenue retention, change failure rate, MTTR, API error budget, cloud cost per tenant, p95 for the top tenant.

**Pruning notes:** if deployment events are not ingested, Q2's correlation is anecdotal — record it as a candidate gap. Without Business Analytics, Q3's funnel is limited to RUM user actions; say which steps that covers.
