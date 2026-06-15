# Capability Scope

## Supported Card Tasks

Use this skill for compact HarmonyOS GenUI desktop cards generated from one sentence, especially:

- Weather + schedule glance: current condition, next meeting, quick action.
- Family care/weather alert: temperature, risk label, call or care action.
- Meeting/schedule reminder: next event, time range, room/location, focus action.
- Sleep/health progress: status, ring progress, duration, reminder action.
- Countdown/training plan: event countdown, today plan, open-plan action.
- Device/product state: product image/resource, battery, music/noise/device toggles.
- Generic status card: one primary metric, one supporting context, one action.

The default output is a single desktop-card surface using `ohos.a2ui.extended.catalog`.

## Unsupported Or Risky Requests

Explain the limitation and offer a smaller supported card alternative when the user asks for:

- Full pages, multi-screen flows, heavy dashboards, or article/detail pages.
- Complex forms requiring many inputs, validation, or large dynamic lists.
- Components outside the GenUI standard or HarmonyOS extended catalogs.
- Layouts requiring unsupported absolute positioning or CSS-like properties.
- Real-time data fetching, device APIs, or host functions not supplied by the app.
- Remote images or media that the user has not provided and that cannot be represented by local resources.

## Default Assumptions

- Card size: compact desktop card, root width `100%`, visual height around `160`.
- Protocol: JSONL with `createSurface`, `updateComponents`, `updateDataModel`.
- Catalog: `ohos.a2ui.extended.catalog`.
- Content density: 2 to 4 main zones, mostly one-line text, no long paragraphs.
- Interaction: at most one primary action unless the user explicitly needs more.

## Alternative Strategy

If a request is too broad, generate a focused card that answers the first glanceable need:

- "做一个旅行计划桌面卡片" -> next trip countdown + weather + open itinerary.
- "做一个财务看板卡片" -> today's spend/budget status + risk label + view detail action.
- "做一个项目管理卡片" -> next milestone + progress + open task action.
