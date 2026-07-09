# Insights Forge — Round 2 Implementation Runbook

**Status: awaiting the approved workstream/decision list from the team review. Nothing executes until then.**

How to use this document: when you return with approvals, reference them as workstream IDs (WS-1…WS-14) and decision rulings (D1…D27). Execution proceeds in the step order below; each step lists what it contains, what it depends on, and what happens if a piece wasn't approved. Full verbatim specs (exact insertion text, line anchors as of commit `339a7f8`) are preserved in the working session and get re-anchored at edit time.

---

## Approval index — what each workstream needs, and what depends on it

| WS | What it is | Depends on | If not approved |
|---|---|---|---|
| WS-1 | Phase 0: seed intake, Q0 calibration, thin-answer rule, Direction Check, question visibility | — | WS-13 loses Q0 routing (defaults to Moderate); form seeds have no consumer |
| WS-2 | Skills → `.claude/skills/` registration, deliverable routing rule, pptx permission gate | — | /engage, /wrap-up, methodical-execution stay unregistered (CLAUDE.md-table invocation only); look/feel variance root cause stays open |
| WS-3 | 30/60/90 Gap→Solution roadmap, Exec Sponsor default, slimmed council (D1) + opt-out, focus selection (D24), manager checkpoint (D27) | WS-1 (maturity field paces buckets) | Plan keeps current 5-section shape; council stays ≥3 rounds |
| WS-4 | Engagement scope declaration + consent gates | WS-1 (Q5 seeds the declaration) | Biz-Events-style drift remains documented behavior |
| WS-5 | Reopen mode + Client redirect log + binding exclusions | — | Post-delivery replan stays accidental-only |
| WS-6 | Docs drift fixes, plain-English pass, index.html rebuild, doc-impact rule | — | Docs keep 15 known defects; triple-copy drift machine persists |
| WS-7 | Knowledge wiki-links, hub splits, memory-graph tool (round 2.5) | WS-2, WS-6 land first | Session-init stays ~15K tokens; no graph |
| WS-8 | Engagement viewer (tool + template) | WS-3 filenames settle first | Gate/manager review stays file-explorer-only |
| WS-9 | Model aliases everywhere (D15 ✓), read-only lens tools, Model Matrix, session hygiene, paths-not-paste, parallel dispatch | 9b skill edits ride WS-2's move | Models stay pinned a generation back; council stays sequential + pasted |
| WS-10 | Always-on methodical-execution (D18 ✓), evidence chain, lens calibration edits, pptx inspection | Evidence chain rides WS-3's file pass | Claims stay untiered; "it ran" deck risk stays open |
| WS-11 | /engage entry command | WS-2 (registration), WS-5 (Reopen) | Entry stays "describe the problem" only |
| WS-12 | /wrap-up + session-export tool + Pause hook | WS-2 for registration; export tool standalone | Pause keeps capturing nothing; no transcript export |
| WS-13 | Mid-phase analyst engagement (5 question points + rules) | WS-1 (Q0), WS-10 (tiers) for full effect | Phases 1–2 stay silent between gates |
| WS-14 | "What to review" gate blocks + Phase 1 gate definition + /wrap-up Reasoning trail + auto-export | WS-12 (wrap-up exists) | Phase 1 gate stays undefined; reasoning stays transcript-only |

Cross-cutting decisions that shape multiple steps: D1 (council slim + ask-first escalation), D5 (register all 13 skills), D15 (aliases — decided), D18 (always-on — decided), D24 (focus selection), D27 (manager checkpoint).

---

## Execution order

### Step 1 — Docs consolidation first (WS-6a/b)
*Why first: every later workstream's doc updates then land in one copy, not three.*

- Fix the 15 drift defects (drift register in the plan; the two contradictions first: C.S.I.R. expansion in docs/skills.md, one-pager structure in docs/deliverables.md).
- Rebuild `html/index.html` to the single-page spec: promote the Phase Flow strip (with gates shown, including Direction Check and Reopen), per-phase cards (produces / asks you / gate), gate cheat-sheet, condensed getting-started, links to docs/. Delete: Doc Browser + 8 embedded doc copies, force-graph + physics engine, Default Files viewer (move its ~60 field-guide annotations into docs/memory.md), Source Files viewer, page router, marked.js.
- Apply the 15 plain-English rewrites + create glossary, annotated-first-session, troubleshooting pages (D10).
- Tombstone deletions if D13 approved: `past-investigations.md`, `client-environments/` (git rm), fix tools/README.md:43 pointer.
- Relocate or untrack `insights-forge-leadership-brief.html` per main-branch hygiene.

**Verify:** grep for the two contradiction strings returns nothing; index.html loads from file:// with zero console errors; every docs/ link resolves.

### Step 2 — Phase 0 bundle + the CLAUDE.md single pass (WS-1, WS-4 Phase-0 parts, WS-3 Q7 default, WS-9b/10/13/14 CLAUDE.md items)
*One coordinated pass over `context-framing/SKILL.md` and CLAUDE.md so each is edited once.*

context-framing: Seed-prompt intake section (the v1 contract — coordinate with your form build), Q0 calibration, customer-maturity into Q3-C, three rubric rows, thin-answer rule, Direction Check gate (step 11 rewrite), scope declaration (step 7 rewrite + Q5 line), Exec Sponsor default at Q7, output-table rows.

CLAUDE.md: Questions-for-you rule · What-to-review gate rule (WS-14) · mid-phase engagement paragraph (WS-13) · Session hygiene section (WS-9b) · parallel dispatch rule + gates multi-lens wording (WS-9c) · deliverable routing rule (WS-2's text can land early — it's harmless pre-move) · session-init entry for methodical-execution + create `.claude/skills/methodical-execution/SKILL.md` (WS-10, ~70–80 lines, gates→checks) · interaction starter → /engage phrasing (activates fully at step 6) · Direction Check named in gates section · line-74 contradiction fix (WS-5's wording).

Supporting: decisions-log template vocabulary (Direction Check, Client redirect, Post-delivery), client-question-bank maturity entry, template README updates.

**Verify:** fresh session smoke test — paste a synthetic seed block, confirm: intake summary echoes answered/missing/thin; only gap questions asked; Direction Check presents scope + hypotheses + review list + questions in the specced order; current-context.md written with new fields; decisions-log row uses `Phase 0 Direction Check`.

### Step 3 — Phase 1–2 bundle (WS-3, WS-4, WS-10 evidence chain, WS-13 question points, WS-14 Phase 1 gate, WS-5/9b riders)
*One pass over the analysis-phase files.*

- `frameworks.md`: Evidence tiers subsection (~15 lines) + worked-example update.
- `hypothesis-generation`: Evidence field (step 2), scope-check step (new step 5 + renumber), mid-phase step 4a (evidence-chain hook), exclusions-binding input line, pitfalls.
- `signal-mapping`: quantified-linkage tier rule (step 3) + KPI/measured-linkage asks + pitfall strengthening.
- `ice-scoring`: Confidence anchor bands + deviation rule (step 2), band-deviation surfacing note, Phase-2 boundary sentence, **new final step: the Phase 1 gate presentation** (summary + What-to-review + gate ask + focus selection if D24 + decisions-log/phase-bump obligations).
- `action-plan-builder`: Sequenced roadmap restructure (step 3 + template + rollup), step 2a scope split, step 2b analyst asks (owners/cadence/budget), council rewrite (single blind round if D1: paths-not-paste, parallel single-message dispatch, blind-round file-naming guardrail, escalation ask-first checkpoint, scope-expansion candidates routing), ICE-after-council, tier inheritance, D27 manager checkpoint step if approved, pitfalls.
- `exec-onepager`: section 4 → Sequenced plan (30/60/90), gap-ID tracing clause, plan-fidelity gate update, What-to-review anchor.
- `pptx-builder`: column-semantics row edit + WS-10 output-inspection step.
- Lens body coordination (WS-3's ≥3-round text in the four council lens files — all five files in the same change, per the five-file contradiction catch).
- `optimist-lens`: scope-tagging edits. `consultative-lens`: profile-excerpt dispatch + anti-laundering rule (calibration edits can ride here or step 6 — keep with this pass since bodies are open).
- docs/lenses.md + docs/deliverables.md + docs/workflow.md updates per doc-impact map.

**Verify:** dry-run Phase 1→2 on a copy of the U-Haul engagement: hypotheses carry Evidence lines; ICE table shows tiers with in-band scores; Phase 1 gate presents with review list; council dispatches all four lenses in one message; roadmap renders Gap→Solution→30/60/90 with rollup; one-pager section 4 reads from the rollup.

### Step 4 — Reopen + session capture (WS-5, WS-12, WS-14 Part B)
- `investigation-reset`: Reopen mode (new section, mirrors Archive/Pause format), frontmatter description rewrite (also fixes the stale pointer language), resume-scan exclusion note, Pause Step 0 → wrap-up (default-yes), Archive offer, pitfalls.
- `.claude/skills/wrap-up/SKILL.md`: full skill incl. Reasoning trail section + auto-run of `session-export.py --full` (D26), no-engagement edge case.
- `tools/session-export.py`: ~150-line stdlib exporter (--session/--out/--full/--list/--selftest) + `.gitignore` exports/ entry + tools/README rewrite (also registers pptx-generator; fix its OUTPUT_DIR default while in there).
- Template README + current-context template rows (Client feedback / exclusions; session-notes line).

**Verify:** `session-export.py --selftest` passes; `--list` shows this session; export renders with tool calls collapsed; a synthetic Reopen flips state/phase and writes the Client redirect row; wrap-up produces notes with Reasoning trail citing the export filename.

### Step 5 — Engagement viewer (WS-8)
- `tools/engagement-viewer.py` (~120-line stdlib server, per-request manifest scan) + `html/engagement-viewer.html` (ported renderer/CSS, manifest-driven, PHASE_GROUPS map incl. session-notes → Log).
- docs/getting-started "Reviewing at gates" section + isolation sentence.

**Verify:** viewer lists u-haul engagement with correct phase pills; markdown renders; refresh reflects a newly written file; empty client dir renders gracefully; binds localhost only.

### Step 6 — Registration + runtime bundle, last (WS-2, WS-9a, WS-11, WS-12 registration)
- `git mv skills/ .claude/skills/` (13 folders) + guarded sed pass (~130 refs, 36 files; preserve `/mnt/skills/`) + grep verification.
- `settings.json`: model → `sonnet` alias (D15 ✓), drop `Read(skills/**)`, drop pptx pre-allow.
- Agent frontmatter pass: all 7 → aliases + tool restrictions (lens read-only; freshness checker Read/Write/WebFetch + "ONLY these three files" fix).
- Model Matrix section in docs/customizing.md; README/ROADMAP stop naming model IDs.
- `.claude/skills/engage/SKILL.md` (WS-11) — menu: new (seed) / resume / reopen / jump (gate-validating) / regenerate.
- CLAUDE.md path rewrites + on-demand table rows (engage, wrap-up, methodical-execution already present).
- One-time model comparison: re-run council + one MECE pass against archived U-Haul artifacts on the alias-resolved model; eyeball vs originals.

**Verify (the full smoke run):** fresh session → `/engage` → new engagement with seed → Direction Check → Phase 1 with mid-phase batch (CONTINUING line present) → Phase 1 gate with review list → Phase 2 single-round council (one message, four lenses) → escalation checkpoint → roadmap → one-pager prompt → deck permission prompt fires → `/wrap-up` writes notes + export. Confirm every decisions-log row uses the new vocabulary.

### Step 7 — Round 2.5: knowledge linking (WS-7)
*Only after everything above is merged and stable.*

- README.md → MOC + linking convention; playbooks + profiles hub-splits (verify by concatenation diff); CLAUDE.md session-init swap to hubs + traverse-on-need rule; 9 skill/agent Inputs updates; doc-freshness read-list update (same change as the split — silent-failure guard); `tools/memory-graph.py` + generated `docs/memory-graph.md`; docs/memory.md + Obsidian/Foam note.

**Verify:** memory-graph.py exits 0 (no broken links/dupes/orphans); session-init token count ≈ 5.5K; a Phase 1 dry run reads only matched playbook pages.

---

## Standing rules during implementation

1. **Docs ship with the workstream** — a step isn't done until its doc-impact entries land.
2. **Re-verify line anchors at edit time** — specs cite commit `339a7f8`; earlier steps shift later ones.
3. **One file, one pass** — where multiple workstreams touch a file, all edits land together (the step bundles above encode this).
4. **Branch + PR per step** — six reviewable PRs (plus round 2.5), not one monolith; each PR description carries its verify checklist results.
5. **The methodical-execution checks apply to this work too** — it goes live in step 2 and governs the rest of the implementation.
