# Template Catalog

Pick one closest template before generating DSL. Read the selected `.dsl.jsonl` file and adapt its structure; do not copy business facts.

## Templates

| Template | Use When | Shape |
| --- | --- | --- |
| [`top-left-weather-schedule.dsl.jsonl`](templates/top-left-weather-schedule.dsl.jsonl) | One primary metric plus a nearby schedule/context and one action. Good default for "weather + meeting", "today status", "next thing". | `Column`: hero row, translucent context card, action pill. |
| [`parents-care-weather.dsl.jsonl`](templates/parents-care-weather.dsl.jsonl) | Care or alert cards with weather, risk state, and contact action. | `Column`: top weather row, bottom care card + circular action. |
| [`great-second-meeting.dsl.jsonl`](templates/great-second-meeting.dsl.jsonl) | Next meeting, class, appointment, focus mode, room/location. | `Column`: top label, event block, location row, action bar. |
| [`great-first-sleep.dsl.jsonl`](templates/great-first-sleep.dsl.jsonl) | Sleep, health, progress-to-goal, habit reminder. | `Stack`: glow layer, ring `Progress`, duration block, reminder action. |
| [`great-fourth-marathon.dsl.jsonl`](templates/great-fourth-marathon.dsl.jsonl) | Countdown to event, race, exam, trip, launch, training/action plan. | `Stack`: glow layer, large countdown digits, bottom plan card. |
| [`free-clip-2-widget.dsl.jsonl`](templates/free-clip-2-widget.dsl.jsonl) | Device/product state with a real local image resource and small stats. | `Stack`: full image background, content overlay, stat blocks. |

## Selection Rules

- If the request mentions time/date/location/meeting, prefer `great-second-meeting`.
- If it mentions weather and another context, prefer `top-left-weather-schedule`; use `parents-care-weather` when care/contact is central.
- If it mentions progress, goal, completion, sleep, health, hydration, or habit, prefer `great-first-sleep`.
- If it mentions days left, exam, marathon, delivery, launch, anniversary, or trip countdown, prefer `great-fourth-marathon`.
- If it mentions earbuds, phone, car, appliance, battery, mode, device state, or product image, prefer `free-clip-2-widget`.
- If no template is exact, use `top-left-weather-schedule` as the generic status/action card.

## Template Adaptation Rules

- Keep the chosen template's overall rhythm, not its business data.
- Rename IDs semantically, but keep them stable and unique.
- Keep root compact. Existing templates use `height: 160` where explicit.
- Replace sample host functions (`handlePrimaryAction`, `enterFocusMode`, etc.) with function names that match the user's scenario.
- Replace all sample data values with values inferred from the user request or neutral demo values that are clearly part of the generated data model.
- If a template uses a local image resource, only keep an image if the user provided a real resource path or the output can reference a known local asset.
