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
- Output is JSONL, one object per line.
- `createSurface.catalogId` is `ohos.a2ui.extended.catalog`.
- All `surfaceId` values match.
- All component IDs are unique and references resolve.
- Component names are from the GenUI extended catalog.
- Extended field names are used: `content`, `src`, `label`.
- All data paths use `/` separators, not dots.
- Absolute paths outside templates exist in `updateDataModel.value`.
- Template internals use relative paths.
- Layout rationale was stated before formal output.
- At least one improvement pass happened before final output.
- No fake remote media URLs are present.
- All clickable visuals have `onClick` or `Button.action`.
- The card remains compact and summary-like.

## Component/Card Checks

- Height and density fit desktop-card scope.
- Main sections are <= 3 unless very small.
- The visual focal point is obvious.
- The card is not a page-sized block.
- Internal blocks do not become many competing mini-cards.
- Horizontal rows distinguish protected and compressible content.
- CTA, time, percentage, status, and short labels remain readable.
- Fixed widths on protected text are justified.
- If a local image exists, it uses `Image.src` and `styles.objectFit`.

## Protected Content Wrapping Review

For each horizontal layout:

1. List protected content in the row: CTA, time, status, percentage, short label, primary number.
2. Check if it sits in a narrow fixed-width container.
3. Check if weak text is allowed to compress before protected content breaks.
4. Fix in this order:
   - widen protected column
   - shorten or move weak text
   - split the row into a `Column`
   - use `minFontSize`/`maxLines`/`textOverflow` for bounded text

Do not accept character-by-character wrapping for protected short phrases.

## User Requirement First Exception

If the user explicitly requests a risky layout or unsupported-looking detail:

- Apply the smallest possible scoped exception.
- Keep protocol validity checks active.
- Mention the exception in the final response.
