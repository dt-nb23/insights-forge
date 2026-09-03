---
vertical: Financial Services (FSI)
status: draft — validate with a practitioner who works this vertical
---

# Financial Services (FSI) drill sheet

Ask in this order, in one message, after Phase B. Prune per the capability dependency column and the engagement's exclusions. In this vertical, Q1 often produces exclusions — capture them as out-of-scope items before going further.

| # | Consultant-facing question | Client-facing phrasing | Capability dependency | Phase 1 hook |
|---|---|---|---|---|
| 1 | What regulatory or data-handling constraints limit what can be captured — PII masking, Session Replay restrictions, log retention, data residency — and are any of them already configured as exclusions in the tenant? | "Before we look at anything, what are we not allowed to capture or replay about your customers?" | Applies to RUM, Session Replay, Log Management | Defines the exclusion list for the whole engagement; anything captured in violation is a finding, not a signal |
| 2 | Which transactions does leadership actually watch — payments, transfers, trades, onboarding/KYC, loan decisions — and what latency or failure target does each carry? | "If one of your transaction types slowed down or failed for an hour, which one would reach the executive floor first?" | APM / Full-Stack; Site Reliability Guardian or defined SLOs if present | Transaction success rate and latency ↔ straight-through-processing rate, abandoned onboarding, regulatory incident count; SLO-burn playbook |
| 3 | Where do batch, end-of-day, or settlement windows sit, and what has failed or run long inside them in the last quarter? | "What has to finish overnight, and how often does it not?" | Log Management (Grail) for batch evidence; APM for job services | Log investigation playbook; batch overruns ↔ next-day service availability and reporting deadlines |
| 4 | How much friction is in authentication — login success rate, MFA failures, session timeouts — and what does a failed login cost in support volume or abandoned sessions? | "How often do customers give up before they get in, and where do you see that?" | RUM — Web or Mobile; APM for the identity provider calls | Auth latency and error rate ↔ sign-in success and new-customer activation |
| 5 | Which external rails and providers is the business exposed to — card networks, core banking, market data, credit bureaus, identity providers — and which has an incident history? | "Whose outage becomes your outage?" | Synthetic Monitoring; APM outbound spans | Third-party playbook; provider failure ↔ transaction success rate and complaint volume |

**KPI vocabulary to listen for:** transaction success rate, straight-through-processing rate, onboarding completion, false-decline rate, complaint volume, regulatory incidents, error budget on a named SLO.

**Pruning notes:** if Session Replay or PII capture is excluded (typical), drop any Q4 follow-up that would need replay and anchor the UX story on RUM timings and error rates only. If no SLOs exist, Q2's targets become an instrumentation gap candidate for Phase 2.
