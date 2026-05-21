# Getting started

This is the page to read before your first real session. It walks you through three things:

1. What the workspace expects to be in place before you start.
2. How to run a complete investigation from "describe the problem" to "deck approved."
3. How to leave the workspace clean for the next engagement.

If you've never used a phase-gated agent before, the most important thing to internalize is this: **the agent will not advance to the next phase without your explicit approval**. You're not just a passenger — you're the human-in-the-loop, and the workspace is designed around that.

## Prerequisites

- **Claude Code** open on this repository, with the working directory at the repo root. You'll find the project at [`/Users/nburwick/insights-forge/`](../).
- The agent reads [`CLAUDE.md`](../CLAUDE.md) automatically on every session, so you don't need to do anything to "load" the operating manual. If you want to know exactly what it reads, open that file — it's the agent's job description.
- Optional but recommended: skim [workflow.md](workflow.md) so you know which phase you're in and what the next gate will ask of you.

## One-time setup

Before your first real engagement, take 15 minutes to populate the durable knowledge the agent will consult. These are the files that make the workspace *yours*, not generic.

### 1. Stakeholder profiles
Open [`memory/long-term/stakeholder-profiles.md`](../memory/long-term/stakeholder-profiles.md) and add the leaders you produce outputs for — VPs of Engineering, Reliability, Product. Each profile drives the *voice* of the Phase 3 one-pager and deck, so the more specific the better. A profile that says "Director of Reliability, came up through SRE, allergic to vague timelines, owns the error-budget decision" produces a sharper one-pager than "VP of Engineering."

### 2. Domain knowledge — fill in the slots
Open [`memory/long-term/domain-knowledge.md`](../memory/long-term/domain-knowledge.md) and look for `[team to note: …]` slots. The vendor-sourced Dynatrace concepts are already populated — what's missing is anything *your environment* does differently. Retention policy, custom RUM tagging, named SLOs, DPS quota, anything an agent reading the file would otherwise have to guess.

### 3. Terminology
Open [`memory/long-term/terminology.md`](../memory/long-term/terminology.md) and add acronyms or product names your team uses that aren't already there. Internal service names matter most — the agent will refer to them by your name, not a generic one.

### 4. (Optional) Adjust `CLAUDE.md`
[`CLAUDE.md`](../CLAUDE.md) is the operating manual the agent reads on every session. The defaults are sensible, but if your team has a stronger preference (different stakeholder roles, different default vertical, a citation-freshness window other than 7 days), this is where to set it.

You do **not** need to populate [`memory/project-space/`](../memory/project-space/) — that folder is reset at the start of every investigation. Look inside if you're curious about the templates the agent works from.

## Running your first investigation

### Step 1 — Open with the problem

In the Claude Code chat, start with the canonical opener:

> *"Describe the problem you're trying to solve."*

…or just describe the problem directly. The agent will route to the [`context-framing`](../skills/context-framing/SKILL.md) skill and begin Phase 0. If you want to see exactly what's about to happen, open [`skills/context-framing/SKILL.md`](../skills/context-framing/SKILL.md) — every step is documented there.

### Step 2 — Answer Phase 0 clarifying questions

The agent will walk you through up to nine clarifying questions one at a time. They're adaptive — if your opening paragraph already covers customer and vertical, it'll skip Q1 and Q2 and pick up where the gap is.

The nine, in default order:

- **Q1** — Customer and what they do
- **Q2** — Customer vertical
- **Q3** — Engagement framing, structured as a four-part sub-sequence: **C**ontext, **S**takeholders, **I**ntent, **R**esult
- **Q4–Q9** — Environment, capabilities, instrumentation, prior work

While you're answering Phase 0, a background sub-agent ([`doc-freshness-checker`](../.claude/agents/doc-freshness-checker.md)) silently runs in parallel and checks every cited Dynatrace URL for drift. You'll see its findings at the Phase 0 gate — no need to wait on it.

### Step 3 — Approve the Phase 0 gate

The agent presents a reframed engagement summary in [`memory/project-space/current-context.md`](../memory/project-space/current-context.md). This is the first gate. You have three responses:

- **Approve** — the agent proceeds to Phase 1.
- **Redirect** — you change scope, framing, or priority. The agent updates and re-presents.
- **Iterate through a lens** — ask for a re-review through [MECE](../.claude/agents/mece-lens.md), [Optimist](../.claude/agents/optimist-lens.md), [ICE](../.claude/agents/ice-lens.md), [Consultative](../.claude/agents/consultative-lens.md), [Customer](../.claude/agents/customer-lens.md), or [Skeptic](../.claude/agents/skeptic-lens.md). The agent revises before re-presenting.

The agent **will not** advance until you say so. If you want to see the full ritual for each phase, [workflow.md](workflow.md) has the details.

### Step 4 — Continue through Phase 1, 2, 3

Each phase has its own gate and its own artifact. The shape of each is laid out in [workflow.md](workflow.md), and the procedural skills are indexed in [skills.md](skills.md). Don't skip phases — even when the answer feels obvious, the gate exists to let you redirect before downstream work bakes in a bad assumption.

## Finishing an investigation

When the Phase 3 deliverables are approved and you're ready to start a new engagement, tell the agent:

> *"Archive this investigation as `<short-name>` and reset the workspace."*

Behind the scenes, the agent will:

1. Move the contents of [`memory/project-space/`](../memory/project-space/) to `memory/long-term/past-investigations/YYYY-MM-DD-<short-name>/`.
2. Reset the live files in `memory/project-space/` to their template state.
3. Prepare for a fresh Phase 0.

If anything you learned should live on as durable knowledge — a new playbook insight, a stakeholder you want to remember — tell the agent explicitly. By design, the agent does **not** auto-promote findings to long-term memory; [memory.md](memory.md) explains why and lists the trigger phrases.

## What if I'm not sure which phase I'm in?

Read [`memory/project-space/current-context.md`](../memory/project-space/current-context.md). It always reflects the current phase and open questions. If that file looks stale or contradicts what you remember, just ask the agent to reframe — that's a Phase 0 redirect, and it's a normal thing to do.

## Look inside

| The agent reads… | At this file |
|---|---|
| The operating manual | [`CLAUDE.md`](../CLAUDE.md) |
| Phase 0 procedure | [`skills/context-framing/SKILL.md`](../skills/context-framing/SKILL.md) |
| Phase 0 question phrasings for live discovery | [`memory/long-term/client-question-bank.md`](../memory/long-term/client-question-bank.md) |
| The live investigation state | files under [`memory/project-space/`](../memory/project-space/) |
