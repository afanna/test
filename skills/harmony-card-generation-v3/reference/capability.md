# Capability Scope

## Supported Card Tasks

Use this skill for compact HarmonyOS GenUI desktop cards generated from one sentence, especially:

- Weather + schedule glance: current condition, next meeting, quick action.
- Family care/weather alert: temperature, risk label, call or care action.
- Meeting/schedule reminder: next event, time range, room/location, focus action.
- Sleep/health progress: status, ring progress, duration, reminder action.
- Countdown/training plan: event countdown, today plan, open-plan action.
- Device/product state: product image/resource, battery, mode, playback, connection state.
- Generic status card: one primary metric, one supporting context, one action.
- Compact information summary: one entity/concept/place/event summarized as a card, not as an article.

The default output is a single desktop-card surface using `ohos.a2ui.extended.catalog`.

## Supported Sizes

### `2x2` / `160 x 160vp`

Use for glanceable cards that answer one immediate question:

- What is the status?
- What is next?
- What should I do now?
- How far along is this?

### `2x4` / `320 x 160vp`

Use for compact horizontal cards that need more breadth but still remain a card:

- A two-pane schedule or reminder.
- A care/advisory card with status plus contact action.
- A product/device card with media plus state.
- A progress card with primary visual plus 2 to 3 supporting details.

## Unsupported Or Risky Requests

Explain the limitation and offer a smaller supported card alternative when the user asks for:

- Full pages, multi-screen flows, heavy dashboards, or article/detail pages.
- Complex forms requiring many inputs, validation, or large dynamic lists.
- Components outside the GenUI standard or HarmonyOS extended catalogs.
- Layouts requiring unsupported absolute positioning or CSS-like properties.
- Real-time data fetching, device APIs, or host functions not supplied by the app.
- Remote images or media that the user has not provided and that cannot be represented by local resources.
- Content that cannot be compressed into `2x2` or `2x4` without losing the user's core requirement.

## Default Assumptions

- Card size: choose `2x2` unless the request clearly needs `2x4`.
- Width budget: `160vp` for `2x2`, `320vp` for horizontal `2x4`.
- Height budget: `160vp` for both `2x2` and `2x4`.
- Protocol: JSONL with `createSurface`, `updateComponents`, `updateDataModel`.
- Catalog: `ohos.a2ui.extended.catalog`.
- Content density: `2x2` has 2 to 3 main zones; `2x4` has 3 to 4 main zones.
- Interaction: at most one primary action unless the user explicitly needs more.

## Alternative Strategy

If a request is too broad, generate a focused card that answers the first glanceable need:

- Travel plan card -> next trip countdown + weather + open itinerary.
- Finance dashboard card -> today's spend/budget status + risk label + view detail action.
- Project management card -> next milestone + progress + open task action.
- Article summary card -> title + 2 attributes + one-line summary + open detail action.
