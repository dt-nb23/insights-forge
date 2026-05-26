# How memory works

The workspace splits memory into two tiers with strict rules about what goes where. This design is the primary mechanism that prevents client context from bleeding across engagements and keeps the agent's institutional knowledge trustworthy over time.

If you remember one thing: the agent reads freely from the root library on every session, and reads only the **active client's** workspace for anything client-specific. It never reads another client's folder.

## The two tiers

### Tier 1 — Root library (`memory/long-term/`)

The root library holds knowledge that is true regardless of which client is active: Dynatrace concepts, investigation playbooks, consulting frameworks, brand spec, and generic role archetypes.

**Rules:**
- The agent reads this on every session.
- Writes require explicit user approval.
- **This tier must never contain client-identifying information, client-specific environment facts, or named individuals from a client.** If it does, that information bleeds into every future engagement.

| File | What it contains |
|---|---|
| [`frameworks.md`](../memory/long-term/frameworks.md) | MECE, ICE, issue-tree-to-hypothesis mapping, exit-criteria definitions. |
| [`domain-knowledge.md`](../memory/long-term/domain-knowledge.md) | Observability concepts, signal patterns, tech → UX → business linkages, Dynatrace concept definitions with citations. The `[team to note: …]` slots are for org-level context only — not client-specific. |
| [`dynatrace-playbooks.md`](../memory/long-term/dynatrace-playbooks.md) | Eight client-agnostic procedural patterns for common Dynatrace problem shapes. |
| [`terminology.md`](../memory/long-term/terminology.md) | Glossary of recurring terms and Dynatrace platform glossary with citations. |
| [`stakeholder-profiles.md`](../memory/long-term/stakeholder-profiles.md) | Eight generic role archetypes and title-type overlays (e.g., "VP of Engineering" as a role type). **No named individuals. No client associations.** Named leaders at specific clients go in that client's `stakeholder-overlays.md`. |
| [`client-question-bank.md`](../memory/long-term/client-question-bank.md) | Client-facing phrasings of the Phase 0 clarifying questions, grouped by rubric tier. |
| [`brand/brand-spec.md`](../memory/long-term/brand/brand-spec.md) | Dynatrace brand specification (colors, typography, layouts, voice, footer) authoritative for Phase 3 deliverables. |
| [`freshness-report.md`](../memory/long-term/freshness-report.md) | Operational — the doc-freshness-checker sub-agent's output. No client data. |

### Tier 2 — Client workspaces (`memory/clients/`)

Each client has a fully isolated folder. The agent reads only the active client's folder for any client-specific context.

```
memory/clients/
├── _template/                   ← Copy this to create a new client workspace
└── <client-name>/
    ├── README.md                 ← Engagement history and status
    ├── environment.md            ← DT environment: MZs, SLOs, monitors, gaps
    ├── stakeholder-overlays.md   ← Named leaders (confidential to this client)
    ├── project-space/            ← Investigation files when paused
    └── past-investigations/      ← Archived investigations for this client only
        └── YYYY-MM-DD-<name>/
```

**How client folders are populated:**
- `environment.md` — via `skills/environment-intake/SKILL.md` at the Phase 0 gate on first engagement.
- `stakeholder-overlays.md` — via `skills/stakeholder-overlay/SKILL.md` when a specific leader is named in Q7.
- `past-investigations/` — populated automatically by `skills/investigation-reset/SKILL.md` at engagement close.

### Active investigation (`memory/project-space/`)

The active client's investigation files live here while the engagement is open. This is the agent's working directory — it reads and writes freely during a session. The file `active-engagement.md` names which client is active.

| File | Phase | What it contains |
|---|---|---|
| `active-engagement.md` | — | Names the active client; maps to `memory/clients/<name>/`. |
| `current-context.md` | 0 | Problem statement, scope, stakeholders, current phase, open questions. |
| `issue-tree.md` | 1 | MECE issue tree under active development. |
| `hypotheses.md` | 1 | Ranked hypothesis table with ICE scores and status. |
| `signals-map.md` | 1 | SLI/SLO → UX outcome → business KPI mapping. |
| `action-plan.md` | 2 | Investigation actions, recommended actions, decision asks, risks. |
| `decisions-log.md` | all | Append-only record of every gate decision. |

Open any of these during a session to see what the agent is working with — they're not hidden, and reading them is often faster than asking the agent to summarize.

## Engagement states

Each client's investigation exists in one of three states:

| State | Where the files are | How to get there |
|---|---|---|
| **Active** | `memory/project-space/` | Start or resume an engagement |
| **Paused** | `memory/clients/<name>/project-space/` | Tell the agent to pause |
| **Completed** | `memory/clients/<name>/past-investigations/<date>/` | Archive via investigation-reset skill |

Use `skills/investigation-reset/SKILL.md` for all state transitions (archive, pause, resume).

## Context isolation rule

At session start, the agent identifies the active client from `active-engagement.md`. For the rest of that session, client-specific reads — environment, stakeholder overlays, past investigations — come **only** from `memory/clients/<active-client-name>/`. The agent never reads another client's folder, even if the user's question mentions another client by name.

This is what prevents investigation context from one client polluting another. It's enforced by both the agent instructions (CLAUDE.md) and the skill procedures (context-framing, stakeholder-overlay, environment-intake all check `active-engagement.md` before reading any client file).

## Why the read/write asymmetry exists

**Root library writes require explicit user approval** because auto-promoting session-specific findings into shared memory creates two failure modes:

1. **One-off context bleeds into future investigations as if it were universal truth.** A quirk specific to one client environment gets memorized as a general rule, and three engagements later the agent is "confidently" applying it to a client that doesn't have it.
2. **The agent slowly accumulates wrong or stale knowledge nobody asked it to remember.** Long-term memory becomes untrusted, and the team starts ignoring it — at which point the whole "durable knowledge" idea collapses.

**Client workspace writes also require explicit approval** (via the overlay and environment-intake skills) for the same reason: the agent should not silently accumulate facts about a client that you haven't confirmed are accurate.

## Triggering a root library write

The agent writes to `memory/long-term/` only when you ask clearly:

- *"Add [name] to `terminology.md` as [definition]."*
- *"Log a lesson learned: when SDK version segmentation is missing in RUM, always flag it as an instrumentation gap in Phase 1."*
- *"Update `dynatrace-playbooks.md` with the investigation sequence we just validated."*
- *"Promote this observation into `domain-knowledge.md`."*

Vague phrases — *"this seems important"*, *"remember this"* — are logged in `decisions-log.md` but not promoted. The agent will ask you to confirm before writing to any root library file.

## Look inside

| What you'll find | Where to look |
|---|---|
| Active client | [`memory/project-space/active-engagement.md`](../memory/project-space/active-engagement.md) |
| Live investigation state | [`memory/project-space/`](../memory/project-space/) |
| Current client's environment | `memory/clients/<client-name>/environment.md` |
| Current client's leader profiles | `memory/clients/<client-name>/stakeholder-overlays.md` |
| Current client's past investigations | `memory/clients/<client-name>/past-investigations/` |
| Root library rules | [`memory/long-term/README.md`](../memory/long-term/README.md) |
| Client workspace structure template | [`memory/clients/_template/`](../memory/clients/_template/) |
