# Review And Validation

## Purpose

After the first draft is written to disk, use this process to keep the output valid, compact, and visually polished.

## End-To-End Flow

1. Read the on-disk DSL file; do not start a new draft from memory.
2. Run `python scripts/validate_genui_card.py <file>`.
3. Fix validation errors directly in the same file and rerun until it passes.
4. After the script passes, perform design review using `design-review.md`.
5. Perform protected content wrapping review.
6. If design review changes the file, rerun validation.
7. Deliver only when validation passes after the final edit.

## Round Checklist

Check every round:

- Mode is identified: one-sentence card, existing DSL review, or capability boundary.
- Selected size is explicit: `2x2` or `2x4`.
- Output is JSONL, one object per line.
- `createSurface.catalogId` is `ohos.a2ui.extended.catalog`.
- All `surfaceId` values match.
- All component IDs are unique and references resolve.
- Component names are from the GenUI extended catalog.
- Extended field names are used: `content`, `src`, `label`.
- All data paths use `/` separators, not dots.
- Absolute paths outside repeated-item subtrees exist in `updateDataModel.value`.
- Repeated-item subtree internals use relative paths when protocol repeated binding is used.
- Layout rationale was stated before formal output.
- At least one improvement pass happened before final output.
- No fake remote media URLs are present.
- All clickable visuals have `onClick` or `Button.action`.
- The card remains compact and summary-like.
- The card was constructed from generalized rules, not from a selected template.

## Component/Card Checks

- Root dimensions match `2x2` (`160 x 160vp`) or `2x4` (`160 x 320vp`), or width is responsive while still respecting a `160vp` layout budget.
- Main zones are <= 3 for `2x2` and <= 4 for `2x4`.
- The visual focal point is obvious.
- The card is not a page-sized block.
- Internal blocks do not become many competing mini-cards.
- Horizontal rows distinguish protected and compressible content.
- CTA, time, percentage, status, price, and short labels remain readable.
- Date, weekday, time, status, CTA, primary metric, primary title, and user-requested fields display fully without ellipsis or clipping.
- Fixed widths on protected text are justified.
- If a local image exists, it uses `Image.src` and `styles.objectFit`.

## Protected Content Wrapping Review

For each horizontal layout:

1. List protected content in the row: date, weekday, CTA, time, status, percentage, price, short label, primary number, primary title, and user-requested fields.
2. Check if it sits in a narrow fixed-width container.
3. Check if it uses `textOverflow: "ellipsis"`, `clip`, or marquee. Treat that as a blocker for protected content.
4. Check if weak text is allowed to compress before protected content breaks.
5. Fix in this order:
   - widen protected column
   - shorten or move weak text
   - reduce padding, `itemMargin`, divider width, and decorative fixed columns
   - reduce font size within hierarchy
   - split the row into a `Column`
   - choose `2x4` or escalate if the protected text still cannot display fully

Do not accept character-by-character wrapping for protected short phrases.
Do not accept a visual screenshot where protected text appears as `...`.

## User Requirement First Exception

If the user explicitly requests a risky layout or unsupported-looking detail:

- Apply the smallest possible scoped exception.
- Keep protocol validity checks active.
- Mention the exception in the final response.
