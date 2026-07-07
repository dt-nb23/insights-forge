# Pilot Round 2 — Intake Form + Guardrails Design

**Date:** 2026-07-06
**Status:** Approved by Nate (2026-07-06)
**Driver:** Leadership/pilot feedback (Ben, Julie, Jeremy) on output variability, thin inputs, analyst-skill dependence, and deliverable density.

## Problem statement

The pilot produced wildly different results across analysts because quality depended on (a) how much context the analyst volunteered and (b) how well they prompted. The best output (U-Haul) came from a power user with deep context; the tool must produce sign-off-quality plans from any analyst. Specific failures: the agent accepted thin inputs without pushback, recommended a capability (Biz Events) with no account-specific basis, produced dense one-pagers, stalled with no recovery path, and confused Classic vs Grail capability generations.

**Success criterion for this phase (Ben):** "Would we sign off on this plan for any analyst" — not "did the customer execute on it."

## Rulings (settled decisions — do not re-litigate)

| Decision | Ruling |
|---|---|
| v1 form use-case scope | All four use cases in one form (executive one-pager / analyst execution guide / customer action plan / QBR-renewal brief). Pilot can still be run narrowly by instruction. |
| Input depth enforcement | Tiered form + agent probes. Required core tier blocks generation; optional depth upgrades output tier; thin answers get soft nudges in the form and max one follow-up each from the agent. |
| Raw query examples | Pseudo-query middle ground in conversation; **markdown deliverables may carry illustrative, editable query examples labeled unvalidated**. DQL is Gen3/Grail-only; USQL for Classic RUM. Agent never executes queries. Future: Dynatrace-published query skill repos as a source. |
| Early exit from mandatory lenses | **No opt-out.** Lenses stay strictly mandatory per `docs/lenses.md`. |

## Architecture (Approach 1 — layered changes in existing structure)

Input rigor lives in the form (deterministic, analyst-independent). Output rigor lives in CLAUDE.md operating rules (session-wide). Phase-local behavior stays in the phase SKILL.md files. No new session-startup reads.

---

## 1. Intake form — `html/intake-form.html` (new) + published Artifact

Single self-contained HTML file: no external requests (CDN, fonts, images), works offline from the repo and as a claude.ai Artifact. Dynatrace brand styling — navy `#07101e`/`#0d1f38` surfaces, teal `#49C2B3` / royal blue `#1966FF` accents, magenta `#C93FDB` reserved for warnings/gaps, system font stack (Artifacts CSP blocks font loads; DT Flow `@font-face` may be attempted with local file fallback to Arial when opened from repo).

The analyst fills the form → clicks **Generate seed prompt** → gets a structured markdown brief in a textarea with **Copy to clipboard** and **Download .md** buttons. The analyst pastes the brief as their first message in a Claude Code session.

### Form sections and field inventory

Order as listed. "Required" fields block generation when empty; all others optional.

**S1 — Use case** (required; radio, 4 options)
Executive one-pager · Analyst execution guide · Customer action plan · QBR / renewal brief.
First question on the form. Sets the Phase 3 deliverable target and drives conditional visibility/labels in later sections.

**S2 — Analyst context** (required; three dropdowns)
- Analyst experience with Insights Forge + Dynatrace consulting: `new / intermediate / expert`
- Account familiarity: `new-to-me / familiar / deep history`
- Customer's own domain fluency (how well the customer knows observability/Dynatrace): `low / mixed / high`

**S3 — Customer basics** (required)
- Customer name — text
- Vertical — dropdown: Retail/E-commerce, FSI, Healthcare/Life Sciences, Manufacturing, Telco/Media, Public Sector, Technology/SaaS, Logistics/Supply Chain, Other (reveals free text)
- Company size — dropdown: SMB / mid-market / large enterprise / unsure
- Tenant type — radio: SaaS / Managed / unsure

**S4 — Engagement framing (C.S.I.R.)**
- **Context** (required) — textarea: relationship history, mood, recent milestones. Plus consultant role dropdown: CSM / SE / consultant / other.
- **Specific information** (required) — textarea: known pain points, prior QBR outcomes, commitments, constraints.
- **Intent** (required) — goal dropdown: prove value / secure renewal / justify expansion / prepare QBR narrative / improve digital experience / diagnose a problem / other + textarea: what success looks like.
- **Response format** — mostly derived from S1. Additional: audience checkboxes (executive / technical / mixed), time window dropdown (15 min / 30 min / 60 min / async document), tone-or-branding constraints text (optional).

**S5 — Active capabilities** (required: at least one checked, or the "unsure — help me confirm" master checkbox)
Checkbox grid mirroring the Q5 list in `skills/context-framing/SKILL.md`, with a **generation sub-select** (Classic / Grail / both / unsure) on the four generation-split items:

- Core observability: Full-Stack (OneAgent) · Infrastructure only · APM/Distributed Tracing
- User experience: **RUM Web [gen]** · **RUM Mobile [gen]** · **Session Replay [gen]** · Synthetic Monitoring
- Data & logs: Log Management (Grail) · Business Analytics/Business Events · Metrics ingestion
- AI & automation: Davis AI · Davis CoPilot · Workflows/Automation
- Security: Application Security · Cloud Security
- Platform: Grail · Site Reliability Guardian · **Dashboards [Gen2/Gen3/both/unsure]** · Notebooks

**S6 — Focus application & RUM status** (always visible; becomes required when S4 Intent goal = "improve digital experience")
- Application name — text
- RUM enabled on this app — radio: yes / no / unsure
- Session Replay active on this app — radio: yes / no / unsure

**S7 — Stakeholders**
- Primary audience name + title — text
- Role archetype — dropdown of the 8 archetypes from `stakeholder-profiles.md` + "unsure"
- What leadership cares about (named KPIs, strategic priorities) — textarea (optional; tier-upgrading)
- Technical team priorities — textarea (optional; tier-upgrading)

**S8 — Engagement trigger** — dropdown: QBR / renewal / expansion / scheduled touchpoint / incident follow-up / other

### Tier mechanics (Julie's MVP model)

A live badge shows the promised output tier:

- **Simple** — required core only. Output: streamlined artifacts, more agent checkpoints, more explanatory framing.
- **Advanced** — upgrades when ALL of: (a) leadership KPIs textarea has substantive content, (b) technical team priorities has substantive content, and (c) at least one of prior-outcomes detail in Specific Information or a completed S6 section. "Substantive" = at or above the same ~15-word threshold the thin-answer nudge uses, from the shared JS config.

The badge updates on input events and states plainly what would upgrade it ("Add technical team priorities to unlock the Advanced plan").

### Thin-answer nudges (soft, never blocking)

Required textareas with fewer than ~15 words show an inline field-specific hint, e.g. Context: "A sentence or two more materially improves the plan — what changed, when, and who noticed?" The nudge changes styling (magenta accent) but never blocks generation. The word threshold and hint copy live in one JS config object for easy tuning.

### Seed prompt format (the form ↔ agent contract)

```markdown
# Insights Forge intake brief (v1)

> Agent: treat this as a seeded Phase 0 intake per skills/context-framing/SKILL.md.

## Meta
- Use case: <S1>
- Output tier: Simple | Advanced
- Analyst experience: <S2> · Account familiarity: <S2> · Customer domain fluency: <S2>

## Customer
- Name / Vertical / Size / Tenant type: <S3, one per line; unanswered = "not provided">

## Engagement framing (C.S.I.R.)
### Context
<S4-C + consultant role>
### Specific information
<S4-S>
### Intent
<S4-I goal + success criteria>
### Response format
<derived from S1 + S4-R audience/time/tone>

## Active capabilities
<S5 checked items with generation qualifiers; explicitly list "unsure" items>

## Focus application
<S6 or "not provided">

## Stakeholders
<S7; archetype + priorities>

## Trigger
<S8>
```

Every unanswered field renders as the literal string `not provided` — never omitted — so the agent can distinguish "analyst doesn't know" from "form didn't ask."

### Form acceptance criteria

1. Opens and functions with zero network requests (verify offline).
2. Generate is blocked until required core is complete; blocked state lists the missing fields.
3. Tier badge updates live and names the upgrade path.
4. Thin-answer nudges appear/disappear at the word threshold; never block.
5. Copy and Download produce the exact brief format above.
6. S6 required-flag toggles with the Intent goal selection.
7. Renders acceptably at 1280px+ desktop and degrades gracefully at tablet width (analysts may fill it on either).

---

## 2. Seeded-intake mode — `skills/context-framing/SKILL.md`

New subsection under Inputs/Steps: **"Seeded intake (form brief detected)."** Trigger: first user message contains the literal header `# Insights Forge intake brief`.

Behavior:

1. Parse every brief field onto the existing Q1–Q9 / C.S.I.R. structure. Fields with real values are **answered — do not re-ask**. Fields reading `not provided` are unanswered.
2. Run the thin-answer check on pre-filled MUST-HAVE fields: an answer of only a few words does not count as satisfied. **Ask at most ONE follow-up per thin field.** Whatever comes back — including "that's all I know" — is accepted and the residual gap is recorded in `current-context.md` under a new "Known context gaps" row. Never loop. This is the anti-wall rule.
3. Batch the SHOULD-HAVE confirmations into the single gate message (the existing "not required to proceed, but…" phrasing) rather than serial questions.
4. Record four new fields in `current-context.md` front-matter-adjacent body: **use case**, **analyst experience**, **account familiarity**, **customer domain fluency**, plus **output tier** (Simple/Advanced).
5. The use case binds the Phase 3 skill early (executive one-pager / execution guide / action plan / QBR brief → exec-onepager, action-plan-builder emphasis, or value-highlight). Downstream skills read output tier to scale artifact sophistication; analyst experience calibrates how much the agent explains and how often it checkpoints (new → more of both).
6. The exit-criteria rubric is unchanged — a seeded brief must still satisfy every MUST-HAVE before the gate; the brief just pre-populates it.

Unseeded sessions (no form) behave exactly as today, plus the same thin-answer rule now applies to conversational answers.

---

## 3. Cross-cutting guardrails — `CLAUDE.md` (short additions)

Four new operating rules, kept to a few lines each:

1. **Gate and question template.** Every phase gate and every mid-conversation question follows one shape: 2–3 sentence summary of what was just produced → the spelled-out choice (approve / redirect / name a lens) → pointer to the full artifact file. Any question the agent asks is the last, visually separated element of its message. Never a bare "does this look right?"
2. **No off-context capability recommendations.** Any recommended action or hypothesis that introduces a capability not already established as active or in-scope (per `current-context.md` Active capabilities) must be posed as a question to the analyst, never asserted as a recommendation.
3. **Stalled-session recovery.** If three consecutive turns produce no artifact progress (no phase file created or updated), proactively offer to pause and resume via `skills/investigation-reset/SKILL.md` rather than continuing.
4. **Query policy** (replaces "never generates raw DQL" bullets in operating principles and "What this agent does NOT do"): the agent never *executes* queries. In conversation and working artifacts it describes query logic structurally (fetch X → filter Y → summarize Z). In markdown deliverables it MAY include illustrative query examples clearly labeled "unvalidated — verify before use," and only version-correctly: DQL only where Grail/Gen3 is confirmed active for that data type; USQL for Classic RUM. If the generation is unconfirmed, no example — name the gap instead.

Also in CLAUDE.md: one line noting Phase 1 checkpoint mode and the Phase 2 direction check exist and are ON by default (details live in the phase skills).

---

## 4. Phase pacing — checkpoint mode and direction check

**Phase 1 checkpoint mode (default ON; labeled setting).** Documented once in CLAUDE.md's workflow section and implemented as a short "Checkpoint" step at the end of `mece-decomposition`, `hypothesis-generation`, and `signal-mapping` SKILL.md files: after producing the artifact, pause for a quick confirmation (using the gate/question template) before starting the next artifact. When a structuring call is genuinely ambiguous — decomposition axis, playbook match — ask rather than silently choose. The setting is named ("Phase 1 checkpoint mode") so the team can turn it off later; turning it off restores today's single end-of-phase gate.

**Phase 2 direction check.** `action-plan-builder/SKILL.md` gains a step before the persona council: draft a one-screen skeleton — headline framing, wave/phase structure, candidate action list (titles only, no detail) — and pause for confirmation using the gate template. Only after confirmation does the full draft + 3-round council + ICE re-rank run. Redirects at the skeleton cost minutes, not a rebuilt plan (Ben's "reduce upfront over-creation").

---

## 5. Deliverable consistency — `skills/exec-onepager/SKILL.md` (+ pptx-builder note)

Content-structure changes:

1. **TL;DR:** one bold sentence at the very top, before the problem summary — what's happening and what's being asked.
2. **Recommended actions restructured as a 30/60/90-day phased plan** (three labeled blocks) replacing the flat list. Each action keeps owner + timeframe + cost/risk on the same line. Rank order within each block still mirrors action-plan.md (plan-fidelity gate extends to block assignment).
3. **Density target: 450–550 words of prose (~2–3 minute read)**, enforced alongside the one-page constraint. Word count is checked at the finalizing gate; over target → cut, don't compress.
4. **Fixed section order** for every one-pager regardless of analyst: TL;DR → Situation → Business impact → Key findings → Recommended actions (30/60/90) → Decision asks → Sources. This is the consistency needed for eventual Salesforce attachment.
5. **Embedded anonymized exemplar:** a structural skeleton derived from the U-Haul one-pager (section shapes, finding-card pattern with color assignments, decision-ask pattern) embedded in the skill file itself. Client isolation forbids the skill from referencing `memory/clients/u-haul/`; we extract the shape, not the client content.

`skills/pptx-builder/SKILL.md` gets a note: deck agenda inherits the 30/60/90 structure from the markdown one-pager.

---

## 6. Version-accuracy audit — `memory/long-term/` (writes need user approval)

1. New **"Capability generations"** section in `domain-knowledge.md`: Classic RUM vs RUM on Grail (queryability USQL vs DQL, gesture-level events, session action limits, OpenPipeline), Session Replay Classic vs on Grail, Dashboards Gen2 vs Gen3, classic custom metrics vs Grail metrics — each with doc citations. Standing rule stated there and cross-referenced from playbooks: **both generations can be active on the same client simultaneously; confirm which is active before assuming a capability or query path.**
2. **Audit pass** over `dynatrace-playbooks.md` and the rest of `domain-knowledge.md` for version-ambiguous statements (any claim that silently assumes one generation). Run as a parallel multi-agent sweep at implementation time; findings presented as a proposed edit list for approval before any long-term memory file changes (memory rules require explicit approval).
3. The Q5 capability checklist in `context-framing` and the intake form's S5 grid carry the generation split (done in sections 1–2 above).

---

## File-change inventory

| File | Change |
|---|---|
| `html/intake-form.html` | **New** — the form (section 1) |
| `skills/context-framing/SKILL.md` | Seeded-intake mode, thin-answer rule, 4 new fields, generation split in Q5 |
| `CLAUDE.md` | 4 guardrail rules + query-policy rewrite + pacing flags |
| `skills/mece-decomposition/SKILL.md` | Checkpoint step |
| `skills/hypothesis-generation/SKILL.md` | Checkpoint step |
| `skills/signal-mapping/SKILL.md` | Checkpoint step |
| `skills/action-plan-builder/SKILL.md` | Direction-check skeleton step |
| `skills/exec-onepager/SKILL.md` | TL;DR, 30/60/90, word target, fixed order, exemplar |
| `skills/pptx-builder/SKILL.md` | 30/60/90 inheritance note (light) |
| `memory/long-term/domain-knowledge.md` | Capability generations section (approval-gated) |
| `memory/long-term/dynatrace-playbooks.md` | Version-ambiguity fixes from audit (approval-gated) |
| `docs/workflow.md`, `docs/getting-started.md`, `docs/deliverables.md` | Light: intake-form entry path, one-pager spec, pacing notes |
| `ROADMAP.md` | Record the four rulings; new "Pilot round 2 — committed" section |

## Out of scope (named so they aren't silently dropped)

- Licensing/seat expansion (Julie has requested 8 licenses) and Claude Code scalability to the full team — organizational.
- Copilot/OneDrive-style governance concerns — organizational/policy; the workspace's existing client-isolation rules are the codebase-side answer and are unchanged.
- Salesforce/CRM and Slack AI auto-pull integration — already ROADMAP Tier 1; unchanged.
- Customer-execution success metrics — Ben's phase 2 metric, not this round.
- Leadership review/approval before customer-facing use — process, not code; noted in ROADMAP.
