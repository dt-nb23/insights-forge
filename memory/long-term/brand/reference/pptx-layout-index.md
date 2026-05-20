---
name: brand-pptx-layout-index
description: Complete index of the 64 named slide layouts in Dynatrace_Brand_Insights-Forge.pptx, grouped by purpose. Consult before picking a non-default layout in the pptx-builder skill.
metadata:
  type: reference
---

# `.pptx` slide layout index

`Dynatrace_Brand_Insights-Forge.pptx` ships with **64 named slide layouts** on a single slide master, organized by purpose. The pptx-builder skill binds to layouts by name (not by index). Default bindings for the Insights Forge six-section deck are documented in [[brand-spec]] §9; this file is the full menu when an investigation needs something the defaults don't cover.

## Title and section openers

| Layout | Use |
|---|---|
| `Title Slide` | Plain title — no speaker |
| `Title slide_1 speaker` | Title with one named presenter |
| `Title slide_2 speakers` | Two presenters |
| `Title slide_3 speakers` | Three presenters |
| `Title slide_4 speakers` | Four presenters |
| `Agenda` | Agenda slide — useful for Director audiences who expect one |
| `Section Header` | Standard section divider |
| `Section header+content` | Section divider with a short content block beneath |
| `Section header+photo background` | Section divider with a photo backdrop |
| `Section header+photo background_skewed` | Same, with a skewed photo treatment |

## Title + content (the workhorses)

| Layout | Use |
|---|---|
| `Title+content_left` | Title at top-left, content body below — the default content slide |
| `1_Title+content_left_2column` | Title + content split into two columns |
| `Title+content_centered` | Title centered, content centered |
| `Title+content+eyebrow_left` | Adds an eyebrow line above the title (use for "Executive summary", "Decision required" markers) |
| `Title+content+eyebrow_centered` | Centered variant |
| `Title+content+eyebrow_middle aligned_left` | Vertically centered |
| `Title+content+eyebrow_middle aligned_centered` | Vertically and horizontally centered |
| `Title+content_middle aligned_right` | Vertically centered, content right-aligned |

## Title only

| Layout | Use |
|---|---|
| `Title_left` | Big title, no body — for transition slides |
| `Title_centered` | Centered variant |
| `Title+eyebrow_left` | Adds eyebrow |
| `Title+eyebrow_centered` | Centered variant |
| `Title_middle aligned_left` | Vertically centered |
| `Title_middle aligned_right` | Vertically centered, right-aligned |

## Card layouts (great for findings, recommendations, risks)

| Layout | Use |
|---|---|
| `3 icon cards+title` | Three cards with icons — three findings or three actions |
| `4 icon cards+title` | Four cards with icons |
| `icon cards+title` | Variable count — flexible grid |
| `Hero image+3 cards` | Hero image plus three cards |
| `Hero image+4 cards` | Hero image plus four cards |
| `3 cards+footer image` | Three cards above a footer image |
| `4 cards+footer image` | Four cards above a footer image |
| `Hero image+horizontal content` | Hero image with horizontal content strip |

## Multi-column layouts (recommended actions, risks)

| Layout | Use |
|---|---|
| `2 text columns` | Two-column compare (e.g., current vs. proposed) |
| `3 text columns` | Three columns — action / owner / timeframe is the canonical use |
| `4 text columns` | Four columns — adds cost / risk to the action grid |
| `6 text columns` | Six columns — dense compare grids |

## Image-led layouts

| Layout | Use |
|---|---|
| `Image-fullscreen` | Full-bleed image, no other content |
| `Content+image_left` | Content with image on the left |
| `Content+image_left_2` / `1_Content+image_left_2` | Variants |
| `Content+image_right` | Content with image on the right |
| `Content+icons+sidebar image` | Content + icon list + sidebar image |
| `Content+sidebar image` | Content + sidebar image |
| `Content+image fade` | Content with a faded image background |
| `2 images` / `4 images` / `6 images` / `8 images` | Image grids |
| `2 images+caption` / `3 images+caption` / `4 images+caption` | Image grids with captions |
| `Horizontal content+6 images` | Horizontal content strip plus six images |
| `Horizontal content+8 images` | Horizontal content strip plus eight images |

## Customer story / narrative

| Layout | Use |
|---|---|
| `Customer story` | Narrative anchor — when an investigation has a "before story" |
| `Customer story_stats` | Same with stat callouts |
| `Customer story_quote` | Same with a featured quote |
| `Quote` | Standalone quote slide |

## Navigation and utility

| Layout | Use |
|---|---|
| `Menu slide 1` / `2` / `3` / `4` | Internal menu / table-of-contents variants |
| `Blank_graphic` | Blank with the gradient accent — for custom composition |
| `Blank_black` | Black blank — for custom composition on dark background |
| `Thank you slide` | Closing slide |

## How to choose

1. Start from the default binding in [[brand-spec]] §9.
2. Substitute only when the default doesn't fit the content. The eyebrow variant is the most common substitution (executive summary, decision asks).
3. Never combine two layouts on one slide. If the content warrants it, that's two slides.
4. If the content needs a layout that does not exist here, ask the user — do not improvise on the slide master.
