# Procedural skills

Each phase deliverable has a corresponding **skill** the agent reads before producing the artifact. Skills are the workspace's procedural memory: they capture the steps, the inputs, the output location, and the common pitfalls for each deliverable.

If you think of [`CLAUDE.md`](../CLAUDE.md) as the agent's *job description*, the skills under [`skills/`](../skills/) are its *standard operating procedures*. The agent reads the relevant `SKILL.md` first, then produces the artifact — never the other way around.

This page is the index. To see exactly what a skill does, click through to its `SKILL.md` — they're short (40–240 lines each), well-structured, and intended to be read by humans as well as agents.

## Phase 0 — Framing the engagement

### [`context-framing`](../skills/context-framing/SKILL.md)
The required first step of every engagement. Walks the consultant through nine clarifying questions (Q3 is the C.S.I.R. sub-sequence — Context, Stakeholders, Intent, Result), surfaces 3–5 orientation hypotheses as starting candidates (not findings), and produces [`current-context.md`](../memory/project-space/current-context.md).

When the consultant signals that discovery is happening *live with the customer*, this skill pulls phrasings from [`memory/long-term/client-question-bank.md`](../memory/long-term/client-question-bank.md) instead of the consultant-facing prompts.

## Phase 1 — Diagnosing the problem

### [`mece-decomposition`](../skills/mece-decomposition/SKILL.md)
Build a MECE issue tree from the framed problem. Mutually exclusive branches, collectively exhaustive coverage, consistent abstraction within a branch. Output: [`issue-tree.md`](../memory/project-space/issue-tree.md).

### [`hypothesis-generation`](../skills/hypothesis-generation/SKILL.md)
Draft testable hypotheses per branch of the issue tree, each one written as a falsifiable statement with a stated exit criterion. Output: [`hypotheses.md`](../memory/project-space/hypotheses.md).

### [`ice-scoring`](../skills/ice-scoring/SKILL.md)
Score each hypothesis with Impact × Confidence / Effort and rank. This is how the workspace decides what to pursue first — and what to deprioritize even when it's tempting.

### [`signal-mapping`](../skills/signal-mapping/SKILL.md)
Map technical signals (SLI/SLO, RUM, APM) through user-visible UX outcomes to business KPIs. The signals map is also where **instrumentation gaps** get surfaced — if a hypothesis can't be validated with the data available, this is where that limitation lives. Output: [`signals-map.md`](../memory/project-space/signals-map.md).

## Phase 2 — Building the action plan

### [`action-plan-builder`](../skills/action-plan-builder/SKILL.md)
Translate ranked hypotheses into a named investigation plan with owners, timeframes, and "confirmed" versus "ruled out" exit criteria. Pulls procedural steps from [`memory/long-term/dynatrace-playbooks.md`](../memory/long-term/dynatrace-playbooks.md) — eight playbooks for the most common Dynatrace investigation shapes.

Output: [`action-plan.md`](../memory/project-space/action-plan.md).

## Phase 3 — Producing exec-ready deliverables

### [`exec-onepager`](../skills/exec-onepager/SKILL.md)
Produce a one-page written summary tailored to a *named* stakeholder. Reads the matching profile in [`stakeholder-profiles.md`](../memory/long-term/stakeholder-profiles.md) and applies brand directives from [`brand-spec.md`](../memory/long-term/brand/brand-spec.md). See [deliverables.md](deliverables.md) for the brand specifics.

### [`pptx-builder`](../skills/pptx-builder/SKILL.md)
Produce a PowerPoint deck. Adapter that delegates to the standard pptx skill when available and applies the brand spec on top. **Only produced after the one-pager is approved** — see [workflow.md](workflow.md) for the rationale.

## Cross-cutting

### [`external-research`](../skills/external-research/SKILL.md)
Used by any other skill when local memory is silent, contradictory, or stale. Defines the allowlist (`docs.dynatrace.com` and `community.dynatrace.com`), the citation requirement, and the freshness policy. See [research.md](research.md) for the full story.

## Look inside

| Where to find them | What's there |
|---|---|
| [`skills/`](../skills/) | The eight skill folders, one per deliverable |
| Each `SKILL.md` file | When-to-use, inputs, procedure, output location, common pitfalls |
| [`memory/long-term/frameworks.md`](../memory/long-term/frameworks.md) | The shared procedural reference skills draw on (MECE, ICE definitions, exit-criteria patterns) |
