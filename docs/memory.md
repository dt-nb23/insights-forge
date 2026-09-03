# How memory works

The workspace splits memory into two tiers, with the live investigation living **inside** the client tier. This design is the primary mechanism that prevents client context from bleeding across engagements and keeps the agent's institutional knowledge trustworthy over time.

If you remember one thing: the agent reads freely from the root library on every session, and reads only the **active client's** workspace for anything client-specific. It never reads another client's folder, with exactly two narrow, named, read-only exceptions: the resume scan of every engagement's `current-context.md` status front-matter, and the Phase 0 cross-client read of `lessons-learned.md` front-matter and hook lines (see the context isolation rule below).

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
| [`dynatrace-playbooks.md`](../memory/long-term/dynatrace-playbooks.md) | Hub index for the eight client-agnostic procedural patterns. The playbook content itself lives in [`playbooks/`](../memory/long-term/playbooks/) — one file per problem shape, read only when a hypothesis matches that shape. |
| [`playbooks/`](../memory/long-term/playbooks/) | The eight individual playbook files (latency, errors, RUM, Grail logs, SLO burn, deploy correlation, third-party, Davis problem), each with its investigation sequence, exit criteria, and doc citations. |
| [`terminology.md`](../memory/long-term/terminology.md) | Glossary of recurring terms and Dynatrace platform glossary with citations. |
| [`stakeholder-profiles.md`](../memory/long-term/stakeholder-profiles.md) | Hub index for the eight generic role archetypes and title-type overlays (e.g., "VP of Engineering" as a role type). Profile content lives in [`profiles/`](../memory/long-term/profiles/) — read only when calibrating for a named stakeholder. **No named individuals. No client associations.** Named leaders at specific clients go in that client's `stakeholder-overlays.md`. |
| [`profiles/`](../memory/long-term/profiles/) | The eight individual archetype files, with title-type overlays co-located in their parent archetype's file. |
| [`client-question-bank.md`](../memory/long-term/client-question-bank.md) | Client-facing phrasings of the Phase 0 clarifying questions, grouped by rubric tier. |
| [`drill-sheets/`](../memory/long-term/drill-sheets/) | Eight per-vertical drill sheets — five fixed-order questions each, with the capability each depends on and the Phase 1 linkage each feeds — that replace the generic "what does the technical team care about?" probe. Shipped as drafts; a practitioner session per vertical validates them. |
| [`brand/brand-spec.md`](../memory/long-term/brand/brand-spec.md) | Dynatrace brand specification (colors, typography, layouts, voice, footer) authoritative for Phase 3 deliverables. |
| [`phased-plan-timeline-framing.md`](../memory/long-term/phased-plan-timeline-framing.md) | The 30/60/90-day phased-plan framing rules used by Phase 3 content assembly (day framing as the presentation layer over week-range estimates, 90 days max end to end). |
| [`freshness-report.md`](../memory/long-term/freshness-report.md) | Operational — the doc-freshness-checker sub-agent's output. No client data. |

> Archives and environments live in the client tier (below). Earlier architectures kept a shared `past-investigations.md` and a `client-environments/` folder in this tier; both have been removed. Session start loads roughly 40% of what it used to: the two hubs replace the full playbook and profile files, and individual files load only when a phase needs them.

### Tier 2 — Client workspaces (`memory/clients/`)

Each client has a fully isolated folder. The agent reads only the active client's folder for any client-specific context.

```
memory/clients/
├── _template/                   ← Copy this to create a new client workspace
└── <client-name>/
    ├── README.md                 ← Engagement history and status index
    ├── environment.md            ← DT environment: MZs, SLOs, monitors, RUM coverage, gaps
    ├── contract.md               ← Commercial & consumption: DPS commit, renewal date, burn (confidential)
    ├── stakeholder-overlays.md   ← Named leaders (confidential to this client)
    └── engagements/              ← One dated subfolder per engagement
        └── YYYY-MM-DD-<slug>/    ← All phase files for that engagement live here
```

**How client folders are populated:**
- `environment.md` — via `skills/environment-intake/SKILL.md` at the Phase 0 gate on first engagement.
- `contract.md` — captured (with explicit approval) when commercial/consumption context surfaces; read by `skills/value-highlight/SKILL.md` for renewal/QBR briefs.
- `stakeholder-overlays.md` — via `skills/stakeholder-overlay/SKILL.md` when a specific leader is named in Q7.
- `engagements/` — each dated engagement folder is created by `skills/context-framing/SKILL.md` at Phase 0.

### The live investigation — the engagement folder

The active client's investigation files live in a **dated engagement folder** under that client: `memory/clients/<client>/engagements/YYYY-MM-DD-<slug>/`. This is the agent's working directory for the session — it reads and writes here freely.

There is **no global pointer file and no shared `project-space/`.** The engagement folder is *self-describing*: its `current-context.md` opens with a YAML status front-matter block —

```yaml
---
client: <client-short-name>
slug: <slug>
state: active        # active | paused | complete
phase: 0             # current phase, 0–3
opened: YYYY-MM-DD
last-touched: YYYY-MM-DD
---
```

The session holds the engagement path it created (at Phase 0) or resumed, and reads/writes only there. A fresh session resumes by scanning `memory/clients/*/engagements/*/current-context.md` for `state: active` or `state: paused` and letting you pick.

| File | Phase | What it contains |
|---|---|---|
| `current-context.md` | 0 | Status front-matter + problem statement, scope, stakeholders, current phase, open questions. |
| `issue-tree.md` | 1 | MECE issue tree under active development. |
| `hypotheses.md` | 1 | Ranked hypothesis table with ICE scores and status. |
| `signals-map.md` | 1 | SLI/SLO → UX outcome → business KPI mapping. |
| `action-plan.md` | 2 | Investigation actions, recommended actions, decision asks, risks, "Tensions resolved". |
| `decisions-log.md` | all | Append-only record of every gate decision. |
| `lessons-learned.md` | archive | Written by `investigation-reset` when the engagement is archived. |
| `one-pager-YYYY-MM-DD.md` | 3 | The exec one-pager's companion markdown, if produced. |
| `<slug>-onepager.html` | 3 | The exec one-pager HTML — the deliverable itself. |
| `deck-spec-YYYY-MM-DD.json`, `deck-YYYY-MM-DD.pptx` | 3 | The deck spec and the generated deck, if produced. |

Open any of these during a session to see what the agent is working with — they're not hidden.

## Why this prevents cross-session contamination

Because each session holds its **own** dated engagement folder and no shared file decides "which engagement is active," two concurrent sessions for two different clients write to different folders and never contend. State changes (pause, complete) flip a field inside each engagement's *own* `current-context.md`, so any number of engagements can be paused at once without disturbing one another. This is the fix for the failure mode of a single shared "active" pointer that two sessions would race on.

## Engagement states

Each engagement exists in one of three states, all recorded **inside the engagement folder** — nothing ever moves:

| State | Where the files are | How it's recorded |
|---|---|---|
| **Active** | `engagements/<dated-slug>/` | `state: active` in `current-context.md`; the session holds its path |
| **Paused** | Same folder — nothing moves | `state: paused` in `current-context.md` |
| **Completed** | Same folder — nothing moves | `state: complete` in `current-context.md` + an outcome row in the client `README.md` |

Use `skills/investigation-reset/SKILL.md` for all state transitions (archive, pause, resume).

## Context isolation rule

At session start, the agent establishes the active engagement (created at Phase 0 or selected on resume) and derives the client name as the segment between `memory/clients/` and `/engagements/`. For the rest of that session, client-specific reads — environment, contract, stakeholder overlays, prior engagements — come **only** from `memory/clients/<active-client-name>/`. The agent never reads another client's folder, even if the user's question mentions another client by name, with exactly **two narrow, named, read-only exceptions**:

1. **Resume scan** — at session start or resume, the agent scans every client's `engagements/*/current-context.md` **status front-matter** to list resumable work. Front-matter only; it never reads engagement bodies outside the client it then works in.
2. **Lessons readback** — at Phase 0, the agent reads other clients' `engagements/*/lessons-learned.md` **front-matter and Cross-engagement hook line** to surface prior lessons by vertical and problem shape (`skills/context-framing/SKILL.md` Step 4). Never the full file body. This is the one deliberate channel for hard-won knowledge to cross clients: the archive interview tags each lessons file (vertical, problem shape, capabilities) and writes a one-sentence hook, and Phase 0 filters on those tags. Without it, four questions of interview would compress into a single sentence in a per-client README that only that client ever sees again.

This is what prevents investigation context from one client polluting another. It's enforced at three levels: the agent instructions (CLAUDE.md), the skill procedures (context-framing, stakeholder-overlay, environment-intake all resolve the engagement path before reading any client file), and **mechanically** by a PreToolUse hook (`tools/client-isolation-hook.sh`).

**How the mechanical enforcement works.** The hook watches the six file tools (Read, Write, Edit, NotebookEdit, Grep, Glob). On the session's first substantive touch of a client folder — any write, or any read other than the two carve-out files above — it locks the session to that client by writing a **session-keyed** marker at `.claude/session-clients/<session_id>`. From then on, file-tool access to a *different* client's folder is blocked with an explanatory message. Because markers are keyed by session id (not a shared pointer file), concurrent sessions for different clients each lock independently and cannot race; a stale marker from an ended session is inert and pruned at session start. The agent has no permission path to edit its own marker (`Write` and `Edit` on that folder are denied in `.claude/settings.json`); switching clients mid-session goes through `skills/investigation-reset/SKILL.md`, which has you approve the marker removal.

**Named residual gaps** (enforced honesty — these are platform boundaries, not oversights): Bash file access other than the allow-listed tool commands is governed by permission prompts, not the hook; a hook that times out fails open by platform design; and subprocesses that open files themselves are out of the hook's reach. The hook is an accident guard for the agent's own file tools, not an adversarial sandbox.

## Why the read/write asymmetry exists

**Root library writes require explicit user approval** because auto-promoting session-specific findings into shared memory creates two failure modes:

1. **One-off context bleeds into future investigations as if it were universal truth.** A quirk specific to one client environment gets memorized as a general rule, and three engagements later the agent is "confidently" applying it to a client that doesn't have it.
2. **The agent slowly accumulates wrong or stale knowledge nobody asked it to remember.** Long-term memory becomes untrusted, and the team starts ignoring it — at which point the whole "durable knowledge" idea collapses.

**Client workspace writes also require explicit approval** (via the overlay and environment-intake skills) for the same reason: the agent should not silently accumulate facts about a client that you haven't confirmed are accurate.

## Triggering a root library write

The agent writes to `memory/long-term/` only when you ask clearly:

- *"Add [name] to `terminology.md` as [definition]."*
- *"Log a lesson learned: when SDK version segmentation is missing in RUM, always flag it as an instrumentation gap in Phase 1."*
- *"Update the `slo-burn` playbook in `memory/long-term/playbooks/` with the investigation sequence we just validated."* (New playbooks get a new file there plus an index row in `dynatrace-playbooks.md`.)
- *"Promote this observation into `domain-knowledge.md`."*

Vague phrases — *"this seems important"*, *"remember this"* — are logged in `decisions-log.md` but not promoted. The agent will ask you to confirm before writing to any root library file.

## Look inside

| What you'll find | Where to look |
|---|---|
| Active / paused engagements | scan `memory/clients/*/engagements/*/current-context.md` for `state` |
| Live investigation state | the active engagement folder, `memory/clients/<client-name>/engagements/<dated-slug>/` |
| Current client's environment | `memory/clients/<client-name>/environment.md` |
| Current client's contract & consumption | `memory/clients/<client-name>/contract.md` |
| Current client's leader profiles | `memory/clients/<client-name>/stakeholder-overlays.md` |
| Root library rules | [`memory/long-term/README.md`](../memory/long-term/README.md) |
| Client workspace structure template | [`memory/clients/_template/`](../memory/clients/_template/) |
