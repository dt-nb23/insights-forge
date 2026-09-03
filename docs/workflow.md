# The four-phase workflow

This page walks you through what actually happens in each phase, what the gate feels like in practice, and where the artifacts land. If you've read [getting-started.md](getting-started.md) and want the deeper picture, you're in the right place.

The workspace is built around a simple rhythm: **work, present, gate, repeat**. The agent produces something, stops, asks you to weigh in, and only moves forward when you say so. This isn't ceremony — it's the load-bearing safety mechanism that keeps the workspace useful for ambiguous problems. A bad framing in Phase 0 will produce confident-sounding nonsense in Phase 3 if there's no gate to catch it.

The canonical phase rules live in [`CLAUDE.md`](../CLAUDE.md). This page expands on what each phase actually feels like.

## Phase 0 — Context

**What it's for.** Take a vague problem statement and reframe it into a scoped, stakeholder-aware engagement. This is where you turn *"latency is bad on checkout"* into *"P95 checkout latency is up 40% week-over-week for the EU region; the VP of Reliability needs an answer before next Thursday's QBR."*

**The skill the agent reads.** [`skills/context-framing/SKILL.md`](../skills/context-framing/SKILL.md) — open it if you want to see every step the agent runs through, including the nine clarifying questions and the C.S.I.R. sub-sequence for Q3. Two behaviors worth knowing: a pasted **seed-prompt intake brief** is absorbed as provisional answers and only the gaps get asked — collapsing to a single sharpening message when the brief arrives with every required field filled; and the factual questions (tenant, capabilities, RUM status) and the optional SHOULD-HAVE confirmations are batched, while the narrative questions stay one at a time.

**Files the agent reads before asking you anything.**

- [`memory/long-term/stakeholder-profiles.md`](../memory/long-term/stakeholder-profiles.md) — so it can recognize which leaders you might be producing outputs for.
- [`memory/long-term/domain-knowledge.md`](../memory/long-term/domain-knowledge.md) — to anchor in the tech → UX → business linkage table.
- [`memory/long-term/terminology.md`](../memory/long-term/terminology.md) — to use language consistent with the team.
- [`memory/long-term/client-question-bank.md`](../memory/long-term/client-question-bank.md) — when you tell it the discovery is happening **live with the customer**, it switches to the client-facing phrasings.
- `memory/clients/<client>/README.md` — the client's engagement-history index, to spot prior engagements on the same customer and surface relevant lessons.
- Other clients' `engagements/*/lessons-learned.md` — **front-matter and Cross-engagement hook line only** — filtered by vertical and problem shape, so a prior engagement's hard-won lesson surfaces even when this client is new (at most 3, ranked; one of the two named exceptions to the context isolation rule in [memory.md](memory.md)).

**What lands on disk.** `current-context.md` inside the engagement folder — `memory/clients/<client>/engagements/<YYYY-MM-DD-slug>/`. Open it during Phase 0 to see the agent's running understanding of the problem — it's not hidden from you. It opens with a status front-matter block (`state`, `phase`, …) that makes the engagement self-describing.

**The gate question.** *"Does this framing match what you actually need?"*

## Phase 1 — Diagnose

**What it's for.** Decompose the framed problem into a MECE issue tree, generate ranked hypotheses per branch, and map the technical signals that would prove or disprove each one.

The phase runs in a fixed order, and the order resolves a real dependency — ICE cannot anchor Impact to a business KPI until the signals map exists, so scoring comes last:

1. **Issue tree** ([`mece-decomposition`](../skills/mece-decomposition/SKILL.md)) — a structured decomposition of where the problem could be coming from, where every branch is mutually exclusive and the union is collectively exhaustive. The [MECE lens](../.claude/agents/mece-lens.md) critiques the tree here.
2. **Hypotheses** ([`hypothesis-generation`](../skills/hypothesis-generation/SKILL.md)) — each branch gets 2–4 testable statements with stated exit criteria. Any hypothesis that depends on telemetry the team doesn't have is marked, on its own row, with Status **"blocked: instrumentation"** — the gap is recorded *in* `hypotheses.md`, not yet in the signals map. The [Consultative lens](../.claude/agents/consultative-lens.md) then runs a **framing pass** on the issue-tree and hypotheses *wording* — confirming branches and claims read as business outcomes and decisions — before hand-off. It corrects wording only; it does not touch structure or scores. Hand-off goes to signal-mapping, **not** to ICE.
3. **Signals map** ([`signal-mapping`](../skills/signal-mapping/SKILL.md)) — connects each hypothesis to the SLI/SLO, RUM event, or APM trace that would validate it. This step also **scans `hypotheses.md` for the "blocked: instrumentation" rows and consolidates them** into the signals-map "Instrumentation gaps" section. Hand-off goes to ICE.
4. **ICE scoring** ([`ice-scoring`](../skills/ice-scoring/SKILL.md)) — now that the signals map exists, Impact can be anchored to a business KPI. Before scoring, ICE consumes the instrumentation gaps: if a hypothesis can't be validated until a gap is closed, Effort rises (the instrumentation work is now in scope), Confidence drops (it can't be confirmed yet), and Impact drops if the KPI link can't be quantified. The [ICE lens](../.claude/agents/ice-lens.md) sanity-checks the scoring, and ice-scoring itself then presents the Phase 1 gate — the five-part gate summary block with the full ranked table.

In Phase 1, ICE Confidence means *the likelihood the hypothesis is validated by telemetry* and Impact means *the magnitude if it is confirmed*. (Phase 2 re-scores both against execution — see below.)

**What lands on disk.**

- `<engagement folder>/issue-tree.md`
- `<engagement folder>/hypotheses.md`
- `<engagement folder>/signals-map.md`

**Lenses the phase runs (all mandatory).** [MECE](../.claude/agents/mece-lens.md) on the tree, [Consultative](../.claude/agents/consultative-lens.md) as the framing pass on tree + hypotheses wording, then [ICE](../.claude/agents/ice-lens.md) on the scoring after the signals map exists. You can ask for any of the six on top at the gate.

**The gate question.** *"Does this diagnosis frame the problem the right way, and are the top hypotheses worth pursuing?"*

## Phase 2 — Solution

**What it's for.** Turn ranked hypotheses into an investigation plan with named owners, timeframes, and unambiguous exit criteria for "confirmed" versus "ruled out."

This is the phase where the **Dynatrace playbooks** become load-bearing. The agent matches each hypothesis against the index in [`memory/long-term/dynatrace-playbooks.md`](../memory/long-term/dynatrace-playbooks.md) (latency, errors, RUM regression, Grail logs, SLO burn, deploy correlation, third-party dependency, Davis problem), reads only the matched playbook file(s) in [`memory/long-term/playbooks/`](../memory/long-term/playbooks/), and pulls that playbook's procedural steps and exit criteria straight into the live action plan. The playbooks are how the workspace stays specialized to Dynatrace without you having to re-explain Dynatrace investigation patterns every time. The agent also reads the client's `environment.md` and grounds every action in what this client can actually observe — flagging any action that depends on instrumentation the client lacks rather than silently recommending it.

**The skill the agent reads.** [`skills/action-plan-builder/SKILL.md`](../skills/action-plan-builder/SKILL.md).

Phase 2 is built by a **deliberating council of perspectives in a deliberate order**, and like Phase 1 the sequence is the point:

1. **MECE on the opportunity set.** Before drafting, the agent lays out the full set of opportunities and levers the plan could pull, then runs the [MECE lens](../.claude/agents/mece-lens.md) on that set as a completeness check — no viable opportunity missed, no two overlapping. This is the candidate pool the recommended actions are drawn from.
2. **Draft the plan** against that set — investigation actions with exit criteria, recommended actions, decision asks, and risks paired with their mitigations.
3. **Convene the persona council — over two to three rounds.** [Skeptic](../.claude/agents/skeptic-lens.md), [Optimist](../.claude/agents/optimist-lens.md), [Customer](../.claude/agents/customer-lens.md), and [Consultative](../.claude/agents/consultative-lens.md) deliberate, each round dispatched as one message so the four run concurrently: **Round 1** each gives an independent position in parallel, blind to the others; **Round 2** each reacts to the others' positions; **Round 3** runs only if a material tension survives Round 2 — each converges on a final position and flags what it won't concede (more rounds if they're still moving; skipped entirely if the panel has already converged). The full three rounds are **forced** for high-stakes deliverables, when you ask, or when Phase 0's calibration routing called for it. Every panelist is grounded in the client's real instrumentation (`environment.md`), not generic capability. Then the **agent reconciles** every material disagreement — not just Skeptic-vs-Optimist or Customer-vs-Consultative — logging each ruling in the plan's "Tensions resolved" subsection rather than averaging the difference, and folds Skeptic's "questions a leader will ask" into the decision-asks section.
4. **Re-rank with ICE — after the council.** Only once the critique is in does the [ICE lens](../.claude/agents/ice-lens.md) re-score and re-rank the opportunities; the ranking that lands in the plan is this post-council order, not the first cut. Ranking before the council bakes in the pre-critique view and wastes it.

ICE re-scores against **execution**, not validation: in Phase 2, Confidence is *the likelihood the action executes given coordination and risk* and Impact is *the magnitude if the mitigation lands* — a partial fix scores below the problem it targets. So a hypothesis that scored, say, Confidence 7 in Phase 1 may land at Confidence 5 as a Phase 2 action because of coordination risk.

**What lands on disk.** `<engagement folder>/action-plan.md`.

**Lenses the phase runs (all mandatory).** [MECE](../.claude/agents/mece-lens.md) on the opportunity set, then the persona council over 2–3 rounds — [Skeptic](../.claude/agents/skeptic-lens.md), [Optimist](../.claude/agents/optimist-lens.md), [Customer](../.claude/agents/customer-lens.md), [Consultative](../.claude/agents/consultative-lens.md) — then the agent reconciles, then [ICE](../.claude/agents/ice-lens.md) to re-rank. You can ask for any of the six on top at the gate.

**The gate question.** *"Is this the right plan, with the right exit criteria, and are the decision asks clear?"*

## Phase 3 — Deliver

**What it's for.** Produce the exec-ready written and slide deliverables for the named stakeholder.

The order matters here: **one-pager first, deck second**. The one-pager forces the story to fit on a page, which makes the deck dramatically easier to build. The agent won't produce the deck until the one-pager is approved.

**Skills the agent reads, in this order.**

- [`skills/exec-onepager/SKILL.md`](../skills/exec-onepager/SKILL.md) — five-step orchestrator: recipe selection, content draft, brand-humanizer pre-pass (mandatory Step 3, runs before HTML is built), HTML build, and brand gate.
- [`skills/pptx-builder/SKILL.md`](../skills/pptx-builder/SKILL.md) — PowerPoint deck (only after the one-pager is approved).

**Files the agent reads before producing anything.**

- [`memory/long-term/brand/brand-spec.md`](../memory/long-term/brand/brand-spec.md) — colors, typography, layouts, voice, terminology, footer conventions. The brand spec is authoritative; the agent never improvises off-spec. See [deliverables.md](deliverables.md) for what this means in practice.
- The matching profile file in [`memory/long-term/profiles/`](../memory/long-term/profiles/), found via the index in [`memory/long-term/stakeholder-profiles.md`](../memory/long-term/stakeholder-profiles.md). Voice and emphasis come from the profile file — the same investigation produces different one-pagers for a VP of Reliability versus a VP of Product.

**Lenses the phase runs.** None. Phase 3 is **pure packaging** of a plan the persona panel already reviewed and you already approved at the Phase 2 gate. No critique lens runs here — the substance, framing, priorities, and risks were settled in Phase 2, and re-opening them in Phase 3 is a signal to reopen Phase 2, not to patch the one-pager. What remains in Phase 3 is mechanical: the brand-humanizer pre-pass (Step 3 — fixes AI writing patterns and DT voice violations on structured copy before the HTML is built), the one-page constraint, brand conformance (sentence-case headings, product-name trademarks, footer, palette), and the brand gate checklist. Those are formatting gates, not critique. You can still invoke any of the six lenses on demand at the gate if you want a second look, but none runs automatically.

**The gate question.** *"Is this ready to send to the named stakeholder?"* — asked separately for the one-pager and the deck.

## What every gate looks like, in practice

At each gate the agent **stops and presents** using the five-part gate summary block defined in [`CLAUDE.md`](../CLAUDE.md): **1 Conclusion** (the single most important finding, one sentence), **2 What changed** since the prior gate, **3 Assumptions and confidence gaps** (where the agent guessed, where the evidence is thin — the part that lets you judge whether it understood without re-reading the artifact), **4 Out-of-scope cost** (anything excluded because it touched an out-of-scope capability), and **5 the ask** (Approve / Redirect / Iterate). Every phase has one — Phase 3 has two, one for the one-pager and one for the deck. The Phase 0 gate also names any queued follow-on interviews (stakeholder-overlay, environment-intake) with a rough time cost and lets you defer them past the Phase 1 gate, so the full cost of approving is visible before you approve. On approval the agent records the decision in `decisions-log.md` and bumps `phase:` and `last-touched:` in the engagement's `current-context.md`; both writes are part of the gate itself. Only an explicit go-ahead advances the phase — "looks good" or silence is not approval. You always have three responses available:

| Response | What it does |
|---|---|
| **Approve** | Agent proceeds to the next phase. |
| **Redirect** | You change scope, framing, or priority. Agent updates artifacts and re-presents. |
| **Iterate through a lens** | You ask for re-review through one of the six lenses. Agent revises before re-presenting. See [lenses.md](lenses.md) for what each lens catches. |

Every gate decision is appended to `<engagement folder>/decisions-log.md`. That file is the audit trail — if anyone asks weeks later *"why did we pursue that hypothesis?"*, the answer is there.

## Look inside

| What you'll find | Where to look |
|---|---|
| The operating manual the agent reads on every session | [`CLAUDE.md`](../CLAUDE.md) |
| All eight phase skills | [`skills/`](../skills/) |
| The six critique lenses and the doc-freshness-checker | [`.claude/agents/`](../.claude/agents/) |
| The live investigation state (during a session) | the active engagement folder, `memory/clients/<client>/engagements/<dated-slug>/` |
| The audit trail for the current investigation | `<engagement folder>/decisions-log.md` |
