# The Seed Prompt Generator

Phase 0 normally starts cold: you describe the customer, and the agent pulls the context out of you through the three-phase questioning flow. The **Seed Prompt Generator** flips that around. It's a self-contained browser form that you fill out *before* the session; it assembles your answers into a single **seed prompt** — a structured Phase 0 intake brief — that you paste into Claude Code to open the engagement with the context already loaded.

It doesn't replace Phase 0 or its gate. It front-loads the intake so the agent spends its first questions sharpening the framing instead of collecting basics from scratch.

The tool lives at `html/Insights Forge (Seed Prompt Generator).html` — a single browser-runnable file: no install, no build, no network. (The readable application source is [`html/seed-prompt-generator-src.html`](../html/seed-prompt-generator-src.html); edit it and repack with `tools/seed-prompt-generator-bundle.py` — the src file alone will not render in a browser.)

## When to use it

Use it when you already know the customer and want the engagement to start from a shared, complete picture — most QBR, renewal, and expansion prep. Skip it and just describe the problem in chat when the situation is genuinely exploratory (or type `/drill` for a chat-native version of the same intake), or when discovery is happening *live with the customer* (Phase 0 has a client-facing question mode for that — see [workflow.md](workflow.md)).

Either path lands in the same place: a framed `current-context.md` and a Phase 0 gate. The generator is a faster on-ramp, not a different road.

## The flow, end to end

1. **Open the file** in a browser.
2. **Work through the ten sections** using the left rail (or Next). A live **Seed-prompt brief** panel on the right updates as you type.
3. **Fill every Required field.** Copy and Download stay disabled until they're all in — the Review panel lists what's still missing.
4. **Copy to clipboard** (or **Download .md** to keep a file).
5. **Paste it into the Claude Code chat** as your opening message — or save the `.md` into the engagement and point the agent at it. Either way the agent reads it and begins Phase 0.
6. **Answer the follow-ups.** The brief opens with a "For the agent — read first" preamble that tells the agent to still ask 1–3 rounds of clarifying questions and to stop at the Phase 0 gate. Anything you left blank shows up as `not provided` — a genuine gap the agent will probe, not a value it invents. If every required item arrives filled and substantial, the agent uses the **brief-complete fast path**: one combined sharpening message instead of multiple rounds.

The preview text is read-only by design (you can't select or drag it out) — use the Copy button so the whole brief, preamble included, travels intact.

## The ten sections

Fields are tagged **Required** or left optional; the brief's preamble groups them for the agent as **Required context** and **Recommended context**. Only Required fields gate export.

| # | Section | Captures |
|---|---|---|
| 1 | **Outputs & trigger** | Which presentation formats to build on top of the action plan (the customer action plan is always the baseline), what prompted the engagement (QBR, renewal, expansion, incident follow-up), and **your role** (required). |
| 2 | **Analyst context** | Three optional self-calibrations — your Dynatrace consulting experience, account familiarity, and the **customer's Dynatrace maturity**. Each presents its five behavioral anchor statements as the choices themselves: pick the one that fits (stored as 1–5 under the hood; click again to clear). Answer any, all, or none — there is no rate-one-rate-all rule, because forcing three scales at once is exactly the grid pattern that produces straight-lined answers. The brief emits the score *and* the anchor text (e.g. `3/5 — "Comfortable across the common patterns"`). These route the drill depth, the council size, the gate verbosity, and the plan's ambition ceiling. |
| 3 | **Customer basics** | Name, what they do, vertical, **customer size (ACV band)**, tenant type, and **region(s)** (NORAM / LATAM / EMEA / APAC). Region flags laws like GDPR that can shape what the plan may recommend. |
| 4 | **Stakeholders & audience** | Who consumes or influences the deliverable — role archetype (required; at least one), name (strongly preferred), communication level, and what they judge success by. |
| 5 | **Relationship Context** | How the relationship stands — history, commitments, tensions, prior outcomes. Required. |
| 6 | **Customer Pain Points** | The pain and constraints the plan must respect — alert noise, slow root cause, toil, on-call load, plus commitments and limits. Required; this single field carries what the live questions split across Q3-Specific and the vertical drill sheet. |
| 7 | **Goals & success** | Intent as **two required questions**: what *Dynatrace* wants from the engagement (prove value, secure renewal, justify expansion) and what the *customer* would call success. You cannot write the objective without both. |
| 8 | **Active capabilities** | What's actually live in the tenant. This is the **boundary of what insight can be surfaced** — the agent won't propose value that depends on a capability you didn't check. Davis AI is always on; at least one capability beyond Davis (or "unsure") is required. |
| 9 | **Out of scope** | A **hard do-not-suggest list** — capabilities the agent must not recommend even if they're active (e.g. no Session Replay under GDPR). |
| 10 | **Focus applications** | Named apps with RUM and Session Replay status. Becomes required when your goals signal a digital-experience intent (any of: digital experience, user experience, RUM, real user, customer journey, frontend). |

The Required fields that unlock export are: at least one requested output; your role; customer name / what-they-do / vertical; Relationship & context; Pain & constraints; both Goals & success answers; at least one active capability beyond Davis (or "unsure"); at least one stakeholder role archetype; and a focus app with RUM status when the intent is digital-experience. Everything else — the calibration picks included — sharpens the result but won't block you.

## How the brief maps to Phase 0

The emitted format itself — headings, order, and field lines — is specified in [brief-contract.md](brief-contract.md), the canonical contract that the form, `/drill`, and context-framing must all match (verified by `tools/conformance-check.py`).

The generated markdown is organized so the agent can read it against the [context-framing skill](../skills/context-framing/SKILL.md) directly — its **Seed-prompt intake** section carries the exact section-to-question mapping table. In short: `Requested outputs & trigger` covers Q3-R, Q9, and the analyst calibration; `Customer context` covers Q1/Q2/Q4 plus size, regions, and Q3-Context; `Stakeholders & audience` covers Q7; `Goals & success criteria` covers Q3-Intent; `Pain & constraints` covers Q3-Specific and the technical-team pain the drill sheet would otherwise probe; and `Active capabilities`, `Out of scope`, and `Focus applications` cover Q5, the exclusions, and Q6. The preamble states two hard rules for the agent: **active capabilities are the boundary** of surfaceable insight, and **out-of-scope items are a hard exclusion**.

The agent consumes the brief through a dedicated intake path: context-framing detects the `# Insights Forge intake brief` header, maps every populated value as a provisional answer, closes MUST-HAVE gaps first, then sharpens — collapsing to a single sharpening message when the brief arrives complete.

## What it does *not* do

- It **does not skip the Phase 0 gate.** The agent still reframes, still asks follow-ups, and still waits for your explicit approval before Phase 1.
- It **does not fabricate.** Blank fields become `not provided`, which the agent treats as a gap to close — consistent with the workspace's "name the gap, don't invent it" principle.
- It **does not run anything.** It's a static form that produces text. No queries, no network, no writes to the workspace.

## Editing the form

The browser-runnable file is a Claude Artifact bundle export: a small harness plus the application source embedded as one JSON-escaped string. Edit the readable source, then repack:

```bash
python3 tools/seed-prompt-generator-bundle.py unpack "html/Insights Forge (Seed Prompt Generator).html" html/seed-prompt-generator-src.html   # only if the src is out of date
# edit html/seed-prompt-generator-src.html
python3 tools/seed-prompt-generator-bundle.py pack "html/Insights Forge (Seed Prompt Generator).html" html/seed-prompt-generator-src.html "html/Insights Forge (Seed Prompt Generator).html"
```

If the edit touches `buildBrief()` — the function that emits the brief — change [brief-contract.md](brief-contract.md) first and the `/drill` template in the same commit; the conformance check fails when the three drift apart.

## Look inside

| What you'll find | Where to look |
|---|---|
| The tool itself (browser-runnable bundle) | [`html/`](../html/) — `Insights Forge (Seed Prompt Generator).html` |
| The editable application source + repack tool | [`html/seed-prompt-generator-src.html`](../html/seed-prompt-generator-src.html) · [`tools/seed-prompt-generator-bundle.py`](../tools/seed-prompt-generator-bundle.py) |
| The brief format the form emits | [brief-contract.md](brief-contract.md) |
| Screenshots of each section | [`html/screenshots/`](../html/screenshots/) |
| The Phase 0 procedure that consumes the brief | [`skills/context-framing/SKILL.md`](../skills/context-framing/SKILL.md) |
| The chat-native equivalent | [`skills/drill/SKILL.md`](../skills/drill/SKILL.md) |
| The nine clarifying questions and the rubric | [getting-started.md](getting-started.md) · [workflow.md](workflow.md) |
