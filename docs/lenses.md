# The six critique lenses

The workspace ships with six sub-agents whose only job is to **critique work product through a single, narrow point of view**. They don't produce artifacts themselves — they read what the main agent has produced and either bless it, suggest revisions, or push back hard.

You'll meet them in two situations, and both are always true at once:

1. **Mandatory within a phase.** Phases 1 and 2 each run a fixed set of lenses as part of the phase procedure — they are not optional add-ons. The [per-phase table below](#when-each-lens-runs) is the authority for which lenses run in which phase. Phase 0 and Phase 3 run **no** critique lens.
2. **On demand at any gate.** On top of the mandatory set, you can always say *"run this through the Skeptic lens"* or *"check this issue tree with MECE"* — the agent will dispatch the lens and re-present. Any of the six is available at any gate, regardless of phase.

These are not mutually exclusive: the mandatory per-phase lenses always run, and you can request any lens on demand in addition.

Each lens's full definition — including its system prompt and output format — lives at [`.claude/agents/<lens>.md`](../.claude/agents/). Open the file if you want to see exactly what the lens has been told to do.

## Meet the six

### [MECE lens](../.claude/agents/mece-lens.md)
**When it runs.** Mandatory in Phase 1 (on the issue tree, before presenting it) and again in Phase 2 (as a completeness check on the opportunity set, before the plan is drafted against it).

**What it catches.** Branches that overlap (not mutually exclusive). Gaps in coverage (not collectively exhaustive). Abstraction levels that drift within a branch (Marketing-grade buckets mixed with engineering-grade buckets). Silent missing categories.

A clean MECE structure is the foundation everything else builds on — a clean tree in Phase 1, a complete opportunity set in Phase 2 — so this lens runs mandatorily at the start of both diagnosis and planning.

### [Optimist lens](../.claude/agents/optimist-lens.md)
**When it runs.** Mandatory in Phase 2 as a member of the persona panel that critiques the draft action plan. Available on demand at any other gate.

**What it catches.** Plans that have been over-defended. Upside the team has under-weighted. Investigation threads that could run in parallel but are sequenced as if they can't. Recommendations that could be more ambitious without losing rigor.

Think of it as the counterweight to Skeptic — on the Phase 2 council they critique the plan and each other across rounds, and the plan ends up balanced.

### [ICE lens](../.claude/agents/ice-lens.md)
**When it runs.** Mandatory in Phase 1 (sanity-check on hypothesis scoring, run **after** the signals map exists so Impact can be anchored to a business KPI) and again in Phase 2 (re-rank the opportunities **after** the persona panel has weighed in).

**What it catches.** Mis-ranked priorities. Hypotheses that have high Impact but low Confidence and high Effort, masquerading as "the top hypothesis." Actions that look cheap but are buried in dependencies.

The two runs score different things. In Phase 1, Confidence is the likelihood the hypothesis is validated by telemetry and Impact is the magnitude if it is confirmed. In Phase 2, Confidence is the likelihood the action executes given coordination and risk, and Impact is the magnitude if the mitigation lands — a partial fix scores below the problem it targets. So a hypothesis that scored well in Phase 1 can be re-scored lower as a Phase 2 action.

### [Consultative lens](../.claude/agents/consultative-lens.md)
**When it runs.** Mandatory in Phase 1 as a **framing pass** on the issue-tree and hypotheses wording — checking that branches and claims are stated as business outcomes and decisions, not buried in engineering minutiae. It corrects wording only; it does not change the analytical structure (that is the MECE lens's job) or the scores. Mandatory again in Phase 2 as a member of the persona panel on the action plan.

**What it catches.** Passages that read as engineering-internal when the audience is leadership. Generic statements that any consulting firm could have written. Tradeoffs stated as advocacy rather than counsel. Voice mismatches with the named stakeholder profile.

This is the lens that gets the framing right *going into* each gate rather than patching it downstream. It does **not** run in Phase 3 — by then the framing is already settled, and Phase 3 is pure packaging.

### [Customer lens](../.claude/agents/customer-lens.md)
**When it runs.** Mandatory in Phase 2 as a member of the persona panel — checking that the plan targets what users actually experience, not just what is easiest to measure. Available on demand at any other gate.

**What it catches.** Recommendations grounded in a backend SLI that has no observable user impact. Wins that don't move anything the customer would notice. Investigations that "succeed" without actually improving anyone's experience.

A common failure mode this lens catches: a 30% improvement to a metric the user never sees.

### [Skeptic lens](../.claude/agents/skeptic-lens.md)
**When it runs.** Mandatory in Phase 2 as a member of the persona panel on the action plan — its "questions a leader will ask" fold into the decision-asks section so the plan answers them up front. Available on demand at any other gate.

**What it catches.** Failure modes that have been hand-waved. The most uncomfortable question a VP could ask. The spots where the evidence is thinnest. The unsaid assumptions.

If you're going to be in a room defending the work, Skeptic is the lens that simulates the room first — which is why it runs while the plan can still change, in Phase 2, not after it has been packaged in Phase 3.

## When each lens runs

This table is the single source of truth for which lenses run in which phase. The mandatory lenses are part of the phase procedure — they always run. On top of them, you may invoke **any** of the six on demand at that phase's gate.

| Phase | Mandatory lenses (run as part of the phase) | Also available on demand |
|---|---|---|
| 0 — Context | None. (A background [doc-freshness-checker](#look-inside) runs conditionally, but it is not a critique lens.) | Any of the six |
| 1 — Diagnose | [MECE](../.claude/agents/mece-lens.md) on the issue tree, then [Consultative](../.claude/agents/consultative-lens.md) as a framing pass on the issue-tree and hypotheses wording, then [ICE](../.claude/agents/ice-lens.md) on hypothesis scoring (ICE runs **after** the signals map exists) | Any of the six |
| 2 — Solution | [MECE](../.claude/agents/mece-lens.md) on the opportunity set, then the **persona council** — [Skeptic](../.claude/agents/skeptic-lens.md), [Optimist](../.claude/agents/optimist-lens.md), [Customer](../.claude/agents/customer-lens.md), [Consultative](../.claude/agents/consultative-lens.md) — deliberating over **≥3 rounds** (independent → cross-examination → convergence), then the agent reconciles, then [ICE](../.claude/agents/ice-lens.md) re-ranks **after** the council | Any of the six |
| 3 — Deliver | **None.** Phase 3 is pure packaging of the already-reviewed plan plus mechanical gates (one-page constraint, brand conformance, HTML legibility). No critique lens runs. | Any of the six |

The order inside Phase 1 and Phase 2 matters and is not interchangeable — see [workflow.md](workflow.md) for the full sequence and why ICE runs last in each.

## The Phase 2 council runs in rounds

The Phase 2 persona panel is a **deliberating council**, not a single pass. It runs over at least three rounds:

1. **Round 1 — independent positions.** All four lenses are dispatched **in parallel and blind** — each reads only the draft plan (plus the client's `environment.md`) and gives its own position, having seen none of the others.
2. **Round 2 — cross-examination.** Each lens is handed the other three Round-1 positions and reacts: where it agrees, where it contradicts another lens and why, what it concedes.
3. **Round 3 — convergence.** Each lens reads the Round-2 reactions and states its final position, flagging any tension it will not concede. More rounds run if positions are still moving.

Only then does the **agent reconcile** — ruling on every material disagreement and logging each in the plan's "Tensions resolved" subsection — before ICE re-ranks. "Parallel" (Round 1) and "critique each other" (Rounds 2+) are *different rounds*, not a contradiction. `skills/action-plan-builder/SKILL.md` step 6 is the authoritative procedure. You can also ask for this council explicitly at any gate:

> *"Run the action plan through the Skeptic, Optimist, Customer, and Consultative council."*

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
