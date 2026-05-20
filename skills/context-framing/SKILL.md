---
name: context-framing
description: Phase 0 procedure for framing a Dynatrace customer engagement before any diagnosis work. Use at the start of a new engagement when the consultant describes a customer, references a Dynatrace environment, or names an upcoming touchpoint (QBR, renewal, expansion, value-surfacing).
---

# Context Framing

## When to use

**Phase 0 — the required first step of every engagement.** The agent reads this skill before asking the consultant a single clarifying question.

Use this skill when:

- A new engagement begins: a consultant describes a customer, a Dynatrace environment, an upcoming meeting, or a value-surfacing goal.
- The user has redirected scope after a Phase 0 gate and the framing needs to be reset.
- The existing `current-context.md` is stale and the user has asked to reframe.

**Do not advance to Phase 1 until the user explicitly approves the output of this skill.**

## Inputs

Read these files before starting:

- `memory/long-term/stakeholder-profiles.md` — to recognize named stakeholder types and calibrate what "exec-ready" means for this engagement.
- `memory/long-term/domain-knowledge.md` — for the tech → UX → business linkage table; helps identify which insights are likely surfaceable given the active capabilities.
- `memory/long-term/terminology.md` — to use consistent terminology when restating the engagement context.
- `memory/long-term/past-investigations.md` — scan the index for any prior engagement on the same customer, vertical, or problem shape. If a match exists, surface the key lesson from that archive before proceeding.

If the consultant has not yet described the engagement, open with:

> "Tell me about the customer and what you're trying to accomplish with them."

Do not ask multiple questions at once. Let each answer drive the next question.

## Clarifying questions

Ask **one question at a time**, in adaptive order — if the consultant's opening description already answers a question, skip it and move to the next unknown. Stop asking when every **MUST-HAVE** field in the Exit-criteria rubric below is populated with a non-placeholder value.

The nine questions, in default order:

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

### Q6 — RUM on the application in question
> "Is Real User Monitoring enabled on the specific application we'll be focusing on? And if so, is Session Replay active for it?"

This determines whether a user experience story is available. If RUM is not enabled, flag it immediately as a capability gap — the insight narrative will need to anchor on APM and infrastructure signals instead.

### Q7 — Who will consume the deliverable and what they care about
> "Who on the customer side will we be presenting findings to, and what do they care about most — what KPIs, business outcomes, or strategic priorities are top of mind for them right now?"

Capture the person's role and priorities. Then resolve them against `stakeholder-profiles.md` in **two steps**:

1. **Match to a role archetype first.** Focus on what they own and decide, not their exact title. The eight archetypes are: Executive Sponsor, Product Owner, SRE / Reliability Engineer, IT Operations Manager, Application Developer, Platform / DevOps Engineer, Security / Compliance Officer, Data / Analytics Lead.
2. **Then check for a named-leader overlay** under that archetype (e.g., "VP of Engineering" overlays Executive Sponsor; "Director of Reliability" overlays SRE / Reliability Engineer). If an overlay exists, record both the archetype and the overlay so Phase 3 layers them correctly.

If no archetype is close enough, note the gap and ask the consultant whether to create a new profile. Capture named KPIs where possible (conversion rate, MTTR, uptime SLA, cost per transaction).

### Q8 — What the technical team cares about
> "What does their primary technical team care about day-to-day — what are their pain points, priorities, or frustrations with the current setup?"

The technical team and leadership often have different definitions of success. Capturing both ensures the deliverable speaks to both audiences.

### Q9 — Trigger for this engagement
> "What is driving this engagement right now — is it a QBR, a renewal conversation, an expansion discussion, a scheduled touchpoint, or something else?"

The trigger shapes urgency, tone, and what a "good outcome" looks like for the consultant.

## Exit criteria (Phase 0 gate rubric)

Phase 0 is done when every **MUST-HAVE** field below is populated in `current-context.md` with a real value — not a placeholder, not "TBD", not a guess. SHOULD-HAVE fields are not required to proceed but **help refine the framing**; if any are missing, the agent explicitly *confirms with the consultant* whether they have that context before closing the gate, phrased as helpful rather than blocking (e.g., *"Not required to proceed, but do you happen to know X? It would sharpen the framing."*). NICE-TO-HAVE fields are recorded if known but never block the gate and need not be confirmed.

**How to use this rubric:** at the end of Step 2 (Ask clarifying questions), walk through the table top-to-bottom. If a MUST-HAVE is missing, ask the corresponding question. Only proceed to Step 3 once every MUST-HAVE is satisfied.

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

1. **Open the conversation** with the prompt above if the consultant has not described the engagement yet.
2. **Ask clarifying questions** one at a time in adaptive order, skipping any already answered.
3. **Check past investigations** for any prior engagement on the same customer or vertical. Surface the key lesson if found.
4. **Reframe the engagement** as a clear consulting objective: what insight will be surfaced, for whom, and to what end. Write this under "Consulting objective" in `current-context.md`. Example: *"Surface underutilized RUM and Davis AI insights for [Customer]'s Executive Sponsor ahead of their Q3 renewal, demonstrating measurable value from their Full-Stack and RUM investment."*
5. **Surface 3–5 orientation hypotheses** about where value is likely hiding in the environment, given the active capabilities and vertical. Label them clearly as pre-scoring candidates — not findings. Pull from the tech → UX → business linkages in `domain-knowledge.md` and the vertical context. Example: *"Davis AI may be grouping related problems in ways the team hasn't reviewed, understating incident volume and MTTR improvement."*
6. **Confirm scope** — what this engagement will cover and what it will not. Name any capability gaps (e.g., RUM not enabled) that limit the insight surface.
7. **Write `memory/project-space/current-context.md`** fully populated. Every MUST-HAVE row carries a real value. SHOULD-HAVE rows carry either the consultant's answer or the literal string `"not provided (declined at gate)"` if they skipped the confirmation in Step 8. NICE-TO-HAVE rows are written when known and omitted otherwise. No `"TBD"`, no bracketed placeholders.
8. **Verify the exit-criteria rubric.** Walk the rubric table top-to-bottom. Every MUST-HAVE must be populated with a real value before proceeding. For each unfilled SHOULD-HAVE, ask the consultant a short confirming question framed as helpful-not-blocking — e.g., *"Not required to proceed, but do you happen to know [field]? It would help sharpen the framing."* Record their answer (including "don't know" or "skip") and move on. Do not loop on a SHOULD-HAVE the consultant has declined.
9. **Present and pause at the gate.** State clearly:

   > "This is the Phase 0 framing. Please **approve**, **redirect**, or **iterate** before I begin the diagnosis."

   Record the gate decision in `memory/project-space/decisions-log.md`.

**Do not begin Phase 1 until the user approves.**

## Output

`memory/project-space/current-context.md`, fully populated:

| Section | Contents |
|---|---|
| Engagement Framing (C.S.I.R.) | **C** — Customer name/label, business description, consultant role; **S** — Known constraints, environment facts, contract phase, prior outcomes; **I** — Consultant's goal and customer's expected outcome; **R** — Deliverable format, primary audience, tone/length constraints |
| Customer | Name / label, industry, size |
| Vertical | Named vertical |
| Tenant type | SaaS or Managed |
| Active capabilities | Checked list from Q5 |
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
