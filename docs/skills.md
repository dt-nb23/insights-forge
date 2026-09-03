# Procedural skills

Each phase deliverable has a corresponding **skill** the agent reads before producing the artifact. Skills are the workspace's procedural memory: they capture the steps, the inputs, the output location, and the common pitfalls for each deliverable.

If you think of [`CLAUDE.md`](../CLAUDE.md) as the agent's *job description*, the skills under [`skills/`](../skills/) are its *standard operating procedures*. The agent reads the relevant `SKILL.md` first, then produces the artifact — never the other way around.

This page is the index. To see exactly what a skill does, click through to its `SKILL.md` — they're short (40–240 lines each), well-structured, and intended to be read by humans as well as agents.

## Phase 0 — Framing the engagement

### [`context-framing`](../skills/context-framing/SKILL.md)
The required first step of every engagement. Walks the consultant through nine clarifying questions (Q3 is the C.S.I.R. sub-sequence — Context, Stakeholders, Intent, Result), surfaces 3–5 orientation hypotheses as starting candidates (not findings), and produces the engagement's `current-context.md` (which opens with a status front-matter block that marks the engagement `active`).

When the consultant signals that discovery is happening *live with the customer*, this skill pulls phrasings from [`memory/long-term/client-question-bank.md`](../memory/long-term/client-question-bank.md) instead of the consultant-facing prompts.

## Phase 1 — Diagnosing the problem

### [`mece-decomposition`](../skills/mece-decomposition/SKILL.md)
Build a MECE issue tree from the framed problem. Mutually exclusive branches, collectively exhaustive coverage, consistent abstraction within a branch. Output: the engagement's `issue-tree.md`.

### [`hypothesis-generation`](../skills/hypothesis-generation/SKILL.md)
Draft testable hypotheses per branch of the issue tree, each one written as a falsifiable statement with a stated exit criterion. A hypothesis that depends on telemetry the team doesn't have is marked, on its own row, with Status **"blocked: instrumentation"** — the gap originates here, in `hypotheses.md`. The [Consultative lens](../.claude/agents/consultative-lens.md) then runs a framing pass on the issue-tree and hypotheses wording before hand-off to signal-mapping. Output: the engagement's `hypotheses.md`.

### [`signal-mapping`](../skills/signal-mapping/SKILL.md)
Map technical signals (SLI/SLO, RUM, APM) through user-visible UX outcomes to business KPIs. This step also **scans `hypotheses.md` for the "blocked: instrumentation" rows and consolidates them** into the signals-map "Instrumentation gaps" section, so the gaps land in one place for the action plan to address. Runs after hypotheses, before ICE. Output: the engagement's `signals-map.md`.

### [`ice-scoring`](../skills/ice-scoring/SKILL.md)
Score each hypothesis with Impact × Confidence / Effort and rank — run **last** in Phase 1, after the signals map exists, so Impact can be anchored to a business KPI. Before scoring, ICE consumes the consolidated instrumentation gaps: a hypothesis blocked on an unclosed gap gets higher Effort (the instrumentation work is now in scope), lower Confidence (it can't be confirmed yet), and lower Impact if the KPI link can't be quantified. This is how the workspace decides what to pursue first — and what to deprioritize even when it's tempting.

## Phase 2 — Building the action plan

### [`action-plan-builder`](../skills/action-plan-builder/SKILL.md)
Translate ranked hypotheses into a named investigation plan with owners, timeframes, and "confirmed" versus "ruled out" exit criteria. Pulls procedural steps from [`memory/long-term/dynatrace-playbooks.md`](../memory/long-term/dynatrace-playbooks.md) — eight playbooks for the most common Dynatrace investigation shapes.

The plan is built in a deliberate order: the [MECE lens](../.claude/agents/mece-lens.md) checks the opportunity set is complete, the plan is drafted against it **and the client's real instrumentation** (`environment.md`), the **persona council** ([Skeptic](../.claude/agents/skeptic-lens.md), [Optimist](../.claude/agents/optimist-lens.md), [Customer](../.claude/agents/customer-lens.md), [Consultative](../.claude/agents/consultative-lens.md)) deliberates over **at least three rounds** (independent positions → cross-examination → convergence) and the agent reconciles, and the [ICE lens](../.claude/agents/ice-lens.md) re-ranks **after** the council. See [workflow.md](workflow.md) for why ICE runs last.

Output: the engagement's `action-plan.md`.

## Phase 3 — Producing exec-ready deliverables

### [`exec-onepager`](../skills/exec-onepager/SKILL.md)
Produce a one-page written summary tailored to a *named* stakeholder. Runs in five steps: recipe selection from `layout-system.md`, content draft from the engagement files, brand-humanizer pre-pass (mandatory Step 3 — runs on all structured copy before any HTML is built), HTML build, and brand gate. Reads the matching profile in [`stakeholder-profiles.md`](../memory/long-term/stakeholder-profiles.md) and applies brand directives from [`brand-spec.md`](../memory/long-term/brand/brand-spec.md). See [deliverables.md](deliverables.md) for the brand specifics.

### [`brand-humanizer`](../skills/brand-humanizer/SKILL.md)
Polish Phase 3 copy so it passes two independent bars: it reads like a person wrote it (no em dashes, no hedging, no AI vocabulary, no rule-of-three lists) and it reads like Dynatrace wrote it (sentence case, active voice, correct product names and trademarks, American spelling, serial commas, no disallowed phrasings). In the exec-onepager workflow this runs as mandatory Step 3 on all structured draft copy before the HTML is built. In the pptx-builder workflow it runs as mandatory Step 3 on slide copy before any slides are generated. Can also be run standalone when someone asks to "humanize this," "brand-check this," or "make this sound like Dynatrace."

### [`pptx-builder`](../skills/pptx-builder/SKILL.md)
Produce a PowerPoint deck. The in-repo `tools/pptx-generator.py` is the primary renderer, driven by a JSON spec written to the engagement folder; the external pptx skill is a fallback only when the generator is not runnable, with a markdown outline as last resort. The brand spec is applied throughout, and the deck gets its own Phase 3 gate. **Only produced after the one-pager is approved** — see [workflow.md](workflow.md) for the rationale.

## Cross-cutting

### [`external-research`](../skills/external-research/SKILL.md)
Used by any other skill when local memory is silent, contradictory, or stale. Defines the allowlist (`docs.dynatrace.com` and `community.dynatrace.com`), the citation requirement, and the freshness policy. See [research.md](research.md) for the full story.

## Workspace and client management

### [`investigation-reset`](../skills/investigation-reset/SKILL.md)
Archives the current engagement and resets the workspace for the next one — or pauses it to work on a different client. Runs the four lessons-learned questions before archiving, executes any approved root library promotions, and marks the engagement `complete` in its `current-context.md` — nothing moves; the engagement folder stays in `engagements/`. Also handles pausing (`state: paused`) and resuming a paused engagement.

**Trigger:** "Archive this investigation," "Reset the workspace," "Pause this engagement," or "Resume [client name]."

### [`stakeholder-overlay`](../skills/stakeholder-overlay/SKILL.md)
Captures a specific named leader at a client (e.g., "Sarah Chen, VP of Engineering") as a stakeholder overlay in the active client's workspace at `memory/clients/<client-name>/stakeholder-overlays.md`. Builds on the parent role archetype from the shared root library. Requires explicit user approval before writing.

**Never writes named individuals to `memory/long-term/stakeholder-profiles.md`** — that file contains only generic title-type archetypes.

**Trigger:** Named automatically during Phase 0 Q7 when a specific leader is identified and no overlay exists. Can also be run on demand: "Create a stakeholder profile for [name]."

### [`environment-intake`](../skills/environment-intake/SKILL.md)
Captures client-specific Dynatrace environment details that persist across engagements: Management Zones, defined SLOs, load-bearing synthetic monitors, instrumentation gaps, DPS quota status. Writes to `memory/clients/<client-name>/environment.md`. Run at the Phase 0 gate on first engagement; update when the client's environment changes.

**Trigger:** Flagged automatically by context-framing when no environment file exists for the active client. Can also be run on demand: "Capture their environment setup."

### [`value-highlight`](../skills/value-highlight/SKILL.md)
Produces a backward-looking "Dynatrace value delivered" brief for QBR, renewal, and expansion conversations. Reads prior completed engagements from the active client's `engagements/` folders (and the client's `contract.md` for commercial framing) and synthesizes confirmed findings, resolved hypotheses, and actions taken into a 1–2 page written summary.

**Prerequisite:** At least one completed investigation must be archived for the active client.

**Trigger:** When the engagement trigger (Q9) is a QBR or renewal. Can also be run on demand: "Create a value summary for [client]."

## How skills are triggered

Skills are **not slash commands** — you don't call them directly. The main agent reads the relevant `SKILL.md` file via its `Read` tool immediately before producing the artifact it governs. The trigger is the agent's own operating logic (defined in `CLAUDE.md`) and the phase the engagement is in.

The agent tells you which skill it's reading before it starts — so if you want to know what's about to happen, you can open that `SKILL.md` yourself.

## Look inside

| Where to find them | What's there |
|---|---|
| [`skills/`](../skills/) | Fourteen skill folders |
| Each `SKILL.md` file | When-to-use, inputs, procedure, output location, common pitfalls |
| [`memory/long-term/frameworks.md`](../memory/long-term/frameworks.md) | The shared procedural reference skills draw on (MECE, ICE definitions, exit-criteria patterns) |
