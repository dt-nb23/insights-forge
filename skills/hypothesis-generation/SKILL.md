---
name: hypothesis-generation
description: Procedure for generating testable hypotheses from a MECE issue tree. Use after the issue tree is approved.
---

# Hypothesis Generation

## When to use

After the issue tree in the active engagement's `issue-tree.md` has been approved by the user. This is the **second deliverable of Phase 1**, between MECE decomposition and ICE scoring.

Use this skill when:

- The MECE tree has been approved and the team needs concrete, testable claims to investigate.
- New evidence emerges that suggests a new hypothesis under an existing branch.
- A redirected scope requires regenerating hypotheses for one or more branches.

## Inputs

**Resolve the engagement path first (before reading any files):**

1. Read `memory/project-space/active-engagement.md`.
2. Extract the value after `active: `. If `none`, stop: "No active engagement found. Start a new engagement or resume a paused one."
3. ENGAGEMENT_PATH = that value (e.g., `memory/clients/acme-corp/engagements/2026-06-18-api-latency/`)
4. All phase file reads/writes use ENGAGEMENT_PATH as the base — e.g., `<ENGAGEMENT_PATH>/hypotheses.md`.

Then read these files:

- `<ENGAGEMENT_PATH>/issue-tree.md` — for the approved branches.
- `<ENGAGEMENT_PATH>/current-context.md` — for scope and stakeholders.
- `memory/long-term/domain-knowledge.md` — for the standard signal patterns, tech/UX/business linkages, and the "Authoritative external references" allowlist that seeds the "expected signals" field.
- `memory/long-term/dynatrace-playbooks.md` — for client-agnostic investigation patterns. Match each hypothesis to a playbook (latency, error spike, RUM regression, log investigation, SLO burn, deploy correlation, third-party dependency, Davis problem). The playbook's investigation sequence seeds the **validation approach** field; its "confirmed" / "ruled out" criteria seed the **exit criteria**.
- `memory/long-term/frameworks.md` — for the issue-tree-to-hypothesis mapping guidance and the exit criteria standard.

When a hypothesis depends on the specific behavior of a Dynatrace feature (e.g., RUM session capture rules, OneAgent vs OpenTelemetry attribute differences, Davis problem grouping) and local memory is silent or unclear, consult `skills/external-research/SKILL.md` before fixing the hypothesis text. Cite the source URL and retrieval date in the "expected signals" or "validation approach" field for that row.

## Steps

1. **For each branch in the issue tree, draft 2–4 candidate hypotheses.** Each hypothesis is a specific, testable claim about what is happening inside that branch. Specificity is the bar: "the payment SDK is causing errors" is not a hypothesis; "iOS checkout conversion decline is driven by elevated JS exceptions in the payment SDK after the 4.12 rollout" is.
2. **For each hypothesis, write the four required fields**:
   - **Expected signals** — what the team would see in the telemetry if this hypothesis is true. Be concrete: "p95 latency on cart-service rises step-function-like after deploy", not "latency goes up".
   - **Validation approach** — the comparison or analysis the team would run to confirm or rule out. Specify the time window, the segmentation, the comparison baseline.
   - **Required metrics (not queries)** — the *kinds* of data needed. Examples: "RUM JS error rate segmented by OS and route", "service p95/p99 latency over time", "funnel step conversion by platform". Do **not** generate raw DQL or SQL — that is the team's job.
   - **Status** — initialize as **open**. The team updates this as evidence arrives.
3. **Flag instrumentation gaps explicitly.** If a hypothesis requires telemetry the team does not currently have, capture that in `<ENGAGEMENT_PATH>/signals-map.md` under "Instrumentation gaps". The hypothesis stays in the table but is flagged as "blocked: instrumentation".
4. **Verify each hypothesis has falsifiable exit criteria.** A hypothesis that cannot be ruled out by any conceivable observation is not a hypothesis — it is a belief. If you cannot describe a signal pattern that would falsify it, rewrite or discard.
5. **Hand off to ICE scoring.** Invoke `skills/ice-scoring/SKILL.md` to score each new hypothesis. The full table — with ICE scores — is what the agent presents at the Phase 1 gate.

## Output

The agent writes to `<ENGAGEMENT_PATH>/hypotheses.md`. Each new hypothesis becomes a row in the table. Existing rows are not deleted — they are updated when new evidence shifts Confidence or Status.

## Common pitfalls

- **Hypotheses stated as conclusions, not claims.** "The deploy caused the regression" — when stated before evidence arrives — is a belief, not a hypothesis. Rephrase: "A change in the 2026-05-04 cart-service deploy caused the regression. Expected signals: …"
- **Vague "expected signals".** "Errors go up" is not a signal. Specify which errors, on which service, in which window, at what magnitude.
- **Generating queries instead of metric descriptions.** This agent does not write DQL. Describe the data needed; the team writes the query.
- **Skipping the instrumentation-gap check.** A hypothesis that depends on data the team does not have is a planned dead-end unless the gap is named and closed. Flag it explicitly.
- **More than 4 hypotheses per branch.** When you find yourself drafting a fifth hypothesis under one branch, the branch is probably under-decomposed in the tree. Go back and split it.
