# The four-phase workflow

This page walks you through what actually happens in each phase, what the gate feels like in practice, and where the artifacts land. If you've read [getting-started.md](getting-started.md) and want the deeper picture, you're in the right place.

The workspace is built around a simple rhythm: **work, present, gate, repeat**. The agent produces something, stops, asks you to weigh in, and only moves forward when you say so. This isn't ceremony — it's the load-bearing safety mechanism that keeps the workspace useful for ambiguous problems. A bad framing in Phase 0 will produce confident-sounding nonsense in Phase 3 if there's no gate to catch it.

The canonical phase rules live in [`CLAUDE.md`](../CLAUDE.md). This page expands on what each phase actually feels like.

## Phase 0 — Context

**What it's for.** Take a vague problem statement and reframe it into a scoped, stakeholder-aware engagement. This is where you turn *"latency is bad on checkout"* into *"P95 checkout latency is up 40% week-over-week for the EU region; the VP of Reliability needs an answer before next Thursday's QBR."*

**The skill the agent reads.** [`skills/context-framing/SKILL.md`](../skills/context-framing/SKILL.md) — open it if you want to see every step the agent runs through, including the nine clarifying questions and the C.S.I.R. sub-sequence for Q3.

**Files the agent reads before asking you anything.**

- [`memory/long-term/stakeholder-profiles.md`](../memory/long-term/stakeholder-profiles.md) — so it can recognize which leaders you might be producing outputs for.
- [`memory/long-term/domain-knowledge.md`](../memory/long-term/domain-knowledge.md) — to anchor in the tech → UX → business linkage table.
- [`memory/long-term/terminology.md`](../memory/long-term/terminology.md) — to use language consistent with the team.
- [`memory/long-term/client-question-bank.md`](../memory/long-term/client-question-bank.md) — when you tell it the discovery is happening **live with the customer**, it switches to the client-facing phrasings.
- [`memory/long-term/past-investigations.md`](../memory/long-term/past-investigations.md) — to spot prior engagements on the same customer, vertical, or problem shape and surface relevant lessons.

**What lands on disk.** [`memory/project-space/current-context.md`](../memory/project-space/current-context.md). Open it during Phase 0 to see the agent's running understanding of the problem — it's not hidden from you.

**The gate question.** *"Does this framing match what you actually need?"*

## Phase 1 — Diagnose

**What it's for.** Decompose the framed problem into a MECE issue tree, generate ranked hypotheses per branch, and map the technical signals that would prove or disprove each one.

You'll feel three distinct shifts during this phase:

- First, the **issue tree** appears — a structured decomposition of where the problem could be coming from, where every branch is mutually exclusive and the union is collectively exhaustive.
- Then **hypotheses** populate under each branch, each one written as a testable statement with a stated exit criterion.
- Finally, the **signals map** connects each hypothesis to the SLI/SLO, RUM event, or APM trace that would validate it — and importantly, calls out the gaps where the instrumentation doesn't exist.

**Skills the agent reads.**

- [`skills/mece-decomposition/SKILL.md`](../skills/mece-decomposition/SKILL.md) — building the tree.
- [`skills/hypothesis-generation/SKILL.md`](../skills/hypothesis-generation/SKILL.md) — drafting testable hypotheses per branch.
- [`skills/ice-scoring/SKILL.md`](../skills/ice-scoring/SKILL.md) — scoring each hypothesis on Impact × Confidence / Effort.
- [`skills/signal-mapping/SKILL.md`](../skills/signal-mapping/SKILL.md) — connecting signals to UX outcomes and business KPIs.

**What lands on disk.**

- [`memory/project-space/issue-tree.md`](../memory/project-space/issue-tree.md)
- [`memory/project-space/hypotheses.md`](../memory/project-space/hypotheses.md)
- [`memory/project-space/signals-map.md`](../memory/project-space/signals-map.md)

**Lenses the agent runs by default before presenting.** [MECE](../.claude/agents/mece-lens.md) and [ICE](../.claude/agents/ice-lens.md). You can ask for any of the others on top.

**The gate question.** *"Does this diagnosis frame the problem the right way, and are the top hypotheses worth pursuing?"*

## Phase 2 — Solution

**What it's for.** Turn ranked hypotheses into an investigation plan with named owners, timeframes, and unambiguous exit criteria for "confirmed" versus "ruled out."

This is the phase where the **Dynatrace playbooks** become load-bearing. The agent reads [`memory/long-term/dynatrace-playbooks.md`](../memory/long-term/dynatrace-playbooks.md), matches each hypothesis to the playbook that most closely fits its problem shape (latency, errors, RUM regression, Grail logs, SLO burn, deploy correlation, third-party dependency, Davis problem), and pulls the playbook's procedural steps and exit criteria straight into the live action plan. The playbooks are how the workspace stays specialized to Dynatrace without you having to re-explain Dynatrace investigation patterns every time.

**The skill the agent reads.** [`skills/action-plan-builder/SKILL.md`](../skills/action-plan-builder/SKILL.md).

**What lands on disk.** [`memory/project-space/action-plan.md`](../memory/project-space/action-plan.md).

**Lenses the agent runs by default before presenting.** [Skeptic](../.claude/agents/skeptic-lens.md). Ask for [Optimist](../.claude/agents/optimist-lens.md) if the plan feels too defensive, or [Customer](../.claude/agents/customer-lens.md) if you want a sanity check that the proposed work actually maps to something users experience.

**The gate question.** *"Is this the right plan, with the right exit criteria, and are the decision asks clear?"*

## Phase 3 — Deliver

**What it's for.** Produce the exec-ready written and slide deliverables for the named stakeholder.

The order matters here: **one-pager first, deck second**. The one-pager forces the story to fit on a page, which makes the deck dramatically easier to build. The agent won't produce the deck until the one-pager is approved.

**Skills the agent reads, in this order.**

- [`skills/exec-onepager/SKILL.md`](../skills/exec-onepager/SKILL.md) — one-page written summary.
- [`skills/pptx-builder/SKILL.md`](../skills/pptx-builder/SKILL.md) — PowerPoint deck.

**Files the agent reads before producing anything.**

- [`memory/long-term/brand/brand-spec.md`](../memory/long-term/brand/brand-spec.md) — colors, typography, layouts, voice, terminology, footer conventions. The brand spec is authoritative; the agent never improvises off-spec. See [deliverables.md](deliverables.md) for what this means in practice.
- The matching profile in [`memory/long-term/stakeholder-profiles.md`](../memory/long-term/stakeholder-profiles.md). Voice and emphasis come from here — the same investigation produces different one-pagers for a VP of Reliability versus a VP of Product.

**Lenses the agent runs by default before finalizing.** [Consultative](../.claude/agents/consultative-lens.md), [Customer](../.claude/agents/customer-lens.md), and [Skeptic](../.claude/agents/skeptic-lens.md), often in parallel.

**The gate question.** *"Is this ready to send to the named stakeholder?"* — asked separately for the one-pager and the deck.

## What every gate looks like, in practice

At each gate the agent **stops and presents**. You always have three responses available:

| Response | What it does |
|---|---|
| **Approve** | Agent proceeds to the next phase. |
| **Redirect** | You change scope, framing, or priority. Agent updates artifacts and re-presents. |
| **Iterate through a lens** | You ask for re-review through one of the six lenses. Agent revises before re-presenting. See [lenses.md](lenses.md) for what each lens catches. |

Every gate decision is appended to [`memory/project-space/decisions-log.md`](../memory/project-space/decisions-log.md). That file is the audit trail — if anyone asks weeks later *"why did we pursue that hypothesis?"*, the answer is there.

## Look inside

| What you'll find | Where to look |
|---|---|
| The operating manual the agent reads on every session | [`CLAUDE.md`](../CLAUDE.md) |
| All eight phase skills | [`skills/`](../skills/) |
| The six critique lenses and the doc-freshness-checker | [`.claude/agents/`](../.claude/agents/) |
| The live investigation state (during a session) | [`memory/project-space/`](../memory/project-space/) |
| The audit trail for the current investigation | [`memory/project-space/decisions-log.md`](../memory/project-space/decisions-log.md) |
