# Card Design

## Scope

This document covers compact HarmonyOS GenUI desktop-card mode only. It does not cover full pages.

## Card Boundary

- A desktop card is a glanceable summary container, not a mini page.
- Existing local card templates use a compact root around `height: 160` when explicit.
- Default root is one visual shell: `Column` or `Stack` with `styles.width: "100%"`, rounded corners, clipping, background/gradient/image, and optional shadow.
- The HarmonyOS extended catalog does not require a `Card` component for a desktop card shell; use styled `Column`/`Stack` as shown in the bundled GenUI templates.

## Content Budget

Default budget:

- One primary conclusion or visual focal point.
- One critical supporting context group.
- One primary action or status action.
- Usually 2 to 3 main sections; 4 only when each is very small.

Avoid by default:

- Long lists.
- Long tables.
- Long timelines.
- Multi-paragraph explanation.
- Multiple large parallel sections.
- Full article/detail-page structure.

## Information Summary Card Rules

When the one-sentence request is an entity/concept/place/event summary:

- Use `title -> 2-3 attributes -> one short summary -> optional action`.
- Body text must remain <= 2 short lines.
- Do not use dynamic `List` templates by default.
- Do not use a full-width 16:9 hero image; this is a page pattern.
- If more detail is needed, explicitly suggest a page, not a large card.

## Card Escalation Rule

Treat these as exceeding card scope:

- More than 3 main sections are required after compression.
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
- Temperatures and units, e.g. `31°`.
- Battery/progress values, e.g. `47%`.
- Status words and short CJK phrases, e.g. `高温预警`, `专注模式`.
- Event countdown digits and units.

Rules:

- Do not place protected content in a narrow fixed-width column unless the width clearly fits.
- If horizontal space is tight, compress secondary descriptions first.
- Use `layoutWeight` for flexible text columns and fixed sizes only for icons/circles/visual meters.
- Use `maxLines: 1`, `textOverflow: "ellipsis"`, and `minFontSize` for high-risk text.
- Do not let short phrases wrap character-by-character or leave units/punctuation alone.

## Horizontal Layout Policy

- Use `Row` only when there is a real left-right relationship: icon + label, metric + context, image + overlay, action + status.
- Keep direct Row children <= 3 by default.
- Assign roles before sizing:
  - protected: metric, CTA, icon, status, percentage, time
  - compressible: description, subtitle, location, secondary label
- If a row has many small facts, split into two rows or use a `Column`.
- If there are 2+ tags and one CTA, put tags and CTA in separate rows inside a `Column`.

## Visual Shell Guidance

- One card shell only. Avoid nested full visual shells.
- Internal grouping should use translucent blocks, borders, `Divider`, or spacing, not multiple competing mini-cards.
- Outer radius should be >= inner radius.
- Clip rounded root containers when images/gradients may overflow.
- Shadow belongs mostly to the root or one focused floating action, not every small block.

## Missing Data Behavior

When generating from sparse user input:

- Infer neutral but relevant display values only when needed for a self-contained demo.
- Keep data grouped semantically: `weather`, `meeting`, `action`, `asset`, `progress`.
- Do not leave sample values from templates.
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

At most one strong expressive device should dominate a compact card.
