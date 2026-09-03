# External research and citation policy

Dynatrace updates its documentation almost daily. If the workspace cites a doc page and that page changed last week, your Phase 3 one-pager could be defending a behavior that no longer exists. This page explains the three policies the workspace uses to stay honest: **memory-first**, **allowlisted sources only**, and **citation freshness**.

The canonical procedure lives in [`skills/external-research/SKILL.md`](../skills/external-research/SKILL.md). What follows is the friendly tour.

## Policy 1 — Memory first, web second

Before reaching for the web, the agent reads what's already on disk:

- [`memory/long-term/dynatrace-playbooks.md`](../memory/long-term/dynatrace-playbooks.md) — the index for **procedural** questions ("how do I investigate latency in Dynatrace?"). Eight playbook files in [`memory/long-term/playbooks/`](../memory/long-term/playbooks/) cover the most common problem shapes; the agent reads the matched file, which carries its own doc citations. If the playbook answers the question, the agent stops here — no fetch needed.
- [`memory/long-term/domain-knowledge.md`](../memory/long-term/domain-knowledge.md) — for Dynatrace concept definitions and the approved-sources list.
- [`memory/long-term/terminology.md`](../memory/long-term/terminology.md) — for terms the team has already defined.
- The active engagement's `current-context.md` (at `memory/clients/<client>/engagements/<dated-slug>/current-context.md`) — to scope the question to the active investigation.

The agent only fetches externally when local memory is **silent, contradictory, or stale**. This isn't just to save tokens — it's how the workspace stays grounded in the team's own institutional knowledge rather than re-discovering Dynatrace's documentation each session.

## Policy 2 — Allowlisted external sources

External research is **allowlisted**. The agent will fetch from these two domains and no others, ever, without explicit user approval:

| Source | URL root | What it's good for |
|---|---|---|
| Dynatrace product documentation | [`https://docs.dynatrace.com/`](https://docs.dynatrace.com/) | Authoritative reference for features, defaults, configuration, concepts, supported behavior. |
| Dynatrace Community | [`https://community.dynatrace.com/`](https://community.dynatrace.com/) | Practitioner discussions, known issues, workarounds, migration experience. Treat as practitioner reporting, not vendor commitment. |

**Reserved for future integration** (not in use yet — adding them requires user approval and a dedicated tool integration in [`tools/`](../tools/)):

- Internal Slack channels — practitioner discussion, incident retros, oncall handoffs.
- Salesforce — customer tickets, account-specific context, support history.
- Internal wikis.

The agent **never silently expands the allowlist** — and since this round it cannot: the two domains are `WebFetch(domain:…)` allow rules in `.claude/settings.json`, the same two are listed in `tools/fetch-allowlist.txt`, and a PreToolUse hook (`tools/fetch-allowlist-hook.sh`) forces a fetch to any other host into a human prompt. `WebSearch` carries an explicit ask rule. If something you'd like the agent to read isn't on this list, that's a conversation about extending [`skills/external-research/SKILL.md`](../skills/external-research/SKILL.md), the allowlist file, and the settings rule together — not a one-off ask. (What the hook does and does not cover is spelled out in [`tools/README.md`](../tools/README.md).)

## Policy 3 — Citation requirement

Every externally sourced fact lands in the phase artifact with three pieces of information:

1. The **source URL**.
2. The page's own **"Last updated"** date — as published by Dynatrace.
3. The **agent's retrieval date** — when the agent actually fetched the page.

Without all three, the citation is incomplete. This is what makes a Phase 3 deliverable defensible to leadership weeks later: anyone can re-walk the trail and check whether the source has changed since.

## Policy 4 — Freshness

Two rules:

- **Citations older than 7 days are presumed stale** and must be re-validated before reuse in any phase artifact.
- **Every citation is re-validated at the Phase 2 → Phase 3 transition**, regardless of age. Phase 3 is the leadership-facing surface, so it gets a final sweep.

The 7-day threshold is tuned to Dynatrace's actual update cadence. If your team operates in an environment where docs change more slowly, adjust the window in [`skills/external-research/SKILL.md`](../skills/external-research/SKILL.md) (the staleness rule) and the matching dispatch condition in [`skills/context-framing/SKILL.md`](../skills/context-framing/SKILL.md) Step 1 — it does not live in `CLAUDE.md`.

## The doc-freshness-checker

At the start of every engagement (Phase 0), the main agent dispatches a background sub-agent — [`.claude/agents/doc-freshness-checker.md`](../.claude/agents/doc-freshness-checker.md) — that runs in parallel while you're answering the Phase 0 clarifying questions.

Its job, in plain terms:

1. Reads cited URLs from [`memory/long-term/domain-knowledge.md`](../memory/long-term/domain-knowledge.md), all playbook files in [`memory/long-term/playbooks/`](../memory/long-term/playbooks/), and [`memory/long-term/terminology.md`](../memory/long-term/terminology.md).
2. Re-fetches each one via `WebFetch`.
3. Compares stored "Last updated" dates against the current ones.
4. Writes findings to [`memory/long-term/freshness-report.md`](../memory/long-term/freshness-report.md) — and **only** that file.

Crucially, this sub-agent **never edits long-term memory directly**. It surfaces drift; the human decides what to do about it. At the Phase 0 gate, the main agent shows you the report so you can approve memory updates inline with Phase 0 approval.

You can also trigger a manual refresh outside of Phase 0:

> *"Refresh the docs."*

## What this is NOT

Three things the external-research path deliberately does not do:

- **Not a live query path.** The agent never logs in, runs DQL, or submits forms.
- **Not a write path to long-term memory.** Web fetches inform the *current* investigation. Promotion to durable memory still requires explicit user approval — see [memory.md](memory.md).
- **Not an autonomous research agent.** The agent fetches in service of a specific phase artifact, not to "go learn things."

## Look inside

| What you'll find | Where to look |
|---|---|
| The full external-research procedure | [`skills/external-research/SKILL.md`](../skills/external-research/SKILL.md) |
| The doc-freshness-checker sub-agent definition | [`.claude/agents/doc-freshness-checker.md`](../.claude/agents/doc-freshness-checker.md) |
| The latest freshness report (updated each Phase 0) | [`memory/long-term/freshness-report.md`](../memory/long-term/freshness-report.md) |
| Approved external sources list | [`memory/long-term/domain-knowledge.md`](../memory/long-term/domain-knowledge.md) (Authoritative external references section) |
