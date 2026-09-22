import argparse
import json
from pathlib import Path

from bs4 import BeautifulSoup, Doctype
import tinycss2


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inspect_css(tokens):
    for token in tokens:
        require(token.type != "error", "CSS 存在解析错误")
        if token.type == "url":
            require(token.value.startswith(("data:", "#")), "自包含原型引用外部 CSS 资源")
        if token.type == "function" and token.lower_name == "url":
            values = [item for item in token.arguments if item.type not in {"whitespace", "comment"}]
            require(len(values) == 1 and getattr(values[0], "value", "").startswith(("data:", "#")), "自包含原型引用外部 CSS 资源")
        if token.type == "at-rule" and token.lower_at_keyword == "import":
            require(False, "自包含原型不能使用 CSS import")
        for field in ("content", "prelude", "arguments"):
            children = getattr(token, field, None)
            if children:
                inspect_css(children)


def validate(path, self_contained=False):
    require(path.is_file() and path.suffix.lower() in {".html", ".htm"}, "需要存在的 HTML 文件")
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    require(any(isinstance(item, Doctype) for item in soup.contents), "缺少 HTML doctype")
    require(all(soup.find(tag) is not None for tag in ("html", "head", "body")), "HTML 文档结构不完整")
    main_present = soup.select_one('main, [role="main"], [data-screen-id]') is not None
    controls = soup.select("button, input, select, textarea, a[href]")
    runtime_required = not main_present or not controls
    require(not runtime_required or soup.find("script") is not None, "缺少主内容或可操作元素，且无动态渲染入口")
    ids = [element["id"] for element in soup.select("[id]")]
    require(len(ids) == len(set(ids)), "HTML 存在重复 ID")
    if self_contained:
        for element in soup.select("script[src], link[href], img[src], source[src], video[src], audio[src], iframe[src], object[data], [poster], [srcset]"):
            if element.name == "link" and not set(element.get("rel", [])) & {"stylesheet", "icon", "preload", "modulepreload"}:
                continue
            require(not element.has_attr("srcset"), "自包含检查要求将 srcset 资源内联到明确的 src")
            for attr in ("src", "href", "poster", "data"):
                value = element.get(attr)
                if value:
                    require(value.startswith(("data:", "#")), f"自包含原型引用外部资源：{element.name}/{attr}")
        for style in soup.find_all("style"):
            inspect_css(tinycss2.parse_stylesheet(style.get_text(), skip_comments=True, skip_whitespace=True))
        for element in soup.select("[style]"):
            inspect_css(tinycss2.parse_declaration_list(element["style"], skip_comments=True, skip_whitespace=True))
    return {"valid": not runtime_required, "status": "RUNTIME_REQUIRED" if runtime_required else "STATIC_CHECKED", "evidence_kind": "STRUCTURE", "path": str(path.resolve()), "controls": len(controls), "screen_markers": len(soup.select("[data-screen-id]")), "self_contained_checked": self_contained, "interaction_verified": False, "visual_verified": False}


def main():
    parser = argparse.ArgumentParser(description="检查原型 HTML 结构与可选自包含要求")
    parser.add_argument("html", type=Path)
    parser.add_argument("--self-contained", action="store_true")
    args = parser.parse_args()
    result = validate(args.html.resolve(strict=True), args.self_contained)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["valid"] else 2)


if __name__ == "__main__":
    main()
