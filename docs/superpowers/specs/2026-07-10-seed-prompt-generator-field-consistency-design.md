# Seed Prompt Generator — reorder + field-consistency pass (round 3)

## Context

Builds on round 2 (`2026-07-10-seed-prompt-generator-ia-restructure-design.md`, implemented — 9-step form). This round applies leadership feedback: a small reorder, one field merge, a required-default on "Your role", a form-wide vocabulary change to **Required / Recommended / Optional**, and a consistency pass adding a requirement chip **and** a one-line "why/what" helper to every field.

Same mechanics as prior rounds: edit `html/seed-prompt-generator-src.html`, re-pack to `html/Insights Forge (Seed Prompt Generator) - Draft.html`. Tracked bundle and `- Original.html` stay untouched.

## Out of scope

- Replacing the tracked bundle (separate later decision).
- `docs/seed-prompt-generator.md` (already a pending follow-up; will now also cover the vocabulary change away from MUST/SHOULD/NICE).
- Fonts, palette, header.

## Step reorder (stays 9 steps, indices 0–8)

| # (idx) | Step | Change from round 2 |
|---|---|---|
| 1 (0) | Outputs & trigger | **Outputs first, then trigger** (flip); rename trigger `scheduled touchpoint` → **Client Conversation** |
| 2 (1) | Analyst context | Your role becomes **Required + default**; scales become **Optional** |
| 3 (2) | Customer basics | **Relationship & context removed** (moves to Pain step) |
| 4 (3) | Stakeholders & audience | unchanged fields |
| 5 (4) | **Pain & constraints** | now holds **Relationship & context** (folded in) **then** Pain & constraints; both Required |
| 6 (5) | **Goals & success criteria** | moved to **after** Pain (was before) |
| 7 (6) | Active capabilities | unchanged |
| 8 (7) | Out of scope | unchanged |
| 9 (8) | Focus applications & RUM | unchanged |

## Vocabulary change (global)

Replace the three requirement levels everywhere in the analyst-facing UI **and** in the generated brief:

- `Must-have` / `Must` → **Required**
- `Should-have` / `Should` → **Recommended**
- `Nice` → **Optional**

Touch points: section-header chips, per-field chips, the `s6TagLabel` conditional (Focus apps), the live-preview panel ("once every Must-have is filled" → "once every Required field is filled"), the intro screen ("Must-haves unlock Copy/Download" → "Required fields unlock Copy/Download"), and the brief preamble (`Must-have context` → `Required context`, `Should-have context` → `Recommended context`). The dashed-outline chip style used for the old "Nice" is kept; only its text changes to "Optional".

Section-header chips now reflect the section's highest requirement level: Outputs, Analyst, Customer basics, Stakeholders, Pain, Goals, Capabilities → **Required**; Out of scope → **Recommended**; Focus apps → conditional Required/Recommended (unchanged logic). The Analyst header's old "Rate 1–5" tag becomes **Required**.

## Per-field requirement chip + why-line

Every discrete field (input, select, textarea, pill-group) gets a requirement chip on its label and a one-line muted "why/what" helper beneath the label. Repeated-card grids (Active capabilities, Out of scope, Focus applications) keep their existing **section-level** why + chip — individual checkboxes/app-rows are not chipped. Where guiding text already exists (textareas), it is reused as the why-line.

| Step | Field | Chip | Why-line |
|---|---|---|---|
| 1 | Requested output formats | Required | Which presentation formats to build on top of the always-produced action plan. |
| 1 | Engagement trigger | Optional | What prompted this engagement — shapes urgency and tone. |
| 2 | Your role | Required | Your seat in the account — calibrates how the plan is framed and who owns follow-through. |
| 2 | Experience with Dynatrace consulting | Optional | Your depth here — tunes how much the plan explains vs. assumes. |
| 2 | Account familiarity | Optional | How well you know this account — sets how much discovery to prompt. |
| 2 | Customer's Dynatrace Maturity | Optional | How advanced they are on Dynatrace — sets the ambition ceiling. |
| 3 | Customer name | Required | Who this engagement is for. |
| 3 | What the business does | Required | One line on their business — grounds every recommendation. |
| 3 | Vertical | Required | Industry — shapes benchmarks, compliance, and relevant use cases. |
| 3 | Customer size (ACV) | Optional | Commercial tier — sets plan ambition and pace. |
| 3 | Tenant type | Recommended | SaaS or Managed — affects what's available and how you reference it. |
| 3 | Customer region(s) | Recommended | Where they operate — local laws (e.g. GDPR) may constrain the plan. |
| 4 | Name & title | Recommended | Who'll read or influence this — a real name sharpens the output. |
| 4 | Role archetype | Required | Their function — Phase 3 maps deliverables to it. |
| 4 | Communication level | Recommended | How technical this person's read should be. |
| 4 | What they care about | Recommended | The KPIs or outcomes they judge success by. |
| 5 | Relationship & context | Required | Where the relationship stands — history, mood, recent milestones. |
| 5 | Pain & constraints | Required | The team's day-to-day pain and anything limiting the plan. |
| 6 | Intent — goals | Required | What Dynatrace wants from this engagement. |
| 6 | What success looks like | Required | What the customer would call success — the observable "after". |
| 7 | Active capabilities (section) | Required | (existing section why — the boundary of what insight can surface.) |
| 8 | Out of scope (section) | Recommended | (existing section why — a hard do-not-suggest boundary.) |
| 9 | Focus applications (section) | Required/Recommended (conditional) | (existing `s6Why`.) |

## "Your role" — Required default

- Default `state.answers.role = 'Insights Analytics Consultant'`.
- The `<select>` drops its blank `<option value="">— select —</option>` so it always carries a value (a Required field that auto-satisfies the gate, mirroring the stakeholder-archetype pattern). Options otherwise unchanged (CSM / SE / Consultant / Insights Analytics Consultant / Other).

## Validation (`_secData`, `missing`) — new index map

Relationship (`context`) moves from Customer basics to the Pain step; Pain and Goals swap positions; `role` becomes required.

- 0 Outputs & trigger — `fields:[F(outputs), F(triggers)]`, `req:[F(outputs)]`
- 1 Analyst context — `fields:[F(role), !!anyScale]`, `req: anyScale ? [F(role), !!allScale] : [F(role)]`
- 2 Customer basics — `fields:[F(customerName), vertOk, F(customerDesc), F(size), F(regions)]`, `req:[F(customerName), vertOk, F(customerDesc)]` (context removed)
- 3 Stakeholders & audience — `fields:[stakeholders touched]`, `req:[stkOk]`
- 4 Pain & constraints — `fields:[F(context), F(painConstraints)]`, `req:[F(context), F(painConstraints)]`
- 5 Goals & success — `fields:[F(intents), F(intentSuccess)]`, `req:[F(intents), F(intentSuccess)]`
- 6 Active capabilities — `fields:[nonDavis]`, `req:[nonDavis]`
- 7 Out of scope — `fields:[F(outOfScope), F(outOfScopeNotes)]`, `req:[]`
- 8 Focus applications — `fields:[apps touched]`, `req: s6Req() ? [appOk] : []`

`missing()` adds nothing user-visible for `role` (default is non-empty, never missing) but the context/relationship entry stays (message already reads "Customer context (relationship & history)" — reword to "Relationship & context"). Pain/Goals/other checks unchanged in content, only their ordering reflects the new flow.

## Brief (`buildBrief`) impact

- Preamble: `Must-have context` → `Required context`, `Should-have context` → `Recommended context` (per the round-3 choice to align the brief with the UI). The stakeholder clause and the capability/out-of-scope rules are unchanged.
- The `Relationship & context` line stays under `## Customer context` in the brief (brief layout is independent of which UI step captures the field — established pattern). No other brief structural change; `## Pain & constraints` and `## Goals & success criteria` sections keep their content, order unchanged in the brief.

## Verification

Headless Chromium (as prior rounds):
- New order: Step 1 shows outputs above trigger; the trigger option reads "Client Conversation" (not "scheduled touchpoint"); Step 5 shows Relationship & context above Pain & constraints; Step 6 is Goals & success.
- Every field shows a chip reading Required / Recommended / Optional and a why-line; no "Must-have"/"Should"/"Nice" text remains in the UI.
- "Your role" defaults to "Insights Analytics Consultant" and has no blank option; export unlocks without touching it.
- Export gate: Relationship & context and Pain & constraints both block until filled (both Required); role never blocks.
- Brief preamble reads "Required context"/"Recommended context"; the trigger line shows "Client Conversation" when selected.
- No bundler/console errors; theme dots still amber/crimson.
