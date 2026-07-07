# Getting started

This page covers three things:

1. What to do before your first session.
2. How to run a complete investigation from "describe the problem" to "deck approved."
3. How to close an engagement cleanly and open the next one.

The single most important thing to internalize before you start: **the agent will not advance to the next phase without your explicit approval.** You're the human-in-the-loop, not a passenger.

## Installation

**Installation = open this folder in Claude Code.**

Open the `insights-forge/` directory in VS Code with the [Claude Code extension](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code) installed. The agent's operating manual ([`CLAUDE.md`](../CLAUDE.md)) loads automatically on every session — you don't do anything to "load" it. The Claude Code extension is the recommended surface because you can watch the agent write artifacts in the file explorer as it works, which makes the four-phase loop easier to follow. Claude Code in a terminal (`claude`) works too.

> **Other surfaces.** Claude.ai as a Project can run a partial version of the workflow but lacks the local filesystem, so phase artifacts won't persist between sessions. Stick with the VS Code extension or terminal for real engagements.

## Memory architecture — understand this first

Before diving into setup, it helps to understand how memory is organized. It has two tiers:

**Root library (`memory/long-term/`)** — universal knowledge: Dynatrace concepts, investigation playbooks, consulting frameworks, brand spec, and generic stakeholder archetypes. This knowledge applies to every client. The agent reads it on every session. **You never put client-specific information here.**

**Client workspaces (`memory/clients/<client-name>/`)** — one isolated folder per client. Contains everything specific to that client: their Dynatrace environment profile, named leader profiles, and all archived investigations. The agent only reads the active client's folder — never another client's. Each workspace has:

```
memory/clients/<client-name>/
├── README.md                    (engagement history + status index)
├── environment.md               (DT environment facts)
├── contract.md                  (commercial & consumption — confidential)
├── stakeholder-overlays.md      (named leaders at this client)
└── engagements/                 (one dated folder per engagement; all phase files live here)
```

**Active investigation — the engagement folder.** The currently open engagement's files live in its dated folder under the client, `memory/clients/<client-name>/engagements/<YYYY-MM-DD-slug>/`. There is no separate "active project" location and no global pointer — the engagement folder is the session's working directory, and a status front-matter block in its `current-context.md` marks it `active`. Because each session works in its own dated folder, running two clients at once never crosses wires.

See [memory.md](memory.md) for the full architecture.

## One-time workspace setup

Before your first real engagement, take 15 minutes to populate the root library with knowledge that applies to every client. These are the files that make the workspace *yours*, not generic.

### 1. Terminology

Open [`memory/long-term/terminology.md`](../memory/long-term/terminology.md) and add acronyms or internal service names your team uses that aren't already there. Internal names matter most — the agent will refer to them by your name, not a generic one.

### 2. Domain knowledge — org-level slots only

Open [`memory/long-term/domain-knowledge.md`](../memory/long-term/domain-knowledge.md) and look for `[team to note: …]` slots. These are for **org-level operational context only** — for example, which DPS capabilities your org's standard contract includes, or internal tool conventions that apply across all clients. 

**Do not put client-specific environment details here.** Those go into each client's `environment.md` (see "Before your first engagement with a new client" below).

### 3. (Optional) Adjust `CLAUDE.md`

[`CLAUDE.md`](../CLAUDE.md) is the operating manual the agent reads on every session. The defaults are sensible. If your team has preferences (different default vertical, different citation-freshness window, additional operating constraints), adjust them here.

You do **not** need to pre-create any engagement files — the agent creates each engagement's dated folder and its files at Phase 0.

## Before your first engagement with a new client

When you start working with a client for the first time, the agent will create their workspace automatically at Phase 0 close. You can also prepare ahead:

1. Copy `memory/clients/_template/` to `memory/clients/<client-name>/`.
2. The agent will populate `environment.md` (via `skills/environment-intake/SKILL.md` at the Phase 0 gate) and `stakeholder-overlays.md` (via `skills/stakeholder-overlay/SKILL.md` when you name a specific leader).

These files persist between engagements with the same client, so you only go through the intake once. On subsequent engagements, the agent reads these files automatically during Phase 0.

## Running an investigation

### Step 1 — Open with the problem

In the Claude Code chat, start with:

> *"Describe the problem you're trying to solve."*

…or just describe the problem and client directly. The agent will read `skills/context-framing/SKILL.md` and begin Phase 0. At session start it also:
- Reads the four root library files (domain knowledge, playbooks, frameworks, stakeholder archetypes)
- Establishes the active engagement — the one this session creates at Phase 0, or one you resume (the agent scans engagement folders' status front-matter to offer resumable ones)
- Reads that client's `environment.md` and `stakeholder-overlays.md` (if they exist)
- Conditionally dispatches the doc-freshness-checker background sub-agent (only if the last check was ≥ 7 days ago)

**Or start from the intake form.** Open `html/intake-form.html` in a browser, fill in what you know (required fields unlock generation; optional depth upgrades the output tier), and paste the generated brief as your first message. The agent skips every question the brief already answers and probes only the gaps — one follow-up per thin answer, never a wall.

### Step 2 — Answer Phase 0 clarifying questions

The agent walks you through up to nine clarifying questions, one at a time, in adaptive order. If your opening paragraph already covers Q1 and Q2, it skips them.

| Q | What it asks |
|---|---|
| Q1 | Customer and what they do |
| Q2 | Customer vertical |
| Q3 | Engagement framing: **C**ontext, **S**pecific information, **I**ntent, **R**esponse format (four-part sub-sequence) |
| Q4 | Tenant type (SaaS or Managed) |
| Q5 | Active Dynatrace capabilities (checklist) |
| Q6 | RUM status on the application in question |
| Q7 | Who will consume the deliverable and what they care about |
| Q8 | What the technical team cares about day-to-day |
| Q9 | Trigger for this engagement (QBR, renewal, expansion, other) |

If you name a specific leader in Q7 and no overlay exists for them, the agent will flag it: `skills/stakeholder-overlay/SKILL.md` should run at the gate to capture their profile in the client's workspace.

### Step 3 — Phase 0 gate

The agent presents a reframed engagement summary and writes it to `current-context.md` inside the new engagement folder (`memory/clients/<client>/engagements/<dated-slug>/`). At this gate you have three options:

- **Approve** — proceed to Phase 1.
- **Redirect** — change scope, framing, or priority. The agent updates and re-presents.
- **Iterate through a lens** — ask for a re-review through MECE, Optimist, ICE, Consultative, Customer, or Skeptic. The agent revises before re-presenting.

The agent will not advance until you explicitly approve. See [workflow.md](workflow.md) for the full ritual.

### Step 4 — Continue through Phases 1, 2, 3

Each phase has its own gate and its own set of artifacts. Don't skip phases — the gate exists to let you redirect before downstream work bakes in a bad assumption. [workflow.md](workflow.md) has the full details. [skills.md](skills.md) indexes every procedural skill.

## Finishing an engagement

When Phase 3 deliverables are approved, use the investigation-reset skill to close out:

> *"Archive this investigation and reset the workspace."*

The agent will:
1. Ask you four lessons-learned questions (what worked, what to avoid, new knowledge, proposed memory updates).
2. Write `lessons-learned.md` into the engagement folder.
3. Update the client's `README.md` engagement history with an outcome row.
4. Execute any approved updates to the root library (e.g., a new playbook insight you identified).
5. Mark the engagement `state: complete` in its `current-context.md`.

Nothing moves — the engagement folder stays at `memory/clients/<client-name>/engagements/<dated-slug>/`. The next session starts fresh, and the client's environment profile, contract, stakeholder overlays, and every past engagement remain in `memory/clients/<client-name>/` for the next engagement with the same client.

## Working with multiple clients

If you need to set aside one client and work on another:

> *"Pause this engagement and start a new one."*

The agent marks the current engagement `state: paused` in its `current-context.md` — nothing moves, and any number of engagements can be paused at once. When you come back:

> *"Resume [client name]."*

The agent scans engagement folders for paused/active status, you pick the one to resume, it flips that engagement back to `state: active`, and reminds you where you left off. Client data never crosses client boundaries — each client's workspace is read only when that client is active.

## Checking where you are

Open the active engagement's `current-context.md` (under `memory/clients/<client>/engagements/<dated-slug>/`) to see its status front-matter (`state`, `phase`), the current phase, and open questions. If anything looks stale or wrong, ask the agent to reframe — that's a Phase 0 redirect.

## Look inside

| The agent reads… | At this file |
|---|---|
| Operating manual | [`CLAUDE.md`](../CLAUDE.md) |
| Phase 0 procedure | [`skills/context-framing/SKILL.md`](../skills/context-framing/SKILL.md) |
| Active / resumable engagements | scan `memory/clients/*/engagements/*/current-context.md` for `state` |
| Client environment (if populated) | `memory/clients/<client-name>/environment.md` |
| Client stakeholder overlays | `memory/clients/<client-name>/stakeholder-overlays.md` |
| Live investigation state | the active engagement folder, `memory/clients/<client>/engagements/<dated-slug>/` |
