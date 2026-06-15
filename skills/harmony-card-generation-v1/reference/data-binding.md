# Data Binding And Expressions

## DataModel

Each Surface has a JSON DataModel updated by `updateDataModel`:

```json
{"version":"v0.9","updateDataModel":{"surfaceId":"card","path":"/","value":{"meeting":{"time":"14:00"}}}}
```

Components read from it with JSON Pointer paths:

```json
{"id":"time","component":"Text","content":{"path":"/meeting/time"}}
```

## Absolute Paths

Outside template components, use absolute JSON Pointer paths:

- `/meeting/title`
- `/weather/temperatureLabel`
- `/action/targetId`

Do not use dot paths such as `/meeting.title`.

## Template Paths

When a container uses:

```json
{"children":{"componentId":"itemTemplate","path":"/items"}}
```

the template component and its descendants may bind to the current item with relative paths:

```json
{"id":"itemName","component":"Text","content":{"path":"name"}}
```

Nested templates use relative paths such as `"items"` for the current `$item`.

## Expressions

Expressions are available only in the extended catalog and only in scalar values inside `updateComponents`:

```json
{"content":"{{ '总共有' + size($__dataModel.items) }}"}
```

Use:

- Single-quoted strings inside expressions.
- `$__dataModel.xxx` for DataModel variables.
- `$__widthBreakpoint` for responsive layout.
- `$__colorMode` for light/dark mode.
- `$item` and `$index` inside templates.

Avoid expressions in one-sentence card generation unless they clearly reduce data duplication. Prefer display strings in `updateDataModel`.

## Forbidden Expression Positions

Do not use expressions in:

- `id`
- `component`
- `{"path": "..."}`
- event `call`
- object keys
- whole object values such as `"styles": "{{ ... }}"`

## Binding Checklist

- Every visible text/image/progress binding points to data.
- Every host action argument path points to data.
- Every template source path points to an array.
- Relative paths appear only inside template component subtrees.
