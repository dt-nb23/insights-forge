# Tools

This folder is reserved for **future tool integrations** — MCP servers, file output helpers, deck renderers, format converters, and similar extensions.

## What lives here

Nothing yet. This is a placeholder.

When tools are added, each one should live in its own subfolder with:

- A short `README.md` describing what the tool does, what inputs it expects, and what outputs it produces.
- The tool's configuration or implementation files.
- A clear note on whether the tool is **read-only** (allowed) or **write/execute** (subject to the agent's operating principles).

## Boundary that all future tools must respect

**This agent does not run live queries or execute production changes.** Any tool added to this folder must respect that boundary. Specifically:

- A tool may **read** from internal documentation, design files, or local artifacts. This is fine.
- A tool may **render** outputs into formats the team will use (PPTX, PDF, Markdown). This is fine.
- A tool may **fetch** reference material from approved external sources. This is fine.
- A tool **must not execute DQL, SQL, or any query language against production telemetry or data warehouses** from inside this workspace. Validation against live data is the team's job.
- A tool **must not push configuration, deploy code, or modify production state**. The agent advises; humans execute.

If a future integration is genuinely valuable but would cross this boundary, raise it with the user first. Do not silently expand the agent's scope by adding tools that exceed these limits.

## External reference allowlist

External documentation lookup is governed by [`skills/external-research/SKILL.md`](../skills/external-research/SKILL.md) and the "Authoritative external references" table in [`memory/long-term/domain-knowledge.md`](../memory/long-term/domain-knowledge.md). Today the allowlist is:

- `https://docs.dynatrace.com/` — Dynatrace product documentation (vendor-authoritative).
- `https://community.dynatrace.com/` — Dynatrace community threads (practitioner reporting).

The agent uses `WebFetch` and `WebSearch` against these domains only. Any other domain — and any internal system (Slack, Salesforce, internal wikis) — requires explicit user approval and, where applicable, a dedicated tool integration in this folder before the agent will reach for it.

## Suggested future integrations

Capture ideas here as the workspace matures. Each idea is a candidate, not a commitment.

- **Dynatrace read-only context fetcher** — pulls dashboard summaries or service inventories into project space for reference. Read-only; no query execution.
- **PPTX renderer** — wraps the standard pptx skill, if available, with project-specific styling.
- **Stakeholder profile importer** — bulk-loads stakeholder profiles from a structured source (e.g., a CSV the team maintains).
- **Past-investigation search** — keyword search over the `memory/long-term/past-investigations/` archive to surface relevant prior lessons during Phase 0.
