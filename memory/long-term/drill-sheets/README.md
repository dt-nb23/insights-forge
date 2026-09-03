# Vertical drill sheets — Phase 0, Phase C

One sheet per customer vertical. Each replaces the generic Q8 probe ("what does the technical team care about day-to-day?") with five pre-targeted questions in a fixed order. A pre-targeted question gets a better answer in fewer turns than a generic one — this is a quality change that happens to also be faster.

## How the agent uses a sheet

1. After Phase B (the closed drill block) of `skills/context-framing/SKILL.md`, open the sheet for the vertical captured in Q2. If the customer spans two verticals, use the one the consulting objective anchors on; if none matches, fall back to the generic Q8 prompt in the skill.
2. **Prune** before asking: drop any question whose capability is not active in the Q5 checklist (each row names its capability dependency), and any question whose topic is out of scope. Report every pruned question at the Phase 0 gate under Assumptions so the consultant can override.
3. Ask the surviving questions in **one message**, in the sheet's order — the order is fixed so consultants learn it and can run it themselves in front of a customer. Use the **Client-facing phrasing** column when discovery is happening live with the customer; otherwise the consultant-facing question.
4. Record answers in `current-context.md` under "Technical team priorities", tagged `[sheet Qn]`, so Phase 1 can trace which probe produced which fact. Pre-load the sheet's **Phase 1 hooks** (the signal → KPI linkages it names) into the orientation hypotheses.

## Index

| Vertical (Q2 label) | Sheet |
|---|---|
| Retail / E-commerce | `memory/long-term/drill-sheets/retail-ecommerce.md` |
| Financial Services (FSI) | `memory/long-term/drill-sheets/financial-services.md` |
| Healthcare / Life Sciences | `memory/long-term/drill-sheets/healthcare-life-sciences.md` |
| Manufacturing | `memory/long-term/drill-sheets/manufacturing.md` |
| Telco / Media | `memory/long-term/drill-sheets/telco-media.md` |
| Public Sector | `memory/long-term/drill-sheets/public-sector.md` |
| Technology / SaaS | `memory/long-term/drill-sheets/technology-saas.md` |
| Logistics / Supply Chain | `memory/long-term/drill-sheets/logistics-supply-chain.md` |

## Status and validation

Every sheet carries a `status:` line in its front-matter. The eight sheets ship as **`draft`** — written from the domain linkages in `memory/long-term/domain-knowledge.md` and the playbooks, not yet validated by a practitioner who works the vertical. A working session with such a practitioner is what turns a sheet from draft to `validated: YYYY-MM-DD by <role>`; until then, treat the questions as a strong default, not a finished instrument, and let a consultant who knows the vertical reorder or replace a question on the spot.

## Adding or refining a sheet

- A sheet is five questions, never more than seven: the point is a fixed frame that gets checked against rather than recalled, and a long frame gets skimmed.
- Every question names its **capability dependency** (which Q5 capability must be active for the question to make sense) and a **Phase 1 hook** (the signal → UX → business linkage the answer feeds). A question with no hook is not load-bearing and does not belong on the sheet.
- Keep both phrasings: the consultant-facing question and the client-facing one, so the sheet works in discovery calls as well as in chat.
- This folder is shared-tier memory: no client names, no client-specific facts, ever. A lesson from one engagement that would improve a sheet goes through the lessons-learned → long-term promotion path with explicit approval, like any other long-term write.
