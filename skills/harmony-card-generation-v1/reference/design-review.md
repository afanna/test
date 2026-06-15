# Design Review

Use this after the validator passes. This mirrors the AGenUI design-review phase, but all fixes must use HarmonyOS GenUI extended styles and components.

## Compact Card Checks

- The card answers one glanceable question.
- There are no more than 4 main visual zones.
- The primary metric/title is visibly dominant.
- Secondary context is shorter than the primary content.
- The action is obvious but not larger than the main information.
- Long body copy, article sections, tables, and heavy lists are absent.

## Layout Checks

- Root has a card-like shell: width `100%`, rounded corners, clipping, and a clear background or image.
- Height is compact; existing templates are around `160`.
- Horizontal rows have 2 or 3 direct children, unless they use a scroll/list pattern.
- Fixed narrow widths are not used for protected text such as times, CTAs, status labels, prices, or percentages.
- `layoutWeight` is used for flexible text columns; small icons and fixed circles use explicit width/height.
- `maxLines`, `textOverflow`, and `minFontSize` protect constrained text.

## Visual Checks

- Palette fits the scene and is not copied blindly from the selected template.
- Gradients and glow layers support the content, not decoration for its own sake.
- Text contrast is strong enough over gradients or images.
- Translucent blocks have border or background contrast.
- If using an image, it is a real resource and the important subject is not hidden by text.

## Interaction Checks

- Clickable visual areas have `onClick` or `Button.action`.
- Host function names are meaningful and stable.
- Required action args are bound from DataModel, not hard-coded when they are business IDs.
- Accessibility labels exist for primary metric/action/meaningful icon-only areas.

## Data Checks

- DataModel keys are semantic and grouped by domain: `weather`, `meeting`, `action`, `asset`, etc.
- Display strings are precomputed when localization or formatting would otherwise make expressions brittle.
- No fake URLs, no sample business facts left from the template.

## Final Pass

Run the validator again after any edit:

```bash
python scripts/validate_genui_card.py path/to/card.dsl.jsonl
```
