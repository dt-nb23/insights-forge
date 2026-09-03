# Tools

In-repo tooling and its support files. Every tool here is **read-only with respect to the outside world**: it reads local files and writes deliverables into the engagement folder. Nothing in this folder touches a Dynatrace tenant, a data warehouse, or production state.

## What lives here

| File | Purpose |
|---|---|
| `pptx-generator.py` | Generates branded `.pptx` decks from a JSON spec against `Dynatrace_Brand_Insights-Forge.pptx`. The primary renderer for Phase 3 deck output. A default run performs **no writes outside the output deck** — a missing-font check prints a one-line notice; fonts install only via `--install-fonts`. Supports wave backgrounds with a dark overlay (text turned white, footer re-added) and branded chart slides. |
| `pptx-spec-example.json` | Annotated example spec showing every supported slide type and field. Read this before writing a deck spec. |
| `onepager-lint.py` | Brand-gate linter for Phase 3 one-pagers. Mechanizes gate 1 (one-Letter-page fit via a headless-Chrome render and PDF page count, plus a Chrome-free content-budget check against the reference one-pager), gate 3 (em/en dashes, banned phrasings, trademark first-mentions, sentence-case headings; serial-comma / AI-lexicon / British-spelling heuristics as WARNs), gate 4 (aria/role attributes, font-size minimums, white-on-teal contrast), gate 5 (`.foot-src` citation format, footer boilerplate), and the design-system checks (declared `var(--x)` tokens, palette, Arial fallback). Exit codes: 0 no FAILs · 1 FAILs present · 2 usage/parse error · 3 gate 1 unverifiable (no Chrome — do the manual print preview). Invoked by the Phase 3 brand gate: `python3 tools/onepager-lint.py <ENGAGEMENT_PATH>/<slug>-onepager.html --action-plan <ENGAGEMENT_PATH>/action-plan.md --proper-noun "<Client>"`. |
| `conformance-check.py` | Workspace conformance: (1) repo-rooted paths in skills, agents, `CLAUDE.md`, and docs resolve — backticked paths and relative markdown links alike — and every relative link in the `html/index.html` agent guide resolves; (2) no client names in the shared tier — path form anywhere, plus a name-form prose scan over `skills/`, `memory/long-term/`, `docs/`, `.claude/agents/`, `tools/` (client names derived from `memory/clients/` directory names; `plans/` and `html/` deliberately excluded); (3) every critique lens carries the exact `## Hard exclusions` block; (4) the intake-brief contract stays in sync across its producers; (5) `plans/BACKLOG-STATUS.md` uses only the closed status vocabulary and every done/partial/diverged row's cited paths resolve; (6) `html/agent-guide-docs.js` — the agent guide's docs snapshot — is in sync with the files it lists (regenerate with `python3 tools/agent-guide-bundle.py`). Run after editing skills, agents, long-term memory, docs, or tools: `python3 tools/conformance-check.py`. |
| `agent-guide-bundle.py` | Generates `html/agent-guide-docs.js`, a snapshot of every file the agent guide's Docs browser lists (read from the `data-src` anchors in `html/index.html`, so there is one registry). A `file://` page cannot fetch its sibling files but can load a script from its own folder — this is what lets `html/index.html` render the docs with no server or extension. `--if-stale` writes only on change (what the PostToolUse hook runs); `--check` exits 1 when the snapshot is missing or stale (what conformance check 6 runs). |
| `client-isolation-hook.sh` | PreToolUse hook wired in `.claude/settings.json` (matcher `Read\|Write\|Edit\|NotebookEdit\|Grep\|Glob`). **Hook-managed auto-lock**: on the session's first substantive touch of a client folder it writes a session-keyed marker at `.claude/session-clients/<session_id>` (the hook writes it — no skill step, no shared pointer file), then blocks file-tool access to any *other* client's folder. Read carve-outs, always allowed cross-client: `current-context.md` (resume scans) and `lessons-learned.md` (Phase 0 lessons readback). `../` and symlink traversal are neutralized by realpath; malformed input fails closed for the six file tools. Switching clients mid-session: `skills/investigation-reset/SKILL.md` has you approve `rm .claude/session-clients/<session-id>`. |
| `session-start-hook.sh` | SessionStart hook: announces the session id and marker path into context, and prunes isolation markers older than 7 days. |
| `session-end-hook.sh` | SessionEnd hook: best-effort removal of this session's isolation marker (leftovers are inert — markers are session-keyed). |
| `fetch-allowlist.txt` | Machine source of truth for approved WebFetch domains (one per line). Consumed by `fetch-allowlist-hook.sh`; keep in sync with the allow rules in `.claude/settings.json` and the table in `skills/external-research/SKILL.md`. |
| `fetch-allowlist-hook.sh` | PreToolUse WebFetch hook: hosts on (or subdomains of) an allowlist entry pass; any other host is forced to a human prompt via a `permissionDecision: "ask"` response. |
| `conformance-posttool-hook.sh` | PostToolUse Write/Edit hook: regenerates `html/agent-guide-docs.js` when a file the agent guide lists has changed (`agent-guide-bundle.py --if-stale`), then runs `conformance-check.py` after any edit under `skills/`, `.claude/agents/`, `memory/long-term/`, `tools/`, or `docs/` and surfaces violations to the agent for in-session correction (PostToolUse cannot block a completed write — it is a feedback layer; the pre-commit hook is the gate). |
| `githooks/pre-commit` | Committed git hook running `conformance-check.py`; blocks the commit on violations. One-time activation per clone: `git config core.hooksPath tools/githooks`. |
| `seed-prompt-generator-bundle.py` | Unpacks/repacks the application source embedded in the Seed Prompt Generator's Claude Artifact bundle export (`html/`), so the form can be edited and re-bundled. |
| `requirements.txt` | Python package dependencies (`python-pptx`; scripts require **Python 3.9+**). Install with `pip install -r tools/requirements.txt`. |

## One-time setup

```bash
# Python dependencies
pip install -r tools/requirements.txt

# Activate the conformance pre-commit gate (per clone)
git config core.hooksPath tools/githooks

# Optional: install the DT Flow fonts (the only command that writes outside the repo;
# macOS and Linux only — on Windows, right-click each DTFlow/*.otf and choose Install)
python3 tools/pptx-generator.py --install-fonts
```

## Using the deck generator

```bash
# Generate a deck from a JSON spec (the form the pptx-builder skill documents —
# spec path, then output path, so the deck lands in the engagement folder)
python3 tools/pptx-generator.py <ENGAGEMENT_PATH>/deck-spec-YYYY-MM-DD.json <ENGAGEMENT_PATH>/deck-YYYY-MM-DD.pptx

# List all available layout names in the template
python3 tools/pptx-generator.py --list-layouts
```

If the output path is omitted, the deck defaults to `<spec-dir>/deck-YYYY-MM-DD.pptx` — alongside the spec, inside the engagement folder. A default run never writes outside the output location: if DT Flow fonts are missing it prints one notice and renders with fallback fonts. If any slide fails to render, the generator saves the partial deck, reports the failures, and **exits 1** — an incomplete deck never reports success.

### Layout handling

- Card layouts (`3 icon cards+title`, `4 icon cards+title`, `icon cards+title` for six) and text-column layouts (`2/3/4/6 text columns`) are sized by content: the generator picks the **smallest layout that holds every item**, upgrading a named layout that is too small (five cards on `3 icon cards+title` move to the six-card layout) and removing unused slots so no empty box renders. Only when nothing fits (more than six items) does it fill the largest layout and warn about what it dropped. Any `N icon cards+title` or `N text columns` name routes to these handlers, whether or not `N` is a real template layout.
- A `Chart` slide whose `chart` object lacks `categories` or `series` is a failed slide (exit 1), not a silent empty slide; an unknown `type` falls back to `BAR_CLUSTERED` with a warning.

### Wave background spec fields

Any slide can carry a dark wave background. Add these fields to the slide's spec object:

| Field | Required | Values / notes |
|---|---|---|
| `wave_background` | Yes | `"wave-bg"` (closing / title-only dark slides), `"wave-ask"` (decision-required slides), or a repo-relative path to a PNG in `assets/` |
| `wave_overlay_opacity` | No | `0.0`–`1.0`; default `0.80`. Use `0.65`–`0.70` for title-only slides, `0.80`–`0.85` for body-text slides |

The wave PNG is inserted at the bottom of the z-stack; the deep-navy `#1A2440` overlay sits above it; the slide's text is set to white; and because the layout's own footer sits below the overlay, the brand-spec §8 footer line is re-added on top for body layouts (cover and closing layouts carry no footer in the template).

### Chart spec fields

Use `"layout": "Chart"` to generate a branded chart slide. `"Chart"` is a dispatch key, not a template layout name — the chart is placed on `Blank_graphic` unless the slide spec sets `slide_layout` to another real layout name. The `chart` object contains:

| Field | Required | Values / notes |
|---|---|---|
| `type` | No | `XL_CHART_TYPE` name: `BAR_CLUSTERED`, `COLUMN_CLUSTERED`, `LINE`, `PIE`, etc. Default `BAR_CLUSTERED` |
| `categories` | Yes | List of category label strings (omitting logs a warning and the slide is created without a chart) |
| `series` | Yes | List of `{"name": "...", "values": [...]}` objects (omitting logs a warning and the slide is created without a chart) |
| `left`, `top`, `width`, `height` | No | Position/size in EMUs. Omit for the default: 0.5in left / 1.5in top insets, slide width − 1.0in, slide height − 2.0in |

Brand series colors follow brand-spec §5 (Series 1 → Teal, 2 → Royal blue, 3 → Violet, 4 → Purple, 5 → Magenta, 6 → Light blue), applied automatically and cycling past six series. Never red or green.

## Boundary that all tools must respect

This agent does not run live queries or execute production changes. Any tool added to this folder must respect that boundary:

- A tool may **read** from internal documentation, design files, or local artifacts.
- A tool may **render** outputs into formats the team will use (PPTX, PDF, Markdown).
- A tool may **fetch** reference material from approved external sources.
- A tool **must not execute DQL, SQL, or any query language against production telemetry or data warehouses**.
- A tool **must not push configuration, deploy code, or modify production state**.

If a future integration is genuinely valuable but would cross this boundary, raise it with the user first. Do not silently expand the agent's scope by adding tools that exceed these limits.

## Fetch policy — what is and is not enforced

External documentation lookup is governed by [`skills/external-research/SKILL.md`](../skills/external-research/SKILL.md) and the "Authoritative external references" table in [`memory/long-term/domain-knowledge.md`](../memory/long-term/domain-knowledge.md). The approved domains live in `tools/fetch-allowlist.txt`:

- `docs.dynatrace.com` — Dynatrace product documentation (vendor-authoritative).
- `community.dynatrace.com` — Dynatrace community threads (practitioner reporting).

Enforcement, stated honestly against the platform's actual semantics:

- The two domains are `WebFetch(domain:…)` **allow** rules in `.claude/settings.json`, so allowlisted fetches never prompt.
- Any other host is forced to a **human prompt** by `fetch-allowlist-hook.sh` (a PreToolUse hook answering `permissionDecision: "ask"`). A pure permission-rule "deny everything else" is not expressible in Claude Code — deny rules outrank allow rules, so a broad WebFetch deny would also kill the allowlisted domains — which is why the hook exists.
- `WebSearch` carries an explicit **ask** rule; explicit ask rules still prompt even in permission modes where allow rules are moot.
- WebFetch rules do **not** constrain `curl`/`wget` through Bash; those go through the normal Bash permission prompt.

Any other domain — and any internal system (Slack, Salesforce, internal wikis) — requires explicit user approval and, where applicable, a dedicated tool integration in this folder before the agent will reach for it. Adding a domain means updating all three places together: the allowlist file, the settings allow rule, and the skill's table.

## Candidate future integrations

Each idea is a candidate, not a commitment; the sequencing decisions live in [`plans/ROADMAP.md`](../plans/ROADMAP.md).

- **Dynatrace read-only context fetcher** — pulls configuration inventory (Management Zones, RUM applications, SLO definitions, synthetic monitors) into the environment-intake flow for consultant approval. Configuration reads only; no query execution.
- **PDF renderer** — headless-Chrome render of the one-pager HTML to a print-ready PDF (the linter already drives Chrome for gate 1; the PDF export is the same call with the output kept).
