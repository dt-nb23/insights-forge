# Backlog status ledger

The falsifiable record of every item from the fix backlog (`insights-forge-fix-backlog-v2`). One row per item ID.

Rules, enforced by `tools/conformance-check.py` check 5 once it lands (Group C): every ID keeps a row; Status uses only `pending | done | partial | diverged | deferred | dropped`; done/partial/diverged rows cite the implementing repo path(s), and every cited path must exist; deferred/dropped rows carry a one-line reason. Any change to an item's state updates this file **in the same commit**, and commit messages must not claim completion this ledger does not show.

Status meanings: `pending` — not started this round; `done` — implemented as specified; `partial` — implemented in part, remainder named; `diverged` — implemented differently from the backlog's suggestion, with the reason; `deferred` — deliberately not built this round; `dropped` — will not be built.

## Group A — Phase gates and approval clarity

| ID | Item | Status | Disposition |
|---|---|---|---|
| A1 | Gate procedure for every phase | done | Phase 0 gate rewritten to the block in `skills/context-framing/SKILL.md` (Step 11); Phase 1 gate added to `skills/ice-scoring/SKILL.md`; Phase 2 gate added to `skills/action-plan-builder/SKILL.md`; Phase 3 one-pager gate added to `skills/exec-onepager/steps/3-brand-gate.md` (deck-side gate lands with the B1 rewrite of `skills/pptx-builder/SKILL.md`) |
| A2 | Five-part gate-summary block + binary approval | done | Block, binary-approval rule, and per-phase pointers in `CLAUDE.md` (Human-in-the-loop gates); mirrored in `docs/workflow.md`; vocabulary in `memory/clients/_template/engagements/decisions-log.md` |
| A3 | Phase/last-touched bump at every gate | done | "On approval" paragraph in `CLAUDE.md` defines the semantics (`phase:` = phase being entered; Phase 3 leaves it at 3); each phase gate section names its own write; `skills/exec-onepager/SKILL.md` and `steps/3-brand-gate.md` no longer re-bump `phase:` mid-Phase-3 |

## Group B — Deliverable pipeline

| ID | Item | Status | Disposition |
|---|---|---|---|
| B1 | One generator-first pptx procedure | pending | |
| B2 | Deck output path | pending | |
| B3 | Skill promises match generator capability | pending | |
| B4 | Brand-gate linter + gate-1 fix | pending | |
| B5 | Canonical reference one-pager | pending | |

## Group C — Guardrail enforcement

| ID | Item | Status | Disposition |
|---|---|---|---|
| C1 | Out-of-scope rule reaches the whole pipeline | pending | Gate-side scans already land with A1 (Phase 2 and Phase 3 gate blocks); lens blocks and dispatch rule pending |
| C2 | Mechanical client isolation | pending | |
| C3 | Fetch allowlist + everything-else gate | pending | |
| C4 | Opt-in font install | pending | |
| C5 | Conformance check, wired | pending | |

## Group D — Memory and retrieval

| ID | Item | Status | Disposition |
|---|---|---|---|
| D1 | Lessons write/read contract | pending | |
| D2 | Hub split / retrieval layer | pending | |
| D3 | Client name scrubbed from shared tier | pending | |
| D4 | Cross-client lessons lookup | pending | |
| D5 | Fill the eight [Team to note] slots | pending | |
| D6 | Dangling references and stale docs | pending | |

## Group E — Workflow speed

| ID | Item | Status | Disposition |
|---|---|---|---|
| E1 | Conditional round 3 + force escape hatch | pending | |
| E2 | Brief-complete fast path | pending | |
| E3 | Batched Step 9 + environment block | pending | |
| E4 | Follow-on interviews named at the Phase 0 gate | pending | |
| E5 | One message per round + paths-not-paste | pending | |

## Group F — Structured intake drill

| ID | Item | Status | Disposition |
|---|---|---|---|
| F1 | Narrative funnel then closed drill block | pending | |
| F2 | Eight per-vertical drill sheets | pending | |
| F3 | Ex-ante marginal-value test | pending | |
| F4 | Calibration dial routed | pending | |
| F5 | Un-batch the calibration scales | pending | |
| F6 | One intake-brief contract (/drill) | pending | |

## Group G — Roadmap sequencing

| ID | Item | Status | Disposition |
|---|---|---|---|
| G1 | Intent before CRM pull | pending | |
| G2 | Trigger-scoped CRM field lists | pending | |
| G3 | Isolation hook before CRM; provisional CRM facts | pending | |
| G4 | Dynatrace fetcher ships before CRM | pending | |

## Group H — Code defects

| ID | Item | Status | Disposition |
|---|---|---|---|
| H1 | Column-count fallback discards content | pending | |
| H2 | Under-supplied card layout renders empty card | pending | |
| H3 | OUTPUT_DIR dead path | pending | |
| H4 | Incomplete deck exits 0 | pending | |
| H5 | Unconditional font install | pending | |
| H6 | No requirements.txt | pending | |
| H7 | Python version / platform limits undocumented | pending | |
| H8 | tools/README placeholder text | pending | |

## Extras — outside the backlog, done because they block "A+"

| ID | Item | Status | Disposition |
|---|---|---|---|
| X1 | Model aliases instead of pinned model IDs | pending | |
| X2 | Docs drift found during the review (C.S.I.R. expansion, one-pager "default structure") | pending | |
