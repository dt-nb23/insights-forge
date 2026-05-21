# The six critique lenses

The workspace ships with six sub-agents whose only job is to **critique work product through a single, narrow point of view**. They don't produce artifacts themselves — they read what the main agent has produced and either bless it, suggest revisions, or push back hard.

You'll meet them in three situations:

1. **Automatically before a gate.** The main agent invokes the default lenses for each phase before presenting (you can see the defaults below). This is why a Phase 3 one-pager has already been read by Consultative, Customer, and Skeptic by the time you see it.
2. **On demand at any gate.** You can always say *"run this through the Skeptic lens"* or *"check this issue tree with MECE"* — the agent will dispatch the lens and re-present.
3. **In parallel for Phase 3.** When three or more lenses can review independently (Consultative + Customer + Skeptic on a one-pager is the typical case), the agent dispatches them in parallel rather than one at a time.

Each lens's full definition — including its system prompt and output format — lives at [`.claude/agents/<lens>.md`](../.claude/agents/). Open the file if you want to see exactly what the lens has been told to do.

## Meet the six

### [MECE lens](../.claude/agents/mece-lens.md)
**When you'll use it.** After a Phase 1 issue tree is drafted, before presenting it.

**What it catches.** Branches that overlap (not mutually exclusive). Gaps in coverage (not collectively exhaustive). Abstraction levels that drift within a branch (Marketing-grade buckets mixed with engineering-grade buckets). Silent missing categories.

A clean MECE tree is the foundation everything else in Phase 1 builds on, so this lens is invoked by default before any tree leaves Phase 1.

### [Optimist lens](../.claude/agents/optimist-lens.md)
**When you'll use it.** Before finalizing a Phase 2 action plan or a Phase 3 one-pager.

**What it catches.** Plans that have been over-defended. Upside the team has under-weighted. Investigation threads that could run in parallel but are sequenced as if they can't. Recommendations that could be more ambitious without losing rigor.

Think of it as the counterweight to Skeptic — invoke them both, and your plan ends up balanced.

### [ICE lens](../.claude/agents/ice-lens.md)
**When you'll use it.** After hypotheses or actions are drafted.

**What it catches.** Mis-ranked priorities. Hypotheses that have high Impact but low Confidence and high Effort, masquerading as "the top hypothesis." Actions that look cheap but are buried in dependencies.

The main agent runs ICE by default in Phase 1; you'll invoke it explicitly when actions in Phase 2 need re-ranking after a redirect.

### [Consultative lens](../.claude/agents/consultative-lens.md)
**When you'll use it.** Before finalizing exec one-pagers or decks.

**What it catches.** Passages that read as engineering-internal when the audience is leadership. Generic statements that any consulting firm could have written. Voice mismatches with the named stakeholder profile.

This is the lens that makes the Phase 3 output sound like *your firm*, not *a competent AI*.

### [Customer lens](../.claude/agents/customer-lens.md)
**When you'll use it.** Before finalizing any deliverable that recommends action.

**What it catches.** Recommendations grounded in a backend SLI that has no observable user impact. Wins that don't move anything the customer would notice. Investigations that "succeed" without actually improving anyone's experience.

A common failure mode this lens catches: a 30% improvement to a metric the user never sees.

### [Skeptic lens](../.claude/agents/skeptic-lens.md)
**When you'll use it.** Before any Phase 2 action plan or Phase 3 deliverable goes to leadership.

**What it catches.** Failure modes that have been hand-waved. The most uncomfortable question a VP could ask. The spots where the evidence is thinnest. The unsaid assumptions.

If you're going to be in a room defending the work, Skeptic is the lens that simulates the room first.

## Default invocations per phase

| Phase | Lenses invoked by default | Lenses available on request |
|---|---|---|
| 0 — Context | — | Any |
| 1 — Diagnose | [MECE](../.claude/agents/mece-lens.md), [ICE](../.claude/agents/ice-lens.md) | [Optimist](../.claude/agents/optimist-lens.md), [Skeptic](../.claude/agents/skeptic-lens.md) |
| 2 — Solution | [Skeptic](../.claude/agents/skeptic-lens.md) | [Optimist](../.claude/agents/optimist-lens.md), [ICE](../.claude/agents/ice-lens.md), [Customer](../.claude/agents/customer-lens.md) |
| 3 — Deliver | [Consultative](../.claude/agents/consultative-lens.md), [Customer](../.claude/agents/customer-lens.md), [Skeptic](../.claude/agents/skeptic-lens.md) | [Optimist](../.claude/agents/optimist-lens.md) |

## Running lenses in parallel

If three or more lenses can run independently against the same artifact (typical for Phase 3), invoke them in parallel rather than sequentially. The main agent should already do this automatically; you can also ask explicitly:

> *"Run this one-pager through Consultative, Customer, and Skeptic in parallel."*

## Look inside

| Lens file | What you'll find |
|---|---|
| [`.claude/agents/mece-lens.md`](../.claude/agents/mece-lens.md) | System prompt and output format for MECE critique |
| [`.claude/agents/optimist-lens.md`](../.claude/agents/optimist-lens.md) | Steelmanning prompt and upside output format |
| [`.claude/agents/ice-lens.md`](../.claude/agents/ice-lens.md) | Scoring rubric, ranking output |
| [`.claude/agents/consultative-lens.md`](../.claude/agents/consultative-lens.md) | Leadership-voice rewrite directives |
| [`.claude/agents/customer-lens.md`](../.claude/agents/customer-lens.md) | UX-grounding heuristics |
| [`.claude/agents/skeptic-lens.md`](../.claude/agents/skeptic-lens.md) | Failure-mode and hostile-question probes |

There's a seventh sub-agent in that folder — [`doc-freshness-checker.md`](../.claude/agents/doc-freshness-checker.md) — that isn't a lens. It runs as a background job during Phase 0 to check citation drift. See [research.md](research.md) for what it does.
