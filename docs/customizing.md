# Customizing Insights Forge for your team

Insights Forge is designed to be **specialized to your team** — it's not really useful straight out of the box. The skills, lenses, and workflow are generic; the files under [`memory/long-term/`](../memory/long-term/) are where *your team* lives. This page walks you through what to customize first, in order of how much value each change unlocks, and closes with the things you should think hard about before changing.

## High impact — do these first

### 1. Stakeholder profiles
Open [`memory/long-term/stakeholder-profiles.md`](../memory/long-term/stakeholder-profiles.md).

Add one profile per leader you produce outputs for. Each profile should capture what they care about, what they ignore, decisions they own, and how they prefer to receive information. The Phase 3 [`exec-onepager`](../skills/exec-onepager/SKILL.md) skill reads the matching profile to shape voice and emphasis.

A profile like *"VP of Engineering"* is generic. A profile like *"VP of Engineering, came up through platform, allergic to vague timelines, owns error-budget policy, reads on mobile during commute"* produces a noticeably sharper one-pager.

Trigger phrase: *"Add [name] to the stakeholder profiles as [role]."*

### 2. Domain knowledge — fill in the slots
Open [`memory/long-term/domain-knowledge.md`](../memory/long-term/domain-knowledge.md).

The vendor-sourced Dynatrace concept definitions are populated. The `[team to note: …]` slots are where **your environment's specifics** belong. Retention policy, DPS quota, custom RUM tagging, named SLOs, anything an agent reading the file would otherwise have to guess. Fill these in as you learn them.

This is the file the agent reads in Phase 0 and Phase 1 to ground signal mapping in your reality, not a generic Dynatrace tenant.

### 3. Terminology
Open [`memory/long-term/terminology.md`](../memory/long-term/terminology.md).

Add acronyms and product names your team uses that aren't already listed. Especially valuable: internal service names, custom dashboards, named SLOs, internal nicknames for shared infrastructure. The agent will refer to them by *your* name, not a generic one — which makes Phase 3 deliverables sound like a colleague wrote them.

## Medium impact

### 4. Dynatrace playbooks
Open [`memory/long-term/dynatrace-playbooks.md`](../memory/long-term/dynatrace-playbooks.md).

Eight playbooks ship out of the box: latency, errors, RUM regression, Grail logs, SLO burn, deploy correlation, third-party dependency, Davis problem. Each is a client-agnostic procedural pattern that gets pulled into Phase 2 action plans.

You can extend them with org-specific procedural patterns the team has converged on, or add new playbooks for problem shapes the eight don't cover (cost / quota investigations and security-event triage are common additions).

Trigger phrase: *"Promote this Phase 2 investigation sequence into a new playbook called `<name>`."*

### 5. Client question bank
Open [`memory/long-term/client-question-bank.md`](../memory/long-term/client-question-bank.md).

If your discovery conversations regularly need question phrasings that aren't in the bank, add them — grouped by the MUST-HAVE / SHOULD-HAVE / NICE-TO-HAVE rubric. The [`context-framing`](../skills/context-framing/SKILL.md) skill uses these phrasings when you're doing live customer discovery.

### 6. The operating manual itself
Open [`CLAUDE.md`](../CLAUDE.md).

The operating principles are sensible defaults, but you may want to adjust:

- The list of stakeholder roles.
- The default vertical or domain.
- The citation-freshness window (default 7 days — see [research.md](research.md)).
- The phased workflow if you've added or removed phases.

## Lower impact — adjust as needed

### 7. Brand spec
Open [`memory/long-term/brand/brand-spec.md`](../memory/long-term/brand/brand-spec.md).

Refresh when the Dynatrace brand template changes. The spec is sourced from the official PowerPoint template — when Brandfolder publishes a new version, mirror the changes here. The supporting notes in [`memory/long-term/brand/reference/`](../memory/long-term/brand/reference/) map each pattern in the spec to a page in the source PDF, which makes refreshes easier.

See [deliverables.md](deliverables.md) for how the brand spec gets used during Phase 3.

### 8. Prior-engagement history (per client)
There is no shared cross-client index to populate. Prior engagements live in each client's own workspace: the agent detects them in Phase 0 by reading that client's `memory/clients/<client-name>/README.md` history table and scanning its `engagements/` folders. The history fills in automatically as `investigation-reset` archives each engagement — nothing to pre-populate. (The old shared `memory/long-term/past-investigations.md` is deprecated; do not use it.)

## The `tools/` boundary

The [`tools/`](../tools/) folder is reserved for future integrations — MCP servers, file output helpers, format converters. Any tool added there **must respect the operating principles** in [`CLAUDE.md`](../CLAUDE.md):

- A tool **may** read from internal docs, design files, or local artifacts.
- A tool **may** render outputs into formats the team uses (PPTX, PDF, Markdown).
- A tool **may** fetch from approved external sources (currently `docs.dynatrace.com` and `community.dynatrace.com`).
- A tool **must not** execute DQL, SQL, or any query language against production telemetry or data warehouses.
- A tool **must not** push configuration, deploy code, or modify production state.

The full rule, including suggested future integrations: [`tools/README.md`](../tools/README.md).

## What you should NOT customize lightly

A few load-bearing design decisions exist for non-obvious reasons. Before changing them, read the linked source carefully.

- **The four-phase workflow.** The phase boundaries and the gate-between-phases pattern are the workspace's load-bearing structure. Adjusting the *contents* of a phase is fine; removing the gate between phases breaks the human-in-the-loop guarantee that the entire workspace is designed around.
- **The memory split.** Auto-promoting per-engagement findings into long-term memory was an explicit *non*-design. The full reasoning is in [memory.md](memory.md). Don't quietly add a script that does this.
- **The external allowlist.** Adding a new domain to [`skills/external-research/SKILL.md`](../skills/external-research/SKILL.md) requires explicit user approval per investigation, not a silent edit. See [research.md](research.md).

## Look inside

| What you'll find | Where to look |
|---|---|
| Every long-term memory file you can edit | [`memory/long-term/`](../memory/long-term/) |
| The operating manual | [`CLAUDE.md`](../CLAUDE.md) |
| All eight phase skills | [`skills/`](../skills/) |
| Six critique lenses + the doc-freshness-checker | [`.claude/agents/`](../.claude/agents/) |
| The tooling boundary | [`tools/README.md`](../tools/README.md) |
