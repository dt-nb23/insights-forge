# Action Plan

The Phase 2 deliverable. Two categories of actions live here: **investigation actions** (what we need to learn) and **recommended actions** (what we should do once we have learned it). Each carries an owner, a timeframe, and explicit exit criteria.

## Investigation actions

What the team will look at to validate or rule out each open hypothesis. Each action names what data source it depends on (RUM, backend telemetry, infrastructure metrics, business events) and what counts as "confirmed" vs "ruled out".

| ID | Hypothesis | What we'll look at | Data source(s) | Who's involved | Exit criteria: confirmed | Exit criteria: ruled out | Target completion |
|---|---|---|---|---|---|---|---|
| A-01 | H-01 (iOS payment SDK errors) | Client JS error rate on iOS payment screen, segmented by SDK version, around rollout date | RUM | Frontend platform team, payment squad | JS error rate on iOS payment screen rose >2× baseline within 24h of SDK 4.12 rollout AND error volume correlates with conversion drop window | Error rate flat or unrelated to rollout window | [YYYY-MM-DD] |
| A-02 | H-02 (cart-service latency regression) | cart-service p95/p99 latency 7d before vs 7d after 2026-05-04 deploy; funnel step conversion in same windows | Dynatrace APM; analytics events | Backend platform team, analytics | p95 latency rose >30% step-function-like at deploy AND cart→payment funnel step conversion dropped concurrently | No latency change OR latency changed without funnel impact | [YYYY-MM-DD] |
| A-03 | H-03 (third-party payment gateway by region) | Payment gateway success rate by region; iOS traffic distribution by region; conversion by region/platform | Payment vendor API; analytics events | Payments team, analytics | Gateway success rate in a region dropped >5pp AND iOS share in that region exceeds 1.5× baseline | Gateway success rate stable across regions OR no platform-region concentration | [YYYY-MM-DD] |

## Recommended actions

What the team should do once investigation results are in. Ranked by impact vs effort. Each carries an owner and a timeframe. The first time these appear, they may be conditional on investigation outcomes — that is intentional.

| ID | Action | Conditional on | Owner | Timeframe | Impact | Effort | Notes |
|---|---|---|---|---|---|---|---|
| R-01 | Roll back payment SDK to 4.11 on iOS while 4.12 is patched | A-01 confirms H-01 | Mobile platform lead | Within 24h of confirmation | High | Low | Coordinate with payment SDK vendor on patch ETA |
| R-02 | Revert or hotfix the 2026-05-04 cart-service deploy | A-02 confirms H-02 | Cart-service tech lead | Within 48h of confirmation | High | Medium | Identify the specific change set; coordinate with on-call |
| R-03 | Add SDK version segmentation to RUM as a permanent capability | (always — closes instrumentation gap) | Frontend platform team | Next sprint | Medium | Low | Surfaced in `signals-map.md` as a recurring gap |
| R-04 | [...] | [...] | [...] | [...] | [...] | [...] | [...] |

## Decision asks for leadership

What the team needs leadership to decide before recommended actions can proceed. These are the items the agent surfaces in the Phase 3 one-pager.

- **Ask 1**: [Specific decision needed, who needs to make it, and what changes once they decide. Example: "Approval to roll back iOS SDK to 4.11 in production within 24h of H-01 confirmation — VP of Engineering owns this decision."]
- **Ask 2**: [...]
- **Ask 3**: [...]

## Risks and tradeoffs

Each recommended action has a cost. The Consultative lens insists these be named in the same paragraph as the recommendation. Skeptic lens findings are summarized here.

| Risk | Severity | Mitigation |
|---|---|---|
| [Rolling back the payment SDK reintroduces a known checkout bug fixed in 4.12] | [Medium] | [Apply targeted patch for the 4.12 regression rather than full rollback if vendor can ship in <72h] |
| [Reverting the cart-service deploy may also revert unrelated bug fixes shipped in the same change set] | [Medium] | [Cherry-pick the suspected change rather than full revert; coordinate with cart-service tech lead] |
| [Instrumentation work (R-03) competes with frontend platform Q2 roadmap commitments] | [Low] | [Frame as one-week investment that pays for itself in faster diagnosis next time] |
| [...] | [...] | [...] |
