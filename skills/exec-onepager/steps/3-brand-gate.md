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

Run the lint tool from the repo root:

```bash
python3 tools/onepager-lint.py <ENGAGEMENT_PATH>/<slug>-onepager.html --action-plan <ENGAGEMENT_PATH>/action-plan.md --proper-noun "<Client>"
```

- Fix every **FAIL** and re-run until the tool exits 0.
- Review every **WARN**: fix it, or record a one-line justification for leaving it (report those justifications at the Phase 3 gate, part 3).
- **Exit 3** means gate 1 could not be measured (no Chrome on this machine). The tool still reports `GATE1-BUDGET`, a character-count comparison against the reference one-pager: a budget WARN means the page will almost certainly overflow, so cut first. Then do the manual check: open the HTML in a browser, switch to print preview, and verify the page fits on one Letter-size sheet at `zoom:0.65` (already set in the print media query).

If the page overflows, cut — do not compress type or reduce padding. If it will not cut to one page without losing required content, flag to the user: the underlying plan was not sharp enough for a one-pager.

The linter also covers the mechanical portions of gates 3–5 below. The checklists remain for the judgment calls the tool cannot make — plan fidelity, active voice, and confirming each WARN is genuinely justified.

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

The brand gate is the agent's own checklist; the Phase 3 gate below is the user's. Do not present the Phase 3 gate until every gate above passes — a one-pager that fails its own checklist is not ready for review.

## Phase 3 gate — one-pager

Present the **Phase 3 gate summary block** (per CLAUDE.md "Gate summary block"):

1. **Conclusion** — the single decision or finding the one-pager leads with, in one sentence.
2. **What changed** — what Phase 3 produced: the recipe selected and the one-sentence why, what the brand-humanizer pre-pass changed, and any brand-gate failures found and fixed.
3. **Assumptions and confidence gaps** — any brand-gate item left unverified and how it was checked instead; any content problem flagged as a Phase 2 issue surfacing late (a missing tradeoff, an open hypothesis that reads as confirmed); any place the one-page constraint forced a cut the reader might miss.
4. **Out-of-scope cost** — anything removed from the one-pager because it depended on an excluded capability; otherwise "No out-of-scope items arose this phase."
5. **Approve / Redirect / Iterate** — "**Approve** to generate the deck, **Redirect** [layout, emphasis, or framing change], or **Iterate** [lens to run on the one-pager]."

Record the gate decision in `<ENGAGEMENT_PATH>/decisions-log.md` (row label `Phase 3 Deliver — one-pager`); on approval, set today's `last-touched:` in `<ENGAGEMENT_PATH>/current-context.md` (`phase:` is already `3` — it was set at the Phase 2 approval). Do not generate the deck until the user explicitly approves; the pptx-builder skill presents its own Phase 3 gate for the deck.
