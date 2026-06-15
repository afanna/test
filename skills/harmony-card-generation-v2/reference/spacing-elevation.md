# Spacing And Elevation

GenUI extended styles use numbers as vp by default; strings may use `vp`, `fp`, `%`, and `px` where documented.

## Spacing Scale

Use a consistent small-card scale:

| Token | Value | Use |
| --- | --- | --- |
| `sp-2xs` | `2` | tiny internal text/glyph adjustment |
| `sp-xs` | `4` | icon-to-text gap |
| `sp-sm` | `6` or `8` | tight group spacing |
| `sp-md` | `10` or `12` | normal row/section internal spacing |
| `sp-lg` | `14` or `16` | root padding or major group spacing |
| `sp-xl` | `20` or `24` | only for larger desktop-card shells |

Rules:

- Section spacing must be larger than spacing inside a section.
- In a 160vp card, root padding usually stays around `10` to `16`.
- Do not invent many arbitrary spacings in one card.
- `itemMargin` is the preferred Row/Column child spacing.

## Radius System

| Context | Radius |
| --- | --- |
| Root card shell | `20` to `24` |
| Internal translucent block | `14` to `18` |
| Circle/avatar/metric dial | half of width/height |
| Small icon block | `5` to `8` |
| Pill/action bar | height / 2 |

Rules:

- Outer radius >= inner radius.
- Clip root and image containers when radius is used.
- Button/pill radius should be the most rounded form.

## Shadow

GenUI extended styles use `shadow` objects:

```json
"shadow":{"radius":18,"color":"#22000000","offsetX":0,"offsetY":5,"fill":false,"type":"color","style":"outer"}
```

Guidance:

- Root shell may use one soft shadow.
- A primary circular/action element may use one additional shadow.
- Avoid shadows on every internal block.
- Dark cards can use colored glow shadows with alpha; light cards should use low-alpha black.

## Color Alpha

Use alpha hex values for translucency:

- `#22FFFFFF` for subtle white overlay.
- `#66FFFFFF` for visible border/highlight.
- `#22000000` for subtle dark shadow.

GenUI docs allow `#RRGGBB` and `#AARRGGBB`; alpha-prefixed 8-digit hex is useful for translucent overlays.
