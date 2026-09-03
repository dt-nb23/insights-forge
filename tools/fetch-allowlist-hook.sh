#!/usr/bin/env bash
# tools/fetch-allowlist-hook.sh
# PreToolUse hook (matcher: WebFetch): steer fetches to the documented
# source allowlist in tools/fetch-allowlist.txt.
#
# Reads the hook JSON payload from stdin and extracts tool_input.url.
# If the URL's hostname equals — or is a subdomain of — any non-comment
# line in the allowlist, exits 0 silently (allow). Otherwise it emits a
# hookSpecificOutput JSON on stdout with permissionDecision "ask", so the
# user is prompted before the fetch proceeds.
#
# This hook never blocks outright: malformed input, a missing url, or a
# missing allowlist file all fall through to exit 0. Normal permission
# rules still apply on top of this hook.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ALLOWLIST="$SCRIPT_DIR/fetch-allowlist.txt"

command -v python3 >/dev/null 2>&1 || exit 0

input=$(cat)

printf '%s' "$input" | python3 -c '
import json
import sys
from urllib.parse import urlsplit

try:
    payload = json.load(sys.stdin)
    url = payload.get("tool_input", {}).get("url", "")
    host = (urlsplit(url).hostname or "").lower().rstrip(".")
    if not host:
        sys.exit(0)

    allowed = []
    with open(sys.argv[1], encoding="utf-8") as f:
        for line in f:
            line = line.strip().lower()
            if line and not line.startswith("#"):
                allowed.append(line)

    for entry in allowed:
        if host == entry or host.endswith("." + entry):
            sys.exit(0)

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": (
                f"{host} is outside tools/fetch-allowlist.txt — per "
                "skills/external-research, confirm with the user before fetching"
            ),
        }
    }))
    sys.exit(0)
except SystemExit:
    raise
except Exception:
    # Malformed payload or unreadable allowlist — never block from this hook.
    sys.exit(0)
' "$ALLOWLIST"
exit 0
