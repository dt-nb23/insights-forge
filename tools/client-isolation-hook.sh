#!/usr/bin/env bash
# tools/client-isolation-hook.sh
# PreToolUse hook: enforce per-session client isolation on memory/clients/.
#
# Design: hook-managed auto-lock. The first substantive touch of a client
# folder (Write/Edit/NotebookEdit anywhere under it, or Read of a
# non-carve-out file there) locks the session to that client by writing a
# marker file at .claude/session-clients/<session_id>. Once locked, any
# Read/Write/Edit/NotebookEdit/Grep/Glob that resolves into a DIFFERENT
# client's folder is denied (exit 2). The hook writes the marker itself, as a
# subprocess outside the permission system — no skill has to remember to.
#
# Read carve-outs (always allowed cross-client, read-only):
#   - current-context.md   (resume scans across engagements)
#   - lessons-learned.md   (Phase 0 cross-client lessons readback — approved,
#                           named exception; internal tool, no anonymization)
# Writes to another client's files — including these basenames — stay blocked
# once locked.
#
# Grep/Glob while locked: a search rooted inside another client's folder is
# denied; a search whose root is an ancestor of memory/clients/ (e.g. the
# project root) is denied for Grep (use an explicit path) and allowed for
# Glob only when the pattern's basename is one of the two carve-out filenames.
#
# Exit codes: 2 blocks the tool call (with the reason on stderr); 0 allows.
# The settings matcher is ".*", so this fires for EVERY tool: non-file tools
# always pass through, even on payloads that fail to parse. Only the six file
# tools (Read, Write, Edit, NotebookEdit, Grep, Glob) fail closed.
#
# To switch clients: pause/archive via skills/investigation-reset, which has
# the user approve removing .claude/session-clients/<session_id>.

if ! command -v python3 >/dev/null 2>&1; then
    echo "CLIENT ISOLATION: python3 not found on PATH; failing closed (cannot evaluate hook payload)." >&2
    exit 2
fi

# Script arrives on fd 3 so the hook payload stays on stdin for python3.
exec python3 /dev/fd/3 3<<'PYEOF'
import json
import os
import re
import sys

FILE_TOOLS = ("Read", "Write", "Edit", "NotebookEdit", "Grep", "Glob")
SEARCH_TOOLS = ("Grep", "Glob")
CARVE_OUTS = ("current-context.md", "lessons-learned.md")


def deny(*lines):
    sys.stderr.write("\n".join(lines) + "\n")
    sys.exit(2)


raw = sys.stdin.read()

# --- Tolerant pre-scan ------------------------------------------------------
# The settings matcher is ".*", so this hook fires for every tool. Non-file
# tools must pass through even on weird payloads, so scan for tool_name with
# a regex BEFORE committing to strict parsing; only the six file tools fail
# closed from here on.
m = re.search(r'"tool_name"\s*:\s*"([^"\\]*)"', raw)
if m is None or m.group(1) not in FILE_TOOLS:
    sys.exit(0)
scanned = m.group(1)

# --- Strict parse (file tools only) -----------------------------------------
try:
    payload = json.loads(raw)
except Exception as exc:
    deny("CLIENT ISOLATION: cannot parse hook payload for %s (%s); failing closed." % (scanned, exc))

if not isinstance(payload, dict):
    deny("CLIENT ISOLATION: hook payload for %s is not a JSON object; failing closed." % scanned)

tool = payload.get("tool_name")
if tool not in FILE_TOOLS:
    # The pre-scan matched text embedded elsewhere in the payload (e.g. inside
    # a Bash command string); the real tool is not a file tool.
    sys.exit(0)

tool_input = payload.get("tool_input")
if not isinstance(tool_input, dict):
    deny("CLIENT ISOLATION: %s payload has no tool_input object; failing closed." % tool)

cwd = payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()

# --- Resolve the target path ------------------------------------------------
if tool in ("Read", "Write", "Edit"):
    target = tool_input.get("file_path")
elif tool == "NotebookEdit":
    target = tool_input.get("notebook_path")
else:  # Grep / Glob: search root defaults to cwd
    target = tool_input.get("path") or cwd

if not isinstance(target, str) or not target:
    deny("CLIENT ISOLATION: %s payload has no usable target path; failing closed." % tool)

if not os.path.isabs(target):
    target = os.path.join(cwd, target)
target = os.path.realpath(target)  # kills ../ segments and symlink bypasses

# --- Scope check ------------------------------------------------------------
project = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or cwd)
clients_dir = os.path.join(project, "memory", "clients")


def rel_under(path, base):
    """Relative path if path is at/under base, else None ('' means equal)."""
    rel = os.path.relpath(path, base)
    if rel == ".":
        return ""
    if rel == ".." or rel.startswith(".." + os.sep):
        return None
    return rel


rel = rel_under(target, clients_dir)
is_search = tool in SEARCH_TOOLS
client = None
ancestor = False

if is_search:
    if rel is None:
        # Not rooted inside memory/clients/ — but a root that is an ANCESTOR
        # of it (e.g. the project root) still sees every client folder.
        if rel_under(clients_dir, target) is None:
            sys.exit(0)  # unrelated to client folders entirely
        ancestor = True
    elif rel == "":
        ancestor = True  # rooted at memory/clients/ itself: same exposure
    else:
        client = rel.split(os.sep)[0]
        if client == "_template":
            sys.exit(0)  # shared template, not client data
else:
    if rel is None or rel == "":
        sys.exit(0)  # outside memory/clients/
    client = rel.split(os.sep)[0]
    if client == "_template":
        sys.exit(0)  # shared template, not client data

# --- Session identity -------------------------------------------------------
session_id = payload.get("session_id")
if (
    not isinstance(session_id, str)
    or not re.match(r"^[A-Za-z0-9._-]+$", session_id)
    or session_id in (".", "..")
):
    deny("CLIENT ISOLATION: %s payload has no usable session_id; failing closed." % tool)

marker_dir = os.path.join(project, ".claude", "session-clients")
marker_path = os.path.join(marker_dir, session_id)
unlock_hint = (
    "To switch clients, pause/archive via skills/investigation-reset, "
    "which will have you approve: rm .claude/session-clients/%s" % session_id
)

active = None
if os.path.isfile(marker_path):
    try:
        with open(marker_path) as fh:
            active = fh.read().strip() or None
    except Exception as exc:
        deny("CLIENT ISOLATION: cannot read session marker %s (%s); failing closed." % (marker_path, exc))

# --- Grep / Glob ------------------------------------------------------------
if is_search:
    if active is None:
        sys.exit(0)  # not locked yet; searches never set the lock
    if ancestor:
        if tool == "Grep":
            deny(
                'CLIENT ISOLATION BLOCKED: session is locked to client "%s" and this Grep is '
                "rooted at %s, which spans every client folder." % (active, target),
                "Re-run with an explicit path (e.g. memory/clients/%s/ or a folder outside "
                "memory/clients/)." % active,
                unlock_hint,
            )
        pattern = tool_input.get("pattern")
        basename = pattern.replace("\\", "/").rstrip("/").split("/")[-1] if isinstance(pattern, str) else ""
        if basename in CARVE_OUTS:
            sys.exit(0)  # cross-client resume/lessons globs are an approved read carve-out
        deny(
            'CLIENT ISOLATION BLOCKED: session is locked to client "%s" and this Glob is '
            "rooted at %s, which spans every client folder." % (active, target),
            "Across clients only the carve-out filenames may be globbed "
            "(current-context.md, lessons-learned.md); otherwise root the glob at "
            "memory/clients/%s/ or outside memory/clients/." % active,
            unlock_hint,
        )
    # Rooted inside one specific client's folder.
    if client == active:
        sys.exit(0)
    deny(
        'CLIENT ISOLATION BLOCKED: session is locked to client "%s" but this %s '
        'resolves into client "%s" (%s).' % (active, tool, client, target),
        unlock_hint,
    )

# --- Read / Write / Edit / NotebookEdit -------------------------------------
is_carveout_read = tool == "Read" and os.path.basename(target) in CARVE_OUTS

if active is None:
    if is_carveout_read:
        sys.exit(0)  # cross-client read carve-out; does not lock the session
    # First substantive touch of a client folder locks the session to it. The
    # hook writes the marker itself, outside the permission system.
    try:
        os.makedirs(marker_dir, exist_ok=True)
        with open(marker_path, "w") as fh:
            fh.write(client + "\n")
    except Exception as exc:
        deny("CLIENT ISOLATION: cannot record session lock in %s (%s); failing closed." % (marker_path, exc))
    sys.exit(0)

if client == active:
    sys.exit(0)

if is_carveout_read:
    sys.exit(0)  # current-context.md / lessons-learned.md stay readable cross-client

deny(
    'CLIENT ISOLATION BLOCKED: session is locked to client "%s" but this %s '
    'resolves into client "%s" (%s).' % (active, tool, client, target),
    unlock_hint,
)
PYEOF
