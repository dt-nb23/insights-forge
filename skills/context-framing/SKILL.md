---
name: context-framing
description: Phase 0 procedure for framing a Dynatrace customer engagement before any diagnosis work. Use at the start of a new engagement when the consultant describes a customer, references a Dynatrace environment, or names an upcoming touchpoint (QBR, renewal, expansion, value-surfacing).
---

# Context Framing

## When to use

**Phase 0 — the required first step of every engagement.** The agent reads this skill before asking the consultant a single clarifying question.

Use this skill when:

- A new engagement begins: a consultant describes a customer, a Dynatrace environment, an upcoming meeting, or a value-surfacing goal.
- The consultant's opening message is a **seed-prompt intake brief** from the Seed Prompt Generator (it opens with `# Insights Forge intake brief` and a `> **For the agent — read first.**` preamble). Treat it as pre-filled intake, not a finished framing — see **Seed-prompt intake** below.
- The user has redirected scope after a Phase 0 gate and the framing needs to be reset.
- The existing `current-context.md` is stale and the user has asked to reframe.

**Do not advance to Phase 1 until the user explicitly approves the output of this skill.**

## Inputs

**Establish the engagement for this session (before reading any client files):**

1. If this session is already working an engagement you created or resumed earlier in the conversation and the user is asking to reframe it, reuse that `ENGAGEMENT_PATH` and `CLIENT_NAME` and skip the folder-creation step (Step 3 below) — the folder exists; you overwrite `current-context.md` in place, preserving its status front-matter and bumping `last-touched`.
2. Otherwise this is a new engagement: `ENGAGEMENT_PATH` and `CLIENT_NAME` are set in Step 3 once Q1 (client name) is answered. There is **no global pointer file** — the dated engagement folder you create *is* the session's state, and you hold its path in working context for the rest of the session.

Then read these files:

- `memory/long-term/stakeholder-profiles.md` — hub index (already loaded at session init). When a stakeholder is named, read the specific profile file (e.g., `memory/long-term/profiles/executive-sponsor.md`) to calibrate "exec-ready" depth and tone.
- `memory/long-term/domain-knowledge.md` — for the tech → UX → business linkage table; helps identify which insights are likely surfaceable given the active capabilities.
- `memory/long-term/terminology.md` — to use consistent terminology when restating the engagement context.
- `memory/long-term/client-question-bank.md` — client-facing phrasings of the 9 clarifying questions below, grouped by rubric classification (MUST-HAVE / SHOULD-HAVE / NICE-TO-HAVE). When the consultant indicates this discovery is being done **live with the customer** (rather than the agent gathering context from the consultant), draw question phrasings from this bank instead of the consultant-facing prompts below. Otherwise, treat it as a reference the consultant can take into their own discovery calls.
- `memory/clients/<CLIENT_NAME>/README.md` — scan the engagement history for any prior engagement on this client (once CLIENT_NAME is known — see new Step 3). If prior engagements exist, surface the key lesson before proceeding.
- `memory/clients/<CLIENT_NAME>/environment.md` — if it exists, read it after Q5/Q6 to sharpen orientation hypotheses with environment-specific facts.
- `memory/clients/<CLIENT_NAME>/stakeholder-overlays.md` — if it exists, check for an existing overlay matching the leader identified in Q7.

If the consultant has not yet described the engagement, open with:

> "Tell me about the customer and what you're trying to accomplish with them."

Do not ask multiple questions at once. Let each answer drive the next question.

## Seed-prompt intake

Sometimes the consultant's opening message is not a freeform description but a **seed-prompt intake brief** produced by the Seed Prompt Generator (see `docs/seed-prompt-generator.md`). It opens with `# Insights Forge intake brief` and a `> **For the agent — read first.**` preamble, and it pre-fills most of the nine clarifying questions in one pass.

**A seed-prompt brief front-loads context; it does not replace the conversation.** Absorb it, then still question before you summarize — never jump from a pasted brief straight to the framing summary and the gate.

When the opening message is a seed-prompt brief:

1. **Read the whole brief, including its preamble.** The preamble restates rules you already hold: active capabilities are the boundary of surfaceable insight; **out-of-scope items are a hard exclusion**; anything marked `not provided` is a genuine gap, not a value to invent.
2. **Map its sections onto the question model** and treat every populated value as a **provisional** answer — captured, but not yet confirmed with the consultant:

   | Brief section | Populates |
   |---|---|
   | Requested outputs + Analyst calibration | Response format (Q3-R); analyst / account / customer-maturity calibration |
   | Customer (name, what they do, vertical, size, tenant, region) | Q1, Q2, Q4, plus customer size (ACV band) and region(s) |
   | Engagement framing (C.S.I.R.) | Q3 — Context, Specific, Intent, Response format |
   | Active capabilities | Q5 |
   | Out of scope / do not suggest | Out-of-scope exclusions (hard boundary — carried into every later phase) |
   | Focus applications | Q6 — RUM / Session Replay status per app |
   | Stakeholders | Q7 — archetype match + named-leader overlay trigger |
   | Technical team priorities | Q8 |
   | Trigger(s) | Q9 |

3. **Still run 1–3 rounds of clarifying questions, one topic at a time, before writing `current-context.md`:**
   - **First, close every MUST-HAVE gap** — any rubric MUST-HAVE the brief left `not provided`, filled with a placeholder, or answered thinly. Ask the corresponding question from the list below.
   - **Then sharpen the provisional answers** — confirm and deepen Intent, confirm the active-capability boundary, and probe what each named stakeholder actually cares about. A filled-in form field is a starting point, not a probed answer: treat a one-line brief value as a prompt for a real follow-up, not a closed question.
   - Apply the normal rules: one question at a time, adaptive order, and **skip anything the brief already answers well** (a strong brief value counts as "already answered"). Stop when every MUST-HAVE holds a confirmed, non-placeholder value and you have enough substance to frame confidently.
4. **Capture the fields the brief carries that the live question set does not ask for** — customer size (ACV band), region(s), out-of-scope exclusions, and the customer's-Dynatrace-maturity calibration — into `current-context.md` (see Output). **Record the out-of-scope exclusions explicitly and carry them forward**: later phases must never surface a hypothesis, opportunity, or action that depends on a capability or topic the consultant ruled out, even if it is active. See **Out-of-scope exclusions** below.
5. **Then continue with Steps 3–11 unchanged** — folder creation, past-engagement check, reframe, orientation hypotheses, scope, write, verify, and the gate. The stakeholder-overlay and environment-intake follow-on triggers (Q7, Q5) apply exactly as in a live intake. The Phase 0 gate still requires explicit approval.

## Out-of-scope exclusions

Whether they arrive in a seed-prompt brief or the consultant states them live, **out-of-scope items are a hard exclusion for the entire engagement** — a boundary, not a preference. An item is out of scope for reasons the agent does not get to override: compliance (e.g., no Session Replay under GDPR), contractual limits, prior commitments, or an explicit customer "do not suggest."

The rule the whole workspace holds to:

> **Never surface a hypothesis, opportunity, recommendation, signal, or action that depends on, requires, or would encourage adopting an out-of-scope capability or topic — even if that capability is active in the tenant.** Out-of-scope overrides "active capability": active defines what *could* be surfaced; out-of-scope subtracts from it.

Record the exclusions in `current-context.md` under **Out-of-scope exclusions** (see Output), verbatim enough that a later phase can check against them. If closing a MUST-HAVE gap or the consulting objective would require an out-of-scope capability, say so plainly at the gate rather than quietly routing around it — the exclusion may force a re-anchor of the insight narrative, and that is the consultant's call to make.

## Clarifying questions

**Two-phase questioning structure:**

**Phase A — Narrative funnel (Q1–Q3, C.S.I.R.):** Work through Q1 (customer), Q2 (vertical), and Q3 (C.S.I.R. sub-sequence) as a flowing conversation, not a form. Each answer should naturally surface the next question — if the consultant's opening message answers Q1 and Q2, jump straight into C.S.I.R. context questions without re-asking. Allow 1–3 exchanges per dimension; a confident consultant's crisp answer wraps a dimension in one turn. Skip any dimension the opening message already covered with a real value.

**Phase B — Closed drill block (Q4–Q9):** Once all four C.S.I.R. dimensions are locked, present Q4 through Q9 in **one message**, labeled "To anchor the plan, here are the factual questions I need:". Use the checklist format for Q5 (capabilities). This single message collapses 6 potential turns into one round-trip. Skip any question the opening description or brief has already answered with a real value.

Stop asking when every **MUST-HAVE** field in the Exit-criteria rubric below is populated with a non-placeholder value. If a seed-prompt brief supplied the answers (see **Seed-prompt intake** above), the same skip rule applies to well-filled fields.

The nine questions — use the two-phase structure above, not serial one-at-a-time delivery:

### Q1 — Customer and what they do
> "Who is the customer, and what does their business do?"

Capture: company name (or anonymized label), what product or service they sell, approximate size if known.

### Q2 — Customer vertical
> "Which industry vertical are they in?"

Common verticals: Retail / E-commerce, Financial Services (FSI), Healthcare / Life Sciences, Manufacturing, Telco / Media, Public Sector, Technology / SaaS, Logistics / Supply Chain. Accept the consultant's own label if it doesn't match this list.

The vertical shapes which KPIs matter to leadership and which signal → business linkages are most relevant in Phase 1.

### Q3 — Engagement Framing (C.S.I.R.)

Q3 is a structured sub-sequence, not a single question. Now that the customer and their vertical are established, use C.S.I.R. to lock in the full problem context before moving into environment and capability questions. Work through each dimension in order, one prompt at a time, skipping any already answered in Q1, Q2, or the consultant's opening description.

#### C — Context
> "Walk me through the situation you're walking into — what's the history with this customer, and what's the mood heading into this engagement?"

Capture: relationship history (new logo, established customer, at-risk account), recent interactions or milestones, and the consultant's role (CSM, SE, consultant, other).

*Why this matters:* The relationship context shapes tone, urgency, and how findings should be framed. An at-risk renewal and a healthy expansion require completely different narratives even if the Dynatrace data is identical.

#### S — Specific Information
> "What specific information do you already have — for example, known pain points, prior QBR outcomes, commitments made, or anything that limits or shapes what's possible?"

Capture: known environment facts, prior QBR outcomes, existing commitments, contract phase (new, renewal, expansion), known pain points, and any constraints (e.g., limited data access, regulated industry restrictions).

*Why this matters:* Specific information is the boundary of what's usable. Without it, orientation hypotheses in Step 5 will be generic rather than targeted.

#### I — Intent
> "What are you ultimately trying to accomplish — and what does a successful outcome look like for you as the consultant?"

Capture: the consultant's goal (e.g., prove value, secure renewal, justify expansion, prepare a QBR narrative) and the customer's expected outcome (e.g., confidence in their Dynatrace investment, a clear roadmap, reduced noise in their environment).

*Why this matters:* Intent shapes the consulting objective written in Step 4. If the consultant's goal is renewal and the customer's goal is cost justification, the deliverable must speak to ROI — not feature breadth.

#### R — Response Format
> "What does the deliverable need to look like — for example, a slide deck, a written findings report, a live walkthrough, a dashboard, or something else? And who is the primary audience?"

Capture: format (deck / report / walkthrough / dashboard / other), audience (exec / technical / mixed), and any known constraints on length, tone, or branding.

*Why this matters:* Format and audience determine how findings are packaged in Phase 3. An exec deck and a technical findings report require completely different structures, depths, and vocabularies.

---

**Q3 gate:** Before moving to Q4, confirm all four C.S.I.R. dimensions are captured. If any are still unknown, ask one follow-up question to close the gap. Record Q3 outputs in `current-context.md` under "Engagement Framing (C.S.I.R.)".

### Q4 — Tenant type
> "Is this customer on a SaaS tenant or a Managed (on-premises) deployment?"

This affects which features and data are available and constrains what insights and recommendations are possible in later phases.

### Q5 — Active Dynatrace capabilities
> "Which of these Dynatrace capabilities are active in their environment? Select all that apply."

Present as a multi-select checklist — do not pre-check anything:

**Core observability**
- [ ] Full-Stack Monitoring (OneAgent)
- [ ] Infrastructure Monitoring only
- [ ] Application Performance Monitoring (APM / Distributed Tracing)

**User experience**
- [ ] Real User Monitoring — Web
- [ ] Real User Monitoring — Mobile
- [ ] Session Replay
- [ ] Synthetic Monitoring

**Data & logs**
- [ ] Log Management (Grail)
- [ ] Business Analytics / Business Events
- [ ] Metrics ingestion (custom or third-party)

**AI & automation**
- [ ] Davis AI (problem detection)
- [ ] Davis CoPilot
- [ ] Workflows / Automation

**Security**
- [ ] Application Security
- [ ] Cloud Security

**Platform**
- [ ] Grail (data lakehouse)
- [ ] Site Reliability Guardian
- [ ] Dashboards & Notebooks

Record the checked items in `current-context.md` under "Active capabilities". This list is the boundary of what insights can be surfaced in Phase 1.

**Environment intake check:** After Q5 and Q6, check `memory/clients/<CLIENT_NAME>/environment.md`. If found, read it now — it contains environment-specific facts (Management Zones, defined SLOs, instrumentation gaps, DPS quota) that persist across engagements and should inform orientation hypotheses in Step 5. If no file exists, note that `skills/environment-intake/SKILL.md` should be run at the Phase 0 gate to capture these facts for future engagements.

### Q6 — RUM on the application in question
> "Is Real User Monitoring enabled on the specific application we'll be focusing on? And if so, is Session Replay active for it?"

This determines whether a user experience story is available. If RUM is not enabled, flag it immediately as a capability gap — the insight narrative will need to anchor on APM and infrastructure signals instead.

### Q7 — Who will consume the deliverable and what they care about
> "Who on the customer side will we be presenting findings to, and what do they care about most — what KPIs, business outcomes, or strategic priorities are top of mind for them right now?"

Capture the person's role and priorities. Then resolve them against `stakeholder-profiles.md` in **two steps**:

1. **Match to a role archetype first.** Focus on what they own and decide, not their exact title. The eight archetypes are: Executive Sponsor, Product Owner, SRE / Reliability Engineer, IT Operations Manager, Application Developer, Platform / DevOps Engineer, Security / Compliance Officer, Data / Analytics Lead.
2. **Then check for a named-leader overlay** under that archetype (e.g., "VP of Engineering" overlays Executive Sponsor; "Director of Reliability" overlays SRE / Reliability Engineer). If an overlay exists, record both the archetype and the overlay so Phase 3 layers them correctly.

If no archetype is close enough, note the gap and ask the consultant whether to create a new profile. Capture named KPIs where possible (conversion rate, MTTR, uptime SLA, cost per transaction).

**Stakeholder overlay trigger:** If the consultant names a specific leader (e.g., "Sarah Chen, VP of Engineering"), check `memory/clients/<CLIENT_NAME>/stakeholder-overlays.md` for an existing overlay for this person. If no overlay exists, note that `skills/stakeholder-overlay/SKILL.md` should be run at the Phase 0 gate to capture this leader's specifics. The overlay will be saved to this client's workspace — not to the shared `stakeholder-profiles.md`. Do not run the overlay skill mid-questioning — flag it as a follow-on action.

### Q8 — What the technical team cares about
> "What does their primary technical team care about day-to-day — what are their pain points, priorities, or frustrations with the current setup?"

The technical team and leadership often have different definitions of success. Capturing both ensures the deliverable speaks to both audiences.

### Q9 — Trigger for this engagement
> "What is driving this engagement right now — is it a QBR, a renewal conversation, an expansion discussion, a scheduled touchpoint, or something else?"

The trigger shapes urgency, tone, and what a "good outcome" looks like for the consultant.

## Calibration dial routing

The "Analyst calibration" row in `current-context.md` carries three 1–5 scores (consultant experience, account familiarity, customer DT maturity). Read these values and route the engagement accordingly. If no scores were provided, default to 3 on all three.

| Score axis | 1–2 (low) | 3 (mid) | 4–5 (high) |
|---|---|---|---|
| **Consultant experience** | Deeper drill in Phase A (more CSIR follow-up turns); explain signal → business linkages explicitly in orientation hypotheses | Default depth | Terse orientation hypotheses; assume the consultant follows signal logic without elaboration |
| **Account familiarity** | Ask more S (Specific Information) follow-up questions; probe for unknown constraints | Default | Skip basic S clarifications the consultant has likely already covered |
| **Customer DT maturity** | Use simpler Dynatrace terminology in hypotheses and signals map; avoid jargon-dense phrasing | Default | Assume Dynatrace fluency; use precise DT product and capability names without definition |
| **Council size (Phase 2)** | Low experience + low maturity → reduce panel to 3 lenses (drop Consultative for internal framing) | Default 4 lenses | High experience + high maturity → 4 lenses standard; consider adding a second Skeptic pass |
| **Gate verbosity (Phase gates)** | Low familiarity → longer gate narrative, more context for each decision | Default | High familiarity + high experience → terse gate block; lead with the decision ask, not the summary |
| **Ambition ceiling (Phase 2)** | Low maturity → cap at "confirm and fix" scope; do not propose transformation-level actions | Default | High maturity → full ambition ceiling; propose strategic capability builds if evidence supports |

Record the routing decision in `current-context.md` under "Calibration routing" (one sentence per axis that deviates from the default), so later skills can inherit it without re-computing.

**Note on form calibration (F5):** the seed-prompt form currently collects the three 1–5 scores but does not display behavioral anchors for each level. When next updating the seed-prompt form, add a tooltip or label per scale showing what 1 and 5 mean. Until then, the routing above is the canonical definition; the form scores are the input, and this table is the mapping.

## Brief-complete fast path (E2)

When the opening message is a seed-prompt brief and **every MUST-HAVE field is already populated** with a real non-placeholder value, collapse Phase A and Phase B questioning into a **single sharpening message** instead of multiple turns. The sharpening message:

1. Acknowledges the brief ("Brief received — all required fields are populated.")
2. Calls out any SHOULD-HAVE field left blank and asks all of them in one batch (or notes them if the marginal-value stopping rule applies).
3. Names the one element with the most analytical uncertainty — the field or claim that, if wrong, would most change the consulting objective — and asks the consultant to confirm or sharpen it.
4. Moves directly to creating the engagement folder and writing `current-context.md` after the consultant's one-turn reply.

The fast path is triggered when: opening message has the `# Insights Forge intake brief` header AND every row of the MUST-HAVE column in the rubric below maps to a filled value in the brief. If any MUST-HAVE is missing, fall back to the standard two-phase flow.

## Exit criteria (Phase 0 gate rubric)

Phase 0 is done when every **MUST-HAVE** field below is populated in `current-context.md` with a real value — not a placeholder, not "TBD", not a guess. SHOULD-HAVE fields are not required to proceed but **help refine the framing**; if any are missing, the agent explicitly *confirms with the consultant* whether they have that context before closing the gate, phrased as helpful rather than blocking (e.g., *"Not required to proceed, but do you happen to know X? It would sharpen the framing."*). NICE-TO-HAVE fields are recorded if known but never block the gate and need not be confirmed.

**How to use this rubric:** at the end of Step 2 (Ask clarifying questions), walk through the table top-to-bottom. If a MUST-HAVE is missing, ask the corresponding question. Only proceed to Step 4 once every MUST-HAVE is satisfied (Step 3 — folder creation — can and should happen mid-questioning as soon as the client name is known, without waiting for all MUSTs).

| Field | Classification | Notes |
|---|---|---|
| Customer (name/label + business description) | **MUST-HAVE** | Without this, every downstream artifact is anonymous and ungrounded. |
| Vertical | **MUST-HAVE** | Drives which KPIs and signal → business linkages are load-bearing in Phase 1. |
| Engagement Framing — Context (C) | **MUST-HAVE** | Tone and urgency depend on it. |
| Engagement Framing — Specific Information (S) | **MUST-HAVE** | The boundary of what's usable in Phase 1. |
| Engagement Framing — Intent (I) | **MUST-HAVE** | The consulting objective in Step 4 cannot be written without it. |
| Engagement Framing — Response Format (R) | **MUST-HAVE** | Phase 3 packaging cannot be deferred — format shapes Phase 1 and Phase 2 framing. |
| Tenant type (SaaS vs Managed) | **SHOULD-HAVE** | Flag if missing but don't block. The agent generally produces useful Phase 1 hypotheses even when tenant type is uncertain; surface Managed-vs-SaaS feature gaps in capability gaps when known. |
| Active capabilities (Q5 checklist) | **MUST-HAVE** | This is the literal boundary of what insights can be surfaced. Phase 1 will hallucinate without it. |
| RUM status on the app in question | **MUST-HAVE if Q3-Intent is UX-focused; otherwise SHOULD-HAVE** | Conditional. If the consulting objective hinges on user experience, RUM status decides whether the UX story is even available — gate on it. If the engagement anchors on infrastructure, APM, or platform reliability, treat as SHOULD-HAVE and flag at the gate. |
| Consulting objective (reframed) | **MUST-HAVE** | This is the central artifact of Phase 0. If it can't be written, Phase 0 is not done. |
| Leadership priorities (named KPIs) | **SHOULD-HAVE** | Flag if missing but don't block. Vertical + archetype gives a reasonable default KPI list; consultant can validate it before Phase 1 signal-mapping. |
| Technical team priorities | **SHOULD-HAVE** | Strongly recommended but not gating. Needed for Phase 2 action-plan ownership language and Phase 3 dual-audience framing; Phase 1 hypotheses can proceed without it. |
| Engagement trigger (QBR / renewal / etc.) | **SHOULD-HAVE** | Flag if missing but don't block. Q3-Intent often captures the underlying motivation; trigger is a useful label but not analytically load-bearing. |
| Stakeholder role archetype (+ named overlay) | **MUST-HAVE** | Phase 3 reads stakeholder-profiles.md against this match. No match → generic deliverable. |
| Capability gaps | Derived in Step 6 | Not asked of the consultant — agent derives from Q5 + Q6. |
| Orientation hypotheses (3–5) | Derived in Step 5 | Not asked of the consultant — agent produces from active capabilities + vertical. |
| Prior engagement reference | **NICE-TO-HAVE** | Recorded if Step 3 finds a match; absent otherwise. |

**On the conditional rubric row (RUM status):** at the end of Step 2, re-read Q3-Intent. If Intent names a user-experience, conversion, session, or front-end outcome, the RUM-status row is MUST-HAVE for this engagement and Phase 0 should not close without it. Otherwise treat as SHOULD-HAVE and flag in the gate message.

## Steps

1. **Conditionally dispatch the doc-freshness-checker sub-agent in background.** Before opening the conversation, read `memory/long-term/freshness-report.md` and check the "Last refresh" run date. If the last check was fewer than 7 days ago AND the report shows zero Drifted or Unreachable entries → skip the dispatch and plan to note at the gate: "Doc citations verified [N days ago] — current." Only dispatch the sub-agent if the last check was 7 or more days ago, OR the report shows any open Drifted or Unreachable entries. When dispatching, call the `Agent` tool with `subagent_type: doc-freshness-checker` and `run_in_background: true`. The sub-agent refreshes Dynatrace doc citation status while the consultant answers Q1–Q9; its wall-clock work is hidden inside the user-input phase. It writes to `memory/long-term/freshness-report.md` only — it never edits long-term memory. Then **open the conversation** with the prompt above if the consultant has not described the engagement yet.
2. **Ask clarifying questions** one at a time in adaptive order, skipping any already answered. If the opening message was a seed-prompt brief, first absorb it per **Seed-prompt intake** — then question the gaps and sharpen the provisional answers before summarizing.
3. **Create the engagement folder (new engagements only — skip if reframing an existing one).**

   Once Q1 has been answered and the client name is known:

   a. Extract client short-name: lowercase, hyphen-separated (e.g., "Acme Corp" → `acme-corp`).
   b. Extract a 2–3 word problem slug from the opening description or Q3-Intent: lowercase, hyphen-separated (e.g., "API latency degrading checkout" → `api-latency`).
   c. Construct the engagement path: `memory/clients/<client-short-name>/engagements/<YYYY-MM-DD>-<slug>/` using today's date.
   d. If that folder already exists (same client, date, and slug), append `-2`, `-3`, etc.
   e. Check whether `memory/clients/<client-short-name>/` exists. If not, create it by copying the template: `memory/clients/_template/README.md`, `memory/clients/_template/environment.md`, `memory/clients/_template/contract.md`, `memory/clients/_template/stakeholder-overlays.md`, and `memory/clients/_template/engagements/README.md`.
   f. Create the engagement folder.
   g. Set ENGAGEMENT_PATH and CLIENT_NAME in working context and **hold them for the rest of this session** — every later skill uses this held value, not a shared file. There is no global pointer to write; the engagement folder is the state, and its `current-context.md` status front-matter (written in Step 8) records that it is active.
   h. **Write `.claude/active-client`** with the client short-name (one line, no trailing newline). This file is read by the client-isolation hook (`tools/client-isolation-hook.sh`) to mechanically block accidental reads from other clients' workspaces. Overwrite silently — it is a session marker, not an artifact.
   i. Confirm briefly: "Engagement folder created at `<path>`."

4. **Check past engagements — current client and cross-client lessons.**
   - **Current client:** Read `memory/clients/<CLIENT_NAME>/README.md` for prior engagement history. Surface the key lesson from the most recent engagement if found.
   - **Cross-client lessons readback:** Glob `memory/clients/*/engagements/*/lessons-learned.md` for all completed engagements across all clients. For each file whose `vertical` or `problem-shape` front-matter tag matches the current engagement's vertical or problem-shape (from Q2/Q3), read its "Cross-engagement hook" line and surface it as a brief "Prior lesson" note — e.g., *"A similar retail RUM-adoption engagement found that Davis AI grouping drift was the root cause; worth checking here."* Do not read the full file; read only the `---` front-matter block and the "Cross-engagement hook" line to keep context lean. Do not read the rest of a matched file unless the user explicitly asks to. This readback is informational — not a constraint on the current engagement — and is listed as a brief addendum before proceeding, not embedded in the framing itself.
5. **Reframe the engagement** as a clear consulting objective: what insight will be surfaced, for whom, and to what end. Write this under "Consulting objective" in `current-context.md`. Example: *"Surface underutilized RUM and Davis AI insights for [Customer]'s Executive Sponsor ahead of their Q3 renewal, demonstrating measurable value from their Full-Stack and RUM investment."*
6. **Surface 3–5 orientation hypotheses** about where value is likely hiding in the environment, given the active capabilities and vertical. Label them clearly as pre-scoring candidates — not findings. Pull from the tech → UX → business linkages in `domain-knowledge.md` and the vertical context. Example: *"Davis AI may be grouping related problems in ways the team hasn't reviewed, understating incident volume and MTTR improvement."*
7. **Confirm scope** — what this engagement will cover and what it will not. Name any capability gaps (e.g., RUM not enabled) that limit the insight surface.
8. **Write `<ENGAGEMENT_PATH>/current-context.md`** fully populated, **beginning with the status front-matter block** described under Output (set `state: active`, `phase: 0`, and today's date for both `opened` and `last-touched`). This front-matter is what `investigation-reset` and any resuming session read to find this engagement and track its lifecycle — it is required, not optional. **Pre-write MUST-HAVE scan (run before writing anything):** walk every MUST-HAVE row and scan its value for `[TBD]`, `"TBD"`, any bracketed placeholder, an empty value, or `"not provided"`. If any MUST-HAVE row trips the scan, do **not** write the file — loop back to the corresponding clarifying question, capture a real value, then re-run the scan. Write only after the scan finds zero MUST-HAVE placeholders. Every MUST-HAVE row carries a real value. SHOULD-HAVE rows carry either the consultant's answer or the literal string `"not provided (declined at gate)"` if they skipped the confirmation in Step 9 — the scan does not block on SHOULD-HAVE or NICE-TO-HAVE rows. NICE-TO-HAVE rows are written when known and omitted otherwise. No `"TBD"`, no bracketed placeholders.
9. **Verify the exit-criteria rubric and close SHOULD-HAVE gaps in one batch.** Walk the rubric table top-to-bottom. Every MUST-HAVE must be populated with a real value before proceeding. For unfilled SHOULD-HAVEs, **collect all open ones and ask them in a single batch message** — e.g., *"Not required to proceed, but these details would sharpen the framing: [field 1]? / [field 2]? / [field 3]?"* Record every answer (including "don't know" or "skip") and move on. Do not loop on a SHOULD-HAVE the consultant has declined.

   **Marginal-value stopping rule:** if the consultant has skipped or answered "don't know" to two consecutive SHOULD-HAVE gaps, stop asking the remaining SHOULD-HAVE fields for this session — additional asks have diminishing returns. Record the remaining fields as `"not provided (declined at gate)"`. MUST-HAVE gaps still require an answer regardless of this rule.
10. **Check freshness results (if dispatch occurred in Step 1).** If the sub-agent was dispatched, read `memory/long-term/freshness-report.md`. If the report shows entries in the **Drifted** or **Unreachable** buckets, list them as a short addendum to the gate presentation — e.g., *"The freshness sub-agent flagged 2 drifted citations and 1 unreachable URL; want to approve those updates as part of this gate?"* If the sub-agent has not completed yet, briefly wait (typically 30–60 seconds for ~30 URLs). If the wait runs longer than ~60 seconds, present the gate without freshness findings and note results will be surfaced at the next phase gate. If the dispatch was **skipped** (last check < 7 days, no Drifted/Unreachable), state at the gate: "Doc citations last verified [date from report] — current, no refresh needed."
11. **Present and pause at the gate.** State clearly:

    > "This is the Phase 0 framing. Please **approve**, **redirect**, or **iterate** before I begin the diagnosis."

    Record the gate decision in `<ENGAGEMENT_PATH>/decisions-log.md`. When the user approves any freshness updates from Step 10, edit the relevant long-term memory file inline (bump page-last-updated and retrieved), then clear those entries from `freshness-report.md`.

**Do not begin Phase 1 until the user approves.**

## Output

`<ENGAGEMENT_PATH>/current-context.md`, fully populated. The file **opens with a YAML status front-matter block** that makes the engagement self-describing — there is no external pointer file, so this block is how a resuming session finds the engagement and how its lifecycle state is tracked:

```yaml
---
client: <client-short-name>
slug: <slug>
state: active        # active | paused | complete
phase: 0             # current phase, 0–3; bump at each gate approval
opened: <YYYY-MM-DD>
last-touched: <YYYY-MM-DD>
---
```

Below the front-matter, the body sections:

| Section | Contents |
|---|---|
| Engagement Framing (C.S.I.R.) | **C** — Customer name/label, business description, consultant role; **S** — Known constraints, environment facts, contract phase, prior outcomes; **I** — Consultant's goal and customer's expected outcome; **R** — Deliverable format, primary audience, tone/length constraints |
| Customer | Name / label, industry, size (ACV band if provided), region(s) |
| Vertical | Named vertical |
| Tenant type | SaaS or Managed |
| Active capabilities | Checked list from Q5 |
| Out-of-scope exclusions | Capabilities or topics the consultant ruled out (e.g., Session Replay under GDPR) — a hard boundary honored in every later phase; from the seed-prompt brief or stated live. Omit the row only if there are none. |
| Analyst calibration | Consultant experience, account familiarity, and customer's Dynatrace maturity (1–5) if provided — tunes depth and tone |
| RUM status | Enabled / not enabled on the app in question; session replay on/off |
| Consulting objective | The reframed engagement goal |
| Leadership priorities | Named KPIs and strategic priorities |
| Technical team priorities | Day-to-day pain points and priorities |
| Engagement trigger | QBR / renewal / expansion / touchpoint / other |
| Orientation hypotheses | 3–5 pre-scoring candidates labeled as such |
| Capability gaps | Anything not active that limits insight surface |
| Stakeholder role archetype (+ named overlay if any) | Matched archetype from `stakeholder-profiles.md`, plus any named-leader overlay underneath it; flag if no close match exists |
| Prior engagement reference | Link to archived investigation if a match was found |
| Gate decision | Approved / Redirected / Iterating — with date |

## Common pitfalls

- **Treating Q3 as a single question.** Q3 is a four-part C.S.I.R. sub-sequence. Skipping Specific Information means orientation hypotheses will be generic. Skipping Intent means the consulting objective won't reflect what the consultant actually needs. Skipping Response Format means Phase 3 packaging decisions are made too late.
- **Jumping to Phase 1 before the gate.** The insight narrative is only as strong as the context underneath it. A wrong scope in Phase 0 propagates through every subsequent artifact.
- **Asking all clarifying questions at once.** One question at a time. A wall of questions produces short, low-quality answers.
- **Skipping the capabilities checklist.** Open-ended capability questions produce vague answers. Always use the checklist for Q5.
- **Assuming RUM is active.** Never assume. If RUM is not enabled, the user experience story is not available and the insight narrative must be reanchored.
- **Ignoring the vertical.** Retail and FSI leadership have completely different KPI vocabularies. The vertical determines which tech → business linkages are load-bearing in Phase 1.
- **Presenting orientation hypotheses as findings.** Label them clearly as pre-scoring candidates. They are navigation aids, not conclusions.
- **Leaving stakeholder profile gaps unflagged.** If the Phase 3 reader doesn't match any of the eight role archetypes closely enough, Phase 3 will be generic. Flag the gap now and ask the consultant whether to create a new profile.
- **Skipping the past engagement check.** If the team has worked with this customer or vertical before, the lessons from that archive save Phase 1 time and prevent repeated mistakes.
- **Omitting the status front-matter in `current-context.md`.** It is the only thing that makes the engagement discoverable — a resuming session scans for it, and `investigation-reset` flips its `state:` on pause/complete. No front-matter means a lost engagement.
