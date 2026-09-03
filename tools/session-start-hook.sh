#!/usr/bin/env bash
# tools/session-start-hook.sh
# SessionStart hook: surface the client-isolation session id (stdout is added
# to session context, so the session knows its own marker path) and best-effort
# prune marker files older than 7 days. Always exits 0 — session start must
# never be blocked by this hook.

input=$(cat 2>/dev/null || true)

session_id=""
cwd=""
if command -v python3 >/dev/null 2>&1; then
    parsed=$(printf '%s' "$input" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    if not isinstance(d, dict):
        d = {}
except Exception:
    d = {}
print(d.get(\"session_id\", \"\"))
print(d.get(\"cwd\", \"\"))
" 2>/dev/null || true)
    session_id=$(printf '%s\n' "$parsed" | sed -n 1p)
    cwd=$(printf '%s\n' "$parsed" | sed -n 2p)
else
    # Tolerant fallback: scrape the fields from the raw payload.
    session_id=$(printf '%s' "$input" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
    cwd=$(printf '%s' "$input" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
fi

[ -n "$session_id" ] || session_id="unknown"

printf 'Client-isolation session id: %s (marker: .claude/session-clients/%s)\n' "$session_id" "$session_id"

# Best-effort prune of stale session markers (older than 7 days by mtime).
root="${CLAUDE_PROJECT_DIR:-$cwd}"
[ -n "$root" ] || root=$(pwd)
find "$root/.claude/session-clients" -type f -mtime +7 -delete 2>/dev/null || true

exit 0
