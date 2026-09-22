import argparse
import csv
import json
from pathlib import Path

from PIL import Image


def require(condition, message):
    if not condition:
        raise ValueError(message)


def resolve_file(root, value, source_roots=()):
    require(bool(value.strip()), "清单路径不能为空")
    path = (root / value).resolve(strict=True)
    require(path.is_file() and any(path.is_relative_to(directory) for directory in (root, *source_roots)), f"清单文件需要位于交付目录或明确指定的来源目录：{value}")
    return path


def read_csv(path, columns):
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        require(columns <= set(reader.fieldnames or []), f"CSV 缺少必要字段：{path.name}")
        rows = list(reader)
    require(all(None not in row and all(value is not None for value in row.values()) for row in rows), f"CSV 列数不一致：{path.name}")
    return rows


def unique(rows, key):
    values = [row[key].strip() for row in rows]
    require(all(values) and len(values) == len(set(values)), f"清单存在重复或空 ID：{key}")
    return set(values)


def audit(root, mode="design", require_generated=False, source_roots=()):
    root = root.resolve(strict=True)
    require(root.is_dir(), "交付位置必须是目录")
    source_roots = tuple(path.resolve(strict=True) for path in source_roots)
    require(all(path.is_dir() for path in source_roots), "来源位置必须是实际目录")
    required = ["ui-audit.md"]
    if mode == "design":
        required += ["design-system.md", "tokens.json"]
    for name in required:
        resolve_file(root, name)
    maps = [root / name for name in ("route-design-map.csv", "screen-design-map.csv") if (root / name).exists()]
    require(len(maps) == 1, "需要一份明确的页面或屏幕映射")
    rows = read_csv(maps[0], {"source_id", "screen_id", "name", "source_type", "status", "artifact_path"})
    require(bool(rows), "屏幕映射不能为空")
    screens = unique(rows, "screen_id")
    for row in rows:
        require(row["source_id"].strip() and row["name"].strip(), "屏幕来源与名称不能为空")
        require(row["source_type"] in {"EXPLICIT", "INFERRED", "UNKNOWN"}, "屏幕来源类型无效")
        require(row["status"] in {"PLANNED", "CREATED", "OBSERVED", "VERIFIED", "BLOCKED", "NOT_APPLICABLE"}, "屏幕产物状态无效")
        if row["status"] in {"CREATED", "OBSERVED", "VERIFIED"}:
            resolve_file(root, row["artifact_path"], source_roots)
    token_path = root / "tokens.json"
    if token_path.exists():
        tokens = json.loads(token_path.read_text())
        require(isinstance(tokens, dict) and bool(tokens), "Token 必须是非空 JSON 对象")
    assets_path = root / "asset-manifest.csv"
    assets = read_csv(assets_path, {"asset_id", "file_path", "usage", "width", "height", "format", "transparency", "source"}) if assets_path.exists() else []
    asset_ids = unique(assets, "asset_id")
    for row in assets:
        path = resolve_file(root, row["file_path"], source_roots)
        require(row["source"].strip() and row["usage"].strip(), "资产需要真实来源和用途")
        if path.suffix.lower() in {".png", ".webp", ".jpg", ".jpeg", ".gif"}:
            with Image.open(path) as picture:
                require(picture.size == (int(row["width"]), int(row["height"])), f"图片尺寸与清单不一致：{row['asset_id']}")
                require(picture.format.lower() == row["format"].lower().replace("jpg", "jpeg"), f"图片格式与清单不一致：{row['asset_id']}")
                picture.verify()
    map_path = root / "page-asset-map.csv"
    links = read_csv(map_path, {"screen_id", "asset_id", "usage"}) if map_path.exists() else []
    require(not assets or bool(links), "存在资产时需要页面引用清单")
    for row in links:
        require(row["screen_id"] in screens and row["asset_id"] in asset_ids, "页面资产引用的 ID 不存在")
    generation_path = root / "image-generation-manifest.csv"
    generations = read_csv(generation_path, {"asset_id", "generation_tool", "prompt_summary", "source_image_path", "output_file_path"}) if generation_path.exists() else []
    unique(generations, "asset_id")
    require(not require_generated or bool(generations), "本次要求生成资产，但缺少来源记录")
    for row in generations:
        require(row["asset_id"] in asset_ids and row["generation_tool"].strip() and row["prompt_summary"].strip(), "生成资产记录不完整")
        for field in ("source_image_path", "output_file_path"):
            path = resolve_file(root, row[field], source_roots)
            with Image.open(path) as picture:
                picture.verify()
    return {"valid": True, "evidence_kind": "STRUCTURE", "mode": mode, "screens": len(rows), "assets": len(assets), "generated_assets": len(generations), "interaction_verified": False, "visual_verified": False}


def main():
    parser = argparse.ArgumentParser(description="核对 UI 交付范围、实际文件、引用和图片格式")
    parser.add_argument("delivery_root", type=Path)
    parser.add_argument("--mode", choices=["design", "audit", "implementation"], default="design")
    parser.add_argument("--require-generated", action="store_true")
    parser.add_argument("--source-root", type=Path, action="append", default=[])
    args = parser.parse_args()
    print(json.dumps(audit(args.delivery_root, args.mode, args.require_generated, args.source_root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
