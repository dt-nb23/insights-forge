---
name: environment-intake
description: Captures client-specific Dynatrace environment details that persist across engagements — Management Zones, defined SLOs, load-bearing synthetic monitors, instrumentation gaps, DPS quota status. Writes to memory/clients/<client-name>/environment.md in the client's isolated workspace, with explicit user approval. Run at the Phase 0 gate on first engagement with a new client, or when environment facts have changed. Never writes to memory/long-term/.
---

# Environment Intake

## When to use

- First engagement with a client that has no `environment.md` in `memory/clients/<client-name>/`.
- An existing client's environment has changed significantly (new Management Zones, SLOs added, DPS tier change, major instrumentation expansion).
- The consultant explicitly says "update the environment profile" or "capture their environment setup."

**This skill writes to `memory/clients/<client-name>/environment.md` — durable, cross-engagement client memory. Always gate the write with the binary approval pattern; write only on an explicit yes/approve, never on "looks good" or silence.**

## Why this matters

Each engagement's `current-context.md` captures environment facts during Phase 0, but those facts are scoped to that engagement folder. Without a persistent environment profile at the client root, every new engagement with the same client starts from scratch on the same ground-truth questions — wasting the consultant's time and producing generic orientation hypotheses. This file is what makes repeat-client engagements feel informed rather than generic.

## Inputs

**Resolve the engagement path first (before reading any files):**

1. Use the `ENGAGEMENT_PATH` already established for this session. The agent fixes it once — when Phase 0 (`context-framing`) creates the engagement folder, or when a paused/active engagement is resumed — and holds it in working context for the rest of the session. There is **no shared pointer file** to read; nothing depends on a global "active" file a second concurrent session could overwrite.
2. If no engagement is established yet (a fresh session picking up earlier work), resolve it with the resume procedure in `skills/investigation-reset/SKILL.md`: scan `memory/clients/*/engagements/*/current-context.md` for a `state:` of `active` or `paused`, present the matches, and have the user pick one. If none, stop: "No active engagement found. Start a new engagement or resume a paused one."
3. ENGAGEMENT_PATH = the established/selected path (e.g., `memory/clients/acme-corp/engagements/2026-06-18-api-latency/`)
4. CLIENT_NAME = the path segment between `memory/clients/` and `/engagements/`
5. Phase file reads use `<ENGAGEMENT_PATH>/<file>`. Client-root files use `memory/clients/<CLIENT_NAME>/<file>`.

Then read these files:

- `<ENGAGEMENT_PATH>/current-context.md` — for the client name, tenant type, and active capabilities already captured in Phase 0 Q4/Q5.
- `memory/clients/<CLIENT_NAME>/environment.md` — if it exists, read it first. This session may be an update, not a first capture.

## Procedure

### Step 1 — Check for existing file

The CLIENT_NAME was derived in the Inputs step. Check `memory/clients/<CLIENT_NAME>/environment.md`.

- **If found:** Read it to the consultant and ask: "This is what we have on [client]'s environment. Does anything need updating?" Proceed to only the fields that need updating, then jump to Step 3.
- **If not found:** Proceed to Step 2 for a full first-time intake.

### Step 2 — Ask the environment questions

Ask the consultant these questions, one at a time. Pull what's already known from `current-context.md` (tenant type, active capabilities) and skip those.

1. **Management Zones:** "What Management Zones are defined in their environment, and which ones are load-bearing for this engagement? (If none, say so.)"
2. **Key applications:** "Which applications or services are the primary focus — the ones leadership cares about most and that we'll likely anchor the engagement on?"
3. **Defined SLOs:** "Are there any Site Reliability Guardian SLOs or manually defined SLOs configured? If yes, which services or journeys do they cover, and what are the targets?"
4. **Synthetic monitors:** "Are there synthetic monitors running on business-critical paths? Which paths, and are any of them currently failing or degraded?"
5. **RUM coverage depth:** "Beyond whether RUM is on or off — do they have custom user actions instrumented? Are any key business events tracked (e.g., checkout complete, form submit, login)?"
6. **Log management:** "Is Log Management (Grail) active? If so, which services are ingesting logs, and are there any known log parsing gaps or high-volume noise sources?"
7. **Business events / analytics:** "Are Business Events configured? If yes, what are they tracking — revenue events, conversion events, user actions?"
8. **Instrumentation gaps:** "What telemetry is missing that would be valuable — for example, no RUM on a critical flow, no logs from a key service, no custom metrics on a business process?"
9. **DPS quota and headroom:** "Do you know their DPS tier or whether they're approaching a quota limit? This affects what we can recommend adding."
10. **Known issues or tech debt in the environment:** "Are there known configuration problems — noisy alerts, outdated dashboards, untuned Davis AI anomaly detection, stale Management Zones — that affect signal quality?"
11. **Prior Dynatrace rollout history:** "How long has Dynatrace been deployed here, and was it rolled out all at once or incrementally? Any services still not covered by OneAgent?"

Stop when you have enough to meaningfully sharpen orientation hypotheses for this client. Not all eleven questions need answers.

### Step 3 — Draft the environment profile

Write a draft profile in this format:

```markdown
# [Client Name] — Dynatrace Environment Profile

**Last updated:** YYYY-MM-DD
**Tenant type:** SaaS / Managed
**Active capabilities:** [from current-context.md Q5]

## Management Zones
[List of zones and their scope, or "none configured / unknown"]

## Key applications
[List of primary applications and services, with brief description of what they do]

## Defined SLOs
[List of SLOs: service, journey, target, status — or "none configured"]

## Synthetic monitors
[Key synthetic paths, pass/fail status — or "none active / unknown"]

## RUM coverage
[Web / mobile / both; custom user actions: yes/no; business events: list or "none"]

## Log management
[Services with log ingestion; known parsing gaps or noise sources — or "not active"]

## Business events
[What is being tracked — or "not configured"]

## Instrumentation gaps
[Named gaps — services, flows, or metrics not currently covered]

## DPS quota
[Tier, current headroom, or "unknown"]

## Known environment issues
[Noisy alerts, stale config, Davis AI tuning gaps — or "none noted"]

## OneAgent coverage
[Full coverage / incremental rollout status / known uncovered services]
```

Present the draft and gate the write with the binary pattern: **"Proposed addition to `memory/clients/<CLIENT_NAME>/environment.md`: environment profile for [client]. Approve?"** Write **only** on an explicit yes/approve/equivalent — never on "looks good" or silence.

### Step 4 — Write on approval

Only after the consultant approves:

- If `memory/clients/<CLIENT_NAME>/environment.md` does not exist, copy from `memory/clients/_template/environment.md` first.
- Write the profile to `memory/clients/<CLIENT_NAME>/environment.md`.
- Confirm: "Environment profile for [client] saved to their workspace. It will be read automatically at the start of future Phase 0 sessions for this client. It is not visible in other clients' sessions."

## Output

`memory/clients/<CLIENT_NAME>/environment.md` — the environment profile file, approved and written. Isolated to this client's workspace.

## Common pitfalls

- **Writing without approval.** This is durable, cross-engagement client memory. Never write until the consultant answers the binary gate with an explicit "yes," "approve," or equivalent. "Looks good" and silence are **not** approval — re-ask the gate.
- **Re-asking what's already in current-context.md.** Tenant type and active capabilities are already captured in Phase 0 Q4/Q5. Read `current-context.md` before asking anything.
- **Capturing too little.** The value of this file is its specificity. "RUM is active" is unhelpful; "RUM active on web app; custom actions on checkout and account creation; no business events" is what makes Phase 1 hypotheses sharp.
- **Capturing too much.** This is a persistent reference file, not a one-pager. Keep each section to the facts that will matter in Phase 1 hypothesis generation and Phase 2 action planning — what signals are available, what gaps exist, what's known to be noisy.
- **Forgetting to update.** Environment profiles go stale. When a consultant mentions a significant change ("they turned on Grail last month," "they've added 3 new Management Zones"), run this skill to update the file.
