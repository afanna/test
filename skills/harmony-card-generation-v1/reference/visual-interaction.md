# Visual And Interaction Guidance

## Default Visual Direction

Unless the user requests minimal/plain output, default to:

- polished
- layered
- compact
- scene-specific
- visually expressive within GenUI extended Catalog limits

Do not default to the fewest components. Use the selected template's rhythm and improve the scene's hierarchy.

## Real Interaction

Clickable areas must be real:

- Use `onClick` on `Stack`, `Row`, or `Column` when the whole zone is tappable.
- Use `Button` with `label` and `action` when it is semantically a button.
- Do not draw inactive fake buttons.
- For app-specific actions, use meaningful host function names such as `enterFocusMode`, `openTrainingPlan`, `makePhoneCall`, and bind required IDs from DataModel.

Example:

```json
{"id":"focusAction","component":"Stack","children":["focusLabel"],"onClick":[{"call":"enterFocusMode","args":{"meetingId":{"path":"/meeting/id"}}}]}
```

## Button Safety

- `Button.label` must be visible text.
- If using `Button.action`, do not also rely on `onClick`; `action` has priority.
- If the action is only a host placeholder, say so in the final response.

## Image Sourcing

- Prefer user-provided local resources or URLs.
- Do not fabricate URLs.
- If no reliable image exists, use gradient, `Stack`, translucent blocks, text glyphs, `Divider`, or `Progress`.

## URL Authenticity

Any URL in `updateDataModel` should be real and loadable. Placeholder domains such as `example.com`, `placeholder.com`, and `picsum.photos` are not acceptable for final card output.

## Anti-Patterns

Avoid:

- Standard-catalog property names inside extended cards.
- Styled text pretending to be a button with no event.
- Too many mini-card blocks inside one compact card.
- Pure vertical text stacking with no visual focal point.
- Tag group and CTA button fighting in one row.
- Reusing template colors blindly when the domain mood is different.
- Image backgrounds that hide the core text.
- Host action args hard-coded when they should come from DataModel.
