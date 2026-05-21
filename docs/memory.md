# How memory works

The workspace splits memory into two zones with **different read/write rules** — and that split is the single design decision that does the most to keep the agent trustworthy over time. This page walks you through both zones, explains the asymmetry, and shows you how to direct long-term writes when they're warranted.

If you remember one thing: the agent writes freely to live investigation state, but writes to durable knowledge **only when you say so**. The reason matters as much as the rule, so we'll get to the *why* before we get to the *how*.

## Two zones, two sets of rules

### `memory/project-space/` — live investigation
This is the **scratch pad for the current engagement**. The agent reads and writes here every session, and every phase deliverable lands here. When you start a new investigation, the contents are archived and the folder resets to template state.

**Canonical rules:** [`memory/project-space/README.md`](../memory/project-space/README.md).

| File | Phase | What's in it |
|---|---|---|
| [`current-context.md`](../memory/project-space/current-context.md) | 0 | Problem statement, scope, stakeholders, current phase, open questions. |
| [`issue-tree.md`](../memory/project-space/issue-tree.md) | 1 | The MECE issue tree under active development. |
| [`hypotheses.md`](../memory/project-space/hypotheses.md) | 1 | Ranked hypothesis table with ICE scores and status. |
| [`signals-map.md`](../memory/project-space/signals-map.md) | 1 | SLI/SLO → UX outcome → business KPI mapping. |
| [`action-plan.md`](../memory/project-space/action-plan.md) | 2 | Investigation actions, recommended actions, decision asks, risks. |
| [`decisions-log.md`](../memory/project-space/decisions-log.md) | all | Append-only record of every gate decision (approve / redirect / iterate). |

Open any of these during a session if you want to see what the agent is working with — they're not hidden from you, and reading them is often faster than asking the agent to summarize.

### `memory/long-term/` — durable knowledge
This is the **archive and the playbook**. The agent reads freely on every session, but only writes when you explicitly approve. This is what makes the workspace's institutional knowledge worth keeping.

**Canonical rules:** [`memory/long-term/README.md`](../memory/long-term/README.md).

| File | Purpose |
|---|---|
| [`frameworks.md`](../memory/long-term/frameworks.md) | MECE, ICE, issue-tree-to-hypothesis mapping, exit criteria. The procedural reference skills draw on. |
| [`domain-knowledge.md`](../memory/long-term/domain-knowledge.md) | Observability concepts, signal patterns, Dynatrace concept definitions, tech → UX → business linkages. |
| [`dynatrace-playbooks.md`](../memory/long-term/dynatrace-playbooks.md) | Eight client-agnostic procedural patterns for common Dynatrace problem shapes. |
| [`terminology.md`](../memory/long-term/terminology.md) | Glossary of recurring terms and Dynatrace platform glossary with citations. |
| [`stakeholder-profiles.md`](../memory/long-term/stakeholder-profiles.md) | One profile per leader the agent regularly produces outputs for. |
| [`client-question-bank.md`](../memory/long-term/client-question-bank.md) | Client-facing phrasings of the Phase 0 clarifying questions, grouped by rubric tier. |
| [`past-investigations.md`](../memory/long-term/past-investigations.md) | Index of archived investigations and lessons each surfaced. |
| [`freshness-report.md`](../memory/long-term/freshness-report.md) | The background sub-agent's findings on Dynatrace citation drift — see [research.md](research.md). |
| [`brand/brand-spec.md`](../memory/long-term/brand/brand-spec.md) | Dynatrace brand specification, authoritative for Phase 3 — see [deliverables.md](deliverables.md). |

## The archive-on-reset workflow

When an investigation ends and a new one starts, tell the agent:

> *"Archive this investigation as `<short-name>` and reset the workspace."*

Behind the scenes the agent will:

1. Move the contents of [`memory/project-space/`](../memory/project-space/) to `memory/long-term/past-investigations/YYYY-MM-DD-<short-name>/`.
2. Reset the files in `memory/project-space/` back to their template state.
3. Get ready for a fresh Phase 0.

This is also the natural moment to promote a specific lesson into durable memory — *"add this playbook insight to `dynatrace-playbooks.md`"*, *"add the new stakeholder we met to `stakeholder-profiles.md`"*. The next section covers how to phrase those triggers.

## Why the read/write asymmetry exists

Auto-promoting session-specific findings into durable memory sounds like a useful convenience until you live with the failure modes:

1. **One-off context bleeds into future investigations as if it were universal truth.** A quirk specific to one customer environment gets memorized as a general rule, and three engagements later the agent is "confidently" applying it to a customer that doesn't have it.
2. **The agent slowly accumulates wrong or stale knowledge that nobody asked it to remember.** Long-term memory becomes untrusted, and the team starts ignoring it — at which point the whole "durable knowledge" idea collapses.

Requiring explicit user approval keeps long-term memory **curated and trustworthy**. The split between `project-space/` and `long-term/` is the structural enforcement of that policy. If you ever feel the urge to "just have the agent auto-save lessons," reread this section — that path has been deliberately not built.

## Triggering a long-term write

The agent will only write to `memory/long-term/` when you ask it to *clearly*. Some examples of phrasings that work:

- *"Add [name] to the stakeholder profiles as Director of Reliability."*
- *"Log a lesson learned: when SDK version segmentation is missing in RUM, always flag it as an instrumentation gap in Phase 1."*
- *"Update the Dynatrace section of domain knowledge with the note that DPS-based reporting recently changed."*
- *"Promote this Phase 2 investigation sequence into a new playbook called `<name>`."*

Phrases that are *not* clear enough — *"this seems important"*, *"remember this"* — get logged in [`decisions-log.md`](../memory/project-space/decisions-log.md) but **not** promoted. The agent will ask you to confirm before writing. If you want to know exactly when it'll confirm versus auto-log, [`memory/long-term/README.md`](../memory/long-term/README.md) lists the rules.

## Look inside

| What you'll find | Where to look |
|---|---|
| The rules for live investigation memory | [`memory/project-space/README.md`](../memory/project-space/README.md) |
| The rules for durable knowledge | [`memory/long-term/README.md`](../memory/long-term/README.md) |
| All the template files in their reset state | [`memory/project-space/`](../memory/project-space/) |
| The full long-term knowledge base | [`memory/long-term/`](../memory/long-term/) |
| The audit trail for the current investigation | [`memory/project-space/decisions-log.md`](../memory/project-space/decisions-log.md) |
