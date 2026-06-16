#!/usr/bin/env python3
"""
Validate a HarmonyOS GenUI desktop-card DSL artifact.

Accepts JSONL messages or a JSON array of messages. The final deliverable should
still be JSONL: createSurface, updateComponents, updateDataModel.
"""

# =============================================================================
# 【文件概述】
# 本脚本用于验证 HarmonyOS GenUI 桌面卡片 DSL（领域特定语言）产物。
# 输入：JSONL 格式（每行一个 JSON 对象）或 JSON 数组，包含卡片的消息流。
# 核心概念：一张卡片由三类消息组成——
#   1. createSurface      - 创建卡片画布（指定组件目录 catalogId）
#   2. updateComponents   - 定义卡片的 UI 组件树
#   3. updateDataModel    - 定义卡片的数据模型（JSON Pointer 路径 + 值）
# =============================================================================

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


# =============================================================================
# 常量定义
# =============================================================================

# 扩展组件目录 ID：HarmonyOS A2UI 扩展组件集
EXTENDED_CATALOG = "ohos.a2ui.extended.catalog"

# ---------------------------------------------------------------------------
# 允许的组件类型白名单
# 基础组件：Text/Image/Divider/Progress
# 交互组件：Button/TextInput/Select/Toggle/Radio/Checkbox/CheckboxGroup
# 布局组件：Row/Column/List/Stack/Grid
# 导航组件：Tabs/TabContent/Navigation/NavContainer
# 特殊组件：Web（内嵌网页）、If（条件渲染/虚拟组件）
# ---------------------------------------------------------------------------
ALLOWED_COMPONENTS = {
    "Text", "Image", "Divider", "Progress",
    "Button", "TextInput", "Select", "Toggle", "Radio", "Checkbox", "CheckboxGroup",
    "Row", "Column", "List", "Stack", "Grid",
    "Tabs", "TabContent", "Navigation", "NavContainer",
    "Web", "If",
}

# 所有组件通用的样式属性（布局、盒模型、边框、背景、阴影、可见性等）
COMMON_STYLE_KEYS = {
    "width", "height", "constraintSize",
    "margin", "padding",
    "borderRadius", "borderWidth", "borderColor",
    "backgroundColor", "backgroundImage", "backgroundImageSizeWithStyle",
    "linearGradient",
    "layoutWeight", "flexShrink",
    "shadow", "visibility", "clip",
}

# Text 组件专属样式属性
TEXT_STYLE_KEYS = {
    "fontColor", "fontSize", "fontWeight", "maxLines",
    "minFontSize", "maxFontSize",
    "fontScaleMode", "minFontScale", "maxFontScale",
    "textOverflow", "textAlign", "wordBreak", "decoration",
}

# Image 组件专属样式属性
IMAGE_STYLE_KEYS = {"objectFit", "aspectRatio"}
# Divider 组件专属样式属性
DIVIDER_STYLE_KEYS = {"strokeWidth", "vertical", "color"}
# Progress 组件专属样式属性
PROGRESS_STYLE_KEYS = {"color", "type"}
# Grid 组件专属样式属性（列模板、行模板、间距）
GRID_STYLE_KEYS = {"columnsTemplate", "rowsTemplate", "columnsGap", "rowsGap"}
# List 组件专属样式属性（方向、滚动条、嵌套滚动）
LIST_STYLE_KEYS = {"listDirection", "scrollBar", "nestedScroll"}
# Button 组件专属样式属性（字体相关）
BUTTON_STYLE_KEYS = {
    "fontSize", "fontWeight", "minFontSize", "maxFontSize",
    "fontScaleMode", "minFontScale", "maxFontScale", "fontColor",
}

# 组件类型 -> 该组件允许的专属样式属性映射
STYLE_KEYS_BY_COMPONENT = {
    "Text": TEXT_STYLE_KEYS,
    "Image": IMAGE_STYLE_KEYS,
    "Divider": DIVIDER_STYLE_KEYS,
    "Progress": PROGRESS_STYLE_KEYS,
    "Grid": GRID_STYLE_KEYS,
    "List": LIST_STYLE_KEYS,
    "Button": BUTTON_STYLE_KEYS,
}

# CSS 风格的样式别名（kebab-case），应使用 GenUI 的 camelCase 样式名而非这些
# 检测到会报错，提示用户使用正确的驼峰命名
CSS_STYLE_ALIASES = {
    "font-size", "font-weight", "font-color", "background-color",
    "border-radius", "border-width", "border-color", "max-lines",
    "text-overflow", "text-align", "object-fit",
}

# 各组件特有属性的合法枚举值
# 不合法的值会报错
COMPONENT_ENUMS = {
    "Row": {
        # 主轴对齐方式
        "justifyContent": {"start", "center", "end", "spaceAround", "spaceBetween", "spaceEvenly"},
        # 交叉轴对齐方式
        "alignItems": {"top", "center", "bottom"},
        # 是否换行
        "wrap": {"noWrap", "wrap"},
    },
    "Column": {
        "justifyContent": {"start", "center", "end", "spaceAround", "spaceBetween", "spaceEvenly"},
        "alignItems": {"start", "center", "end"},
    },
    "Stack": {
        # 层叠布局的内容对齐方式（9 个方位）
        "alignContent": {"topStart", "top", "topEnd", "start", "center", "end", "bottomStart", "bottom", "bottomEnd"},
    },
    "List": {
        # 列表方向：垂直 / 水平
        "listDirection": {"vertical", "horizontal"},
        # 滚动条：关闭 / 自动 / 始终显示
        "scrollBar": {"off", "auto", "on"},
    },
}

# 通用样式属性的合法枚举值（不限于特定组件）
STYLE_ENUMS = {
    # 文本溢出处理
    "textOverflow": {"none", "clip", "ellipsis", "marquee"},
    # 文本对齐
    "textAlign": {"start", "center", "end", "justify"},
    # 单词断行
    "wordBreak": {"normal", "breakAll", "breakWord", "hyphenation"},
    # 字体缩放模式：跟随系统 / 自定义
    "fontScaleMode": {"followSystem", "custom"},
    # 图片/媒体填充模式
    "objectFit": {
        "fill", "contain", "cover", "auto", "none", "scaleDown",
        "topStart", "top", "topEnd", "start", "center", "end",
        "bottomStart", "bottom", "bottomEnd", "matrix",
    },
    # 进度条类型
    "type": {"linear", "ring", "eclipse", "scaleRing", "capsule"},
    # 可见性
    "visibility": {"visible", "hidden", "none"},
}

# ---------------------------------------------------------------------------
# 正则表达式模式
# ---------------------------------------------------------------------------

# 颜色格式：#RRGGBB 或 #AARRGGBB（6 位或 8 位十六进制）
COLOR_RE = re.compile(r"^#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")

# 尺寸格式：数字 + 单位（vp/fp/px/%）
# vp = virtual pixel（虚拟像素），fp = font pixel（字体像素）
DIMENSION_RE = re.compile(r"^\d+(?:\.\d+)?(?:vp|fp|px|%)$")

# 数据绑定表达式：{{ ... }} 包裹的表达式，用于将 UI 属性绑定到 DataModel
EXPR_RE = re.compile(r"^\{\{.*\}\}$", re.DOTALL)

# 占位图片 URL 模式：检测常见占位图服务，确保最终产物不含占位图
PLACEHOLDER_URL_RE = re.compile(
    r"https?://(?:example\.com|placeholder\.com|via\.placeholder\.com|picsum\.photos|dummyimage\.com)",
    re.IGNORECASE,
)

# 「受保护文本」提示正则 —— 匹配看起来像关键信息（标题/价格/状态等）的字段名
# 如果这类文本使用了 textOverflow 截断，会产生警告
PROTECTED_TEXT_HINT_RE = re.compile(
    r"(time|date|day|weekday|status|badge|cta|action|button|title|name|price|"
    r"percent|percentage|battery|temperature|temp|countdown|count|metric|value)",
    re.IGNORECASE,
)

# 「可压缩文本」提示正则 —— 匹配看起来像次要信息（描述/副标题/元数据等）的字段名
# 这类文本被截断时不会产生警告
COMPRESSIBLE_TEXT_HINT_RE = re.compile(
    r"(meta|subtitle|subTitle|description|desc|detail|location|body|summary|"
    r"advisory|note|hint|secondary)",
    re.IGNORECASE,
)


# =============================================================================
# 数据加载与解析
# =============================================================================

def load_messages(path: Path) -> list[dict[str, Any]]:
    """
    从文件加载 DSL 消息。
    支持两种格式：
      - JSON 数组（以 '[' 开头）：直接 json.loads 解析
      - JSONL（每行一个 JSON 对象）：逐行解析，跳过空行
    返回消息字典列表。
    """
    # 读取文件内容（utf-8-sig 会处理 BOM 头）
    text = path.read_text(encoding="utf-8-sig").strip()
    if not text:
        raise ValueError("file is empty")

    # 分支 1：JSON 数组格式
    if text[0] == "[":
        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError("top-level JSON array expected")
        return data

    # 分支 2：JSONL 格式（每行一个 JSON）
    messages: list[dict[str, Any]] = []
    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:          # 跳过空行
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_no}: invalid JSON: {exc}") from exc
        if not isinstance(message, dict):
            raise ValueError(f"line {line_no}: message must be a JSON object")
        messages.append(message)
    return messages


# =============================================================================
# 组件索引与引用解析
# =============================================================================

def collect_components(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    从所有消息中提取组件列表。
    遍历每条消息的 updateComponents.components 字段，将所有组件扁平化收集。
    """
    components: list[dict[str, Any]] = []
    for message in messages:
        body = message.get("updateComponents")
        if isinstance(body, dict):
            batch = body.get("components")
            if isinstance(batch, list):
                components.extend(item for item in batch if isinstance(item, dict))
    return components


def component_index(components: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """
    构建组件 ID -> 组件对象的索引，用于快速查找组件。
    类似数据库主键索引，key 是组件的 id 字段。
    """
    index: dict[str, dict[str, Any]] = {}
    for component in components:
        cid = component.get("id")
        if isinstance(cid, str) and cid:
            index[cid] = component
    return index


def referenced_ids(component: dict[str, Any]) -> list[str]:
    """
    获取一个组件引用的所有子组件 ID。
    子组件可以通过以下方式引用：
      - children: [id1, id2, ...]              → 直接子组件列表
      - children: {componentId: "xxx"}          → 重复项模板（List 的列表项）
      - childrenIf / childrenElse               → If 组件的条件分支
      - Tabs 组件的 children 列表               → TabContent 引用
    """
    refs: list[str] = []

    # 普通子组件列表
    children = component.get("children")
    if isinstance(children, list):
        refs.extend(item for item in children if isinstance(item, str))
    elif isinstance(children, dict):
        # 重复项模式：List 等组件使用 componentId 引用模板组件
        repeated_item_id = children.get("componentId")
        if isinstance(repeated_item_id, str):
            refs.append(repeated_item_id)

    # If 组件的条件分支
    for field in ("childrenIf", "childrenElse"):
        value = component.get(field)
        if isinstance(value, list):
            refs.extend(item for item in value if isinstance(item, str))

    # Tabs 组件的 Tab 页签引用
    tabs = component.get("children")
    if component.get("component") == "Tabs" and isinstance(tabs, list):
        refs.extend(item for item in tabs if isinstance(item, str))

    return refs


def repeated_item_descendant_ids(components: list[dict[str, Any]]) -> set[str]:
    """
    找出所有属于「重复项模板子树」的组件 ID。

    背景：List 等组件使用 children: {componentId: "xxx"} 定义列表项模板，
    该模板组件（及其所有后代组件）的数据绑定可以使用相对路径，
    而非绝对路径（以 / 开头）。此函数用于识别哪些组件属于这种子树。

    实现：
      1. 找到所有重复项模板的根组件（componentId 指向的组件）
      2. 从每个根组件出发，递归遍历其所有后代
      3. 返回所有后代组件的 ID 集合
    """
    index = component_index(components)

    # 步骤 1：找到所有重复项模板根组件
    repeated_item_roots: set[str] = set()
    for component in components:
        children = component.get("children")
        if isinstance(children, dict):
            repeated_item_id = children.get("componentId")
            if isinstance(repeated_item_id, str):
                repeated_item_roots.add(repeated_item_id)

    # 步骤 2+3：递归收集所有后代组件
    descendants: set[str] = set()

    def walk(cid: str) -> None:
        """DFS 遍历组件树，收集后代 ID"""
        if cid in descendants:   # 防止循环引用
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


# =============================================================================
# 数据绑定路径解析
# =============================================================================

def iter_path_bindings(node: Any, component_id: str, location: str = ""):
    """
    递归遍历组件定义，找出所有 path 字段（即数据绑定路径）。

    生成器产出：(component_id, location, path_value) 三元组
      - component_id: 所属组件的 ID
      - location:     该绑定在组件 JSON 中的位置（如 "styles.width"）
      - path_value:   path 字段的值（数据模型路径）

    支持嵌套的 dict 和 list 递归遍历。
    """
    if isinstance(node, dict):
        path_value = node.get("path")
        if isinstance(path_value, str):
            # 找到了一个 path 绑定
            yield component_id, f"{location}.path" if location else "path", path_value
        for key, value in node.items():
            yield from iter_path_bindings(value, component_id, f"{location}.{key}" if location else key)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from iter_path_bindings(value, component_id, f"{location}[{index}]")


def pointer_exists(root: Any, pointer: str) -> bool:
    """
    检查一个 JSON Pointer（RFC 6901）路径在数据中是否存在。

    JSON Pointer 规则：
      - "/" 指向根对象
      - "/foo/bar" 指向 root.foo.bar
      - "~1" 转义为 "/"，"~0" 转义为 "~"
      - 数字段用于数组下标
    """
    if pointer == "/":
        return True
    if not pointer.startswith("/"):
        return False

    node = root
    for raw_segment in pointer.lstrip("/").split("/"):
        # 还原转义字符
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


# =============================================================================
# 交互与事件验证
# =============================================================================

def check_action(action: Any, cid: str, errors: list[str]) -> None:
    """
    验证 action 对象（按钮点击等交互动作）。

    action 必须是一个对象，且恰好包含以下二者之一：
      - event:       { name: "..." }            → 触发事件
      - functionCall: { call: "表达式" }         → 调用函数
    """
    if not isinstance(action, dict):
        errors.append(f"{cid}: action must be an object")
        return

    has_event = "event" in action
    has_call = "functionCall" in action

    # 必须恰好包含一个
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
    """
    验证事件处理器数组（onClick / onAppear / onChange 等）。

    每个 handler 必须有 call 字段，且 call 不能是 {{ ... }} 表达式
    （事件处理器中的 call 是直接执行的表达式，不需要双花括号包裹）。
    """
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
        # 表达式语法在事件处理器中无效 —— 这里应该直接写调用
        if isinstance(call, str) and EXPR_RE.match(call.strip()):
            errors.append(f"{cid}: {field}[{idx}].call must not be an expression")


# =============================================================================
# 样式验证
# =============================================================================

def check_styles(component: dict[str, Any], errors: list[str]) -> None:
    """
    验证组件的 styles 对象。

    检查项：
      1. styles 必须是 dict 类型
      2. If 虚拟组件不能有样式
      3. 样式 key 不能是 CSS kebab-case（如 font-size），必须用 camelCase
      4. 样式 key 必须在允许的范围内（通用 + 该组件专属）
      5. 有枚举约束的值必须在合法值范围内
      6. 颜色值必须是 #RRGGBB 或 #AARRGGBB 格式
      7. 尺寸值必须是合法格式（数字+单位 或 matchParent/wrapContent 等）
    """
    cid = str(component.get("id", "<unknown>"))
    ctype = component.get("component")
    styles = component.get("styles")

    # 没有样式则跳过
    if styles is None:
        return
    if not isinstance(styles, dict):
        errors.append(f"{cid}: styles must be an object")
        return

    # 合并该组件可用的所有样式 key：通用 + 组件专属
    allowed = COMMON_STYLE_KEYS | STYLE_KEYS_BY_COMPONENT.get(str(ctype), set())

    # If 是虚拟组件，不应有样式
    if ctype == "If":
        errors.append(f"{cid}: If is virtual and must not define styles")
        return

    for key, value in styles.items():
        # 检查 1：CSS 风格别名
        if key in CSS_STYLE_ALIASES:
            errors.append(f"{cid}: use GenUI camelCase style key instead of CSS key {key!r}")
            continue

        # 检查 2：未知或不支持的样式 key
        if key not in allowed:
            errors.append(f"{cid}: unknown or unsupported style key {key!r} for {ctype}")
            continue

        # 检查 3：枚举值是否合法（仅检查非表达式的字符串值）
        if key in STYLE_ENUMS and isinstance(value, str) and not EXPR_RE.match(value):
            if value not in STYLE_ENUMS[key]:
                errors.append(f"{cid}: styles.{key} must be one of {sorted(STYLE_ENUMS[key])}, got {value!r}")

        # 检查 4：颜色格式验证
        if key in {"backgroundColor", "borderColor", "fontColor", "color"}:
            if isinstance(value, str) and not EXPR_RE.match(value) and not COLOR_RE.match(value):
                errors.append(f"{cid}: styles.{key} must be #RRGGBB or #AARRGGBB, got {value!r}")

        # 检查 5：尺寸值格式验证
        if key in {"width", "height", "borderWidth", "fontSize", "minFontSize", "maxFontSize", "strokeWidth"}:
            if isinstance(value, str) and not EXPR_RE.match(value):
                if value not in {"matchParent", "wrapContent", "fixAtIdealSize"} and not DIMENSION_RE.match(value):
                    errors.append(f"{cid}: styles.{key} has unsupported dimension string {value!r}")
            elif isinstance(value, (int, float)) and value < 0:
                errors.append(f"{cid}: styles.{key} must be non-negative")


# =============================================================================
# 文本保护检测（防止关键信息被截断）
# =============================================================================

def text_component_hint(component: dict[str, Any]) -> str:
    """
    为 Text 组件生成一个「提示字符串」，用于判断该文本是关键信息还是次要信息。

    提示字符串由以下部分拼接而成：
      - 组件 id（如 "title_text"）
      - content 文本内容
      - content 中的 path 绑定路径（如 "/data/title"）

    这些信息会用于 PROTECTED_TEXT_HINT_RE 和 COMPRESSIBLE_TEXT_HINT_RE 的正则匹配。
    """
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
    """
    判断 Text 组件的内容是否为「关键信息」，不应被截断。

    逻辑：
      1. 如果提示字符串匹配「可压缩文本」模式 → 不是关键信息
      2. 如果提示字符串匹配「受保护文本」模式 → 是关键信息
      3. 否则 → 不是关键信息

    示例：
      - id="title" + path="/data/productName"  → 匹配 "title"+"name" → 受保护
      - id="desc"  + path="/data/description"  → 匹配 "desc"+"description" → 可压缩
    """
    hint = text_component_hint(component)
    if not hint:
        return False
    # 先检查可压缩，避免将明确标注为次要信息的字段误判
    if COMPRESSIBLE_TEXT_HINT_RE.search(hint):
        return False
    return bool(PROTECTED_TEXT_HINT_RE.search(hint))


# =============================================================================
# 主验证逻辑
# =============================================================================

def validate(messages: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    """
    主验证函数。对所有消息进行全面验证，返回 (errors, warnings)。

    验证流程：
      1. 消息数量检查（至少 3 条）
      2. 每条消息的 version 和 body 格式检查
      3. createSurface / updateComponents / updateDataModel 存在性检查
      4. surfaceId 一致性检查（所有消息的 surfaceId 必须一致）
      5. 组件检查：
         - 组件 id 唯一性
         - 组件类型是否在白名单中
         - 必填字段检查（如 Text.content, Image.src, Button.label, Row.children）
         - 组件属性枚举值检查
         - 事件处理器检查
         - 样式检查
      6. 组件引用完整性检查（不能有未定义的引用）
      7. 数据绑定路径检查（相对路径只能在重复项子树中使用）
      8. 根组件 root 的尺寸建议
      9. 占位 URL 检查（最终产物不应含占位图）
    """
    errors: list[str] = []
    warnings: list[str] = []

    # ---- 第 1 步：消息数量 ----
    if len(messages) < 3:
        warnings.append("expected at least createSurface, updateComponents, and updateDataModel messages")

    # ---- 第 2 步：逐条消息格式检查 ----
    for idx, message in enumerate(messages, start=1):
        # 版本号必须为 v0.9
        if message.get("version") != "v0.9":
            errors.append(f"message {idx}: version must be 'v0.9'")

        # 每条消息必须恰好包含一个 A2UI 消息体
        # （createSurface / updateComponents / updateDataModel / deleteSurface 四选一）
        body_keys = [key for key in ("createSurface", "updateComponents", "updateDataModel", "deleteSurface") if key in message]
        if len(body_keys) != 1:
            errors.append(f"message {idx}: must contain exactly one A2UI message body, got {body_keys}")

    # ---- 第 3 步：提取各类型消息体 ----
    create_messages = [m["createSurface"] for m in messages if isinstance(m.get("createSurface"), dict)]
    component_messages = [m["updateComponents"] for m in messages if isinstance(m.get("updateComponents"), dict)]
    data_messages = [m["updateDataModel"] for m in messages if isinstance(m.get("updateDataModel"), dict)]

    # ---- 第 4 步：必要消息存在性 + catalogId 检查 ----
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

    # ---- 第 5 步：surfaceId 一致性 ----
    surface_ids = []
    for body in create_messages + component_messages + data_messages:
        sid = body.get("surfaceId")
        if isinstance(sid, str) and sid:
            surface_ids.append(sid)
        else:
            errors.append("message body missing non-empty surfaceId")
    if surface_ids and len(set(surface_ids)) != 1:
        errors.append(f"surfaceId mismatch: {sorted(set(surface_ids))}")

    # ---- 第 6 步：组件列表提取 ----
    components = collect_components(messages)
    if not components:
        errors.append("updateComponents.components is empty")
        return errors, warnings

    # ---- 第 7 步：组件基础字段检查 ----
    ids: set[str] = set()
    for component in components:
        cid = component.get("id")
        ctype = component.get("component")

        # id 必须是有效字符串
        if not isinstance(cid, str) or not cid:
            errors.append(f"component missing non-empty id: {component}")
            continue

        # id 不能重复
        if cid in ids:
            errors.append(f"duplicate component id: {cid}")
        ids.add(cid)

        # 组件类型必须在白名单中
        if ctype not in ALLOWED_COMPONENTS:
            errors.append(f"{cid}: unsupported component {ctype!r}")

    # 必须有一个 id="root" 的根组件
    if "root" not in ids:
        errors.append("missing root component")

    # ---- 第 8 步：组件详细字段验证 ----
    all_refs: set[str] = set()
    for component in components:
        cid = str(component.get("id", "<unknown>"))
        ctype = component.get("component")

        # 收集所有引用的子组件 ID（用于后续完整性检查）
        all_refs.update(referenced_ids(component))

        # --- 各组件类型的特定验证 ---

        if ctype == "Text":
            # GenUI 扩展：Text 用 content 替代标准 text 字段
            if "text" in component:
                errors.append(f"{cid}: extended Text must use content, not text")
            if "content" not in component:
                errors.append(f"{cid}: Text.content is required")
            # 关键信息截断警告
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
            # GenUI 扩展：Image 用 src 替代标准 url 字段
            if "url" in component:
                errors.append(f"{cid}: extended Image must use src, not url")
            if "src" not in component:
                errors.append(f"{cid}: Image.src is required")

        elif ctype == "Button":
            # GenUI 扩展：Button 用 label 替代标准 child 字段
            if "child" in component:
                errors.append(f"{cid}: extended Button must use label, not child")
            if "label" not in component:
                errors.append(f"{cid}: Button.label is required")
            if "action" in component:
                check_action(component["action"], cid, errors)
            # action 和 onClick 互斥：action 优先
            if "action" in component and "onClick" in component:
                warnings.append(f"{cid}: Button.action has priority over onClick")

        elif ctype in {"Row", "Column"}:
            # 布局容器必须有 children
            if "children" not in component:
                errors.append(f"{cid}: {ctype}.children is required")

        elif ctype == "If":
            # 条件渲染：必须有 condition，且必须是 {{ ... }} 表达式
            if "condition" not in component:
                errors.append(f"{cid}: If.condition is required")
            elif not isinstance(component.get("condition"), str) or not EXPR_RE.match(component["condition"].strip()):
                errors.append(f"{cid}: If.condition must be a full {{ ... }} expression")

        # --- 组件属性枚举值检查 ---
        for field, allowed in COMPONENT_ENUMS.get(str(ctype), {}).items():
            if field in component and component[field] not in allowed:
                errors.append(f"{cid}: {field} must be one of {sorted(allowed)}, got {component[field]!r}")

        # --- 事件处理器检查 ---
        for event_field in ("onClick", "onAppear", "onChange", "onReachStart", "onReachEnd"):
            if event_field in component:
                check_event_handlers(component[event_field], cid, event_field, errors)

        # --- 样式检查 ---
        check_styles(component, errors)

    # ---- 第 9 步：引用完整性检查 ----
    # 任何被引用但未定义的组件 ID 都是错误
    missing = sorted(ref for ref in all_refs if ref not in ids)
    if missing:
        errors.append(f"undefined referenced component ids: {missing}")

    # ---- 第 10 步：DataModel 路径绑定检查 ----
    data_value = {}
    data_path = "/"
    if data_messages:
        data_body = data_messages[-1]  # 使用最后一条 updateDataModel 消息
        data_path = data_body.get("path", "/")
        if not isinstance(data_path, str) or not data_path.startswith("/"):
            errors.append(f"updateDataModel.path must be a JSON Pointer, got {data_path!r}")
        data_value = data_body.get("value", {})

    # 找出所有重复项模板子树中的组件
    repeated_item_ids = repeated_item_descendant_ids(components)

    for component in components:
        cid = str(component.get("id", "<unknown>"))
        for bind_cid, location, path_value in iter_path_bindings(component, cid):
            # 检查 1：不能使用点号分隔的路径（如 "a.b.c"），应使用 "/" 或相对字段路径
            if "." in path_value:
                errors.append(f"{bind_cid}: {location} uses dotted path {path_value!r}; use '/' or relative field paths")

            # 检查 2：绝对路径必须在 DataModel 中存在
            if path_value.startswith("/"):
                if data_path == "/" and not pointer_exists(data_value, path_value):
                    warnings.append(f"{bind_cid}: {location} points to missing DataModel path {path_value!r}")

            # 检查 3：相对路径只能出现在重复项子树中
            elif bind_cid not in repeated_item_ids:
                errors.append(f"{bind_cid}: {location} uses relative path {path_value!r} outside a repeated-item subtree")

    # ---- 第 11 步：根组件样式建议 ----
    root = component_index(components).get("root")
    if root:
        styles = root.get("styles", {})
        if isinstance(styles, dict):
            # 桌面卡片标准尺寸：2x2 = 160vp，2x4 = 320vp
            if styles.get("width") not in ("100%", 160, "160", "160vp"):
                warnings.append("root.styles.width should usually be 160 or '100%' for 2x2/2x4 desktop cards")
            if "height" not in styles:
                warnings.append("root.styles.height is missing; 2x2 cards use 160 and 2x4 cards use 320")
            elif styles.get("height") not in (160, 320, "160", "320", "160vp", "320vp"):
                warnings.append("root.styles.height should usually be 160 for 2x2 or 320 for 2x4 desktop cards")
        else:
            warnings.append("root.styles is missing")

    # ---- 第 12 步：占位 URL 检查 ----
    # 检查组件绑定路径中是否包含占位 URL
    for component in components:
        for _, _, value in iter_path_bindings(component, str(component.get("id", "<unknown>"))):
            if isinstance(value, str) and PLACEHOLDER_URL_RE.search(value):
                errors.append(f"{component.get('id')}: placeholder URL found in binding path")

    # 检查 DataModel 的值中是否包含占位 URL
    if data_messages:
        urls = collect_urls(data_messages[-1].get("value", {}))
        for url in urls:
            if PLACEHOLDER_URL_RE.search(url):
                errors.append(f"updateDataModel contains placeholder URL: {url}")

    return errors, warnings


def collect_urls(node: Any) -> list[str]:
    """
    递归收集数据模型中所有的 URL 字符串。
    用于检查是否包含占位图 URL。
    """
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


# =============================================================================
# CLI 入口
# =============================================================================

def main(argv: list[str]) -> int:
    """
    命令行入口。
    用法：python validate_genui_card.py <card.dsl.jsonl>

    返回值：
      0 - 验证通过（可能有警告）
      1 - 验证失败（有错误）
      2 - 参数错误
    """
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

    # 输出错误（如有）
    if errors:
        print(f"Found {len(errors)} error(s):")
        for error in errors:
            print(f" - {error}")
        if warnings:
            print(f"Found {len(warnings)} warning(s):")
            for warning in warnings:
                print(f" - {warning}")
        return 1

    # 仅有警告时也输出
    if warnings:
        print(f"Found {len(warnings)} warning(s):")
        for warning in warnings:
            print(f" - {warning}")

    # 提取 surfaceId 用于输出摘要
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

    # 验证通过摘要
    print("GenUI card validation passed")
    print(f"messages: {len(messages)}")
    print(f"components: {len(components)}")
    print(f"surfaceId: {surface_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
