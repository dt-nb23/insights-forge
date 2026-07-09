# Insights Forge — Documentation

Welcome. This folder is the friendly tour of Insights Forge. The root [README](../README.md) is the elevator pitch; here we slow down and walk you through how the workspace actually thinks, where each piece of behavior lives, and how to read the agent's own source files alongside the prose.

Every doc in this folder follows the same shape: a short *what is this and why does it exist*, a walkthrough of how it works, and a **Look inside** section that links you to the actual agent files so you can read them yourself. Nothing here is meant to replace the source — it's meant to make the source easier to navigate.

## If you're new — start here

Read these in order. About 20 minutes total.

1. **[getting-started.md](getting-started.md)** — set up the workspace, populate stakeholders, run your first investigation end-to-end.
2. **[workflow.md](workflow.md)** — the four-phase loop in depth. What happens in each phase, what the gate looks like, where artifacts land.
3. **[lenses.md](lenses.md)** — the six critique sub-agents and when each one earns its keep.
4. **[seed-prompt-generator.md](seed-prompt-generator.md)** — the browser intake form that assembles a ready-to-paste Phase 0 seed prompt. The fast on-ramp to a new engagement.

## If you're customizing or extending

These four cover the *why* behind the workspace's design rules and how to safely change them.

4. **[memory.md](memory.md)** — how live investigation state and durable knowledge are kept apart, and why auto-promotion was deliberately not built.
5. **[research.md](research.md)** — the external-reference allowlist, the citation policy, and the background sub-agent that watches Dynatrace docs for drift.
6. **[skills.md](skills.md)** — index of the procedural skills the agent reads before producing each phase's artifact.
7. **[deliverables.md](deliverables.md)** — Phase 3 brand specification: fonts, layouts, voice, terminology.
8. **[customizing.md](customizing.md)** — what to tune for your team first, and what *not* to change without thinking twice.

## Where the truth lives

`/docs/` is the tour. The actual authoritative behavior lives in these files. When the docs and the source disagree, **the source wins** — and please [open an issue](https://github.com/) or just edit the docs so the next person doesn't get tripped up.

| Topic | Read the docs page | Read the source |
|---|---|---|
| Agent operating principles | [workflow.md](workflow.md) | [`CLAUDE.md`](../CLAUDE.md) |
| Live investigation memory | [memory.md](memory.md) | [`memory/clients/README.md`](../memory/clients/README.md) |
| Durable knowledge | [memory.md](memory.md) | [`memory/long-term/README.md`](../memory/long-term/README.md) |
| Phase procedures | [skills.md](skills.md) | individual [`SKILL.md`](../skills/) files |
| Critique-lens behavior | [lenses.md](lenses.md) | individual files in [`.claude/agents/`](../.claude/agents/) |
| Brand spec for Phase 3 | [deliverables.md](deliverables.md) | [`memory/long-term/brand/brand-spec.md`](../memory/long-term/brand/brand-spec.md) |
| Tooling boundary | [customizing.md](customizing.md) | [`tools/README.md`](../tools/README.md) |
