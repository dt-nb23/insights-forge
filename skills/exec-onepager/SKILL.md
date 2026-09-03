---
name: exec-onepager
description: Procedure for producing the Phase 3 exec-ready one-page written deliverable. Use after the action plan has been approved.
---

# Exec one-pager

## When to use

The **Phase 3 written deliverable.** Use after the Phase 2 action plan is explicitly approved and the deliverable is destined for a named senior technical leader (VP of Engineering, Director of Reliability, Head of Data Analytics, or similar).

## Inputs

**Resolve `ENGAGEMENT_PATH` first.** Use the path established at Phase 0. If no engagement is active, run the resume procedure in `skills/investigation-reset/SKILL.md`.

Read these files before starting. Each is required.

| File | Purpose |
|---|---|
| `<ENGAGEMENT_PATH>/action-plan.md` | Source of truth for recommendations, rank order, owners, timeframes, and tradeoffs |
| `<ENGAGEMENT_PATH>/signals-map.md` | Business impact numbers and SLI/SLO grounding |
| `<ENGAGEMENT_PATH>/hypotheses.md` | Confirmed/open/ruled-out status of each hypothesis |
| `memory/long-term/stakeholder-profiles.md` | Named reader profile — governs recipe selection, depth, and tone |
| `memory/long-term/terminology.md` | First-use definitions for any acronym |
| `memory/long-term/brand/brand-spec.md` | **Mandatory.** Voice, typography, product names, footer text |

If no matching stakeholder profile exists, ask the user which profile to use before proceeding.

## Five steps

Run in order. Read the referenced file immediately before that step — do not pre-load all step files at once.

---

### Step 1 — Recipe selection

Read `skills/exec-onepager/reference/layout-system.md`.

Before selecting any component, answer these three questions from the engagement files:

1. **What is the narrative tension?** What changed or went wrong, and what does the plan resolve? (This determines how the problem should land — as a claim, a table, a quote, or a number.)
2. **What does this reader need to feel, understand, or decide by the end?** (This determines how the takeaway and stakes should be structured — explicit decisions, a binary choice, or a confident close.)
3. **What is the strongest evidence in this plan?** Is it quantified metrics, named capabilities, phase ownership, or a stakeholder's own words? (This determines which guide and plan components carry the most weight.)

Select each component based on those answers, not by defaulting to a base recipe and swapping. The component catalog in layout-system.md describes what each variant does and when it works — use it as a menu, not a template.

Record the selected recipe and a `Why:` rationale sentence before proceeding. The rationale must name the narrative logic, not just the component names.

---

### Step 2 — Content draft

Read `skills/exec-onepager/steps/1-content-assembly.md`.

Draft all copy for each component in the recipe. Produce structured labeled text, not HTML. Follow the plan-fidelity rules in that file — do not re-rank recommendations, introduce new findings, or upgrade open hypotheses to confirmed claims.

---

### Step 3 — Brand-humanizer pre-pass

Read `skills/brand-humanizer/SKILL.md`.

Run the full brand-humanizer procedure on every piece of drafted copy: TL;DR sentence, problem section, guide section, plan steps, stakes framing, takeaway line, and all decision asks.

This step runs **before** the HTML is built. Fixing copy inside finished HTML is expensive; fixing it in structured text is not. Deliver corrected copy before proceeding to step 4.

---

### Step 4 — HTML build

Read `skills/exec-onepager/steps/2-html-renderer.md`.

Build the HTML using the humanized copy and the selected recipe. Follow the component patterns from `reference/layout-system.md` exactly — do not improvise CSS or invent color values.

Write the HTML to `<ENGAGEMENT_PATH>/<slug>-onepager.html` — inside the engagement folder, never the repo root or `html/`. Write the companion markdown to `<ENGAGEMENT_PATH>/one-pager-YYYY-MM-DD.md`.

---

### Step 5 — Brand gate

Read `skills/exec-onepager/steps/3-brand-gate.md`.

Run the gate checklist: one-page constraint, plan fidelity, brand text rules, accessibility, sources block, and handoff readiness. Do not mark the deliverable done until every item passes.

---

## Output

- `<ENGAGEMENT_PATH>/<slug>-onepager.html` — the one-pager HTML lives inside the engagement folder, never the repo root or `html/`
- `<ENGAGEMENT_PATH>/one-pager-YYYY-MM-DD.md` companion (required before the pptx step)

After the brand gate passes, **present the Phase 3 gate for the one-pager** (the five-part gate summary block defined in `steps/3-brand-gate.md`) and wait for explicit approval. On approval, record the decision in `<ENGAGEMENT_PATH>/decisions-log.md` and set today's `last-touched:` in `<ENGAGEMENT_PATH>/current-context.md` (`phase:` is already `3`). Do not invoke the pptx-builder automatically — the deck is a separate approval.

## What Phase 3 does not do

- Re-open findings, re-rank recommendations, or introduce new evidence. All of that was settled at the Phase 2 gate.
- Run critique lenses. The Phase 2 persona panel already reviewed the plan. Phase 3 packages it faithfully.
- Auto-generate the deck. The Phase 3 gate is the one-pager. The PPTX step requires explicit user approval.
