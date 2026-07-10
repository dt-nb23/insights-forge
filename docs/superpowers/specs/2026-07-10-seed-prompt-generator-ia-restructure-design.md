# Seed Prompt Generator — information-architecture restructure (round 2)

## Context

Round 1 (`2026-07-10-seed-prompt-generator-ux-revisions-design.md`, already implemented on branch `seed-prompt-generator-ux-revisions`) added leadership-feedback UX changes to the Seed Prompt Generator and produced `html/Insights Forge (Seed Prompt Generator) - Draft.html` via the extract → edit → re-pack tooling (`tools/seed-prompt-generator-bundle.py`, source at `html/seed-prompt-generator-src.html`).

Round 2 restructures the form's information architecture to reduce redundant/overlapping questions and break the single dense "Engagement framing · C.S.I.R." page into shorter sequential steps. It is a cohesive refactor of the same source file — state shape, section markup, navigation, validation, and the generated brief all move together.

This spec builds on the round-1 output. It continues to edit `html/seed-prompt-generator-src.html` and re-pack to `html/Insights Forge (Seed Prompt Generator) - Draft.html`. The tracked shipped bundle and `- Original.html` remain untouched.

## Out of scope

- Replacing the tracked/shipped bundle (`html/Insights Forge (Seed Prompt Generator).html`). Still a separate later decision.
- Updating `docs/seed-prompt-generator.md` (which describes the current 10-section form). Confirmed as a **separate follow-up**, not part of this round.
- Any change to the pack/unpack tool, fonts, palette, or header hero.
- Adding trigger→output auto-suggestion logic (explicitly declined — trigger is captured only).

## Current structure (before)

10 steps + Review, indices 0–9, `STEP_TITLES` = `['Requested outputs','Analyst context','Customer basics','Engagement framing','Active capabilities','Out of scope','Focus applications','Stakeholders','Technical priorities','Trigger']`, `REVIEW = 10`.

The dense step 3 ("Engagement framing · C.S.I.R.") bundles: Context textarea (C), Your role dropdown, Specific information textarea (S), Intent goals pills (I), success textarea, and a Response-format block (audience pills + meeting/read-time window select + tone/branding input).

## Target structure (after)

9 steps + Review, indices 0–8, `REVIEW = 9`.

| # (idx) | Step title | Fields (in order) | Required-to-export (Must) |
|---|---|---|---|
| 1 (0) | **Outputs & trigger** | Trigger (multi-select, optional) · Requested output formats (cards) | ≥1 output format |
| 2 (1) | **Analyst context** | Your role (dropdown) · 3 self-calibration scales | none blocking; "rate all three once you rate one" (unchanged) |
| 3 (2) | **Customer context** | name · what-they-do · vertical (+other) · ACV · tenant · regions · relationship/context textarea | name, what-they-do, vertical, context |
| 4 (3) | **Stakeholders & audience** | per stakeholder: name&title (Should) · role archetype · **technical level** · what they care about | ≥1 stakeholder archetype (auto-satisfied by default) |
| 5 (4) | **Goals & success criteria** | Intent goals (pills) · what success looks like (textarea) | goals ≥1, success text |
| 6 (5) | **Pain & constraints** | one merged textarea + combined starter chips | pain-and-constraints text |
| 7 (6) | **Active capabilities** | (unchanged) | ≥1 capability beyond Davis, or "unsure" |
| 8 (7) | **Out of scope** | (unchanged) | none |
| 9 (8) | **Focus applications & RUM** | (unchanged) | conditional-Must if Intent includes "improve digital experience" |

## Field-level changes

### Moved
- **Your role** (analyst dropdown: CSM/SE/Consultant/Insights Analytics Consultant/Other): from old Engagement-framing step → **Analyst context** step. State key `role` unchanged; only its render location moves.
- **Relationship/context textarea** (the "Context (C)" field, state key `context`, with its guiding text + starter chips): from old Engagement-framing step → **Customer context** step. Stays a Must-have.
- **Trigger** (state key `triggers`, multi-select pills): from its own final step → **Outputs & trigger** step (index 0), rendered above/with the output-format cards. Stays optional. Captured only — selecting a trigger does not change output selection.
- **Intent goals** (`intents`) + **what success looks like** (`intentSuccess`): from old Engagement-framing step → **Goals & success criteria** step. Both stay Must-have.

### Merged
- **Specific information** (`specific`, was Must) **+ Technical team priorities** (`techPriorities`, was optional) → a single new field **`painConstraints`** in the **Pain & constraints** step. Tagged **Must-have** (preserves Specific info's old gating). One textarea with a merged guiding line and combined starter chips drawn from both former fields:
  - from Specific info: "Prior QBR commitment", "Regulated / limited data", "Known pain point", "Renewal, budget scrutiny"
  - from Technical priorities: "Alert noise", "Slow root cause", "Tool sprawl", "Manual toil", "On-call load"
- **Audience** (form-level `audience` Exec/Technical/Mixed pills) → folded into each stakeholder as a per-stakeholder **technical level** dropdown (see Added).

### Added
- **Per-stakeholder technical level**: a new dropdown on each stakeholder card with options **Executive / Technical / Mixed**, defaulting to **Mixed**. New key `level` on each stakeholder object (`{name, archetype, level, cares}`). Sits between "role archetype" and "what they care about". Because it defaults to Mixed it is never blank and never blocks export.

### Removed outright
- Form-level **Audience** field (`audience`) and its Must-have gate.
- **Meeting/read-time window** select (`timeWindow`).
- **Tone/branding constraints** input (`tone`).
- **`specific`** and **`techPriorities`** state keys (replaced by `painConstraints`).
- The **"· C.S.I.R."** branding and the old Engagement-framing section wrapper (its fields are now distributed across steps 3–6).

## State shape changes (`this.state.answers`)

- Add `painConstraints: ''`.
- Remove `specific`, `audience`, `timeWindow`, `tone`, `techPriorities`.
- Stakeholder object shape becomes `{ name:'', archetype:'Stakeholder — role to be confirmed', level:'Mixed', cares:'' }` — in the initial seed and in `addStk()`.
- `FREE` map (the guiding/tip/chips config for textareas) becomes `{ context, intentSuccess, painConstraints }` — drop `specific` and `techPriorities`, add `painConstraints` with the merged guiding/tip and combined chips listed above.

## Constants

- `STEP_TITLES = ['Outputs & trigger','Analyst context','Customer context','Stakeholders & audience','Goals & success','Pain & constraints','Active capabilities','Out of scope','Focus applications']` (9 entries).
- `REVIEW = 9`.
- The `show` object loop bound changes from `< 10` to `< 9`.

## Validation (`_secData`, `missing`)

`_secData(i)` required/fields mapping by new index:

- 0 Outputs & trigger — `fields:[F(outputs), F(triggers)]`, `req:[F(outputs)]`
- 1 Analyst context — `fields:[!!anyScale, F(role)]`, `req: anyScale ? [!!allScale] : []` (unchanged scale logic; role optional)
- 2 Customer context — `fields:[F(customerName), vertOk, F(customerDesc), F(size), F(regions), F(context)]`, `req:[F(customerName), vertOk, F(customerDesc), F(context)]`
- 3 Stakeholders & audience — `fields:[stakeholders touched]`, `req:[stkOk]` where `stkOk = a.stakeholders.some(s => F(s.archetype))` (unchanged from round 1)
- 4 Goals & success — `fields:[F(intents), F(intentSuccess)]`, `req:[F(intents), F(intentSuccess)]`
- 5 Pain & constraints — `fields:[F(painConstraints)]`, `req:[F(painConstraints)]`
- 6 Active capabilities — `fields:[nonDavis]`, `req:[nonDavis]`
- 7 Out of scope — `fields:[F(outOfScope), F(outOfScopeNotes)]`, `req:[]`
- 8 Focus applications — `fields:[apps touched]`, `req: this.s6Req() ? [appOk] : []`

`secTouched` and `dotState` (done/required/neutral, round-1 form) are unchanged.

`missing()` list becomes: requested output, analyst-all-three-if-any, customer name, what-they-do, vertical, relationship/context, goals, success, **pain & constraints**, capability-beyond-Davis, focus-app (conditional), stakeholder archetype. The **audience** entry is removed; the `specific` entry becomes the `painConstraints` entry with an updated message.

## `renderVals()` view-model changes

- `freeVM` now iterates the new `FREE` keys (`context`, `intentSuccess`, `painConstraints`).
- Remove `audienceOptions` from the view-model.
- Stakeholder view-model gains `level` + an `onLevel` handler + a `levelOptions` (or inline `<select>`); each stakeholder renders its level dropdown.
- `triggers` view-model stays; its markup moves into the step-0 section.
- Remove template references to `answers.timeWindow` and `answers.tone`.
- `navItems` derives from the 9-entry `STEP_TITLES`; the Review push keeps round-1's `dotFor(canExport ? 'done' : 'required')`.

## Generated brief (`buildBrief`) restructure

The brief reorganizes to mirror the new steps while preserving the "For the agent — read first" preamble and the Must/Should categorization. New section order and content:

```
# Insights Forge intake brief
> **For the agent — read first.** … (preamble; Must/Should lists updated below)

## Requested outputs & trigger
- Baseline (always): Customer action plan
- Additional formats: <outputs or "none selected (action plan only)">
- Trigger(s): <triggers or "not provided">
- Analyst: role <role>; experience <x/5>, account familiarity <x/5>, customer Dynatrace maturity <x/5>
- Generated: <date>

## Customer context
- Name: … / What they do: … / Vertical(s): … / Customer size (ACV): … / Tenant type: … / Region(s): …
- Relationship & context: <context>

## Stakeholders & audience
- <name or (unnamed)> · <archetype> · communication level: <level> — cares about: <cares or "not provided">
  (one line per stakeholder)

## Goals & success criteria
- Goals: <intents>
- Success looks like: <intentSuccess>

## Pain & constraints
<painConstraints>

## Active capabilities
<caps>

## Out of scope / do not suggest
<oos>

## Focus applications
<apps>
```

Preamble Must/Should lists update to:
- **Must-have context** — Requested outputs, Customer (name / what-they-do / vertical), Customer context (relationship), Goals + success criteria, Pain & constraints, Active capabilities, and at least one Stakeholder (role archetype required; a named person strongly preferred).
- **Should-have context** — Analyst calibration + role, Tenant, Customer region(s), per-stakeholder communication level & priorities, and Trigger.
- The "active capabilities are the boundary" and "out of scope is a hard exclusion" rules are unchanged.

The removed fields (`timeWindow`, `tone`) drop from the brief entirely; `audience` is replaced by the per-stakeholder communication level.

## Implementation shape

This is a cohesive refactor, not independent edits: the section markup references view-model keys, which reference state keys, which drive validation and the brief. Intermediate states may not render cleanly. The plan will therefore use a few larger coordinated tasks (e.g. logic+markup restructure as one; brief restructure as another; end-to-end verification as a third) rather than many tiny ones, each verified by re-packing and loading the Draft in headless Chromium.

Wherever a field merely moves (Your role, Context, Trigger, Intent, success), the implementation reuses that field's existing markup (inputs, pills, chips, styles) so behavior and styling carry over unchanged — only its containing section and the `showSecN`/badge/`data-screen-label` wrappers change.

## Verification

No build step; verification is driving the re-packed Draft in real headless Chromium (the harness proven in round 1):
- All 9 steps navigate; nav rail shows 9 sections + Review; no bundler/console errors.
- Step 1 shows Trigger + output cards together; Step 2 shows Your role with the scales; Step 3 shows the relationship/context textarea with customer basics; Step 4 shows a per-stakeholder technical-level dropdown defaulting to Mixed; Step 5 shows goals + success; Step 6 shows the single merged Pain & constraints textarea with combined chips.
- Removed fields (audience, time window, tone) are absent everywhere.
- Export gate: Copy/Download enable once all new Must-haves are filled; the removed audience gate no longer blocks; the per-stakeholder level never blocks.
- Generated brief contains the new section order, the trigger line, per-stakeholder communication level, and the merged Pain & constraints section, and omits timeWindow/tone.
