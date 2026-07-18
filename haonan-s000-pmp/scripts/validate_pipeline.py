#!/usr/bin/env python3
"""Validate the Haonan S000-S012 Codex skill suite using the standard library."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


EXPECTED = (
    "haonan-s000-pmp",
    "haonan-s001-ceo-strategy",
    "haonan-s002-prd",
    "haonan-s003-1-prototype",
    "haonan-s003-2-ui",
    "haonan-s004-hld",
    "haonan-s005-1-lld-data",
    "haonan-s005-2-lld-back",
    "haonan-s005-3-lld-agent",
    "haonan-s005-4-lld-front",
    "haonan-s006-review",
    "haonan-s007-planner",
    "haonan-s008-coder",
    "haonan-s009-test",
    "haonan-s010-safety",
    "haonan-s011-devops",
    "haonan-s012-docs",
)

DISALLOWED_TEXT = (
    "AskUserQuestion",
    "capture_local_screenshot",
    "Web_Search",
    '"A".repeat(',
    "url: [http",
)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields, text[end + 5 :]


def relative_markdown_links(body: str) -> list[str]:
    links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", body)
    return [
        link.split("#", 1)[0]
        for link in links
        if link and not link.startswith(("http://", "https://", "#", "/"))
    ]


def validate(root: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    checked: list[str] = []

    for name in EXPECTED:
        skill_dir = root / name
        skill_file = skill_dir / "SKILL.md"
        agent_file = skill_dir / "agents" / "openai.yaml"
        if not skill_file.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue
        checked.append(name)
        text = skill_file.read_text(encoding="utf-8")
        parsed = parse_frontmatter(text)
        if parsed is None:
            errors.append(f"{name}: invalid frontmatter")
            continue
        fields, body = parsed
        if set(fields) != {"name", "description"}:
            errors.append(f"{name}: frontmatter keys must be name and description only")
        if fields.get("name") != name:
            errors.append(f"{name}: frontmatter name mismatch: {fields.get('name')}")
        if "Use when" not in fields.get("description", ""):
            errors.append(f"{name}: description must include Use when trigger boundary")
        if len(text.splitlines()) > 500:
            errors.append(f"{name}: SKILL.md exceeds 500 lines")
        if sum(1 for line in body.splitlines() if line.lstrip().startswith("```")) % 2:
            errors.append(f"{name}: unbalanced fenced code block")
        for needle in DISALLOWED_TEXT:
            if needle in text:
                errors.append(f"{name}: contains disallowed legacy text: {needle}")
        for link in relative_markdown_links(body):
            if not (skill_dir / link).exists():
                errors.append(f"{name}: missing linked resource: {link}")

        if not agent_file.is_file():
            errors.append(f"{name}: missing agents/openai.yaml")
            continue
        agent = agent_file.read_text(encoding="utf-8")
        if f"$${name}" in agent or f"${name}" not in agent:
            errors.append(f"{name}: default_prompt must mention ${name}")
        expected_implicit = "true" if name == "haonan-s000-pmp" else "false"
        if f"allow_implicit_invocation: {expected_implicit}" not in agent:
            errors.append(f"{name}: implicit invocation should be {expected_implicit}")
        values: dict[str, str] = {}
        for key in ("display_name", "short_description", "default_prompt"):
            match = re.search(rf"^\s*{key}:\s*(.+)$", agent, re.MULTILINE)
            if not match or not (match.group(1).startswith('"') and match.group(1).endswith('"')):
                errors.append(f"{name}: {key} must be a quoted string")
            elif match:
                values[key] = match.group(1)[1:-1]
        short = values.get("short_description", "")
        if short and not 25 <= len(short) <= 64:
            errors.append(f"{name}: short_description must be 25-64 characters, got {len(short)}")

    router = root / "haonan-s000-pmp" / "SKILL.md"
    if router.is_file():
        router_text = router.read_text(encoding="utf-8")
        for name in EXPECTED[1:]:
            if f"${name}" not in router_text:
                errors.append(f"haonan-s000-pmp: route table missing ${name}")

    unexpected = sorted(
        path.name for path in root.glob("haonan-s0*") if path.is_dir() and path.name not in EXPECTED
    )
    if unexpected:
        warnings.append("Unexpected similarly named directories: " + ", ".join(unexpected))

    return {
        "ok": not errors,
        "root": str(root.resolve()),
        "expected": len(EXPECTED),
        "checked": len(checked),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "skills_root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Directory containing the haonan-s* skill folders",
    )
    args = parser.parse_args()
    result = validate(args.skills_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
