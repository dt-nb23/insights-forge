# Seed Prompt Generator — leadership-feedback UX revisions

## Context

`html/Insights Forge (Seed Prompt Generator).html` (and its untracked sibling `- Original.html`) is a downloaded Claude Artifact export, not hand-authored HTML. The 197-line outer file is a generic bundler shell plus an asset dictionary (fonts, icons, header image, React/ReactDOM UMD — line 186, unchanged by this work). Line 194 is a single JSON-escaped string holding the actual application: an HTML document containing `<script type="text/x-dc">class Component extends DCLogic { ... }</script>`, using a declarative template syntax (`{{ }}` bindings, `<sc-if>`, `<sc-for>`).

This is the real, editable source. It reads cleanly once JSON-decoded — readable variable names, an existing design-token system (`--bg`, `--card`, `--field`, `--border`, `--text`, `--primary`, `--success`, `--warning`, `--critical`, etc., themed for dark/light via `THEMES.dark` / `THEMES.light` in the `Component` constructor), and reusable style-helper methods (`card()`, `pill()`, `box()`, `scaleBtn()`, `chipStyle()`, `capRow()`).

Six leadership-feedback items are in scope. Several are partial — this spec calls out what already exists vs. what's net-new so the diff stays honest.

## Out of scope for this pass

- Rebuilding the file from scratch, switching frameworks, or changing the bundler/asset mechanism.
- Editing the tracked `Insights Forge (Seed Prompt Generator).html` or the untracked `- Original.html` — both stay byte-identical to their current state.
- Any change to fonts, color palette, or the header hero treatment beyond reusing existing tokens.

## Technical approach

1. Decode line 194's JSON string to readable multi-line HTML/JS (already done for this session; will be redone deterministically at implementation time — decode, edit, re-encode is a repeatable mechanical step, not a one-off).
2. Edit the `Component` class and its template in the decoded form.
3. Re-encode the edited string as JSON and splice it back into a full copy of the outer 197-line file, replacing only line 194.
4. Write the result to a new file: `html/Insights Forge (Seed Prompt Generator) - Draft.html`. `Original.html` and the tracked file are left untouched.
5. Open the new file directly in a browser (`file://`) and click through all 10 sections plus the intro screen to verify — this is a static, no-build artifact, so "run the tests" means exercising the UI end to end, matching the `verify` skill's spirit for a change with a real runtime surface.

## Feature 1 — Intro / landing screen

Net-new. Add `showIntro: true` to initial state. When true, render a landing view in place of the nav rail + step layout (reusing the existing dark header hero for visual continuity) and hide progress/nav until dismissed.

Copy:

> **Start the engagement with the context already loaded.**
> Phase 0 normally starts cold — the agent pulls the customer's story out of you one question at a time. This form flips that around: fill in what you know before the session, and it assembles a structured Phase 0 intake brief you paste into Claude Code to open the engagement already framed.
>
> - 10 short sections — Must-haves unlock Copy/Download; everything else sharpens the result.
> - Nothing here replaces Phase 0 — the agent still asks 1–3 rounds of clarifying questions and waits for your approval.
> - Blank fields become "not provided" — a real gap the agent probes, never an invented answer.
>
> **[ Get Started → ]**

"Get Started" sets `showIntro: false` (reusing the existing primary pill-button style already used for Copy/Download).

## Feature 2 — Field-level "why it matters" explanations

Already exists at the section level: every one of the 10 sections has a "Why —" paragraph under its heading (`Why —` + one sentence, e.g. Section 6's Out of scope: *"A hard boundary, not a preference — the agent will not suggest these even if the capability is active..."*). No change to that mechanism.

The intro screen (Feature 1) now carries the "why the form as a whole matters" framing. No separate required-field-only explanation layer is added — the Must/Should/Nice tag pill already sits directly beside each section's Why line, so required fields are already in explanatory context. This item is considered satisfied by Features 1 + 3 combined; flag at review if leadership meant something more granular (e.g. per-input tooltips).

## Feature 3 — Inline clarifying copy on ambiguous fields

Two specific ambiguities, both net-new copy on existing structure (both fields already support the underlying behavior — this is purely making it legible):

- **Applications** (Section 7 already supports multiple named apps via a repeatable row + "+ Add application"). Append to the existing Why line: *"Add one row per application in scope — most engagements name 2–4."*
- **Audience vs. Stakeholders** — two distinct existing fields that read as similar:
  - Section 4 "Response format — audience" (quick-pick buttons: reader type for tone/format) gets a new caption underneath: *"The general reader type for the deliverable's tone. For specific named people, see Stakeholders (Section 8)."*
  - Section 8 "Stakeholders" Why line gets an appended clause: *"Different from the Audience picked in Engagement framing — this is specific people (or a role fallback) who'll read or influence the result."*

## Feature 4 — Explicit ACV label + tiers

Section 3, "Customer size" field:
- Label changes to **"Customer size (ACV)"**.
- Dropdown options change from the current `Below $250k` / `Above $250K & Below $1M` / `Above $1M` to:
  - `Acceleration (< $250K ACV)`
  - `Mid-Enterprise ($250K–$1M ACV)`
  - `Large Enterprise (> $1M ACV)`
- Same breakpoints as today — this only relabels, no new dollar data invented.
- `buildBrief()`'s `Customer size (ACV): ...` output line needs no change (already says ACV); it will just emit the new tier label text.

## Feature 5 — Role archetype fallback, defaulted value

Section 8, per-stakeholder row:
- The archetype `<select>`'s current blank first option (`<option value="">— select —</option>`) is replaced with a real, non-blank default option: **`Stakeholder — role to be confirmed`**. The existing `unsure` option at the end of the list is unchanged (it remains a distinct, explicit "I looked and don't know" signal, separate from the passive default).
- New stakeholder rows (`addStk()` and the initial `state.answers.stakeholders` seed) default `archetype` to `'Stakeholder — role to be confirmed'` instead of `''`.
- Must-have validation (`stkOk` in `_secData()`, and the matching check in `missing()`) changes from *(name present AND archetype present)* to *(archetype present alone)* — i.e. `a.stakeholders.some(s => F(s.archetype))`. Since archetype now always carries a real default value, this is satisfied without user action.
- The "Name & title" field's tag pill downgrades from **Must** to **Should**, since it no longer gates export.

**Trade-off to flag explicitly:** this makes the Stakeholders Must-have trivially satisfied on page load — a consultant who never touches Section 8 still clears the gate. That's what "defaulted value fulfills the requirement" was asked for, but it's worth confirming that's genuinely intended before this ships, since it measurably weakens the export gate's guarantee that *someone* thought about stakeholders. The Salesforce nudge (Feature 6) is the mitigation — it's a visible nag toward replacing the default, just not a blocking one.

## Feature 6 — Salesforce note near stakeholders

Net-new. Small callout under Section 8's heading/Why line, reusing the existing tip-callout visual pattern already used for Section 4's "Need ideas?" expandable tip (left-border accent, field background, rounded corners — no new component):

> Check Salesforce for the account team and named contacts — a real, named stakeholder sharpens the output far more than a role-only fallback.

Plain text, no link (no specific Salesforce URL was provided).

## Feature 7 — Color-coded status indicators (nav rail dots)

Partially exists: `dotState()` / `dotFor()` already implement done (green) / partial (amber) / empty (neutral outline), keyed off each section's required-field checklist.

Change: collapse to three states —
- **done** — all of a section's required fields filled → `var(--success, ...)` (unchanged).
- **required** — a Must-have section not fully satisfied, regardless of whether it's partially or fully empty (today's separate partial/empty split is removed) → `var(--warning, ...)`.
- **neutral** — an optional (no required fields) section, untouched → today's neutral outline (unchanged). Once any field in an optional section is filled it shows **done**, same as today.

No new CSS variable needed: `--warning` is already `#eea83f` (amber) in the dark theme and `#c62239` (crimson) in the light theme, so the yellow-in-dark / red-in-light behavior falls out of the existing theme system for free. The "Review & generate" nav item's dot simplifies the same way: `dotFor(canExport ? 'done' : 'required')`.

## Verification

No build step, no test framework — this is a static file. Verification is: open the new Draft.html directly in a browser, walk the intro screen and all 10 sections plus Review, confirm:
- Get Started dismisses the intro and reveals the guided layout.
- The three ambiguity-copy additions render where specified.
- ACV tier labels appear correctly in the dropdown and in the generated brief text.
- A fresh stakeholder row shows the defaulted archetype and alone clears the Stakeholders nav dot to green; Copy/Download unlock without a name ever being entered.
- Toggling light/dark theme swaps a required-but-incomplete section's nav dot between amber and crimson.
- The Salesforce note renders under Stakeholders in the existing tip-callout style.
