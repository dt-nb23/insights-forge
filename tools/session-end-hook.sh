#!/bin/bash
# SessionEnd hook: best-effort removal of this session's client-isolation marker.
# Markers are keyed by session_id, so a leftover from a crashed session is inert;
# tools/session-start-hook.sh prunes anything older than 7 days.
command -v python3 >/dev/null 2>&1 || exit 0
python3 - <<'PY' 2>/dev/null
import json, os, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
sid = d.get("session_id", "")
cwd = d.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR", "")
if not sid or not cwd:
    sys.exit(0)
p = os.path.join(cwd, ".claude", "session-clients", sid)
try:
    if os.path.isfile(p):
        os.remove(p)
except OSError:
    pass
PY
exit 0
