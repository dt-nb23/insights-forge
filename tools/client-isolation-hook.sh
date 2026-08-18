#!/usr/bin/env bash
# tools/client-isolation-hook.sh
# PreToolUse hook: enforce client isolation on memory/clients reads and writes.
#
# Reads the hook JSON payload from stdin. Exits 1 to block the tool call,
# exits 0 to allow it. When blocking, prints a human-readable reason to stderr.
#
# Mechanism: Phase 0 (context-framing) writes the active client name to
# .claude/active-client. This hook reads that file and blocks any Read or
# Write call that targets a different client's workspace folder.
#
# Allowed without restriction:
#   - All tools other than Read and Write
#   - Paths outside memory/clients/
#   - Paths inside memory/clients/_template/ (shared template, not client data)
#   - Calls made before .claude/active-client is written (Phase 0 setup)

input=$(cat)

# Extract fields from the hook JSON payload
tool=$(echo "$input" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_name', ''))
except Exception:
    print('')
" 2>/dev/null || echo "")

path=$(echo "$input" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null || echo "")

cwd=$(echo "$input" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('cwd', ''))
except Exception:
    print('')
" 2>/dev/null || echo "")

# Only enforce on Read and Write
[[ "$tool" == "Read" || "$tool" == "Write" ]] || exit 0

# Normalize to absolute path
if [[ -n "$cwd" && "$path" != /* ]]; then
    path="${cwd}/${path}"
fi

# Only enforce on paths under memory/clients/
[[ "$path" == */memory/clients/* ]] || exit 0

# Template is always allowed (shared, not client-specific)
[[ "$path" == */memory/clients/_template/* ]] && exit 0

# Extract the client name from the path
client_in_path=$(echo "$path" | sed 's|.*/memory/clients/||' | cut -d'/' -f1)

# Read the active client marker written by Phase 0
marker="${cwd}/.claude/active-client"
[[ -f "$marker" ]] || exit 0  # Marker not yet set; allow (Phase 0 may be starting)

active=$(tr -d '[:space:]' < "$marker")
[[ -n "$active" ]] || exit 0  # Empty marker; allow

if [[ "$client_in_path" != "$active" ]]; then
    echo "CLIENT ISOLATION BLOCKED: attempted ${tool} on '${client_in_path}/' but active client is '${active}'." >&2
    echo "To access another client's data, use investigation-reset/SKILL.md to archive the current engagement first." >&2
    exit 1
fi

exit 0
