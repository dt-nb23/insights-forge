# Root Library — Universal Knowledge

This folder is the **root library** — knowledge that applies to every client and every engagement. The agent reads it on every session. It is intentionally kept free of client data.

## The rule: no client data here

**This folder must never contain:**
- Client names, company names, or organization-identifying information
- Named individuals from a client (stakeholder overlays go in `memory/clients/<client-name>/stakeholder-overlays.md`)
- Client-specific Dynatrace environment details (environment profiles go in `memory/clients/<client-name>/environment.md`)
- Investigation artifacts from a specific engagement (these live in `memory/clients/<client-name>/engagements/<dated-slug>/`)

If client data ends up here, it bleeds into every future engagement. That is the failure mode this design prevents.

The `[team to note: …]` slots in `domain-knowledge.md` are for **org-level operational context only** (e.g., which DPS capabilities the org's standard contract includes). They are not for client-specific facts.

## What lives here

| File | What it contains | Read frequency |
|---|---|---|
| `domain-knowledge.md` | Observability concepts, signal patterns, tech → UX → business linkages, Dynatrace concept definitions with citations. | Every session (session initialization) |
| `dynatrace-playbooks.md` | Eight client-agnostic investigation patterns for common Dynatrace problem shapes. | Every session (session initialization) |
| `frameworks.md` | MECE, ICE, issue-tree-to-hypothesis mapping, exit-criteria definitions. | Every session (session initialization) |
| `stakeholder-profiles.md` | Eight generic role archetypes and title-type overlays (e.g., "VP of Engineering" as a role type). **No named individuals.** | Every session (session initialization) |
| `terminology.md` | Glossary of recurring terms and Dynatrace platform glossary with citations. | On demand |
| `client-question-bank.md` | Client-facing phrasings of Phase 0 questions, by rubric tier. | Phase 0 (when doing live discovery with the customer) |
| `brand/brand-spec.md` | Dynatrace brand specification (colors, typography, layouts, voice, footer) for Phase 3 deliverables. | Phase 3 |
| `freshness-report.md` | Operational — the doc-freshness-checker sub-agent's citation drift findings. Overwritten each run. | Phase 0 gate |

## Rules

- The agent **reads** from this folder freely. Every file here is fair game as context.
- The agent **writes** here only on explicit user instruction.
- `freshness-report.md` is the only file the agent writes to automatically (the doc-freshness-checker sub-agent updates it; it contains no client data).

## Valid write triggers (root library only)

- *"Add [term] to `terminology.md` as [definition]."*
- *"Update `domain-knowledge.md` — DPS-based reporting recently changed."*
- *"Promote this investigation sequence into a new playbook in `dynatrace-playbooks.md`."*

For client-specific data, use the appropriate skill instead: `skills/environment-intake/SKILL.md` or `skills/stakeholder-overlay/SKILL.md`.

## Deprecated files in this folder

- `client-environments/README.md` — marked deprecated. Client environment profiles moved to `memory/clients/<client-name>/environment.md`.
- `past-investigations.md` — marked deprecated. Engagement artifacts now live in `memory/clients/<client-name>/engagements/<dated-slug>/`; nothing is moved on archive (the folder is marked `state: complete`).
