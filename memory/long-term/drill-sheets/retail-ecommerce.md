---
vertical: Retail / E-commerce
status: draft — validate with a practitioner who works this vertical
---

# Retail / E-commerce drill sheet

Ask in this order, in one message, after Phase B. Prune per the capability dependency column and the engagement's exclusions.

| # | Consultant-facing question | Client-facing phrasing | Capability dependency | Phase 1 hook |
|---|---|---|---|---|
| 1 | Which journey carries the revenue — checkout, search-to-cart, account, returns — and is each step of that funnel instrumented as a user action or business event, or only as backend calls? | "Walk me through the path a customer takes to give you money. Which of those steps can your team see today, step by step?" | RUM (web or mobile); Business Analytics for business events | Funnel-step abandonment ↔ conversion rate; uninstrumented steps become instrumentation gaps, not hypotheses |
| 2 | When is the next peak (promo, holiday, launch), and what broke during the last one — capacity, third-party, or a release? | "What happened to the site during your last big peak, and when is the next one?" | Full-Stack or APM | Saturation and step-function patterns; deploy correlation; sets the urgency window for Phase 2 |
| 3 | What is the web vs. mobile app split of traffic and conversion, and which one converts worse than it should? | "Do customers on the app and on the web have the same experience? Where does one fall behind?" | RUM — Web and/or Mobile | Mobile crash rate ↔ retention; segment-specific regression (browser/OS/route) from the RUM playbook |
| 4 | Which third parties sit on the purchase path — payment, fraud scoring, tax, shipping rates, promotions — and which of them has caused a checkout failure before? | "Who else has to answer before a customer can finish buying, and has any of them let you down?" | Synthetic Monitoring for the third-party lens; APM for outbound spans | Payment SDK / third-party error rate ↔ checkout conversion and revenue at risk; third-party playbook |
| 5 | How is search and catalog performance tracked, and does anyone connect it to search-to-conversion? | "When search is slow or wrong, do you see it in the numbers, or do customers just leave quietly?" | APM; RUM for search route timing | Search latency ↔ search-to-conversion rate and revenue per search |

**KPI vocabulary to listen for:** conversion rate, cart abandonment, average order value, revenue per session, checkout completion, app-store rating, peak-day revenue.

**Pruning notes:** without any RUM, ask Q1 only for backend instrumentation and mark the UX story as unavailable (context-framing Q6 already flagged it). Without Synthetic Monitoring, keep Q4 but expect the answer to be anecdotal — record it as a candidate instrumentation gap.
