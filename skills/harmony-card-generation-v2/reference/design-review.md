# Design Review

Use this after the validator passes. This mirrors the AGenUI design-review phase, but all fixes must use HarmonyOS GenUI extended styles and components.

## Compact Card Checks

- The card answers one glanceable question.
- The chosen size is explicit: `2x2` (`160 x 160vp`) or `2x4` (`160 x 320vp`).
- `2x2` has no more than 3 main visual zones.
- `2x4` has no more than 4 main visual zones.
- The primary metric/title is visibly dominant.
- Secondary context is shorter than the primary content.
- The action is obvious but not larger than the main information.
- Long body copy, article sections, tables, and heavy lists are absent.
- The card is constructed from generalized rules, not copied from a template/example artifact.

## Layout Checks

- Root has a card-like shell: rounded corners, clipping, and a clear background or image.
- Root dimensions fit the selected target. If width is `"100%"`, the internal layout still respects a `160vp` width budget.
- Horizontal rows have 2 or 3 direct children, unless they use a justified repeated-item pattern.
- Fixed narrow widths are not used for protected text such as times, CTAs, status labels, prices, or percentages.
- `layoutWeight` is used for flexible text columns; small icons and fixed circles use explicit width/height.
- `maxLines` and `minFontSize` protect constrained text without hiding key information.
- Key information is not protected by truncation. Date, weekday, time, status, CTA, primary metric, primary title, and user-requested fields must display fully rather than using ellipsis, clip, or marquee.
- Crowded Rows have an explicit width budget; dividers, gaps, padding, and fixed columns do not consume space needed by protected text.

## Visual Checks

- Palette fits the scene and was chosen for the current scenario.
- Gradients and glow layers support the content, not decoration for its own sake.
- Text contrast is strong enough over gradients or images.
- Translucent blocks have border or background contrast.
- If using an image, it is a real resource and the important subject is not hidden by text.
- `2x2` has one dominant visual anchor only.
- `2x4` has one dominant visual anchor and at most one secondary visual device.

## Interaction Checks

- Clickable visual areas have `onClick` or `Button.action`.
- Host function names are meaningful and stable.
- Required action args are bound from DataModel, not hard-coded when they are business IDs.
- Accessibility labels exist for primary metric/action/meaningful icon-only areas.

## Data Checks

- DataModel keys are semantic and grouped by domain: `weather`, `meeting`, `action`, `asset`, etc.
- Display strings are precomputed when localization or formatting would otherwise make expressions brittle.
- No fake URLs, no sample business facts left from examples.

## Final Pass

Run the validator again after any edit:

```bash
python scripts/validate_genui_card.py path/to/card.dsl.jsonl
```
