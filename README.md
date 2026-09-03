# insights-forge

An agentic workspace that helps consultants and analytics teams **structure ambiguous problems**, generate testable hypotheses, connect technical signals to user-visible UX outcomes and business impact, and produce **exec-ready** outputs for senior technical leadership.

The agent works in **explicit phases with a human approval gate between each phase**. It accelerates engineering and analytics judgment — it does not replace it.

## What it does

- Reframes vague problem statements into **MECE-decomposed** issue trees.
- Generates **ranked, testable hypotheses** with explicit exit criteria.
- Scores hypotheses and actions with **ICE** (Impact × Confidence / Effort).
- Maps technical signals (SLI/SLO, RUM, APM) → UX outcomes → business KPIs.
- Builds investigation plans with **named owners, timeframes, and exit criteria**.
- Produces **VP/Director-ready one-pagers and decks** tailored to a named stakeholder.
- Stress-tests recommendations through **six critique lenses** before leadership review.

## What it does NOT do

- **No live queries** against Dynatrace, data warehouses, or any production system.
- **No raw DQL, SQL, or executable query syntax** — references signals; never generates queries.
- **No production changes**, deploys, or configuration updates.
- **No replacing** engineering or analytics judgment.
- **No bypassing review gates** — every phase ends with an explicit user approval.

## Phased workflow

| Phase | Purpose | Artifact |
|---|---|---|
| 0 — Context | Frame the problem; confirm scope and stakeholders | `current-context.md` |
| 1 — Diagnose | MECE issue tree, ranked hypotheses, signals map | `issue-tree.md`, `hypotheses.md`, `signals-map.md` |
| 2 — Solution | Investigation plan, recommended actions, decision asks | `action-plan.md` |
| 3 — Deliver | Exec one-pager and PowerPoint deck | one-pager + deck (generated) |

All phase artifacts live in the engagement's own folder, `memory/clients/<client>/engagements/<YYYY-MM-DD-slug>/`. At each gate the user can **approve**, **redirect**, or **iterate through a critique lens**. Full detail in [docs/workflow.md](docs/workflow.md).

## How it installs

**Installation = open this folder in Claude Code.** No npm, no build step, no CLI commands.

Three mechanisms activate automatically:
- **`CLAUDE.md`** — Claude Code reads this on every session start. It is the agent's operating manual and the workspace's entry point.
- **`.claude/settings.json`** — sets the model tier by alias (`sonnet`; the lenses inherit it, the freshness checker runs on `haiku`), scopes file permissions, and registers the hooks that mechanically enforce client isolation, the fetch allowlist, and workspace conformance.
- **`.claude/agents/`** — registers the seven sub-agents (six critique lenses + doc-freshness-checker). The main agent dispatches these via the `Agent` tool; you don't invoke them directly.

The `skills/` files are **not** slash commands. The main agent reads them as reference documents immediately before producing each phase artifact — triggered by its own operating logic, not by user commands.

## Quickstart

1. Open this workspace in **VS Code** with the **[Claude Code extension](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)** installed. The VS Code extension is the recommended surface — you can watch the agent write artifacts into the engagement folder under `memory/clients/` in the file explorer as it works. Claude Code in a terminal works too.
2. Follow the one-time setup in [docs/getting-started.md](docs/getting-started.md) — takes about 15 minutes.
3. Begin an investigation in the Claude Code sidebar chat:

   > *"Describe the problem you're trying to solve."*

   Or pre-fill the context first: open [`html/seed-prompt-generator-src.html`](html/seed-prompt-generator-src.html) in VS Code or Claude Code Desktop App, fill it out, and paste the generated seed prompt as your opening message. See [docs/seed-prompt-generator.md](docs/seed-prompt-generator.md).

## Cost management

Claude Code automatically caches the system prompt — which includes `CLAUDE.md` and tool definitions — so you don't pay full re-ingestion cost on every conversational turn within a session. The four session-start file reads (`domain-knowledge.md`, `dynatrace-playbooks.md`, `frameworks.md`, `stakeholder-profiles.md`) enter conversation context and stay cached within that session; starting a new session re-reads them cold.

Practical implications for budget-conscious users:

- **Complete as much of a phase as possible within one session** before closing Claude Code. Continuing a conversation reuses cached context; reopening starts fresh.
- **`CLAUDE.md` size directly affects system prompt cache footprint.** It is intentionally kept lean — detail lives in skill files and agent files, which are only loaded on demand.
- **Stable content stays at the top of `CLAUDE.md`.** Claude Code caches the file as a prefix — if you ever customize the file, put frequently-changing content (new skills, new client notes) at the bottom so earlier sections remain cached across edits.

## Documentation

The detailed reference lives in [`/docs/`](docs/). Start with [docs/README.md](docs/README.md) for the table of contents.

| If you want to… | Read |
|---|---|
| Set up the workspace and run your first investigation | [docs/getting-started.md](docs/getting-started.md) |
| Pre-fill Phase 0 with the browser intake form | [docs/seed-prompt-generator.md](docs/seed-prompt-generator.md) |
| Understand the four phases in depth | [docs/workflow.md](docs/workflow.md) |
| Learn the six critique lenses | [docs/lenses.md](docs/lenses.md) |
| See the procedural skills index | [docs/skills.md](docs/skills.md) |
| Understand the memory model | [docs/memory.md](docs/memory.md) |
| Understand external research and citations | [docs/research.md](docs/research.md) |
| Produce a Phase 3 one-pager or deck | [docs/deliverables.md](docs/deliverables.md) |
| Customize for your team | [docs/customizing.md](docs/customizing.md) |

The agent's operating manual is [`CLAUDE.md`](CLAUDE.md) — read on every session and authoritative when `/docs/` and `CLAUDE.md` disagree.

## Repository layout

```
.
├── CLAUDE.md                     # Agent operating manual (authoritative, auto-loaded)
├── .claude/
│   ├── settings.json             # Model alias, permissions, hooks (isolation, fetch allowlist, conformance)
│   └── agents/                   # Seven sub-agents (6 lenses + doc-freshness-checker)
├── skills/                       # Procedural reference files, one per phase artifact
│   ├── context-framing/          # Phase 0
│   ├── mece-decomposition/       # Phase 1
│   ├── hypothesis-generation/    # Phase 1
│   ├── ice-scoring/              # Phase 1 & 2
│   ├── signal-mapping/           # Phase 1
│   ├── action-plan-builder/      # Phase 2
│   ├── exec-onepager/            # Phase 3
│   ├── brand-humanizer/          # Phase 3 (mandatory copy-editing pre-pass)
│   ├── pptx-builder/             # Phase 3
│   ├── external-research/        # All phases (web lookup)
│   ├── investigation-reset/      # Archive / pause / resume an engagement
│   ├── stakeholder-overlay/      # Capture a named client leader
│   ├── environment-intake/       # Capture client DT environment details
│   └── value-highlight/          # QBR / renewal value brief
├── memory/
│   ├── long-term/                # Root library — universal knowledge only, no client data
│   └── clients/                  # Per-client isolated workspaces (live + past engagements)
│       ├── _template/            # Copy this to create a new client workspace
│       └── <client-name>/        # README, environment.md, contract.md, stakeholder-overlays.md,
│                                 #   engagements/<YYYY-MM-DD-slug>/  (all phase files live here)
├── html/                         # Seed Prompt Generator (VS Code / Claude Code Desktop App tool) + screenshots
├── docs/                         # Human-readable documentation
└── tools/                        # Deck generator, one-pager linter, conformance check, hooks
```
