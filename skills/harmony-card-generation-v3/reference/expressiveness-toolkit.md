# Expressiveness Toolkit

Use these techniques to create visual richness while staying inside HarmonyOS GenUI extended Catalog.

## 1. Linear Gradient Shells

Use `styles.linearGradient` for root backgrounds and glow layers.

```json
"linearGradient":{"direction":"RightBottom","colors":[["#25272E",0],["#3037B8",0.72],["#5D49E8",1]]}
```

Rules:

- Choose colors for the scene, not from any example artifact.
- Keep one coherent hue system with one accent family.
- Use dark gradients for night/sleep/focus/device mood; use warmer/light gradients for weather/lifestyle.

## 2. Translucent Blocks

Use `backgroundColor` with alpha hex and `borderColor` to group secondary context.

```json
"styles":{"backgroundColor":"#24FFFFFF","borderWidth":1,"borderColor":"#3DFFFFFF","borderRadius":15}
```

Rules:

- Max 1 major translucent block in a `2x2` card.
- Max 2 major translucent blocks in a `2x4` card.
- Blocks should support hierarchy, not become competing cards.

## 3. Text Glyph Icons

Use `Text` as compact glyph/icon carriers when no icon asset is required.

```json
{"id":"weatherIcon","component":"Text","content":{"path":"/weather/icon"},"styles":{"fontSize":38,"maxLines":1,"textAlign":"center"}}
```

Use glyph icons for simple symbolic markers. Add `accessibility.label` when the glyph carries meaning.

## 4. Progress As Visual Anchor

Use `Progress` for sleep, habit, battery, completion, training, and goal cards.

```json
{"id":"goalProgress","component":"Progress","value":{"path":"/goal/value"},"total":{"path":"/goal/total"},"styles":{"type":"ring","color":"#A77DFF","width":72,"height":72}}
```

The progress component should be one of the main focal elements, not a tiny afterthought.

## 5. Accent Divider

Use `Divider` as a lightweight structure element.

```json
{"id":"accentLine","component":"Divider","styles":{"vertical":true,"strokeWidth":3,"color":"#73FFFFFF","height":28}}
```

This is useful for context cards, separating metadata from title, or adding rhythm without extra containers.

## 6. Image Background

For product/device cards with a real asset:

```json
{"id":"root","component":"Stack","children":["productImage","contentLayer"],"styles":{"width":160,"height":160,"clip":true}}
{"id":"productImage","component":"Image","src":{"path":"/asset/productImage"},"styles":{"width":"100%","height":"100%","objectFit":"cover"}}
```

Rules:

- Only use if the asset is real.
- Protect text contrast with overlay blocks or placement.
- Do not cover important product details with text.

## Anti-Patterns

- Gradient + glow + image + many blocks all in one `2x2` card.
- Pure decoration that does not clarify the scenario.
- Multiple unrelated accent hues.
- Replacing a meaningful `Progress` or image with plain text when visual data exists.
