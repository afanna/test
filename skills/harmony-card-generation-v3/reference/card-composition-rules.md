# Generalized Card Construction Rules

This document replaces template-based generation. It defines reusable construction rules for `2x2` and `2x4` HarmonyOS GenUI desktop cards.

## Construction Mindset

Build from the user's meaning, not from an example artifact.

1. Extract semantic roles.
2. Choose `2x2` or `2x4`.
3. Allocate a size budget.
4. Compose zones with a simple grammar.
5. Bind data semantically.
6. Validate, then review visual quality.

## Semantic Roles

Every generated card should assign the user's content into these roles before writing DSL:

| Role | Meaning | Typical Components |
| --- | --- | --- |
| `identity` | What this card is about: title, device name, person, place, event | `Text`, small `Row` |
| `primaryAnswer` | The most important glanceable result | large `Text`, `Progress`, image focal point |
| `metric` | Number, time, temperature, battery, price, duration | protected `Text`, `Progress` |
| `context` | Secondary explanation or nearby event/detail | compact `Column`, `Row`, `Divider` |
| `status` | Good/warning/error/mode label | small `Text` with background, glyph, or accent |
| `media` | Real local/URL asset supplied by user | `Image` inside `Stack` |
| `action` | One next operation | tappable `Stack`/`Row`/`Column` or `Button` |

Rules:

- `primaryAnswer` must be visually dominant.
- `context` must be shorter than `primaryAnswer`.
- `action` supports the card; it must not become the main visual unless the user asks for an action-only card.
- If `media` is absent or unreliable, use gradient, translucent block, glyph text, `Divider`, or `Progress`.

## Size Decision Rules

Use `2x2` when:

- The card has one primary answer and at most one context group.
- The user asks for a compact widget or a single status/reminder.
- A `160 x 160vp` layout can fit without scroll.

Use `2x4` when:

- The card needs 2 to 3 compact supporting facts.
- The scenario naturally has a left-right relationship: media plus state, primary metric plus details, schedule plus action, care status plus contact.
- Protected key text needs more horizontal space than `2x2` can safely provide.
- The primary visual needs breathing room and the action/context still matters within a `160vp` height.

Escalate instead of using `2x4` when:

- More than 4 major zones are required.
- The content requires paragraphs, tables, forms, or a long dynamic list.
- The user really wants a detail page.

## `2x2` Rules: `160 x 160vp`

### Hard Budget

- Root target: `width: 160`, `height: 160`.
- Root padding: `10` to `12`.
- Usable inner area: about `136 x 136vp`.
- Main zones: <= 3.
- Direct `Row` children: <= 3.
- No scrolling.
- No dynamic list pattern by default.

### Zone Budget

Choose one of these allocation rhythms:

| Rhythm | Use When | Budget |
| --- | --- | --- |
| `header-primary-action` | reminder, event, CTA card | header `18-24`, primary `58-72`, action `30-36` |
| `primary-context-action` | status/metric with detail | primary `58-76`, context `34-44`, action `28-34` |
| `visual-primary-context` | progress/device/health glance | visual `56-76`, primary/context share remaining height |
| `single-focal` | one strong result, optional tiny meta | focal `88-110`, meta/action `22-34` |

The budgets are guidance, not exact templates. Use them to keep text from colliding inside `160vp`.

### Composition Grammar

Use one root shell:

```text
RootShell(Column|Stack)
  -> Identity? 
  -> PrimaryAnchor
  -> ContextStrip? 
  -> ActionPill?
```

Allowed variations:

- `Stack` root when using image background, glow, or progress overlay.
- `Column` root when the card is mostly text/metric/action.
- `Row` inside a zone only when it expresses a real relationship: icon + label, metric + status, progress + value.

### Text Budget

- Title/identity: 1 line.
- Primary value: 1 line; use `minFontSize` if it may vary.
- Context: 1 line, or 2 very short lines if no action exists.
- CTA: 1 line; content-driven width or full-width pill.
- Avoid any paragraph-like body text.

### Visual Rules

- One visual anchor only: large metric, progress ring, image subject, icon/glyph, or status badge.
- At most 1 major translucent block.
- Use image only if it is real and useful. Otherwise use non-media visual techniques.
- Keep contrast strong; text over image needs overlay or safe placement.

## `2x4` Rules: `320 x 160vp`

### Hard Budget

- Root target: `width: 320`, `height: 160`.
- Root padding: `10` to `12`.
- Usable inner area: about `296 x 136vp`.
- Main zones: <= 4.
- Direct `Row` children: <= 3.
- No scrolling by default. If static content cannot fit, converge the content.

### Zone Budget

Choose one horizontal rhythm:

| Rhythm | Use When | Budget |
| --- | --- | --- |
| `focal-detail-action` | general rich compact card | focal pane `108-132w`, detail pane `120-150w`, action/status `40-56w` or bottom strip |
| `media-state-action` | product/device/place with real image | media pane `112-140w`, state/details `120-150w`, action `40-56w` |
| `metric-context-action` | weather, progress, health, finance | metric pane `96-124w`, context pane `132-164w`, action/status `44-60w` |
| `sequence-detail-action` | schedule/plan/care card | sequence pane `132-164w`, detail pane `92-124w`, action/status `44-60w` |

The 2x4 card may feel like two side-by-side 2x2 regions, but it must remain one card shell with one hierarchy.

### Composition Grammar

```text
RootShell(Row|Stack)
  -> FocalPane
  -> DetailPane
  -> ActionOrStatus?
```

Allowed variations:

- Use a `Column` inside each pane for vertical rhythm.
- Use `Stack` root when a real image/background or glow layer spans the card.
- Put `ActionOrStatus` as a right rail, bottom strip, or last detail row only when protected text remains readable.
- Use a static detail cluster of 2 to 3 rows; avoid dynamic lists unless the user explicitly needs variable repeated data.

### Text Budget

- Focal pane: 1 primary value/title line plus 1 optional caption.
- Detail pane: 2 to 3 compact rows, each row 1 line.
- Advisory/body text: <= 2 short lines total.
- CTA/status: 1 line, protected; avoid a narrow fixed CTA unless the full label is known to fit.

### Visual Rules

- One dominant visual anchor and at most one secondary visual device.
- At most 2 major translucent blocks.
- A progress ring, media subject, or large number may own the left pane.
- The right pane should carry details and action, not another competing hero.

## Scenario-To-Structure Mapping

These are rules, not templates. Select the structure by semantic role, then create fresh IDs, data keys, colors, and spacing for the scenario.

| Scenario | Preferred Size | Structure Logic |
| --- | --- | --- |
| Weather + next thing | `2x2` | primary weather metric + next event context + action/status |
| Meeting/reminder | `2x2` | identity label + protected time/title + location/action |
| Countdown | `2x2` for one event, `2x4` for event + mini plan | large countdown + unit + supporting plan/action |
| Health/progress | `2x2` for one metric, `2x4` for metric + trends | progress visual + duration/value + reminder/advice |
| Family care alert | `2x4` if advice/contact/details matter | status/weather + risk detail + contact action |
| Device/product state | `2x2` for simple battery/mode, `2x4` for media + states | real asset or glyph + battery/mode rows + action |
| Information summary | `2x2` for tiny summary, `2x4` for attributes + short context | title + attributes + <=2-line summary + action |

## Width And Wrapping Rules

The width budget is strict: `2x2` is `160vp` wide and horizontal `2x4` is `320vp` wide. Both are only `160vp` tall.

- Protected values get explicit width only when the value length is known and the full string fits.
- Text columns should use `layoutWeight: 1` when next to fixed icons or meters.
- If a row contains a metric and a sentence, the sentence is compressible.
- Use `maxLines: 1` and `minFontSize` for constrained key text. Use `textOverflow: "ellipsis"` only for optional secondary text.
- Do not split short CJK labels, units, times, prices, temperatures, or CTA labels character by character.

## Key-Info Full-Display Rules

Key information must be visible in full unless the user explicitly accepts truncation.

Treat these as key information by default:

- Date, weekday, time, countdown, duration, temperature, price, rating, battery, percentage, and primary metric values.
- CTA labels, status badges, alert labels, short CJK phrases, and primary event/item titles.
- Any field the user explicitly asks the card to display.

Rules:

- Do not put `textOverflow: "ellipsis"` on key Text components.
- Do not switch from ellipsis to `clip` as a fix for key text; clipping still hides information.
- If key text cannot fit horizontally, rebalance the layout before writing JSON:
  1. Reduce decorative padding and `itemMargin`.
  2. Reduce fixed columns and divider thickness/width.
  3. Lower font size while preserving hierarchy.
  4. Move compressible secondary text to another line or remove it from demo data.
  5. Split the row into a `Column`, choose horizontal `2x4`, or escalate if the request cannot fit.

## Row Width Budget

Before generating any crowded Row, write the arithmetic in the layout rationale:

```text
available = parentWidth - horizontalPadding - totalItemMargins - fixedIconOrDividerWidths - fixedTextWidths
```

Then check that each protected string fits its assigned width. For a `2x2` card, assume the parent content width is usually `136vp` after root padding. Inside a nested translucent block, padding and row gaps can easily leave less than `120vp`; keep dividers and gaps small when multiple protected strings share the row.

For compact reminder/event rows that must show time + title + meta in a `2x2` card:

- Keep event-block horizontal padding around `4-6vp`.
- Keep Row `itemMargin` around `3-4vp`.
- Use thin dividers (`strokeWidth: 1`) or omit them if they cause crowding.
- Keep `HH:MM` time around `18fp` with `48-50vp` width, not a large `22fp`/`56vp` block, when title and meta must also show.
- Keep short CJK titles around `12fp` and meta around `9fp` when they share the same compact block.

For horizontal `2x4`, assume the parent content width is usually about `296vp` after root padding. Prefer a main `Row` with 2 or 3 panes, and budget each pane explicitly. Do not spend the extra width on oversized decorative gaps; use it to keep protected values complete.

## Interaction Rules By Size

`2x2`:

- Usually one primary tappable zone or one full-width action pill.
- Avoid more than one CTA.

`2x4`:

- One primary action plus optional passive status is acceptable.
- If there are multiple actions, they must be visually subordinate, explicitly requested, and fit the horizontal right rail or bottom strip without clipping.

## DataModel Shape

Group data by meaning, not by layout:

```json
{
  "primary": {"label": "Status", "valueLabel": "31 deg"},
  "context": {"title": "Next meeting", "meta": "09:30 A14"},
  "action": {"label": "Open", "targetId": "demo-001"}
}
```

Rules:

- Do not name data keys after visual zones only, such as `topText1`.
- Precompute display strings when formatting or localization matters.
- Bind action IDs from DataModel instead of hard-coding business IDs in event handlers.

## Pre-Generation Self-Check

Before writing JSON:

- [ ] Did I choose `2x2` or `2x4` explicitly?
- [ ] Did I identify the semantic roles?
- [ ] Does the structure fit the size budget without scroll?
- [ ] Is there only one dominant focal point?
- [ ] Are protected values safe from narrow wrapping?
- [ ] Am I constructing from rules rather than adapting a template?
