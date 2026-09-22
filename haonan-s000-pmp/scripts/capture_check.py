import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(paths):
    result = []
    for value in paths:
        path = Path(value).resolve(strict=True)
        if not path.is_file():
            raise ValueError(f"检查输入必须是文件：{path}")
        result.append({"path": str(path), "sha256": digest(path)})
    return result


def run_check(args):
    cwd = args.cwd.resolve(strict=True)
    if not cwd.is_dir() or not args.command:
        raise ValueError("需要有效工作目录和执行命令")
    command = args.command[1:] if args.command[0] == "--" else args.command
    if not command:
        raise ValueError("执行命令不能为空")
    inputs = snapshot([cwd / Path(path) for path in args.input])
    root = args.output_dir.resolve()
    root.mkdir(parents=True, exist_ok=False)
    output_path = root / "output.log"
    started_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with output_path.open("wb") as stream:
        completed = subprocess.run(command, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT, timeout=args.timeout, check=False)
    unchanged = all(digest(Path(item["path"])) == item["sha256"] for item in inputs)
    artifacts = snapshot([output_path] + [cwd / path for path in args.artifact])
    receipt = {
        "schema_version": 1,
        "captured_by": "haonan-s000-capture-check/v1",
        "check_id": args.check_id,
        "kind": args.kind,
        "baseline_id": args.baseline_id,
        "cwd": str(cwd),
        "command": command,
        "started_at": started_at,
        "ended_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "exit_code": completed.returncode,
        "inputs_unchanged": unchanged,
        "inputs": inputs,
        "artifacts": artifacts,
    }
    receipt_path = root / "receipt.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    result = {"receipt_path": str(receipt_path), "receipt_sha256": digest(receipt_path), "exit_code": completed.returncode, "inputs_unchanged": unchanged}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if completed.returncode == 0 and unchanged else 1


def main():
    parser = argparse.ArgumentParser(description="执行真实检查并保存原始结果与版本证据")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--check-id", required=True)
    parser.add_argument("--kind", required=True, choices=["STRUCTURE", "STATIC", "UNIT", "API", "SECURITY", "BUSINESS", "INTEGRATION", "EXTERNAL", "EVAL", "VISUAL"])
    parser.add_argument("--baseline-id", required=True)
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("--input", action="append", required=True)
    parser.add_argument("--artifact", action="append", type=Path, default=[])
    parser.add_argument("--timeout", type=float, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("执行时限必须大于零")
    raise SystemExit(run_check(args))


if __name__ == "__main__":
    main()
