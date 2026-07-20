---
name: brand-gate
description: |
  Step 3 of the exec-onepager build. A mechanical pass/fail checklist that
  runs after the HTML is built. Do not mark the deliverable done until every
  item passes.
---

# Step 3 — Brand gate

Read this file at step 5 of the exec-onepager skill. The HTML is built. This is a verification pass, not a design review. Every item below is a binary pass/fail. Work through them in order.

**Phase 3 does not re-open findings or re-rank recommendations.** If a gate failure reveals a content problem (wrong recommendation order, a missing tradeoff), that is a Phase 2 issue surfacing late — flag it to the user rather than silently patching it.

---

## Gate 1 — One-page constraint

Open the HTML in a browser. Switch to print preview. Verify the page fits on one Letter-size sheet at `zoom:0.65` (already set in the print media query). If it overflows, cut — do not compress type or reduce padding. If it will not cut to one page without losing required content, flag to the user: the underlying plan was not sharp enough for a one-pager.

---

## Gate 2 — Plan fidelity

Read `<ENGAGEMENT_PATH>/action-plan.md` and the HTML side by side.

- [ ] Recommended actions appear in the same rank order as the action plan.
- [ ] Every recommendation has its tradeoff or cost in the same paragraph — not in a separate risks section.
- [ ] The first sentence of the problem section (01) states a business change, not a telemetry observation.
- [ ] Any hypothesis still marked "open" in `hypotheses.md` reads as open in the one-pager ("if confirmed," "pending validation," "gated on"). No open finding is stated as confirmed.

---

## Gate 3 — Brand text rules

Read `memory/long-term/brand/brand-spec.md` §6–7 alongside the HTML.

- [ ] All headings and section titles are sentence case. Check every `.beat-name`, `.mast-title`, `.p-name`, `.p-eyebrow`, and decision `.d-name`.
- [ ] Serial commas: "owner, timeframe, and cost" — not "owner, timeframe and cost."
- [ ] First formal mention of **Dynatrace®**, **OneAgent®**, **Smartscape®**, **Grail®** carries `®`. Subsequent mentions in the same document may drop it.
- [ ] No em dashes (`—`) or en dashes (`–`) anywhere in the copy. Scan the HTML source.
- [ ] No disallowed phrasings: "Dynatrace Server" (use "Dynatrace Cluster"), "plugin" or "add-on" (use "extension"), "out-of-the-box" (use "ready-made"), "Dynatrace interface" (use "Dynatrace web UI").
- [ ] Active voice: "We confirmed X" not "X was confirmed."
- [ ] No AI-writing patterns from `skills/brand-humanizer/reference/ai-writing-patterns.md` survived the pre-pass (spot-check: em dashes, "delve," "crucial," "leverage," title-case headings).

---

## Gate 4 — Accessibility

- [ ] `aria-hidden="true"` on all decorative elements: wave gradient containers, `.stripe` divs, `.foot-bar`, `.grad-bar`, `.mast-divider`, `.arrow` spans, `.proof-div` divs.
- [ ] `role="list"` + `role="listitem"` on visual card groups functioning as lists: `.stats`, `.tiles`, `.chips`, `.phases`, `.steps`, `.decisions`, `.cmap` rows.
- [ ] `role="table"` + `role="row"` + `role="columnheader"` + `role="cell"` on `.ptable` (01B only).
- [ ] `role="note"` with `aria-label` on `.stake` and `.h2h-side` panels.
- [ ] `aria-label` on `<section class="tldr">` and `<section class="takeaway">`.
- [ ] `aria-labelledby` on `.beat` sections pointing to the correct `id` on the `.beat-name` span.
- [ ] No text below 9px (eyebrow labels). No body text below 10px.
- [ ] No white text on `#49C2B3` brand teal — use `rgba(255,255,255,0.8)` on dark backgrounds.

---

## Gate 5 — Sources block

- [ ] `.foot-src` lists every externally sourced fact used in the one-pager.
- [ ] Each citation includes source name, domain, and retrieval date: `[Source] — [domain] (retrieved YYYY-MM-DD)`.
- [ ] Citations that were in `action-plan.md` are carried forward; no new external claims were introduced in Phase 3.

---

## Gate 6 — Handoff

- [ ] The companion markdown `<ENGAGEMENT_PATH>/one-pager-YYYY-MM-DD.md` was written alongside the HTML.
- [ ] The markdown front-matter comment records the recipe string and color assignments.
- [ ] The markdown is complete enough for the pptx-builder to produce a consistent deck without re-reading the HTML.

---

## After the gate passes

Record gate completion in `<ENGAGEMENT_PATH>/decisions-log.md`. Bump `phase: 3` and `last-touched:` in `<ENGAGEMENT_PATH>/current-context.md`.

Then prompt the user to approve PPTX generation. Do not invoke the pptx-builder automatically.
