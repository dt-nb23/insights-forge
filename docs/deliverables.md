# Phase 3 deliverables — brand, layout, voice

Phase 3 is where the workspace earns its keep — a one-page written summary and a PowerPoint deck, both brand-conformant and tuned to a *named* stakeholder. This page walks you through what the brand spec actually requires, how the one-pager and deck come together, and how to spot-check brand conformance before sending.

If you remember one thing: the **brand spec is authoritative**. The agent will not improvise off-palette colors, off-brand fonts, or made-up layouts — and you shouldn't either. The spec lives at [`memory/long-term/brand/brand-spec.md`](../memory/long-term/brand/brand-spec.md) and is loaded before any Phase 3 artifact gets produced.

## What the brand spec covers

The spec is the single source of truth for these eight dimensions:

| Dimension | Where in the spec |
|---|---|
| Color palette (HEX values) | Color section |
| Typography (DT Flow Medium / DT Flow Light, Arial fallback) | Typography section |
| Slide format (16:9, 13.33" × 7.5") | Header |
| Layout templates (64 named slide layouts) | Layout patterns section |
| Logo lockups (horizontal preferred for headers) | Logo usage section |
| Voice and tone | Voice section, sourced from `styleguide.dynatrace.com` |
| Product-name capitalization (Dynatrace®, OneAgent®, Grail®, Smartscape®, AppEngine, ActiveGate, Davis AI) | Terminology section |
| Footer conventions | Footer section |

Each of these is sourced from one of three places — the spec's "Sources" table lists which source confirms which dimension. When the official PowerPoint template and the brand PDF disagree, the **PowerPoint wins** because it's what gets rendered.

**Source files in this repo.**

- [`Dynatrace_Brand_Insights-Forge.pptx`](../Dynatrace_Brand_Insights-Forge.pptx) — the rendered theme; source of truth.
- [`DTFlow/`](../DTFlow/) — the DT Flow typeface files.
- [`memory/long-term/brand/`](../memory/long-term/brand/) — the spec and supporting reference notes.

## What the one-pager looks like

Produced by [`skills/exec-onepager/SKILL.md`](../skills/exec-onepager/SKILL.md). One page, written for a *named* stakeholder whose profile file is read from [`memory/long-term/profiles/`](../memory/long-term/profiles/) via the index in [`memory/long-term/stakeholder-profiles.md`](../memory/long-term/stakeholder-profiles.md). This isn't decoration — the voice and emphasis genuinely change between stakeholders. A VP of Reliability and a VP of Product get different one-pagers from the same investigation:

- VP of Reliability — error-budget framing, SLO impact, on-call burden, post-incident learnings.
- VP of Product — feature impact, customer-experience surface, release velocity, competitive considerations.

Default structure: TL;DR → top hypothesis → recommended action → decision ask → risks. The skill defines the exact section order and word-budget guidance — open the `SKILL.md` if you want to see the template.

The exec-onepager skill runs in five steps: recipe selection, content draft, brand-humanizer pre-pass, HTML build, and brand gate. The brand-humanizer pre-pass (Step 3) runs on all drafted copy before any HTML is assembled, catching AI writing patterns and DT voice violations while the copy is still in plain text and easy to fix.

## What the deck looks like

Produced by [`skills/pptx-builder/SKILL.md`](../skills/pptx-builder/SKILL.md), **only after** the one-pager is approved. The order matters — it's much easier to expand a tight one-pager into a deck than to compress a sprawling deck into a one-pager.

The pptx skill is an adapter: it delegates to the standard pptx skill when available, applies the brand spec on top, and uses layouts from the official template. Practical implications you'll see in the output:

- **Slide format.** 16:9 widescreen, 13.33" × 7.5". No square slides, no 4:3.
- **Typography.** DT Flow Medium / DT Flow Light. Arial is the rendering-side fallback only — if a viewer doesn't have DT Flow installed, the slide falls back gracefully. The agent never substitutes a different font on its own.
- **Layouts.** 64 named layouts from the template — content card, chart, table, swimlane, gantt, timeline, funnel, hashtag-stat, and so on. The agent picks from this set, not freeform.
- **Logo lockup.** Horizontal lockup preferred for slide title bars and one-pager headers where horizontal space allows.
- **Product names.** Capitalized and trademarked as the spec requires. The agent never coins variants like "Dynatraces" or "the Dynatrace platform" when the spec says "Dynatrace®".

## Voice and tone

Voice comes from `styleguide.dynatrace.com/docs/best-practices/top-10-tips` and from the matching stakeholder profile. **No critique lens runs in Phase 3** — the voice and framing were already enforced upstream, while the work could still change:

- The [Consultative lens](../.claude/agents/consultative-lens.md) ran a framing pass on the issue tree and hypotheses in Phase 1, and reviewed the action plan as a panel member in Phase 2, so the firm's voice is baked into the plan the one-pager summarizes.
- The [Customer lens](../.claude/agents/customer-lens.md) and [Skeptic lens](../.claude/agents/skeptic-lens.md) were both on the Phase 2 persona panel, so user-impact grounding and the hostile-leadership questions are already answered in the approved plan.

Phase 3 inherits that reviewed plan and packages it faithfully — it does not re-open the message. The deliverable stays in voice because the plan it summarizes was already in voice. You can still ask for any lens on demand at the Phase 3 gate, but none runs automatically. If you want to know exactly which lens catches what and when it runs, [lenses.md](lenses.md) has the full breakdown.

## Spot-checking before you send

Before you send a one-pager or deck, you can ask the agent for an explicit verification pass:

> *"Verify this one-pager against the brand spec — colors, typography, layout, terminology."*

The agent will load [`memory/long-term/brand/brand-spec.md`](../memory/long-term/brand/brand-spec.md), walk the artifact section by section, and flag anything off-spec. This catches the kinds of drift that are easy to miss: a trademarked product name without the ®, an Arial fallback that shouldn't be visible, a HEX value that's close to but not exactly the palette.

## Look inside

| What you'll find | Where to look |
|---|---|
| The authoritative brand spec | [`memory/long-term/brand/brand-spec.md`](../memory/long-term/brand/brand-spec.md) |
| Supporting reference notes (which page in the source PDF maps to which pattern) | [`memory/long-term/brand/reference/`](../memory/long-term/brand/reference/) |
| The rendered PowerPoint theme | [`Dynatrace_Brand_Insights-Forge.pptx`](../Dynatrace_Brand_Insights-Forge.pptx) |
| The DT Flow typeface files | [`DTFlow/`](../DTFlow/) |
| The one-pager skill | [`skills/exec-onepager/SKILL.md`](../skills/exec-onepager/SKILL.md) |
| The deck skill | [`skills/pptx-builder/SKILL.md`](../skills/pptx-builder/SKILL.md) |
