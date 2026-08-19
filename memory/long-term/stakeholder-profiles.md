# Stakeholder Profiles — Hub

This file is the session-init index. Full archetype content (tone notes, typical questions, decisions owned) lives in `memory/long-term/profiles/`. Read the matching profile file when you have a named stakeholder to calibrate for — do not load all profiles at session start.

## How to use this file

When a Phase 3 one-pager or deck is intended for a specific reader:

1. **Match to a role archetype** using the index below. Focus on what the person owns and decides, not what their badge says.
2. **Read the specific profile file** for full content (tone notes, questions, decision ownership).
3. **Check the individual file for overlays** — VP of Engineering overlays live in `executive-sponsor.md`; Director of Reliability in `sre-reliability.md`; Head of Data Analytics in `data-analytics.md`.
4. **If no archetype is close enough,** ask the consultant whether to create a new one.

Named-leader overlays (specific individuals at specific clients) belong in `memory/clients/<client-name>/stakeholder-overlays.md` — never here.

## Profile index

| Archetype | File | Typical titles |
|---|---|---|
| Executive Sponsor | `memory/long-term/profiles/executive-sponsor.md` | CTO, CIO, VP of Engineering, SVP of Digital |
| Product Owner | `memory/long-term/profiles/product-owner.md` | Product Manager, Director of Product, VP of Product |
| SRE / Reliability Engineer | `memory/long-term/profiles/sre-reliability.md` | SRE, Director of Reliability, Platform Reliability Lead |
| IT Operations Manager | `memory/long-term/profiles/it-operations.md` | IT Ops Manager, NOC Manager, Director of Infrastructure |
| Application Developer | `memory/long-term/profiles/application-developer.md` | Software Engineer, Staff Engineer, Engineering Manager (technical) |
| Platform / DevOps Engineer | `memory/long-term/profiles/platform-devops.md` | Platform Engineer, DevOps Engineer, Cloud Engineer |
| Security / Compliance Officer | `memory/long-term/profiles/security-compliance.md` | CISO, Director of Security, Compliance Manager |
| Data / Analytics Lead | `memory/long-term/profiles/data-analytics.md` | Head of Data Analytics, VP of Analytics, CDO |

## Named-leader overlay index

Title-type overlays are co-located with their parent archetype file. Client-specific named-leader overlays are **never** stored here — they live in `memory/clients/<client-name>/stakeholder-overlays.md`.

| Overlay | Lives in |
|---|---|
| VP of Engineering | `memory/long-term/profiles/executive-sponsor.md` |
| Director of Reliability | `memory/long-term/profiles/sre-reliability.md` |
| Head of Data Analytics | `memory/long-term/profiles/data-analytics.md` |

Updated only on explicit user approval. Use `skills/stakeholder-overlay/SKILL.md` to add a new named-leader overlay to the client workspace.
