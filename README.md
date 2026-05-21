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
| 0 — Context | Frame the problem; confirm scope and stakeholders | [`current-context.md`](memory/project-space/current-context.md) |
| 1 — Diagnose | MECE issue tree, ranked hypotheses, signals map | [`issue-tree.md`](memory/project-space/issue-tree.md), [`hypotheses.md`](memory/project-space/hypotheses.md), [`signals-map.md`](memory/project-space/signals-map.md) |
| 2 — Solution | Investigation plan, recommended actions, decision asks | [`action-plan.md`](memory/project-space/action-plan.md) |
| 3 — Deliver | Exec one-pager and PowerPoint deck | one-pager + deck (generated) |

At each gate the user can **approve**, **redirect**, or **iterate through a critique lens**. Full detail in [docs/workflow.md](docs/workflow.md).

## Quickstart

1. Open this workspace in **VS Code** with the **[Claude Code extension](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)** installed. This is the recommended surface today — the workspace assumes a local filesystem for memory and a sidebar chat for the human-in-the-loop gates, and the VS Code extension delivers both. Claude Code in a terminal works too, but VS Code makes it easier to see the artifacts the agent is writing as it works.
2. Populate stakeholder profiles, domain knowledge, and terminology — see [docs/getting-started.md](docs/getting-started.md).
3. Begin an investigation in the Claude Code sidebar chat:

   > *"Describe the problem you're trying to solve."*

## Documentation

The detailed reference lives in [`/docs/`](docs/). Start with [docs/README.md](docs/README.md) for the table of contents.

| If you want to… | Read |
|---|---|
| Set up the workspace and run your first investigation | [docs/getting-started.md](docs/getting-started.md) |
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
├── CLAUDE.md                  # Agent operating manual (authoritative)
├── docs/                      # Detailed documentation (you are here)
├── skills/                    # Procedural skills, one per phase deliverable
├── .claude/agents/            # Six critique-lens sub-agents + doc-freshness-checker
├── memory/
│   ├── project-space/         # Live investigation (read/write)
│   └── long-term/             # Durable knowledge (read freely; write on approval)
└── tools/                     # Reserved for future integrations (read-only boundary)
```
