---
name: mece-decomposition
description: Procedure for building a MECE issue tree from an ambiguous problem statement. Use any time a vague problem needs decomposition before hypotheses can be generated.
---

# MECE Decomposition

## When to use

Any time a vague problem needs decomposition before hypotheses can be generated. This is the **first deliverable of Phase 1**. The agent must read this skill before producing a tree.

Use this skill when:

- The user has approved the Phase 0 framing in `current-context.md` and the team is ready to enumerate possible causes.
- The user has redirected scope after Phase 0 or Phase 1 and the tree needs to be rebuilt.
- The MECE lens has flagged structural issues and the tree needs revision.

## Inputs

**Resolve the engagement path first (before reading any files):**

1. Use the `ENGAGEMENT_PATH` already established for this session. The agent fixes it once — when Phase 0 (`context-framing`) creates the engagement folder, or when a paused/active engagement is resumed — and holds it in working context for the rest of the session. There is **no shared pointer file** to read; nothing depends on a global "active" file a second concurrent session could overwrite.
2. If no engagement is established yet (a fresh session picking up earlier work), resolve it with the resume procedure in `skills/investigation-reset/SKILL.md`: scan `memory/clients/*/engagements/*/current-context.md` for a `state:` of `active` or `paused`, present the matches, and have the user pick one. If none, stop: "No active engagement found. Start a new engagement or resume a paused one."
3. ENGAGEMENT_PATH = the established/selected path (e.g., `memory/clients/acme-corp/engagements/2026-06-18-api-latency/`). CLIENT_NAME = the segment between `memory/clients/` and `/engagements/`.
4. All phase file reads/writes use ENGAGEMENT_PATH as the base — e.g., `<ENGAGEMENT_PATH>/current-context.md`.

Then read these files:

- `<ENGAGEMENT_PATH>/current-context.md` — for the reframed problem and scope.
- `memory/long-term/frameworks.md` — for MECE definitions and pitfalls.
- `memory/long-term/domain-knowledge.md` — for the common signal patterns and tech/UX/business linkages.

If any of these inputs is missing or stale, raise that with the user before drafting.

If a Dynatrace concept needed to shape a branch (e.g., Smartscape grouping, Management Zone scoping, Davis problem boundaries) is not adequately defined in local memory, consult `skills/external-research/SKILL.md` before drafting. The allowlist is `docs.dynatrace.com` and `community.dynatrace.com`. Cite the source URL and retrieval date in the branch's "what we'd see if this is the cause" line when the branch leans on an externally sourced concept.

## Steps

1. **Restate the problem as a question.** A good root for an issue tree is a question, not a statement. "Why has iOS checkout conversion declined 8% week-over-week while web is flat?" — not "iOS checkout is broken." Write the question in `issue-tree.md` under "Root problem".
2. **Identify the axis of decomposition.** Pick one. Common axes:
   - **System layer** (client → network → backend → data → third-party).
   - **User journey stage** (entry → navigation → cart → payment → confirmation).
   - **Stakeholder/team boundary** (frontend → backend → payments → analytics).
   - **Time** (pre-deploy vs post-deploy; before vs after a known event).
   Use the axis that maps cleanly to where the problem might live. Do not mix axes inside a single level of the tree.
   If two axes fit comparably well, present both with one line on what each surfaces best and ask (per the CLAUDE.md communication protocol) rather than picking silently — this is a Phase 1 checkpoint mode behavior.
3. **Draft 4–7 branches.** Fewer than 4 is usually under-decomposed; more than 7 usually means abstraction is mixed. Branches should be problem spaces, not solutions and not conclusions.
4. **For each branch, write the "what we'd see if this is the cause" line.** This forces the branch to be concrete and seeds the hypothesis generation step.
5. **Check each pair of branches for overlap.** For every pair, name a plausible cause and ask: "Where does this go?" If the answer is "either branch", you have overlap. Rename or restructure.
6. **Check the set for gaps.** Cycle through the high-frequency missed branches: **third-party**, **business process / configuration change**, **instrumentation gaps**, **deploy events**, **data quality**. Confirm each is represented or genuinely not relevant.
7. **Verify all branches are at the same level of abstraction.** Read them out loud. If one sounds like a stack layer and another sounds like a specific component, the abstraction is mixed — restructure.
8. **Invoke the MECE lens** (`.claude/agents/mece-lens.md`) for critique. Capture the findings in the "MECE check" section of `issue-tree.md`.
9. **Revise** based on the lens output. Re-invoke if the revision was substantial.
10. **Write to `<ENGAGEMENT_PATH>/issue-tree.md`.** Append a "Version history" entry describing what changed.
11. **Checkpoint (Phase 1 checkpoint mode — default ON).** Before hypothesis generation begins, pause and present per the CLAUDE.md communication protocol: a 2–3 sentence summary of the tree and its axis, the choice (confirm / adjust / name a lens), and a pointer to `issue-tree.md`. Skip this step only if the user has explicitly turned Phase 1 checkpoint mode off for the session.

## Output

The agent writes (and overwrites) `<ENGAGEMENT_PATH>/issue-tree.md`. The file follows the template: root problem, branches with "what we'd see" notes, MECE check, version history.

## Common pitfalls

- **Solution-shaped branches** — "Add caching" is not a problem space. "Cache behavior" is. Rephrase.
- **Mixed abstraction levels** — Do not put a platform ("iOS") next to a service ("payment-service") at the same level. Pick one axis.
- **Missing the third-party / business-process / instrumentation-gap branches** — These are the three most commonly omitted. Cycle through them deliberately at step 6.
- **Branches phrased as conclusions** — "Backend is slow" presupposes the answer. Use "Backend behavior" so the tree can actually do its job.
- **Skipping the MECE lens because the tree "feels right"** — The lens exists to catch what looks fine to the author. Always run it.
