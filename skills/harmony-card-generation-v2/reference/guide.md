# DSL And Card Generation Guide

## Required Message Shape

Generate JSONL with exactly one JSON object per line:

```jsonl
{"version":"v0.9","createSurface":{"surfaceId":"sample-card","catalogId":"ohos.a2ui.extended.catalog","theme":{"primaryColor":"#4D5CFF"}}}
{"version":"v0.9","updateComponents":{"surfaceId":"sample-card","components":[{"id":"root","component":"Column","children":["title"],"styles":{"width":160,"height":160}}]}}
{"version":"v0.9","updateDataModel":{"surfaceId":"sample-card","path":"/","value":{"title":"Sample"}}}
```

Rules:

- `version` is always `"v0.9"`.
- Use `createSurface` before components or data.
- Use `catalogId: "ohos.a2ui.extended.catalog"`.
- Keep the same `surfaceId` in all messages.
- Prefer `path: "/"` in `updateDataModel`.

## Root Size

Design against exact card budgets:

```json
{"id":"root","component":"Column","children":["primary"],"styles":{"width":160,"height":160,"borderRadius":22,"clip":true}}
```

```json
{"id":"root","component":"Column","children":["header","focal","details","action"],"styles":{"width":160,"height":320,"borderRadius":22,"clip":true}}
```

If the host runtime requires responsive width, `styles.width` may be `"100%"`, but the composition must still fit a `160vp` width budget.

## Component Model

Use a flat adjacency list:

```json
{"id":"root","component":"Column","children":["title","action"]}
{"id":"title","component":"Text","content":{"path":"/title"}}
```

Do not inline child component objects:

```json
{"id":"root","component":"Column","children":[{"component":"Text","content":"Wrong"}]}
```

## Extended-Catalog Property Names

Desktop cards use the HarmonyOS extended catalog. Use:

- `Text.content`, not `Text.text`.
- `Image.src`, not `Image.url`.
- `Button.label`, not `Button.child`.
- `styles.backgroundColor`, `styles.borderRadius`, `styles.fontSize`, not CSS kebab-case.
- `onClick: [{ "call": "...", "args": {...} }]` for clickable containers.
- `Button.action` only when a semantic Button is used; if both `action` and `onClick` are present, `action` takes priority.

## Card Layout Guidance

- `2x2`: root `width: 160`, `height: 160`, root padding `10` to `12`, 2 to 3 main zones.
- `2x4`: root `width: 160`, `height: 320`, root padding `12` to `14`, 3 to 4 main zones.
- Use `borderRadius` around `20` to `24` and `clip: true`.
- Limit rows to 2 or 3 direct children unless using a clearly justified repeated-item pattern.
- Use `Stack` for layered glow/image/progress effects and `Column`/`Row` for information layout.
- Use `itemMargin` for spacing between Row/Column children.
- Keep short protected text readable: time, temperature, count, CTA, status labels, battery percentages.
- Prefer `maxLines: 1` and `minFontSize` for constrained headline values.
- Do not put `textOverflow: "ellipsis"` on key information such as date, weekday, time, status, CTA, primary metric, primary title, or user-requested fields. Make the key text fit by reducing padding/gaps/font size, moving secondary text, splitting rows, or choosing `2x4`.

## Data Model Rules

- Bind dynamic visible data with `{ "path": "/..." }`.
- Keep static decorative values literal only when they are structural, such as empty spacer text.
- Make every absolute path used by a visible component exist in `updateDataModel.value`.
- Keep host action arguments bound to data where possible:

```json
"onClick":[{"call":"openTrainingPlan","args":{"planId":{"path":"/plan/id"}}}]
```

## Expression Rules

Expressions are available only in the extended catalog and only in `updateComponents` scalar values:

```json
{"content":"{{ 'Left ' + $__dataModel.countdown.days + ' days' }}"}
```

Use expressions sparingly in desktop cards. For one-sentence generation, prefer precomputed display strings in `updateDataModel` because they are easier to validate and localize.

Do not use expressions in `id`, `component`, path strings, or event `call` names.

## Interaction Rules

- At most one primary action by default.
- Use `onClick` on `Stack`, `Row`, or `Column` when the whole visual zone is tappable.
- Use `Button` when the control should be semantically a button with direct label text.
- EventHandler entries require `call`; `args`, `as`, and `condition` are optional.
- Built-in extension functions include `setDataModel`, `setAttributes`, `navigate`, `scrollTo`, `break`, and `sendToAssistant`. App-specific functions are allowed only as host-provided functions.

## Media Rules

- Use local resources or user-provided URLs when available.
- Do not fabricate `https://example.com` or placeholder image URLs.
- If no real media exists, create visual richness with `linearGradient`, translucent blocks, text glyphs, `Progress`, and `Divider`.

## Output Quality Checklist

- [ ] One JSON object per line.
- [ ] Same `surfaceId` everywhere.
- [ ] Extended catalog used.
- [ ] `root` exists and all child references resolve.
- [ ] `Text.content`, `Image.src`, `Button.label` used correctly.
- [ ] Root fits either `160 x 160vp` or `160 x 320vp`.
- [ ] All visible binding paths have data.
- [ ] Text is compact and likely to fit the selected card size.
- [ ] Key information has an explicit full-display width plan and does not rely on ellipsis/clip.
- [ ] Action has a real event/function handler.
- [ ] No placeholder remote media URLs.
- [ ] The structure was constructed from rules, not a copied template.
