---
name: hypothesis-generation
description: Procedure for generating testable hypotheses from a MECE issue tree. Use after the issue tree is approved.
---

# Hypothesis Generation

## When to use

After the issue tree in the active engagement's `issue-tree.md` has been approved by the user. This is the **second deliverable of Phase 1**, after MECE decomposition and immediately before signal mapping (ICE scoring runs last, once signals are mapped).

Use this skill when:

- The MECE tree has been approved and the team needs concrete, testable claims to investigate.
- New evidence emerges that suggests a new hypothesis under an existing branch.
- A redirected scope requires regenerating hypotheses for one or more branches.

## Inputs

**Resolve the engagement path first (before reading any files):**

1. Use the `ENGAGEMENT_PATH` already established for this session. The agent fixes it once — when Phase 0 (`context-framing`) creates the engagement folder, or when a paused/active engagement is resumed — and holds it in working context for the rest of the session. There is **no shared pointer file** to read; nothing depends on a global "active" file a second concurrent session could overwrite.
2. If no engagement is established yet (a fresh session picking up earlier work), resolve it with the resume procedure in `skills/investigation-reset/SKILL.md`: scan `memory/clients/*/engagements/*/current-context.md` for a `state:` of `active` or `paused`, present the matches, and have the user pick one. If none, stop: "No active engagement found. Start a new engagement or resume a paused one."
3. ENGAGEMENT_PATH = the established/selected path (e.g., `memory/clients/acme-corp/engagements/2026-06-18-api-latency/`). CLIENT_NAME = the segment between `memory/clients/` and `/engagements/`.
4. All phase file reads/writes use ENGAGEMENT_PATH as the base — e.g., `<ENGAGEMENT_PATH>/hypotheses.md`.

Then read these files:

- `<ENGAGEMENT_PATH>/issue-tree.md` — for the approved branches.
- `<ENGAGEMENT_PATH>/current-context.md` — for scope, stakeholders, and the **Out-of-scope exclusions**.
- `memory/long-term/domain-knowledge.md` — for the standard signal patterns, tech/UX/business linkages, and the "Authoritative external references" allowlist that seeds the "expected signals" field.
- `memory/long-term/dynatrace-playbooks.md` — hub index (already loaded at session init). For each hypothesis, match it to a problem shape using the index, then **read the specific playbook file** (e.g., `memory/long-term/playbooks/latency-backend.md`). The playbook's investigation sequence seeds the **validation approach** field; its "confirmed" / "ruled out" criteria seed the **exit criteria**. Read only the matched file(s) — do not load all playbooks.
- `memory/long-term/frameworks.md` — for the issue-tree-to-hypothesis mapping guidance and the exit criteria standard.

When a hypothesis depends on the specific behavior of a Dynatrace feature (e.g., RUM session capture rules, OneAgent vs OpenTelemetry attribute differences, Davis problem grouping) and local memory is silent or unclear, consult `skills/external-research/SKILL.md` before fixing the hypothesis text. Cite the source URL and retrieval date in the "expected signals" or "validation approach" field for that row.

**Out-of-scope exclusions are binding.** Do not generate a hypothesis that depends on, requires, or would encourage adopting an out-of-scope capability or topic — even if it is active in the tenant. If a branch's most natural hypothesis is out of scope, record the exclusion on that branch instead of proposing the hypothesis. (Enforces the CLAUDE.md out-of-scope rule for Phase 1.)

## Steps

1. **For each branch in the issue tree, draft 2–4 candidate hypotheses.** Each hypothesis is a specific, testable claim about what is happening inside that branch. Specificity is the bar: "the payment SDK is causing errors" is not a hypothesis; "iOS checkout conversion decline is driven by elevated JS exceptions in the payment SDK after the 4.12 rollout" is.
2. **For each hypothesis, write the four required fields**:
   - **Expected signals** — what the team would see in the telemetry if this hypothesis is true. Be concrete: "p95 latency on cart-service rises step-function-like after deploy", not "latency goes up".
   - **Validation approach** — the comparison or analysis the team would run to confirm or rule out. Specify the time window, the segmentation, the comparison baseline.
   - **Required metrics (not queries)** — the *kinds* of data needed. Examples: "RUM JS error rate segmented by OS and route", "service p95/p99 latency over time", "funnel step conversion by platform". Do **not** generate raw DQL or SQL — that is the team's job.
   - **Status** — initialize as **open**. The team updates this as evidence arrives.
3. **Flag instrumentation gaps explicitly.** If a hypothesis requires telemetry the team does not currently have, set that hypothesis row's **Status** to **"blocked: instrumentation"** inside `<ENGAGEMENT_PATH>/hypotheses.md`, and name the missing telemetry in the row's "expected signals" or "validation approach" field. Do **not** write to `signals-map.md` here — signal mapping (the next deliverable) scans for these statuses and consolidates them into its "Instrumentation gaps" section, and ICE scoring then consumes that gap when scoring the hypothesis.
4. **Verify each hypothesis has falsifiable exit criteria.** A hypothesis that cannot be ruled out by any conceivable observation is not a hypothesis — it is a belief. If you cannot describe a signal pattern that would falsify it, rewrite or discard.
5. **Invoke the Consultative lens** (`.claude/agents/consultative-lens.md`) on the issue tree and the drafted hypotheses, in its Phase 1 framing mode. It checks that the diagnosis is worded in the business and leadership terms the intended reader expects — branches and claims stated as outcomes and decisions, not buried in engineering minutiae — so the framing is right going into the gate rather than patched in downstream. Apply its rewrites to the wording only; it does not change the analytical structure (that is the MECE lens's job) or the scores.
6. **Hand off to signal mapping.** Invoke `skills/signal-mapping/SKILL.md` to map business KPIs and consolidate the "blocked: instrumentation" statuses from step 3 into `signals-map.md`. Signal mapping then hands off to ICE scoring. Do **not** invoke ICE scoring from here — it runs only after signals are mapped, because Impact anchoring depends on the signals map. The full ranked table — with ICE scores and the framing pass applied — is what the agent presents at the Phase 1 gate.

## Output

The agent writes to `<ENGAGEMENT_PATH>/hypotheses.md`. Each new hypothesis becomes a row in the table. Existing rows are not deleted — they are updated when new evidence shifts Confidence or Status.

## Common pitfalls

- **Hypotheses stated as conclusions, not claims.** "The deploy caused the regression" — when stated before evidence arrives — is a belief, not a hypothesis. Rephrase: "A change in the 2026-05-04 cart-service deploy caused the regression. Expected signals: …"
- **Vague "expected signals".** "Errors go up" is not a signal. Specify which errors, on which service, in which window, at what magnitude.
- **Generating queries instead of metric descriptions.** This agent does not write DQL. Describe the data needed; the team writes the query.
- **Skipping the instrumentation-gap check.** A hypothesis that depends on data the team does not have is a planned dead-end unless the gap is named and closed. Flag it explicitly.
- **More than 4 hypotheses per branch.** When you find yourself drafting a fifth hypothesis under one branch, the branch is probably under-decomposed in the tree. Go back and split it.
- **Engineering-voiced hypotheses reaching the gate.** The Consultative framing pass (step 5) catches branches and claims worded for engineers rather than for the leader who will read them. A technically correct hypothesis stated in raw telemetry terms still fails if the reader cannot see the business stake.
