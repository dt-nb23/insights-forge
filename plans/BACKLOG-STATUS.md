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
| B2 | Deck output path | done | `tools/pptx-generator.py` defaults the output alongside the spec (the dead project-space default is gone); the documented command in `skills/pptx-builder/SKILL.md` and `tools/README.md` passes the output path explicitly; `CLAUDE.md` states every Phase 3 artifact lives in `<ENGAGEMENT_PATH>/`; `.gitignore` no longer references project-space |
| B3 | Skill promises match generator capability | done | Chose the "build it" side: wave background + overlay (with white text and a re-added footer so body layouts stay legible) and branded chart slides implemented in `tools/pptx-generator.py`; the skill's wave section now describes only the two shipped assets and no longer points at a nonexistent ".ai rendering" procedure; chart-series labels reconciled to §5 in `memory/long-term/brand/brand-spec.md` |
| B4 | Brand-gate linter + gate-1 fix | done | `tools/onepager-lint.py` (gates 1/3/4/5 + design checks; gate 1 via headless Chrome, plus a `GATE1-BUDGET` content-budget check against the reference one-pager so the fit signal survives without Chrome); wired into `skills/exec-onepager/steps/3-brand-gate.md` |
| B5 | Canonical reference one-pager | done | `skills/exec-onepager/reference/reference-onepager.html` (sanitized: fictional client, people, and vendor; passes the linter with 0 FAIL); retargeted in `skills/exec-onepager/reference/layout-system.md`, which was also made self-consistent with the gate (9px floor, no dash day ranges) |

## Group C — Guardrail enforcement

| ID | Item | Status | Disposition |
|---|---|---|---|
| C1 | Out-of-scope rule reaches the whole pipeline | done | Identical `## Hard exclusions` block in all six `.claude/agents/*-lens.md` files (verified by conformance check 3); verbatim-inline dispatch rule in `CLAUDE.md`; exclusion handling added to `skills/signal-mapping/SKILL.md`, `skills/ice-scoring/SKILL.md`, and `skills/value-highlight/SKILL.md`; exclusion scans at the Phase 2 gate (`skills/action-plan-builder/SKILL.md`), the one-pager gate (`skills/exec-onepager/steps/3-brand-gate.md`), and the deck gate (`skills/pptx-builder/SKILL.md`) |
| C2 | Mechanical client isolation | done | Hook-managed auto-lock in `tools/client-isolation-hook.sh` (session-keyed markers, realpath, fail-closed for the six file tools, Grep/Glob coverage, carve-outs matching the two named exceptions) + `tools/session-start-hook.sh` + `tools/session-end-hook.sh`; wired in `.claude/settings.json` with `Write` and `Edit` on the marker folder denied; unlock path in `skills/investigation-reset/SKILL.md`; behavior and residual gaps documented in `docs/memory.md` |
| C3 | Fetch allowlist + everything-else gate | done | `WebFetch(domain:…)` allow rules and the `WebSearch` ask rule in `.claude/settings.json`; off-list hosts forced to a human prompt by `tools/fetch-allowlist-hook.sh` (source of truth `tools/fetch-allowlist.txt`); semantics stated honestly in `tools/README.md` and `docs/research.md` |
| C4 | Opt-in font install | done | `tools/pptx-generator.py`: default run performs a read-only `check_dtflow_fonts()` and prints one platform-aware notice; installation only via `--install-fonts` (macOS/Linux; Windows documented as manual) |
| C5 | Conformance check, wired | done | Five named checks in `tools/conformance-check.py` (paths resolve — including markdown links in docs and `CLAUDE.md`; no client names in the shared tier; lens exclusion blocks; brief-contract sync; ledger integrity); three trigger layers: PostToolUse hook `tools/conformance-posttool-hook.sh` registered in `.claude/settings.json`, committed `tools/githooks/pre-commit`, and the habit line in `CLAUDE.md` |

## Group D — Memory and retrieval

| ID | Item | Status | Disposition |
|---|---|---|---|
| D1 | Lessons write/read contract | done | Write side: `skills/investigation-reset/SKILL.md` Step 2 (question → heading map, front-matter tags, Cross-engagement hook drafted and confirmed, backfill offer on resume) + the contract template `memory/clients/_template/engagements/lessons-learned.md`; read side: `skills/context-framing/SKILL.md` Step 4 (state filter, vertical/problem-shape ranking, cap of 3, front-matter + hook line only); the exception is named in `CLAUDE.md` and `docs/memory.md` |
| D2 | Hub split / retrieval layer | done | `memory/long-term/dynatrace-playbooks.md` + `memory/long-term/playbooks/` (8 files) and `memory/long-term/stakeholder-profiles.md` + `memory/long-term/profiles/` (8 files) — verified verbatim splits of the prior hub files; session init in `CLAUDE.md` loads hubs only with a traverse-on-need rule; every consuming skill and lens points at the matched file; `.claude/agents/doc-freshness-checker.md` reads `playbooks/*` so the 16 playbook citations stay in the freshness sweep; the split's intra-document playbook links were converted to explicit file references |
| D3 | Client name scrubbed from shared tier | done | Names, people, and vendor removed from `skills/exec-onepager/reference/layout-system.md`, `skills/exec-onepager/steps/1-content-assembly.md`, `skills/exec-onepager/steps/2-html-renderer.md`, and the reference one-pager (Group B); the mechanical name-form scan lands with C5 |
| D4 | Cross-client lessons lookup | done | Tagged front-matter + glob in `skills/context-framing/SKILL.md` Step 4, functional now that the write side (`skills/investigation-reset/SKILL.md`) produces matching tags; embeddings search stays a roadmap item in `plans/ROADMAP.md` until there is a corpus |
| D5 | Fill the eight [Team to note] slots | deferred | Org-level context that only a senior consultant can supply; the slots remain in `memory/long-term/domain-knowledge.md` and nothing claims otherwise. The two definition-less entries (Service-flow, Synthetic monitoring) are called out in the round summary as the highest-value slots to fill first |
| D6 | Dangling references and stale docs | done | `memory/long-term/phased-plan-timeline-framing.md` written and made a real read in `skills/exec-onepager/steps/1-content-assembly.md` (no more "(if loaded)" hedge); the two tombstones under `memory/long-term/` (past-investigations and client-environments) deleted; inventory tables updated in `memory/long-term/README.md` and `docs/memory.md`; `tools/README.md` was rewritten in Group B |

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
| X1 | Model aliases instead of pinned model IDs | done | `.claude/settings.json` sets `sonnet`; the six lens files in `.claude/agents/` use `sonnet` and `.claude/agents/doc-freshness-checker.md` uses `haiku`, so the repo can no longer pin itself a model generation back (the round-2 runbook's decision D15) |
| X2 | Docs drift found during the review (C.S.I.R. expansion, one-pager "default structure") | partial | One-pager structure corrected in `docs/deliverables.md` (five-beat arc, no fixed template); the C.S.I.R. expansion in `docs/skills.md` lands with Group F |
