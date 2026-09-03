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
| B1 | One generator-first pptx procedure | done | `skills/pptx-builder/SKILL.md` rewritten: renderer priority (generator → external skill → outline), numbered steps lead with the spec JSON and the generator run, deck-side Phase 3 gate as step 8 |
| B2 | Deck output path | done | `tools/pptx-generator.py` defaults the output alongside the spec (the dead `memory/project-space` path is gone); the documented command in `skills/pptx-builder/SKILL.md` and `tools/README.md` passes the output path explicitly; `CLAUDE.md` states every Phase 3 artifact lives in `<ENGAGEMENT_PATH>/`; `.gitignore` no longer references project-space |
| B3 | Skill promises match generator capability | done | Chose the "build it" side: wave background + overlay (with white text and a re-added footer so body layouts stay legible) and branded chart slides implemented in `tools/pptx-generator.py`; the skill's wave section now describes only the two shipped assets and no longer points at a nonexistent ".ai rendering" procedure; chart-series labels reconciled to §5 in `memory/long-term/brand/brand-spec.md` |
| B4 | Brand-gate linter + gate-1 fix | done | `tools/onepager-lint.py` (gates 1/3/4/5 + design checks; gate 1 via headless Chrome, plus a `GATE1-BUDGET` content-budget check against the reference one-pager so the fit signal survives without Chrome); wired into `skills/exec-onepager/steps/3-brand-gate.md` |
| B5 | Canonical reference one-pager | done | `skills/exec-onepager/reference/reference-onepager.html` (sanitized: fictional client, people, and vendor; passes the linter with 0 FAIL); retargeted in `skills/exec-onepager/reference/layout-system.md`, which was also made self-consistent with the gate (9px floor, no dash day ranges) |

## Group C — Guardrail enforcement

| ID | Item | Status | Disposition |
|---|---|---|---|
| C1 | Out-of-scope rule reaches the whole pipeline | pending | Gate-side scans already land with A1 (Phase 2 and Phase 3 gate blocks); lens blocks and dispatch rule pending |
| C2 | Mechanical client isolation | pending | |
| C3 | Fetch allowlist + everything-else gate | pending | |
| C4 | Opt-in font install | done | `tools/pptx-generator.py`: default run performs a read-only `check_dtflow_fonts()` and prints one platform-aware notice; installation only via `--install-fonts` (macOS/Linux; Windows documented as manual) |
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
| H1 | Column-count fallback discards content | done | `tools/pptx-generator.py`: slot layouts are sized by content — the smallest layout that holds every item (five columns land on `6 text columns`, five cards on the six-card layout); content is dropped only above six, with a loud warning; any `N text columns` / `N icon cards+title` spelling routes to the handler |
| H2 | Under-supplied card layout renders empty card | done | `tools/pptx-generator.py`: unused slots on the smallest fitting layout are removed (header, card, subcopy, icon, icon shape), so no empty box renders; verified on the 3/4/6-card and 2/3/4/6-column layouts |
| H3 | OUTPUT_DIR dead path | done | `tools/pptx-generator.py` (same fix as B2) |
| H4 | Incomplete deck exits 0 | done | `tools/pptx-generator.py` `generate()`: per-slide failure count, partial-output warning, exit 1; a chart slide missing `categories`/`series` is now a counted failure rather than a silent empty slide |
| H5 | Unconditional font install | done | `tools/pptx-generator.py` (same fix as C4) |
| H6 | No requirements.txt | done | `tools/requirements.txt` |
| H7 | Python version / platform limits undocumented | done | Floor lowered to Python 3.9 (`Optional[Path]` instead of `X \| None`) and stated in `tools/pptx-generator.py` and `tools/requirements.txt`; Windows font install documented as manual rather than half-implemented |
| H8 | tools/README placeholder text | done | `tools/README.md` rewritten against the tools that exist |

## Extras — outside the backlog, done because they block "A+"

| ID | Item | Status | Disposition |
|---|---|---|---|
| X1 | Model aliases instead of pinned model IDs | pending | |
| X2 | Docs drift found during the review (C.S.I.R. expansion, one-pager "default structure") | partial | One-pager structure corrected in `docs/deliverables.md` (five-beat arc, no fixed template); the C.S.I.R. expansion in `docs/skills.md` lands with Group F |
