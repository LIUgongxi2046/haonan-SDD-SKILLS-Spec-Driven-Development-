#!/usr/bin/env python3
"""Audit a haonan-s003-2-ui delivery package using only the standard library."""

from __future__ import annotations

import argparse
import csv
import json
import tempfile
from pathlib import Path


BASE_REQUIRED = (
    "assumptions-and-open-questions.md",
    "design-system.md",
    "tokens.json",
    "asset-manifest.csv",
    "page-asset-map.csv",
    "ui-audit.md",
)

MAP_HEADERS = {"source_id", "screen_id", "name", "source_type", "status", "artifact_path"}
ASSET_HEADERS = {
    "asset_id",
    "file_path",
    "usage",
    "width",
    "height",
    "format",
    "transparency",
    "source",
}
PAGE_ASSET_HEADERS = {"screen_id", "asset_id", "usage"}


def read_csv(path: Path, required_headers: set[str], errors: list[str]) -> list[dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            headers = set(reader.fieldnames or [])
            missing = sorted(required_headers - headers)
            if missing:
                errors.append(f"{path.name}: missing headers: {', '.join(missing)}")
            return list(reader)
    except (OSError, csv.Error) as exc:
        errors.append(f"{path.name}: cannot read CSV: {exc}")
        return []


def resolve_relative(root: Path, raw: str) -> Path | None:
    value = raw.strip()
    if not value:
        return None
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def audit(root: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        return {"ok": False, "errors": [f"Delivery root is not a directory: {root}"], "warnings": []}

    for name in BASE_REQUIRED:
        if not (root / name).is_file():
            errors.append(f"Missing required file: {name}")

    map_candidates = [root / "route-design-map.csv", root / "screen-design-map.csv"]
    map_path = next((path for path in map_candidates if path.is_file()), None)
    if map_path is None:
        errors.append("Missing route-design-map.csv or screen-design-map.csv")
        map_rows: list[dict[str, str]] = []
    else:
        map_rows = read_csv(map_path, MAP_HEADERS, errors)

    tokens_path = root / "tokens.json"
    if tokens_path.is_file():
        try:
            tokens = json.loads(tokens_path.read_text(encoding="utf-8"))
            if not isinstance(tokens, dict) or not tokens:
                errors.append("tokens.json: expected a non-empty JSON object")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"tokens.json: invalid JSON: {exc}")

    asset_rows = []
    asset_path = root / "asset-manifest.csv"
    if asset_path.is_file():
        asset_rows = read_csv(asset_path, ASSET_HEADERS, errors)

    page_asset_rows = []
    page_asset_path = root / "page-asset-map.csv"
    if page_asset_path.is_file():
        page_asset_rows = read_csv(page_asset_path, PAGE_ASSET_HEADERS, errors)

    complete_statuses = {"CREATED", "VERIFIED"}
    for index, row in enumerate(map_rows, start=2):
        status = (row.get("status") or "").strip().upper()
        artifact = resolve_relative(root, row.get("artifact_path") or "")
        if status in complete_statuses and artifact is None:
            errors.append(f"{map_path.name}:{index}: completed screen has no safe artifact_path")
        elif artifact is not None and not artifact.exists():
            errors.append(f"{map_path.name}:{index}: artifact not found: {row.get('artifact_path')}")

    asset_ids: set[str] = set()
    for index, row in enumerate(asset_rows, start=2):
        asset_id = (row.get("asset_id") or "").strip()
        if not asset_id:
            errors.append(f"asset-manifest.csv:{index}: empty asset_id")
        elif asset_id in asset_ids:
            errors.append(f"asset-manifest.csv:{index}: duplicate asset_id: {asset_id}")
        asset_ids.add(asset_id)

        asset_file = resolve_relative(root, row.get("file_path") or "")
        if asset_file is None:
            errors.append(f"asset-manifest.csv:{index}: empty or unsafe file_path")
        elif not asset_file.is_file():
            errors.append(f"asset-manifest.csv:{index}: file not found: {row.get('file_path')}")

    for index, row in enumerate(page_asset_rows, start=2):
        asset_id = (row.get("asset_id") or "").strip()
        if asset_id and asset_id not in asset_ids:
            errors.append(f"page-asset-map.csv:{index}: unknown asset_id: {asset_id}")

    if not map_rows:
        warnings.append("Screen map has no data rows")
    if not asset_rows:
        warnings.append("Asset manifest has no data rows")

    return {
        "ok": not errors,
        "root": str(root.resolve()),
        "screens": len(map_rows),
        "assets": len(asset_rows),
        "page_asset_links": len(page_asset_rows),
        "errors": errors,
        "warnings": warnings,
    }


def write_self_test_fixture(root: Path) -> None:
    (root / "screens").mkdir()
    (root / "assets").mkdir()
    (root / "screens" / "home.png").write_bytes(b"test")
    (root / "assets" / "hero.png").write_bytes(b"test")
    for name in ("assumptions-and-open-questions.md", "design-system.md", "ui-audit.md"):
        (root / name).write_text("# Test\n", encoding="utf-8")
    (root / "tokens.json").write_text('{"color":{"brand":{"primary":"#123456"}}}', encoding="utf-8")
    (root / "screen-design-map.csv").write_text(
        "source_id,screen_id,name,source_type,status,artifact_path\nP-1,home,Home,EXPLICIT,VERIFIED,screens/home.png\n",
        encoding="utf-8",
    )
    (root / "asset-manifest.csv").write_text(
        "asset_id,file_path,usage,width,height,format,transparency,source\nhero,assets/hero.png,hero,100,100,png,true,generated\n",
        encoding="utf-8",
    )
    (root / "page-asset-map.csv").write_text(
        "screen_id,asset_id,usage\nhome,hero,hero\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("delivery_root", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        with tempfile.TemporaryDirectory(prefix="haonan-ui-audit-") as temp_dir:
            root = Path(temp_dir)
            write_self_test_fixture(root)
            result = audit(root)
    elif args.delivery_root is not None:
        result = audit(args.delivery_root)
    else:
        parser.error("delivery_root is required unless --self-test is used")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
