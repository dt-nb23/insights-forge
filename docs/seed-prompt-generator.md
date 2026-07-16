# The Seed Prompt Generator

Phase 0 normally starts cold: you describe the customer, and the agent pulls the context out of you one clarifying question at a time. The **Seed Prompt Generator** flips that around. It's a self-contained browser form that you fill out *before* the session; it assembles your answers into a single **seed prompt** — a structured Phase 0 intake brief — that you paste into Claude Code to open the engagement with the context already loaded.

It doesn't replace Phase 0 or its gate. It front-loads the intake so the agent spends its first questions sharpening the framing instead of collecting basics from scratch.

The tool lives at [`html/Insights Forge (Seed Prompt Generator).html`](<../html/Insights Forge (Seed Prompt Generator).html>). It's a single file — no install, no build, no network. Double-click it to open in any modern browser (React and its runtime are embedded in the file, so it works fully offline from `file://`).

## When to use it

Use it when you already know the customer and want the engagement to start from a shared, complete picture — most QBR, renewal, and expansion prep. Skip it and just describe the problem in chat when the situation is genuinely exploratory, or when discovery is happening *live with the customer* (Phase 0 has a client-facing question mode for that — see [workflow.md](workflow.md)).

Either path lands in the same place: a framed `current-context.md` and a Phase 0 gate. The generator is a faster on-ramp, not a different road.

## The flow, end to end

1. **Open the file** in a browser.
2. **Work through the ten sections** using the left rail (or Next). A live **Seed-prompt brief** panel on the right updates as you type.
3. **Fill every Must-have.** Copy and Download stay disabled until they're all in — the panel lists what's still missing.
4. **Copy to clipboard** (or **Download .md** to keep a file).
5. **Paste it into the Claude Code chat** as your opening message — or save the `.md` into the engagement and point the agent at it. Either way the agent reads it and begins Phase 0.
6. **Answer the follow-ups.** The brief opens with a "For the agent — read first" preamble that tells the agent to still ask 1–3 rounds of clarifying questions and to stop at the Phase 0 gate. Anything you left blank shows up as `not provided` — a genuine gap the agent will probe, not a value it invents.

The preview text is read-only by design (you can't select or drag it out) — use the Copy button so the whole brief, preamble included, travels intact.

## The ten sections

Each field is tagged **Must** / **Should** / **Nice**, mirroring the MUST-/SHOULD-/NICE-HAVE rubric Phase 0 uses. Only Must-haves gate export.

| # | Section | Captures |
|---|---|---|
| 1 | **Requested outputs** | Which presentation formats to build on top of the action plan (one-pager, deck, execution guides). The customer action plan is always the baseline. |
| 2 | **Analyst context** | Three 1–5 self-calibrations — your Dynatrace consulting experience, account familiarity, and the **customer's Dynatrace maturity**. Rate one and you rate all three. Tunes depth and tone. |
| 3 | **Customer basics** | Name, what they do, vertical, **customer size (ACV band)**, tenant type, and **region(s)** (NORAM / LATAM / EMEA / APAC). Region flags laws like GDPR that can shape what the plan may recommend. |
| 4 | **Engagement framing** | The **C.S.I.R.** sub-sequence — Context, Specific information, Intent, Response format (audience, time window, tone). Intent is captured as **two required questions**: what *Dynatrace* wants from the engagement (prove value, secure renewal, justify expansion) and what the *customer* would call success. You cannot write the objective without both. This is the heart of the brief; starter chips help if you're staring at a blank box. |
| 5 | **Active Dynatrace capabilities** | What's actually live in the tenant. This is the **boundary of what insight can be surfaced** — the agent won't propose value that depends on a capability you didn't check. Davis AI is always on. |
| 6 | **Out of scope** | A **hard do-not-suggest list** — capabilities the agent must not recommend even if they're active (e.g. no Session Replay under GDPR), plus a free-text reason. |
| 7 | **Focus applications & RUM** | Named apps with RUM and Session Replay status. Becomes a Must-have if your goals mention improving digital experience. |
| 8 | **Stakeholders** | Who consumes or influences the deliverable — name, role archetype, and what they judge success by. At least one (name + archetype) is required. |
| 9 | **Technical team priorities** | The day-to-day pain the technical team feels — alert noise, slow root cause, toil, on-call load. |
| 10 | **Trigger** | What prompted the engagement — QBR, renewal, expansion, incident follow-up. |

The Must-haves that unlock export are: a requested output, customer name / what-they-do / vertical, C.S.I.R. Context + Specific + Dynatrace intent + customer success + audience, at least one active capability beyond Davis (or "unsure"), and at least one stakeholder. Everything else sharpens the result but won't block you.

## How the brief maps to Phase 0

The generated markdown is organized so the agent can read it against the [context-framing skill](../skills/context-framing/SKILL.md) directly. Its sections line up with the nine Phase 0 clarifying questions (Q1 customer, Q2 vertical, Q3 C.S.I.R. — Intent carried as two labeled values, Dynatrace intent and customer success, matching what Q3-I captures, Q4 tenant, Q5 capabilities, Q6 RUM, Q7 audience, Q8 technical priorities, Q9 trigger), and it adds three fields the live question set doesn't ask for — customer size (ACV), region(s), and the out-of-scope exclusions — plus the customer-maturity calibration. The preamble categorizes every input as Must-/Should-have context and states two hard rules for the agent: **active capabilities are the boundary** of surfaceable insight, and **out-of-scope items are a hard exclusion**.

Because the brief is just a rich, structured problem description, no change to the agent is needed to consume it — it enters Phase 0 through the same "describe the engagement" path as a typed problem statement, only far more complete.

## What it does *not* do

- It **does not skip the Phase 0 gate.** The agent still reframes, still asks follow-ups, and still waits for your explicit approval before Phase 1.
- It **does not fabricate.** Blank fields become `not provided`, which the agent treats as a gap to close — consistent with the workspace's "name the gap, don't invent it" principle.
- It **does not run anything.** It's a static form that produces text. No queries, no network, no writes to the workspace.

## Look inside

| What you'll find | Where to look |
|---|---|
| The tool itself | [`html/Insights Forge (Seed Prompt Generator).html`](<../html/Insights Forge (Seed Prompt Generator).html>) |
| Screenshots of each section | [`html/screenshots/`](../html/screenshots/) |
| The Phase 0 procedure that consumes the brief | [`skills/context-framing/SKILL.md`](../skills/context-framing/SKILL.md) |
| The nine clarifying questions and the rubric | [getting-started.md](getting-started.md) · [workflow.md](workflow.md) |
