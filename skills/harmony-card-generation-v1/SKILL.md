---
name: harmony-card-generation
description: Generate HarmonyOS GenUI desktop-card DSL JSONL from a one-sentence scenario using the local GenUI developer documentation and bundled card templates. Use when asked to create, refine, validate, or write 鸿蒙/GenUI/桌面卡片/万能卡片/卡片场景/DSL/JSONL from a short natural-language request, especially "一句话生成鸿蒙桌面卡片", widget-style compact cards, schedule/weather/device/status/reminder cards, or HarmonyOS extended-catalog card artifacts.
---

# Harmony Card Generation

## What This Skill Does

- Generate compact HarmonyOS GenUI desktop-card DSL from one sentence.
- Follow the internal generation logic of `a2ui-generation`: mode detection, scoped reference reading, layout rationale before JSON, explicit improvement, file-first iteration, script validation, and design review.
- Use HarmonyOS GenUI extended Catalog rules, not AGenUI component semantics.

## Execution Boundary

- Do not use AGenUI protocol/component details as source material for HarmonyOS output. Only borrow the workflow discipline and review logic.
- Do not browse by default. Use the local GenUI docs and this skill's bundled references/templates.
- Do not expand a desktop card into a page, article, long list, or dashboard unless the user explicitly changes the task.
- Do not invent components, style keys, or built-in functions. App-specific host functions are allowed only when named as host-provided assumptions.

## First Principle: User Requirements First

- Treat the user's explicit requirement as the top priority.
- When an explicit user request conflicts with a default card rule, satisfy the user request and record the scoped exception.
- Keep all unrelated validation and design checks active. Do not use one exception to bypass the whole workflow.

## Scenario Detection

Before generation, classify the user's one sentence:

- `status glance`: a current state, metric, weather, battery, health, progress, or warning.
- `time/reminder`: meeting, course, appointment, countdown, trip, deadline, reminder.
- `action card`: one clear next action such as call, open, focus, remind, navigate, toggle.
- `device/product`: resource image, battery, mode, playback, connection state.
- `unsupported/page-like`: many sections, long explanation, complex form, table, full page.

For any information-summary query such as a place/person/event/concept, keep it as a compact summary card:

- Main sections <= 3.
- Body text <= 2 short lines.
- No dynamic list templates by default.
- No full-width page hero image.
- Escalate to page only if the user explicitly wants rich detail.

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

Use when the request exceeds compact desktop card scope.

Deliverable:

1. Clear explanation of the unsupported part
2. Closest supported card alternative
3. Ask or proceed only if the user accepts the narrower card

## Read Only What You Need

| Task type | Required docs | Load on demand |
| --- | --- | --- |
| New one-sentence card | [`reference/capability.md`](reference/capability.md), [`reference/template-catalog.md`](reference/template-catalog.md), one selected template, [`reference/card-design.md`](reference/card-design.md), [`reference/guide.md`](reference/guide.md) | [`reference/component-catalog.md`](reference/component-catalog.md), [`reference/data-binding.md`](reference/data-binding.md), [`reference/visual-interaction.md`](reference/visual-interaction.md), [`reference/spacing-elevation.md`](reference/spacing-elevation.md), [`reference/expressiveness-toolkit.md`](reference/expressiveness-toolkit.md), [`reference/design-review.md`](reference/design-review.md) |
| Existing DSL fix/review | [`reference/review-validation.md`](reference/review-validation.md), [`reference/component-catalog.md`](reference/component-catalog.md), [`reference/data-binding.md`](reference/data-binding.md) | whichever template/design doc relates to the issue |
| Visual polish after validation | [`reference/design-review.md`](reference/design-review.md), [`reference/visual-interaction.md`](reference/visual-interaction.md) | [`reference/spacing-elevation.md`](reference/spacing-elevation.md), [`reference/expressiveness-toolkit.md`](reference/expressiveness-toolkit.md) |
| Unsupported request triage | [`reference/capability.md`](reference/capability.md) | [`reference/template-catalog.md`](reference/template-catalog.md) for alternatives |

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
3. Select the closest template from [`reference/template-catalog.md`](reference/template-catalog.md), then read that template.
4. Read the required design/protocol references for the mode.
5. Before writing JSON, explicitly state a layout rationale covering:
   - selected template
   - main sections
   - visual focal point
   - information rhythm
   - key horizontal relationships
   - interaction and DataModel shape
6. Perform at least one explicit improvement pass before formal output:
   - identify what the first internal version lacks
   - improve premium feel, hierarchy, compactness, or protected-text safety
7. Generate and save the JSONL file.
8. Run `python scripts/validate_genui_card.py <path-to-dsl.jsonl>`.
9. Fix validation errors directly in the file and rerun until it passes.
10. Only after the script passes, perform design review using [`reference/design-review.md`](reference/design-review.md) and protected wrapping review using [`reference/review-validation.md`](reference/review-validation.md).
11. If design review edits the file, rerun the validator.
12. Deliver only after validation passes and review is complete.

## Non-Negotiables

- Use `version: "v0.9"` for every message.
- Use `catalogId: "ohos.a2ui.extended.catalog"`.
- Output JSONL, not Markdown-wrapped JSON, for final artifacts.
- Use extended property names: `Text.content`, `Image.src`, `Button.label`.
- Do not use standard-only `Text.text`, `Image.url`, `Button.child`, or CSS kebab-case style keys.
- Use a flat `components` adjacency list with `id` references. Never inline components in `children`.
- Include a `root` component and keep all references resolvable.
- Default desktop card shell: one compact root `Column` or `Stack`, width `100%`, around 160vp high, rounded, clipped.
- A card is not a page: main sections <= 3 by default, no long prose, no large tables, no long dynamic lists.
- Before formal output, layout rationale and at least one improvement pass are mandatory.
- Clickable UI must have real `onClick` or `Button.action`.
- Do not fabricate remote media URLs. Use provided URLs/local resources or omit the image.
- Absolute data bindings must use `/` JSON Pointer paths; template internals may use relative paths.
- Horizontal `Row` should have <= 3 direct children by default. Split, stack, or use a template/list if more are needed.
- Protected content such as time, CTA, status, temperature, battery percentage, and short CJK phrases must not be squeezed into fragments.
- Tag groups and primary CTA should not share one crowded row when there are 2+ tags; use separate rows inside a `Column`.
- After any manual/design edit, rerun the validator.

## Resources

- Sub-document index: [`reference.md`](reference.md)
- Capability scope: [`reference/capability.md`](reference/capability.md)
- Template catalog: [`reference/template-catalog.md`](reference/template-catalog.md)
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
