# Card Design

## Scope

This document covers compact HarmonyOS GenUI desktop-card mode only. It does not cover full pages.

## Card Boundary

- A desktop card is a glanceable summary container, not a mini page.
- Supported physical targets are `2x2` (`160 x 160vp`) and `2x4` (`160 x 320vp`).
- Default root is one visual shell: `Column` or `Stack` with rounded corners, clipping, background/gradient/image, and optional shadow.
- The HarmonyOS extended catalog does not require a `Card` component for the desktop card shell; use a styled `Column` or `Stack` unless a real `Card` component is specifically useful.
- Generation is rule-driven. Do not choose a historical DSL template as the starting structure.

## Content Budget

`2x2` default budget:

- One primary conclusion or visual focal point.
- One critical supporting context group.
- One primary action or status action.
- Usually 2 to 3 main zones.

`2x4` default budget:

- One primary conclusion or visual focal point.
- Two to three supporting facts or a compact detail cluster.
- One primary action or passive status.
- Usually 3 to 4 main zones.

Avoid by default:

- Long lists.
- Long tables.
- Long timelines.
- Multi-paragraph explanation.
- Multiple large parallel sections.
- Full article/detail-page structure.

## Information Summary Card Rules

When the one-sentence request is an entity/concept/place/event summary:

- Use `title -> 1 to 3 attributes -> one short summary -> optional action`.
- Body text must remain <= 2 short lines.
- Do not use a dynamic list pattern by default.
- Do not use a full-width 16:9 hero image; this is a page pattern.
- If more detail is needed, explicitly suggest a page, not a large card.

## Card Escalation Rule

Treat these as exceeding card scope:

- More than 3 main zones are required in `2x2`.
- More than 4 main zones are required in `2x4`.
- Primary information requires scrolling.
- The card becomes close to a full-screen panel.
- The user needs complex form/table/page navigation.

Correct response:

1. Converge to a summary card.
2. If convergence fails, use Mode 3 and suggest page scope.
3. Do not silently deliver a page-sized card.

## Protected Content Readability

Protected content includes:

- CTA labels.
- Times and dates, e.g. `14:00-15:30`.
- Weekday labels and user-requested date parts.
- Temperatures and units, e.g. `31 deg`.
- Battery/progress values, e.g. `47%`.
- Status words and short CJK phrases.
- Primary event/item titles when the user asks to display them.
- Event countdown digits and units.
- Prices, ratings, and compact quantities.

Rules:

- Do not place protected content in a narrow fixed-width column unless the width clearly fits.
- If horizontal space is tight, compress secondary descriptions first.
- Use `layoutWeight` for flexible text columns and fixed sizes only for icons, circles, images, and visual meters.
- Use `maxLines: 1` and `minFontSize` for high-risk protected text.
- Do not use `textOverflow: "ellipsis"` or `clip` to hide protected content. Rebalance spacing, font sizes, row structure, or card size instead.
- Use ellipsis only for nonessential secondary text after the protected content has enough width.
- Do not let short phrases wrap character-by-character or leave units/punctuation alone.

## Horizontal Layout Policy

- Use `Row` only when there is a real left-right relationship: icon + label, metric + context, image + overlay, action + status.
- Keep direct `Row` children <= 3 by default.
- Assign roles before sizing:
  - protected: metric, CTA, icon, status, percentage, time
  - compressible: description, subtitle, location, secondary label
- If a row has many small facts, split into two rows or use a `Column`.
- If there are 2+ tags and one CTA, put tags and CTA in separate rows inside a `Column`.
- Before writing a crowded Row, budget its inner width: parent width minus horizontal padding, item margins, dividers/icons, and fixed columns. If the remaining width cannot fully show protected text, simplify the row before generating DSL.

## Visual Shell Guidance

- One card shell only. Avoid nested full visual shells.
- Internal grouping should use translucent blocks, borders, `Divider`, or spacing, not multiple competing mini-cards.
- Outer radius should be >= inner radius.
- Clip rounded root containers when images/gradients may overflow.
- Shadow belongs mostly to the root or one focused floating action, not every small block.

## Missing Data Behavior

When generating from sparse user input:

- Infer neutral but relevant display values only when needed for a self-contained demo.
- Keep data grouped semantically: `weather`, `meeting`, `action`, `asset`, `progress`, etc.
- Do not leave sample values from examples or previous outputs.
- If real image/resource data is absent, omit `Image` and use non-media visual techniques.

## Image Strategy

- Use `Image.src` only with provided real URLs or local resource paths.
- For image-background cards, use `Stack` root, `Image` as first child, content overlay as second child.
- Use `styles.objectFit: "cover"` for background/hero fills.
- Avoid images when they do not add scene-specific information.

## Expressiveness Hierarchy

Within HarmonyOS GenUI extended catalog:

- Use `Image` when real visual material exists.
- Use `Progress` for progress/ring/capsule indicators.
- Use `Divider` for lightweight structure.
- Use `Stack` for layered glow/image/progress composition.
- Use `Grid`/`List` sparingly for repeated compact facts.
- Use plain `Text` for labels, values, and glyph-like icons when that is the most stable option.

At most one strong expressive device should dominate a `2x2` card. A `2x4` card may have one dominant device and one secondary device.
