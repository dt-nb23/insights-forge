---
name: content-assembly
description: |
  Step 1 of the exec-onepager build. Drafts all copy for the selected recipe
  from the engagement's approved action plan. Produces structured text ready
  for the brand-humanizer pre-pass — no HTML yet.
---

# Step 1 — Content assembly

Read this file at step 2 of the exec-onepager skill. The recipe has already been selected (step 1). The goal here is to draft every piece of copy — section by section — in plain text before any HTML is written. Do not build HTML in this step.

## Sources to read (in order)

1. `<ENGAGEMENT_PATH>/action-plan.md` — recommendations, rank order, owners, timeframes, tradeoffs
2. `<ENGAGEMENT_PATH>/signals-map.md` — business impact numbers, SLI/SLO grounding
3. `<ENGAGEMENT_PATH>/hypotheses.md` — confirmed/open/ruled-out status per hypothesis
4. `memory/long-term/stakeholder-profiles.md` — depth and tone calibration for the named reader
5. `memory/long-term/terminology.md` — first-use definitions for any acronym

## Plan-fidelity rules (enforce throughout)

These are hard constraints, not style preferences. The Phase 2 persona panel approved a specific plan. Phase 3 packages it faithfully.

- **Same recommendation rank order.** The recommended-actions section follows the action plan's ordering exactly — no silent re-ranking.
- **Tradeoff paired with the recommendation.** Every recommendation states its cost or risk on the same line or in the same paragraph. Never move tradeoffs to a separate section.
- **Business-impact-first opening.** The first sentence of the problem section states what changed in the business, not what was observed in telemetry. "Checkout conversion dropped 8%" not "p95 latency on cart-service rose 200ms."
- **Open hypotheses keep their uncertainty qualifier.** Any hypothesis still marked "open" in `hypotheses.md` must read as open in the one-pager — "if confirmed," "pending H-01 validation," or "gated on confirmation." The no-hedging brand rule strips weasel words; it does not license upgrading an open finding to a confident claim.
- **No new findings.** If drafting surfaces something not in the approved plan, flag it for the user rather than folding it in.

## Draft each section

Work through the recipe components in order. For each, write out the copy in structured text. Label each block clearly (e.g. `TL;DR sentence:`, `01 problem statement:`, `02 thesis:`). This output is what goes into the brand-humanizer pre-pass.

---

### TL;DR block

Draft two things:

**Summary sentence** — one sentence that answers: what already exists, what the plan does with it, and when results arrive. The key date or outcome goes in bold. Example: "uhaul.com already captures every user interaction in Dynatrace®. This plan refines that data into answers the team reaches on its own: **first results in 30 days, the full picture in 90.**"

**4 stats** — pull from `signals-map.md`. Each stat needs a number and a label (≤ 6 words). The four stats should together answer: scope, timeline, confidence, and the ask. Use the section accent token for the color (match the stat to the section it relates to).

---

### 01 · Problem

Lead with the business change, not the technical symptom. Write one of:

- **For 01A:** Two-part claim. First half: what exists or what changed. Second half: what the audience currently lacks as a result. Support sentence: context or evidence. Stat: one number that quantifies the gap.
- **For 01B:** Three rows: each with a symptom and the business consequence. Beat-line (optional subheading): one sentence framing all three symptoms together.
- **For 01C:** A verbatim or paraphrased quote from a named stakeholder. Attribution. Two context pills: short noun phrases that ground the quote in fact.
- **For 01D:** Three numbers with labels. Tie-line: one sentence tying all three together.

---

### 02 · Guide

State Dynatrace's value. Write one of:

- **For 02A:** Thesis paragraph (2–3 sentences). Then 3–4 pain→capability rows: each with the customer's question phrased as they'd ask it, and the specific capability that answers it. Capability names use approved Dynatrace terminology (brand-spec §7).
- **For 02B:** Positioning line (one sentence). List of active capabilities (just names). Trust stat (one number + label).
- **For 02D:** One confident assertion sentence with an accented key phrase. Three proof numbers with labels.

---

### 03 · Plan

State the recommended actions with owners and timeframes. Write one of:

- **For 03A/03B:** Phase names, day ranges, and descriptions. 03B adds: owner, gate, output per phase.
- **For 03D:** Numbered steps with names, day ranges, and one-line descriptions.

Always include the 30/60/90 framing from `memory/long-term/phased-plan-timeline-framing.md` (if loaded). Always include a concurrency or sequencing note.

Every action from `action-plan.md` must appear here with its paired tradeoff (plan-fidelity rule). If the tradeoff text is too long for the phase card, state it in the concurrency note or in the section's beat-line.

---

### 04 · Stakes

Frame what happens if the audience approves vs. what happens if they wait. Write one of:

- **For 04A:** Two panels: "If we wait" (risk) and "By day [N]" (outcome). 3–4 bullet items per panel.
- **For 04B:** Two panels: "If we wait" and "If we act." Plus a single verdict sentence.
- **For 04D:** Risk bullets (✕) then win bullets (✓), separated by a divider.

Stakes come directly from the risk section of `action-plan.md`. Do not invent new risks.

---

### 05 · Takeaway

State the ask explicitly. Write one of:

- **For 05A/05C:** One tk-line sentence: setup phrase, the ask (highlighted), payoff phrase (accent colored). Two named decisions: each with a name, and a description of who approves it and what they're agreeing to. 05C: add a reassurance line.
- **For 05D:** One tk-line sentence with a payoff phrase. Optional qualifier sentence (e.g., "Decision detail lives in the leadership deck.").

The decisions must come from `action-plan.md`'s explicit ask section. Do not rephrase decisions to reduce their specificity.

---

## Output format

Deliver a labeled draft block for each recipe component:

```
TL;DR sentence: [...]
TL;DR stats:
  Stat 1: [N] — [label] — color: [token]
  Stat 2: [N] — [label] — color: [token]
  Stat 3: [N] — [label] — color: [token]
  Stat 4: [N] — [label] — color: [token]

01 · Problem ([variant]):
  [beat-line if applicable]
  [main content text]

02 · Guide ([variant]):
  [thesis or positioning line]
  [supporting content]

03 · Plan ([variant]):
  Phase 1: [name] · [days] · [description] · [owner/gate/output if 03B]
  Phase 2: [...]
  Phase 3: [...]
  Concurrency note: [...]

04 · Stakes ([variant]):
  [risk panel or bullets]
  [win/success panel or bullets]

05 · Takeaway ([variant]):
  tk-line: [...]
  Decision 1: [name] — [desc]
  Decision 2: [name] — [desc]
  [reassure if 05C]
```

Hand this output to the brand-humanizer pre-pass before proceeding to step 2 (HTML build).
