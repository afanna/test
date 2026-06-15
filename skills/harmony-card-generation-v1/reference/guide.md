# DSL And Card Generation Guide

## Required Message Shape

Generate JSONL with exactly one JSON object per line:

```jsonl
{"version":"v0.9","createSurface":{"surfaceId":"sample-card","catalogId":"ohos.a2ui.extended.catalog","theme":{"primaryColor":"#4D5CFF"}}}
{"version":"v0.9","updateComponents":{"surfaceId":"sample-card","components":[{"id":"root","component":"Column","children":["title"],"styles":{"width":"100%","height":160}}]}}
{"version":"v0.9","updateDataModel":{"surfaceId":"sample-card","path":"/","value":{"title":"示例"}}}
```

Rules:

- `version` is always `"v0.9"`.
- Use `createSurface` before components or data.
- Use `catalogId: "ohos.a2ui.extended.catalog"`.
- Keep the same `surfaceId` in all messages.
- Prefer `path: "/"` in `updateDataModel`.

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

- Default root: `width: "100%"`, `height: 160`, `borderRadius` around 20-24, `clip: true`.
- Use 2 to 4 main zones. Examples: top status, hero metric, secondary context, action.
- Limit rows to 2 or 3 direct children unless using a scroll/list pattern.
- Use `Stack` for layered glow/image effects and `Column`/`Row` for information layout.
- Use `itemMargin` for spacing between Row/Column children.
- Keep short protected text readable: time, temperature, count, CTA, status labels, battery percentages.
- Prefer `maxLines: 1`, `textOverflow: "ellipsis"`, and `minFontSize` for constrained headline values.

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
{"content":"{{ '剩余' + $__dataModel.countdown.days + '天' }}"}
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

- Use local resources such as `resources/base/media/free_clip_2_earbuds.png` when available.
- Do not fabricate `https://example.com` or placeholder image URLs.
- If no real media exists, create visual richness with `linearGradient`, translucent blocks, text icons, `Progress`, and `Divider`.

## Output Quality Checklist

- [ ] One JSON object per line.
- [ ] Same `surfaceId` everywhere.
- [ ] Extended catalog used.
- [ ] `root` exists and all child references resolve.
- [ ] `Text.content`, `Image.src`, `Button.label` used correctly.
- [ ] All visible binding paths have data.
- [ ] Text is compact and likely to fit inside 160vp height.
- [ ] Action has a real event/function handler.
- [ ] No placeholder remote media URLs.
