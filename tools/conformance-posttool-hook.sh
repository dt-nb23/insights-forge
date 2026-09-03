#!/usr/bin/env bash
# tools/conformance-posttool-hook.sh
# PostToolUse hook (matcher: Write|Edit): keep the agent guide's docs
# snapshot in sync, then run the conformance checker after any write into
# the governed trees (skills/, .claude/agents/, memory/long-term/, tools/,
# docs/).
#
# Reads the hook JSON payload from stdin and extracts tool_input.file_path.
# If the path is one the agent guide's Docs browser may list (docs, skills,
# agents, long-term memory, the client template, plans, CLAUDE.md, README.md,
# the guide itself), regenerates html/agent-guide-docs.js when it differs
# (tools/agent-guide-bundle.py --if-stale — a no-op otherwise). If the path
# is inside a governed tree, runs python3 tools/conformance-check.py from the
# repo root. On a nonzero checker exit, echoes the violations to stderr and
# exits 2 — a PostToolUse exit 2 cannot block the already-completed write,
# but it surfaces the output to Claude for in-session correction. Everything
# else (paths elsewhere, malformed input, missing checker or python3) exits 0
# silently.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
CHECKER="$SCRIPT_DIR/conformance-check.py"

command -v python3 >/dev/null 2>&1 || exit 0
[ -f "$CHECKER" ] || exit 0

file_path=$(python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('file_path', ''))
except Exception:
    pass
" 2>/dev/null)

[ -n "$file_path" ] || exit 0

# Normalize to a repo-relative path so the prefix match works for both
# absolute and relative file_path values.
rel_path="${file_path#"$REPO_ROOT"/}"

# Snapshot sync: regenerate html/agent-guide-docs.js only when a file the
# guide lists has actually changed its content (the bundler compares first).
case "$rel_path" in
    skills/*|.claude/agents/*|memory/long-term/*|memory/clients/_template/*|docs/*|plans/*|tools/*|CLAUDE.md|README.md|html/index.html)
        if [ -f "$SCRIPT_DIR/agent-guide-bundle.py" ]; then
            (cd "$REPO_ROOT" && python3 tools/agent-guide-bundle.py --if-stale >/dev/null 2>&1) || true
        fi
        ;;
esac

case "$rel_path" in
    skills/*|.claude/agents/*|memory/long-term/*|tools/*|docs/*)
        output=$(cd "$REPO_ROOT" && python3 tools/conformance-check.py 2>&1)
        if [ $? -ne 0 ]; then
            echo "$output" >&2
            exit 2
        fi
        ;;
esac

exit 0
