---
name: harmony-card-generation-v3
description: Generate HarmonyOS GenUI desktop-card DSL JSONL from a one-sentence scenario by applying generalized 2x2 and horizontal 2x4 card construction rules, protected key-info full-display checks, and component-internal width budgeting, not bundled templates. Use when asked to create, refine, validate, or write HarmonyOS/GenUI/desktop card/widget card/DSL/JSONL artifacts for 160x160vp or 320x160vp scenes.
---

# Harmony Card Generation V3

## What This Skill Does

- Generate HarmonyOS GenUI desktop-card DSL from one sentence.
- Build cards from generalized composition rules for:
  - `2x2`: `160 x 160vp`
  - `2x4`: `320 x 160vp` horizontal
- Follow a self-contained GenUI workflow: mode detection, scoped reference reading, layout rationale before JSON, explicit improvement, file-first iteration, script validation, and design review.
- Use HarmonyOS GenUI extended Catalog rules.

## Execution Boundary

- Do not browse by default. Use the local GenUI docs and this skill's bundled references.
- Do not proactively read, copy, adapt, or imitate historical card templates, sample cards, old artifacts, screenshots, or generated JSON unless the user explicitly provides an existing DSL file for refinement.
- Do not use template selection as a generation step. Generalized construction rules are the source of layout decisions.
- Do not expand a desktop card into a page, article, long list, or dashboard unless the user explicitly changes the task.
- Do not invent components, style keys, or built-in functions. App-specific host functions are allowed only when named as host-provided assumptions.

## First Principle: User Requirements First

- Treat the user's explicit requirement as the top priority.
- When an explicit user request conflicts with a default card rule, satisfy the user request and record the scoped exception.
- Keep all unrelated validation and design checks active. Do not use one exception to bypass the whole workflow.
- Choose visual language from the user's scenario, not from examples or previous outputs.

## Scenario Detection

Before generation, classify the user's one sentence:

- `status glance`: a current state, metric, weather, battery, health, progress, or warning.
- `time/reminder`: meeting, course, appointment, countdown, trip, deadline, reminder.
- `action card`: one clear next action such as call, open, focus, remind, navigate, toggle.
- `device/product`: resource image, battery, mode, playback, connection state.
- `information summary`: a place/person/event/concept/entity summarized into a compact card.
- `unsupported/page-like`: many sections, long explanation, complex form, table, full page.

For information-summary queries, keep the output card-shaped:

- Structure: title -> 1 to 3 core attributes -> brief summary -> optional tag/action.
- Body text <= 2 short lines.
- No dynamic list pattern by default.
- No full-width 16:9 hero image.
- Escalate to page only if the user explicitly wants rich detail.

## Size Selection

Choose exactly one size before writing DSL:

### `2x2` / `160 x 160vp`

Default size. Use for one primary conclusion and one supporting context:

- Status glance, simple reminder, weather+next event, device state, single progress metric, one action.
- Main zones: <= 3.
- Best when the answer can be understood in one glance without scrolling or reading a paragraph.

### `2x4` / `320 x 160vp`

Use only when the scenario genuinely needs horizontal breadth:

- A left-right relationship, two compact panes, wider protected text, richer device/product state, media plus state, or detail plus action.
- Main zones: <= 4.
- No scrolling by default. If a card needs scrolling, it is probably page-like.

If neither size can hold the request after compression, use Mode 3.

## Mode Selection

Enter exactly one mode:

### Mode 1: One-Sentence Desktop Card

Default mode. The user asks for a new card from natural language and has not provided existing DSL.

Deliverable:

1. `*_card.dsl.jsonl`

### Mode 2: Existing DSL Refinement / Review

Use when the user provides an existing GenUI card DSL file or asks to fix/review one.

Deliverable:

1. Edited on-disk DSL file
2. Validator result
3. Brief issue/fix summary

### Mode 3: Capability Boundary / Escalation

Use when the request exceeds compact desktop-card scope.

Deliverable:

1. Clear explanation of the unsupported part
2. Closest supported 2x2 or 2x4 card alternative
3. Ask or proceed only if the user accepts the narrower card

## Read Only What You Need

| Task type | Required docs | Load on demand |
| --- | --- | --- |
| New one-sentence card | [`reference/capability.md`](reference/capability.md), [`reference/card-composition-rules.md`](reference/card-composition-rules.md), [`reference/card-design.md`](reference/card-design.md), [`reference/guide.md`](reference/guide.md) | [`reference/component-catalog.md`](reference/component-catalog.md), [`reference/data-binding.md`](reference/data-binding.md), [`reference/visual-interaction.md`](reference/visual-interaction.md), [`reference/spacing-elevation.md`](reference/spacing-elevation.md), [`reference/expressiveness-toolkit.md`](reference/expressiveness-toolkit.md), [`reference/design-review.md`](reference/design-review.md) |
| Existing DSL fix/review | [`reference/review-validation.md`](reference/review-validation.md), [`reference/component-catalog.md`](reference/component-catalog.md), [`reference/data-binding.md`](reference/data-binding.md) | whichever design/protocol doc directly relates to the issue |
| Visual polish after validation | [`reference/design-review.md`](reference/design-review.md), [`reference/visual-interaction.md`](reference/visual-interaction.md) | [`reference/spacing-elevation.md`](reference/spacing-elevation.md), [`reference/expressiveness-toolkit.md`](reference/expressiveness-toolkit.md) |
| Unsupported request triage | [`reference/capability.md`](reference/capability.md), [`reference/card-composition-rules.md`](reference/card-composition-rules.md) | none by default |

## Output Persistence

Final artifacts should be written to files by default.

Priority:

1. Use the user-specified path when provided.
2. If refining an existing file, edit that file.
3. Otherwise save under the current working directory with a concise slug, e.g. `meeting-focus_card.dsl.jsonl`.

Default JSONL order:

1. `createSurface`
2. `updateComponents`
3. `updateDataModel`

After the first draft is saved, iterate on the existing file. Do not regenerate an entirely new artifact each round unless the structure is unusable.

## Workflow

1. Read the user request and classify the scenario/mode.
2. Confirm the request is within [`reference/capability.md`](reference/capability.md). If not, use Mode 3.
3. Choose `2x2` or `2x4` using [`reference/card-composition-rules.md`](reference/card-composition-rules.md).
4. Derive semantic roles from the request: identity, primary answer, metric, context, progress/trend, media, action.
5. Read the required design/protocol references for the mode.
6. Before writing JSON, explicitly state a layout rationale covering:
   - chosen size and why
   - semantic roles and main zones
   - visual focal point
   - information rhythm
   - key horizontal relationships
   - protected key information that must display fully
   - component-internal width budget for every crowded Row
   - interaction and DataModel shape
7. Perform at least one explicit improvement pass before formal output:
   - identify what the first internal version lacks
   - improve hierarchy, compactness, visual specificity, or protected-text full-display safety
8. Generate and save the JSONL file.
9. Run `python scripts/validate_genui_card.py <path-to-dsl.jsonl>`.
10. Fix validation errors directly in the file and rerun until it passes.
11. Only after the script passes, perform design review using [`reference/design-review.md`](reference/design-review.md) and protected wrapping review using [`reference/review-validation.md`](reference/review-validation.md).
12. If design review edits the file, rerun the validator.
13. Deliver only after validation passes and review is complete.

## Non-Negotiables

- Generation is rule-driven. Do not select, copy, or adapt a bundled template.
- Use `version: "v0.9"` for every message.
- Use `catalogId: "ohos.a2ui.extended.catalog"`.
- Output JSONL, not Markdown-wrapped JSON, for final artifacts.
- Use extended property names: `Text.content`, `Image.src`, `Button.label`.
- Do not use standard-only `Text.text`, `Image.url`, `Button.child`, or CSS kebab-case style keys.
- Use a flat `components` adjacency list with `id` references. Never inline components in `children`.
- Include a `root` component and keep all references resolvable.
- Target card sizes are `2x2 = 160 x 160vp` and horizontal `2x4 = 320 x 160vp`. If the host requires `width: "100%"`, still design against the selected width budget: `160vp` for `2x2`, `320vp` for `2x4`.
- A card is not a page: `2x2` main zones <= 3, `2x4` main zones <= 4, no long prose, no large tables, no long dynamic lists.
- Before formal output, layout rationale and at least one improvement pass are mandatory.
- Clickable UI must have real `onClick` or `Button.action`.
- Do not fabricate remote media URLs. Use provided URLs/local resources or omit the image.
- Absolute data bindings must use `/` JSON Pointer paths.
- Protocol repeated-item bindings may use relative paths only inside the repeated-item subtree.
- Horizontal `Row` should have <= 3 direct children by default. Split, stack, or use vertical grouping if more are needed.
- Protected content such as time, CTA, status, temperature, battery percentage, price, and short CJK phrases must not be squeezed into fragments.
- Key information must display fully by default: date, weekday, time, CTA, status, primary metric/value, primary title/name, countdown, price/count, and user-requested fields. Do not rely on `textOverflow: "ellipsis"`, `clip`, or marquee to hide missing key content.
- Use `textOverflow: "ellipsis"` only for explicitly compressible secondary text such as optional location, subtitle, or advisory copy. If a key value does not fit, first reduce padding, itemMargin, decorative dividers, fixed columns, and font size within hierarchy; then split the row, choose horizontal `2x4`, or use Mode 3.
- For every Row with two or more protected text values, do a width budget before writing JSON: available width = parent width - parent horizontal padding - row gaps - fixed dividers/icons - fixed text columns. If the fit is close, make the row simpler before generating DSL.
- Tag groups and primary CTA should not share one crowded row when there are 2+ tags; use separate rows inside a `Column`.
- After any manual/design edit, rerun the validator.

## Resources

- Sub-document index: [`reference.md`](reference.md)
- Capability scope: [`reference/capability.md`](reference/capability.md)
- Generalized card construction rules: [`reference/card-composition-rules.md`](reference/card-composition-rules.md)
- Card design: [`reference/card-design.md`](reference/card-design.md)
- DSL guide: [`reference/guide.md`](reference/guide.md)
- Component catalog: [`reference/component-catalog.md`](reference/component-catalog.md)
- Data binding: [`reference/data-binding.md`](reference/data-binding.md)
- Visual interaction: [`reference/visual-interaction.md`](reference/visual-interaction.md)
- Spacing and elevation: [`reference/spacing-elevation.md`](reference/spacing-elevation.md)
- Expressiveness toolkit: [`reference/expressiveness-toolkit.md`](reference/expressiveness-toolkit.md)
- Design review: [`reference/design-review.md`](reference/design-review.md)
- Review and validation: [`reference/review-validation.md`](reference/review-validation.md)
- Validation script: [`scripts/validate_genui_card.py`](scripts/validate_genui_card.py)
