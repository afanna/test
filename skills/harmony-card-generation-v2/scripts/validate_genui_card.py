#!/usr/bin/env python3
"""
Validate a HarmonyOS GenUI desktop-card DSL artifact.

Accepts JSONL messages or a JSON array of messages. The final deliverable should
still be JSONL: createSurface, updateComponents, updateDataModel.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


EXTENDED_CATALOG = "ohos.a2ui.extended.catalog"

ALLOWED_COMPONENTS = {
    "Text", "Image", "Divider", "Progress",
    "Button", "TextInput", "Select", "Toggle", "Radio", "Checkbox", "CheckboxGroup",
    "Row", "Column", "List", "Stack", "Grid",
    "Tabs", "TabContent", "Navigation", "NavContainer",
    "Web", "If",
}

COMMON_STYLE_KEYS = {
    "width", "height", "constraintSize",
    "margin", "padding",
    "borderRadius", "borderWidth", "borderColor",
    "backgroundColor", "backgroundImage", "backgroundImageSizeWithStyle",
    "linearGradient",
    "layoutWeight", "flexShrink",
    "shadow", "visibility", "clip",
}

TEXT_STYLE_KEYS = {
    "fontColor", "fontSize", "fontWeight", "maxLines",
    "minFontSize", "maxFontSize",
    "fontScaleMode", "minFontScale", "maxFontScale",
    "textOverflow", "textAlign", "wordBreak", "decoration",
}

IMAGE_STYLE_KEYS = {"objectFit", "aspectRatio"}
DIVIDER_STYLE_KEYS = {"strokeWidth", "vertical", "color"}
PROGRESS_STYLE_KEYS = {"color", "type"}
GRID_STYLE_KEYS = {"columnsTemplate", "rowsTemplate", "columnsGap", "rowsGap"}
LIST_STYLE_KEYS = {"listDirection", "scrollBar", "nestedScroll"}
BUTTON_STYLE_KEYS = {
    "fontSize", "fontWeight", "minFontSize", "maxFontSize",
    "fontScaleMode", "minFontScale", "maxFontScale", "fontColor",
}

STYLE_KEYS_BY_COMPONENT = {
    "Text": TEXT_STYLE_KEYS,
    "Image": IMAGE_STYLE_KEYS,
    "Divider": DIVIDER_STYLE_KEYS,
    "Progress": PROGRESS_STYLE_KEYS,
    "Grid": GRID_STYLE_KEYS,
    "List": LIST_STYLE_KEYS,
    "Button": BUTTON_STYLE_KEYS,
}

CSS_STYLE_ALIASES = {
    "font-size", "font-weight", "font-color", "background-color",
    "border-radius", "border-width", "border-color", "max-lines",
    "text-overflow", "text-align", "object-fit",
}

COMPONENT_ENUMS = {
    "Row": {
        "justifyContent": {"start", "center", "end", "spaceAround", "spaceBetween", "spaceEvenly"},
        "alignItems": {"top", "center", "bottom"},
        "wrap": {"noWrap", "wrap"},
    },
    "Column": {
        "justifyContent": {"start", "center", "end", "spaceAround", "spaceBetween", "spaceEvenly"},
        "alignItems": {"start", "center", "end"},
    },
    "Stack": {
        "alignContent": {"topStart", "top", "topEnd", "start", "center", "end", "bottomStart", "bottom", "bottomEnd"},
    },
    "List": {
        "listDirection": {"vertical", "horizontal"},
        "scrollBar": {"off", "auto", "on"},
    },
}

STYLE_ENUMS = {
    "textOverflow": {"none", "clip", "ellipsis", "marquee"},
    "textAlign": {"start", "center", "end", "justify"},
    "wordBreak": {"normal", "breakAll", "breakWord", "hyphenation"},
    "fontScaleMode": {"followSystem", "custom"},
    "objectFit": {
        "fill", "contain", "cover", "auto", "none", "scaleDown",
        "topStart", "top", "topEnd", "start", "center", "end",
        "bottomStart", "bottom", "bottomEnd", "matrix",
    },
    "type": {"linear", "ring", "eclipse", "scaleRing", "capsule"},
    "visibility": {"visible", "hidden", "none"},
}

COLOR_RE = re.compile(r"^#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
DIMENSION_RE = re.compile(r"^\d+(?:\.\d+)?(?:vp|fp|px|%)$")
EXPR_RE = re.compile(r"^\{\{.*\}\}$", re.DOTALL)
PLACEHOLDER_URL_RE = re.compile(
    r"https?://(?:example\.com|placeholder\.com|via\.placeholder\.com|picsum\.photos|dummyimage\.com)",
    re.IGNORECASE,
)
PROTECTED_TEXT_HINT_RE = re.compile(
    r"(time|date|day|weekday|status|badge|cta|action|button|title|name|price|"
    r"percent|percentage|battery|temperature|temp|countdown|count|metric|value)",
    re.IGNORECASE,
)
COMPRESSIBLE_TEXT_HINT_RE = re.compile(
    r"(meta|subtitle|subTitle|description|desc|detail|location|body|summary|"
    r"advisory|note|hint|secondary)",
    re.IGNORECASE,
)


def load_messages(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8-sig").strip()
    if not text:
        raise ValueError("file is empty")

    if text[0] == "[":
        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError("top-level JSON array expected")
        return data

    messages: list[dict[str, Any]] = []
    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_no}: invalid JSON: {exc}") from exc
        if not isinstance(message, dict):
            raise ValueError(f"line {line_no}: message must be a JSON object")
        messages.append(message)
    return messages


def collect_components(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    components: list[dict[str, Any]] = []
    for message in messages:
        body = message.get("updateComponents")
        if isinstance(body, dict):
            batch = body.get("components")
            if isinstance(batch, list):
                components.extend(item for item in batch if isinstance(item, dict))
    return components


def component_index(components: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for component in components:
        cid = component.get("id")
        if isinstance(cid, str) and cid:
            index[cid] = component
    return index


def referenced_ids(component: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    children = component.get("children")
    if isinstance(children, list):
        refs.extend(item for item in children if isinstance(item, str))
    elif isinstance(children, dict):
        repeated_item_id = children.get("componentId")
        if isinstance(repeated_item_id, str):
            refs.append(repeated_item_id)

    for field in ("childrenIf", "childrenElse"):
        value = component.get(field)
        if isinstance(value, list):
            refs.extend(item for item in value if isinstance(item, str))

    tabs = component.get("children")
    if component.get("component") == "Tabs" and isinstance(tabs, list):
        refs.extend(item for item in tabs if isinstance(item, str))

    return refs


def repeated_item_descendant_ids(components: list[dict[str, Any]]) -> set[str]:
    index = component_index(components)
    repeated_item_roots: set[str] = set()
    for component in components:
        children = component.get("children")
        if isinstance(children, dict):
            repeated_item_id = children.get("componentId")
            if isinstance(repeated_item_id, str):
                repeated_item_roots.add(repeated_item_id)

    descendants: set[str] = set()

    def walk(cid: str) -> None:
        if cid in descendants:
            return
        descendants.add(cid)
        child = index.get(cid)
        if not child:
            return
        for ref in referenced_ids(child):
            walk(ref)

    for root in repeated_item_roots:
        walk(root)
    return descendants


def iter_path_bindings(node: Any, component_id: str, location: str = ""):
    if isinstance(node, dict):
        path_value = node.get("path")
        if isinstance(path_value, str):
            yield component_id, f"{location}.path" if location else "path", path_value
        for key, value in node.items():
            yield from iter_path_bindings(value, component_id, f"{location}.{key}" if location else key)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from iter_path_bindings(value, component_id, f"{location}[{index}]")


def pointer_exists(root: Any, pointer: str) -> bool:
    if pointer == "/":
        return True
    if not pointer.startswith("/"):
        return False
    node = root
    for raw_segment in pointer.lstrip("/").split("/"):
        segment = raw_segment.replace("~1", "/").replace("~0", "~")
        if isinstance(node, dict):
            if segment not in node:
                return False
            node = node[segment]
        elif isinstance(node, list):
            if not segment.isdigit():
                return False
            index = int(segment)
            if index < 0 or index >= len(node):
                return False
            node = node[index]
        else:
            return False
    return True


def check_action(action: Any, cid: str, errors: list[str]) -> None:
    if not isinstance(action, dict):
        errors.append(f"{cid}: action must be an object")
        return
    has_event = "event" in action
    has_call = "functionCall" in action
    if has_event == has_call:
        errors.append(f"{cid}: action must contain exactly one of event or functionCall")
        return
    if has_event:
        event = action.get("event")
        if not isinstance(event, dict) or not isinstance(event.get("name"), str) or not event.get("name"):
            errors.append(f"{cid}: action.event.name is required")
    if has_call:
        call = action.get("functionCall")
        if not isinstance(call, dict) or not isinstance(call.get("call"), str) or not call.get("call"):
            errors.append(f"{cid}: action.functionCall.call is required")


def check_event_handlers(value: Any, cid: str, field: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{cid}: {field} must be an EventHandler array")
        return
    for idx, handler in enumerate(value):
        if not isinstance(handler, dict):
            errors.append(f"{cid}: {field}[{idx}] must be an object")
            continue
        call = handler.get("call")
        if not isinstance(call, str) or not call:
            errors.append(f"{cid}: {field}[{idx}].call is required")
        if isinstance(call, str) and EXPR_RE.match(call.strip()):
            errors.append(f"{cid}: {field}[{idx}].call must not be an expression")


def check_styles(component: dict[str, Any], errors: list[str]) -> None:
    cid = str(component.get("id", "<unknown>"))
    ctype = component.get("component")
    styles = component.get("styles")
    if styles is None:
        return
    if not isinstance(styles, dict):
        errors.append(f"{cid}: styles must be an object")
        return

    allowed = COMMON_STYLE_KEYS | STYLE_KEYS_BY_COMPONENT.get(str(ctype), set())
    if ctype == "If":
        errors.append(f"{cid}: If is virtual and must not define styles")
        return

    for key, value in styles.items():
        if key in CSS_STYLE_ALIASES:
            errors.append(f"{cid}: use GenUI camelCase style key instead of CSS key {key!r}")
            continue
        if key not in allowed:
            errors.append(f"{cid}: unknown or unsupported style key {key!r} for {ctype}")
            continue

        if key in STYLE_ENUMS and isinstance(value, str) and not EXPR_RE.match(value):
            if value not in STYLE_ENUMS[key]:
                errors.append(f"{cid}: styles.{key} must be one of {sorted(STYLE_ENUMS[key])}, got {value!r}")

        if key in {"backgroundColor", "borderColor", "fontColor", "color"}:
            if isinstance(value, str) and not EXPR_RE.match(value) and not COLOR_RE.match(value):
                errors.append(f"{cid}: styles.{key} must be #RRGGBB or #AARRGGBB, got {value!r}")

        if key in {"width", "height", "borderWidth", "fontSize", "minFontSize", "maxFontSize", "strokeWidth"}:
            if isinstance(value, str) and not EXPR_RE.match(value):
                if value not in {"matchParent", "wrapContent", "fixAtIdealSize"} and not DIMENSION_RE.match(value):
                    errors.append(f"{cid}: styles.{key} has unsupported dimension string {value!r}")
            elif isinstance(value, (int, float)) and value < 0:
                errors.append(f"{cid}: styles.{key} must be non-negative")


def text_component_hint(component: dict[str, Any]) -> str:
    parts: list[str] = []
    cid = component.get("id")
    if isinstance(cid, str):
        parts.append(cid)

    content = component.get("content")
    if isinstance(content, str):
        parts.append(content)
    elif isinstance(content, dict):
        path = content.get("path")
        if isinstance(path, str):
            parts.append(path)

    return " ".join(parts)


def is_likely_protected_text(component: dict[str, Any]) -> bool:
    hint = text_component_hint(component)
    if not hint:
        return False
    if COMPRESSIBLE_TEXT_HINT_RE.search(hint):
        return False
    return bool(PROTECTED_TEXT_HINT_RE.search(hint))


def validate(messages: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if len(messages) < 3:
        warnings.append("expected at least createSurface, updateComponents, and updateDataModel messages")

    for idx, message in enumerate(messages, start=1):
        if message.get("version") != "v0.9":
            errors.append(f"message {idx}: version must be 'v0.9'")
        body_keys = [key for key in ("createSurface", "updateComponents", "updateDataModel", "deleteSurface") if key in message]
        if len(body_keys) != 1:
            errors.append(f"message {idx}: must contain exactly one A2UI message body, got {body_keys}")

    create_messages = [m["createSurface"] for m in messages if isinstance(m.get("createSurface"), dict)]
    component_messages = [m["updateComponents"] for m in messages if isinstance(m.get("updateComponents"), dict)]
    data_messages = [m["updateDataModel"] for m in messages if isinstance(m.get("updateDataModel"), dict)]

    if not create_messages:
        errors.append("missing createSurface")
    else:
        catalog = create_messages[0].get("catalogId")
        if catalog != EXTENDED_CATALOG:
            errors.append(f"createSurface.catalogId must be {EXTENDED_CATALOG!r}, got {catalog!r}")

    if not component_messages:
        errors.append("missing updateComponents")
    if not data_messages:
        errors.append("missing updateDataModel")

    surface_ids = []
    for body in create_messages + component_messages + data_messages:
        sid = body.get("surfaceId")
        if isinstance(sid, str) and sid:
            surface_ids.append(sid)
        else:
            errors.append("message body missing non-empty surfaceId")
    if surface_ids and len(set(surface_ids)) != 1:
        errors.append(f"surfaceId mismatch: {sorted(set(surface_ids))}")

    components = collect_components(messages)
    if not components:
        errors.append("updateComponents.components is empty")
        return errors, warnings

    ids: set[str] = set()
    for component in components:
        cid = component.get("id")
        ctype = component.get("component")
        if not isinstance(cid, str) or not cid:
            errors.append(f"component missing non-empty id: {component}")
            continue
        if cid in ids:
            errors.append(f"duplicate component id: {cid}")
        ids.add(cid)
        if ctype not in ALLOWED_COMPONENTS:
            errors.append(f"{cid}: unsupported component {ctype!r}")

    if "root" not in ids:
        errors.append("missing root component")

    all_refs: set[str] = set()
    for component in components:
        cid = str(component.get("id", "<unknown>"))
        ctype = component.get("component")

        all_refs.update(referenced_ids(component))

        if ctype == "Text":
            if "text" in component:
                errors.append(f"{cid}: extended Text must use content, not text")
            if "content" not in component:
                errors.append(f"{cid}: Text.content is required")
            styles = component.get("styles")
            if (
                isinstance(styles, dict)
                and styles.get("textOverflow") in {"ellipsis", "clip", "marquee"}
                and is_likely_protected_text(component)
            ):
                warnings.append(
                    f"{cid}: likely protected text uses textOverflow={styles.get('textOverflow')!r}; "
                    "key information should display fully by rebalancing width, font, or row structure"
                )
        elif ctype == "Image":
            if "url" in component:
                errors.append(f"{cid}: extended Image must use src, not url")
            if "src" not in component:
                errors.append(f"{cid}: Image.src is required")
        elif ctype == "Button":
            if "child" in component:
                errors.append(f"{cid}: extended Button must use label, not child")
            if "label" not in component:
                errors.append(f"{cid}: Button.label is required")
            if "action" in component:
                check_action(component["action"], cid, errors)
            if "action" in component and "onClick" in component:
                warnings.append(f"{cid}: Button.action has priority over onClick")
        elif ctype in {"Row", "Column"}:
            if "children" not in component:
                errors.append(f"{cid}: {ctype}.children is required")
        elif ctype == "If":
            if "condition" not in component:
                errors.append(f"{cid}: If.condition is required")
            elif not isinstance(component.get("condition"), str) or not EXPR_RE.match(component["condition"].strip()):
                errors.append(f"{cid}: If.condition must be a full {{ ... }} expression")

        for field, allowed in COMPONENT_ENUMS.get(str(ctype), {}).items():
            if field in component and component[field] not in allowed:
                errors.append(f"{cid}: {field} must be one of {sorted(allowed)}, got {component[field]!r}")

        for event_field in ("onClick", "onAppear", "onChange", "onReachStart", "onReachEnd"):
            if event_field in component:
                check_event_handlers(component[event_field], cid, event_field, errors)

        check_styles(component, errors)

    missing = sorted(ref for ref in all_refs if ref not in ids)
    if missing:
        errors.append(f"undefined referenced component ids: {missing}")

    data_value = {}
    data_path = "/"
    if data_messages:
        data_body = data_messages[-1]
        data_path = data_body.get("path", "/")
        if not isinstance(data_path, str) or not data_path.startswith("/"):
            errors.append(f"updateDataModel.path must be a JSON Pointer, got {data_path!r}")
        data_value = data_body.get("value", {})

    repeated_item_ids = repeated_item_descendant_ids(components)
    for component in components:
        cid = str(component.get("id", "<unknown>"))
        for bind_cid, location, path_value in iter_path_bindings(component, cid):
            if "." in path_value:
                errors.append(f"{bind_cid}: {location} uses dotted path {path_value!r}; use '/' or relative field paths")
            if path_value.startswith("/"):
                if data_path == "/" and not pointer_exists(data_value, path_value):
                    warnings.append(f"{bind_cid}: {location} points to missing DataModel path {path_value!r}")
            elif bind_cid not in repeated_item_ids:
                errors.append(f"{bind_cid}: {location} uses relative path {path_value!r} outside a repeated-item subtree")

    root = component_index(components).get("root")
    if root:
        styles = root.get("styles", {})
        if isinstance(styles, dict):
            if styles.get("width") not in ("100%", 160, "160", "160vp"):
                warnings.append("root.styles.width should usually be 160 or '100%' for 2x2/2x4 desktop cards")
            if "height" not in styles:
                warnings.append("root.styles.height is missing; 2x2 cards use 160 and 2x4 cards use 320")
            elif styles.get("height") not in (160, 320, "160", "320", "160vp", "320vp"):
                warnings.append("root.styles.height should usually be 160 for 2x2 or 320 for 2x4 desktop cards")
        else:
            warnings.append("root.styles is missing")

    for component in components:
        for _, _, value in iter_path_bindings(component, str(component.get("id", "<unknown>"))):
            if isinstance(value, str) and PLACEHOLDER_URL_RE.search(value):
                errors.append(f"{component.get('id')}: placeholder URL found in binding path")
    if data_messages:
        urls = collect_urls(data_messages[-1].get("value", {}))
        for url in urls:
            if PLACEHOLDER_URL_RE.search(url):
                errors.append(f"updateDataModel contains placeholder URL: {url}")

    return errors, warnings


def collect_urls(node: Any) -> list[str]:
    found: list[str] = []
    if isinstance(node, str) and node.startswith(("http://", "https://")):
        found.append(node)
    elif isinstance(node, dict):
        for value in node.values():
            found.extend(collect_urls(value))
    elif isinstance(node, list):
        for value in node:
            found.extend(collect_urls(value))
    return found


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python validate_genui_card.py <card.dsl.jsonl>")
        return 2

    path = Path(argv[1])
    try:
        messages = load_messages(path)
    except Exception as exc:
        print(f"Failed to load DSL: {exc}")
        return 1

    errors, warnings = validate(messages)
    if errors:
        print(f"Found {len(errors)} error(s):")
        for error in errors:
            print(f" - {error}")
        if warnings:
            print(f"Found {len(warnings)} warning(s):")
            for warning in warnings:
                print(f" - {warning}")
        return 1

    if warnings:
        print(f"Found {len(warnings)} warning(s):")
        for warning in warnings:
            print(f" - {warning}")

    components = collect_components(messages)
    surface_id = "N/A"
    for message in messages:
        for key in ("createSurface", "updateComponents", "updateDataModel"):
            body = message.get(key)
            if isinstance(body, dict) and body.get("surfaceId"):
                surface_id = body["surfaceId"]
                break
        if surface_id != "N/A":
            break

    print("GenUI card validation passed")
    print(f"messages: {len(messages)}")
    print(f"components: {len(components)}")
    print(f"surfaceId: {surface_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
