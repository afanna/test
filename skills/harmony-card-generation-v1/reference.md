# Harmony Card Generation Reference Index

Use this file as navigation only. Load the minimum reference needed for the current card task.

## Read By Task

- New one-sentence desktop card:
  [`reference/capability.md`](reference/capability.md),
  [`reference/template-catalog.md`](reference/template-catalog.md),
  one selected template under [`reference/templates/`](reference/templates/),
  [`reference/card-design.md`](reference/card-design.md),
  then [`reference/guide.md`](reference/guide.md).
- Component or style uncertainty:
  [`reference/component-catalog.md`](reference/component-catalog.md).
- Data binding, expressions, or template paths:
  [`reference/data-binding.md`](reference/data-binding.md).
- Interaction, image, CTA, or tap behavior:
  [`reference/visual-interaction.md`](reference/visual-interaction.md).
- Spacing, radius, shadow, visual depth:
  [`reference/spacing-elevation.md`](reference/spacing-elevation.md).
- Need richer visual expression inside GenUI constraints:
  [`reference/expressiveness-toolkit.md`](reference/expressiveness-toolkit.md).
- Final polish and card quality review:
  [`reference/design-review.md`](reference/design-review.md).
- Validator failure:
  [`reference/review-validation.md`](reference/review-validation.md), then the directly related reference above.

## Source Basis

This skill is derived from the local GenUI developer documentation outside `AGenUI`, especially:

- `specification/1_0/a2ui-native-protocol.md`
- `specification/1_0/harmonyos-extension-protocol.md`
- `reference/messages.md`
- `reference/types.md`
- `reference/extended-components/overview.md`
- `reference/extended-components/*.md`
- `concepts/components-and-layout.md`
- `concepts/data-model-and-binding.md`
- `concepts/expression-language.md`
- `concepts/theme-and-color-mode.md`
- `concepts/multi-device-adaptation.md`
- `dsl_template/*.dsl.jsonl`

Do not treat AGenUI documents as source material for HarmonyOS GenUI output.
The AGenUI skill is mirrored only in workflow shape: scoped reading, mode selection, layout rationale, improvement pass, validation, design review, and non-negotiable quality gates.

## Validation

Run:

```bash
python scripts/validate_genui_card.py path/to/card.dsl.jsonl
```

The script accepts either JSONL messages or a JSON array of messages. Final deliverables should still be JSONL.
