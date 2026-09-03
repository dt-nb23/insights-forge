## SLO breach / error-budget burn

### When this applies

A hypothesis depends on the state of an SLO — is the SLO at risk, is the error budget burning fast, is a recent change pushing burn rate up?

### Investigation sequence

1. Identify the SLO that protects the affected user experience or service. Confirm its **threshold** (target), its **evaluation period**, and the SLI it tracks.
2. Read the **error budget** as the difference between current SLO status and SLO threshold. A positive error budget means the SLO is currently compliant; a negative one means it is breached.
3. Pull the **burn rate** over the last hour. Fast-burn alerts in Dynatrace use a **-1h look-back window**; a static threshold of **10–14** is the documented starting point for fast-burn detection.
4. If the burn rate is elevated, correlate the burn window against deploy events, traffic shifts, and any open Davis problem — burn rate by itself is the symptom, not the cause.
5. If the SLO is breached but burn is now flat, the breach is historical — confirm whether the underlying SLI has recovered and the SLO is now compliant going forward.

### What "confirmed" looks like

- Burn rate is sustained above the fast-burn threshold over the look-back window, with an identifiable cause in the same window (deploy, dependency regression, traffic shift).

### What "ruled out" looks like

- Burn rate is within normal bounds across the affected window and the error budget is intact, even if the underlying signal looks visually concerning. The SLO is the contract; absent burn-rate signal, the SLO is not at risk.

### Common dead-ends

- Reading the SLO status snapshot without the burn rate. A compliant SLO with rapidly burning budget will breach tomorrow; treat burn rate as the leading indicator.
- Using a too-short look-back window for slow-burn problems. Slow-burn alerts use a longer look-back than the -1h fast-burn window; pick the window that matches the failure mode.

### Source

- https://docs.dynatrace.com/docs/deliver/service-level-objectives — page last-updated 2026-03-17; retrieved 2026-05-20.

> Note: a prior citation to `https://docs.dynatrace.com/docs/deliver/service-level-objectives/service-level-objective-basics` was removed on 2026-05-20 after the freshness sub-agent reported it as a 404. The parent `service-level-objectives` page above covers the same material.
