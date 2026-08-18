# ⚠️ Deprecated — Do Not Use

Past investigation archives have moved to the per-client workspace architecture to prevent cross-client context pollution.

**The correct location for engagement artifacts is:**
`memory/clients/<client-name>/engagements/<YYYY-MM-DD-slug>/` (nothing is moved on archive — the folder is marked `state: complete`)

**The correct location for a client's engagement history index is:**
`memory/clients/<client-name>/README.md`

Use `skills/investigation-reset/SKILL.md` to archive an investigation. Files placed in this directory will not be read by any skill.

See `memory/clients/README.md` for the full per-client workspace structure.

