# Seed Prompt Generator — reorder + field-consistency — Implementation Plan

> REQUIRED SUB-SKILL: executing-plans / inline. Source of truth for microcopy and the index map is the spec: `docs/superpowers/specs/2026-07-10-seed-prompt-generator-field-consistency-design.md`.

**Goal:** Apply round-3 feedback to `html/seed-prompt-generator-src.html`: flip outputs/trigger, rename `scheduled touchpoint`→`Client Conversation`, make Your role a required default, fold Relationship & context into the Pain step, move Goals after Pain, switch vocabulary to Required/Recommended/Optional (UI + brief), and add a chip + why-line to every field.

**Architecture:** Atomic single-file refactor; re-pack to the Draft; verify in headless Chromium; adversarial multi-lens review of the diff. Tracked bundle + Original.html untouched.

## Global Constraints
- Never modify `html/Insights Forge (Seed Prompt Generator).html` or `- Original.html`.
- Curly quotes / en-em dashes to match file style; no new deps.
- 9 steps (indices 0–8), REVIEW=9 (unchanged from round 2).
- Microcopy (chip + why per field) comes verbatim from the spec's field table.

## Task 1 — Logic edits (exact)

- [ ] **State: role default** — `context:'', role:'', intents:[]` → `context:'', role:'Insights Analytics Consultant', intents:[]`
- [ ] **TRIGGERS rename** — in `this.TRIGGERS`, `'scheduled touchpoint'` → `'Client Conversation'`
- [ ] **`_secData` grp** — replace indices 1,2,4,5 so role is required, context moves to the Pain step, and Pain/Goals swap:
```js
      1: { fields: [F(a.role), !!anyScale], req: anyScale ? [F(a.role), !!allScale] : [F(a.role)] },
      2: { fields: [F(a.customerName), vertOk, F(a.customerDesc), F(a.size), F(a.regions)], req: [F(a.customerName), vertOk, F(a.customerDesc)] },
      4: { fields: [F(a.context), F(a.painConstraints)], req: [F(a.context), F(a.painConstraints)] },
      5: { fields: [F(a.intents), F(a.intentSuccess)], req: [F(a.intents), F(a.intentSuccess)] },
```
(0,3,6,7,8 unchanged.)
- [ ] **`missing()`** — reword the context line and reorder relationship→pain→goals:
```js
    if (!a.context.trim()) m.push('Relationship & context');
    if (!a.painConstraints.trim()) m.push('Pain & constraints');
    if (!a.intents.length) m.push('Intent — pick at least one goal');
    if (!a.intentSuccess.trim()) m.push('What success looks like');
```
(replacing the current context/intents/intentSuccess/painConstraints four lines, in that new order.)
- [ ] **`buildBrief` preamble vocab** — `**Must-have context**` → `**Required context**`; `**Should-have context**` → `**Recommended context**`.

## Task 2 — UI vocab in fixed strings (outside the section markup)

- [ ] **Intro screen** (line ~440) — `10 short sections — Must-haves unlock Copy/Download` → `9 short sections — Required fields unlock Copy/Download`.
- [ ] **Preview panel** (line ~849) — `Copy / download unlock once every <span …>Must-have</span> is filled.` → `… once every <span …>Required field</span> is filled.`

## Task 3 — Section markup region rewrite (splice)

Replace the sections region (`<!-- SECTION 1 — Outputs & trigger -->` through the last section `</sc-if>` before `<!-- Review panel -->`) with a new region implementing, per the spec's field table:
- **Section 1:** Requested outputs block FIRST, then Trigger block. Chips: outputs=Required, trigger=Optional; why-lines from table.
- **Section 2:** Your role (Required; `<select>` drops the blank `<option value="">— select —</option>` so it always carries the default) + why; each of the 3 scales gets an **Optional** chip + why; section header chip → **Required**.
- **Section 3:** Customer basics WITHOUT the relationship block; every field gets its chip + why; ACV chip → **Optional**.
- **Section 4:** Stakeholders — each field (name/archetype/level/cares) gets its chip + why per table.
- **Section 5 → Pain & constraints:** Relationship & context textarea (moved from §3) FIRST, then the Pain & constraints textarea; both **Required** with why-lines; uses `free.context` and `free.painConstraints`.
- **Section 6 → Goals & success:** Intent goals + success (moved to after Pain); both Required with why-lines.
- **Sections 7–9:** Active capabilities / Out of scope / Focus apps — section-level chip + why only; convert header chips to Required / Recommended / conditional.
- Global: badges renumber 1–9; `data-screen-label`s updated; every `Must`/`Must-have`→Required, `Should`/`Should-have`→Recommended, `Nice`→Optional; `showSec0..8` mapping preserved (Section 5 markup gated by `showSec4`, Section 6 by `showSec5`).
- `s6TagLabel` in the view-model → `'Required'`/`'Recommended'`.

## Task 4 — Verify
- [ ] Pack; static grep: no `Must-have`/`>Must<`/`>Should<`/`>Nice<`/`scheduled touchpoint` remain in the file; `Client Conversation`, `Insights Analytics Consultant` default, `Required`/`Recommended`/`Optional` present; sc-if balanced.
- [ ] Headless Chromium: new order (outputs→trigger; Pain before Goals; relationship inside Pain), role defaulted + no blank option, every field shows a chip + why, gate blocks on relationship+pain, brief preamble reads Required/Recommended, trigger option reads "Client Conversation".
- [ ] Adversarial multi-lens review of the diff (correctness / spec-fidelity / orphaned-keys / microcopy) before finalizing.
