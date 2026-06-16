# Component Catalog For Desktop Cards

This is a concise subset of the local GenUI extended component references. Use it for card generation; load the full local docs only when a component is not covered here.

## Required Catalog

Use:

```json
"catalogId": "ohos.a2ui.extended.catalog"
```

Do not mix Basic Catalog property names into this surface.

## High-Frequency Components

### Column

Vertical container.

```json
{"id":"col","component":"Column","children":["a","b"],"itemMargin":8,"justifyContent":"spaceBetween","alignItems":"start"}
```

- `children`: string array or `{ "componentId": "...", "path": "/items" }`
- `itemMargin`: number, vp
- `justifyContent`: `start|center|end|spaceAround|spaceBetween|spaceEvenly`
- `alignItems`: `start|center|end`

### Row

Horizontal container.

```json
{"id":"row","component":"Row","children":["a","b"],"itemMargin":8,"justifyContent":"spaceBetween","alignItems":"center"}
```

- `children`: string array or repeated-item binding object
- `itemMargin`: number, vp
- `justifyContent`: `start|center|end|spaceAround|spaceBetween|spaceEvenly`
- `alignItems`: `top|center|bottom`
- `wrap`: `noWrap|wrap`

### Stack

Layered container. Use for glows, image background, overlaid content, progress rings.

```json
{"id":"stack","component":"Stack","children":["bg","content"],"alignContent":"center"}
```

- `children`: string array
- `alignContent`: `topStart|top|topEnd|start|center|end|bottomStart|bottom|bottomEnd`

### Text

Text display. Required field is `content`.

```json
{"id":"title","component":"Text","content":{"path":"/title"},"styles":{"fontSize":16,"fontWeight":700,"fontColor":"#FFFFFFFF","maxLines":1,"textOverflow":"none"}}
```

Common styles:

- `fontSize`: number, fp
- `fontWeight`: number `100..900` for `Text`
- `fontColor`: `#RRGGBB` or `#AARRGGBB`
- `maxLines`: number
- `minFontSize`, `maxFontSize`: number
- `textOverflow`: `none|clip|ellipsis|marquee`
- `textAlign`: `start|center|end|justify`
- `wordBreak`: `normal|breakAll|breakWord|hyphenation`

### Image

Image display. Required field is `src`.

```json
{"id":"img","component":"Image","src":{"path":"/asset/image"},"styles":{"width":"100%","height":"100%","objectFit":"cover"}}
```

Common styles:

- `objectFit`: `fill|contain|cover|auto|none|scaleDown|topStart|top|topEnd|start|center|end|bottomStart|bottom|bottomEnd|matrix`
- `aspectRatio`: number

### Divider

Line separator. Extended properties live in `styles`.

```json
{"id":"line","component":"Divider","styles":{"vertical":true,"strokeWidth":3,"color":"#73FFFFFF","height":28}}
```

Styles:

- `strokeWidth`: number or unit string
- `vertical`: boolean
- `color`: color string

### Progress

Progress bar/ring.

```json
{"id":"progress","component":"Progress","value":{"path":"/progress/value"},"total":{"path":"/progress/total"},"styles":{"type":"ring","color":"#A77DFF","width":72,"height":72}}
```

- `value`: number or binding
- `total`: number or binding
- `styles.type`: `linear|ring|eclipse|scaleRing|capsule`
- `styles.color`: color string

### Button

Semantic button. Use `label`, not child text.

```json
{"id":"btn","component":"Button","label":"打开","action":{"event":{"name":"openDetail"}}}
```

- `label`: string or binding
- `enabled`: boolean or binding
- `action`: `{ "event": { "name": "...", "context": {...} } }` or `{ "functionCall": { "call": "...", "args": {...} } }`
- `styles.fontWeight`: number or `normal|regular|medium|bold|bolder`
- If `action` and `onClick` are both present, `action` has priority.

### If

Conditional virtual node.

```json
{"id":"adaptive","component":"If","condition":"{{ $__widthBreakpoint == 'sm' }}","childrenIf":["narrow"],"childrenElse":["wide"]}
```

- `condition`: full `{{ ... }}` expression
- `childrenIf` / `childrenElse`: string arrays
- Do not set styles or accessibility on `If`.

### List And Grid

Use sparingly in desktop cards. Prefer static compact rows unless the user's request truly needs repeated items.

List:

```json
{"id":"list","component":"List","children":{"componentId":"itemTpl","path":"/items"},"space":6,"listDirection":"vertical","scrollBar":"off"}
```

Grid:

```json
{"id":"grid","component":"Grid","children":["a","b"],"columnsTemplate":"1fr 1fr","columnsGap":8,"rowsGap":8}
```

## Common Styles

All extended components except virtual `If` support common `styles`:

- `width`, `height`
- `constraintSize`
- `margin`, `padding`
- `borderRadius`
- `borderWidth`, `borderColor`
- `backgroundColor`
- `backgroundImage`, `backgroundImageSizeWithStyle`
- `linearGradient`
- `layoutWeight`, `flexShrink`
- `shadow`
- `visibility`
- `clip` boolean

Value notes:

- Numbers default to vp for dimensions.
- Strings may use `vp`, `fp`, `%`, and sometimes `px` where documented.
- Colors use `#RRGGBB` or `#AARRGGBB`. `#RRGGBB` alpha is treated as opaque by GenUI.
- `linearGradient.colors` can use `["#RRGGBB", stop]` pairs.

## Supported Component Names

The extended catalog contains:

`Text`, `Image`, `Divider`, `Progress`, `Button`, `TextInput`, `Select`, `Toggle`, `Radio`, `Checkbox`, `CheckboxGroup`, `Row`, `Column`, `List`, `Stack`, `Grid`, `Tabs`, `TabContent`, `Navigation`/`NavContainer`, `Web`, `If`.

For desktop cards, default to the high-frequency subset above.
