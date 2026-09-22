import argparse
from graphlib import TopologicalSorter
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator


def require(condition, code, detail):
    if not condition:
        raise ValueError(f"{code}: {detail}")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unique_index(items, label):
    result = {item["id"]: item for item in items}
    require(len(result) == len(items), "DUPLICATE_ID", label)
    return result


def verify_receipt(evidence, baseline, root):
    path = (root / evidence["receipt_path"]).resolve(strict=True)
    require(digest(path) == evidence["receipt_sha256"], "RECEIPT_CHANGED", evidence["id"])
    receipt = json.loads(path.read_text())
    require(receipt["schema_version"] == 1 and receipt["captured_by"] == "haonan-s000-capture-check/v1", "RECEIPT_FORMAT", evidence["id"])
    for field in ("check_id", "kind", "baseline_id"):
        require(receipt[field] == evidence[field], "EVIDENCE_BINDING", f"{evidence['id']} {field}")
    require(evidence["baseline_id"] == baseline["id"], "STALE_BASELINE", evidence["id"])
    require(type(receipt["exit_code"]) is int and receipt["exit_code"] == 0, "CHECK_FAILED", evidence["id"])
    require(receipt["inputs_unchanged"] is True, "INPUT_CHANGED_DURING_RUN", evidence["id"])
    require(receipt["command"] and receipt["inputs"] and receipt["artifacts"], "MISSING_EXECUTION", evidence["id"])
    environment = (root / baseline["environment_ref"]).resolve(strict=True)
    require(any(Path(item["path"]).resolve(strict=True) == environment for item in receipt["inputs"]), "UNBOUND_ENVIRONMENT", evidence["id"])
    for item in receipt["inputs"] + receipt["artifacts"]:
        file = Path(item["path"]).resolve(strict=True)
        require(file.is_file() and digest(file) == item["sha256"], "STALE_FILE", str(file))
    return receipt


def validate(path, require_complete=False):
    data = json.loads(path.read_text())
    schema_path = Path(__file__).resolve().parent.parent / "references/delivery-ledger.schema.json"
    schema = json.loads(schema_path.read_text())
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(data)
    environment = (path.parent / data["baseline"]["environment_ref"]).resolve(strict=True)
    require(environment.is_file(), "MISSING_ENVIRONMENT", str(environment))
    commitments = unique_index(data["commitments"], "commitments")
    acceptances = unique_index(data["acceptances"], "acceptances")
    tasks = unique_index(data["tasks"], "tasks")
    evidence = unique_index(data["evidence"], "evidence")
    for commitment in commitments.values():
        for aid in commitment["acceptance_ids"]:
            require(aid in acceptances, "MISSING_ACCEPTANCE", aid)
            require(acceptances[aid]["commitment_id"] == commitment["id"], "COMMITMENT_BINDING", aid)
    covered = set()
    for task in tasks.values():
        for aid in task["acceptance_ids"]:
            require(aid in acceptances, "UNKNOWN_ACCEPTANCE", aid)
            covered.add(aid)
        for dependency in task["depends_on"]:
            require(dependency in tasks, "UNKNOWN_DEPENDENCY", dependency)
        if task["state"] == "ACCEPTED":
            require(not task["blockers"], "ACCEPTED_WITH_BLOCKERS", task["id"])
            require(all(acceptances[aid]["status"] == "PASS" for aid in task["acceptance_ids"]), "UNVERIFIED_TASK", task["id"])
            require(all(tasks[tid]["state"] == "ACCEPTED" for tid in task["depends_on"]), "INCOMPLETE_DEPENDENCY", task["id"])
    list(TopologicalSorter({tid: task["depends_on"] for tid, task in tasks.items()}).static_order())
    receipts = {}
    for acceptance in acceptances.values():
        aid = acceptance["id"]
        cid = acceptance["commitment_id"]
        require(cid in commitments, "UNKNOWN_COMMITMENT", cid)
        require(commitments[cid]["disposition"] == "IN_SCOPE" and aid in commitments[cid]["acceptance_ids"], "ORPHAN_ACCEPTANCE", aid)
        require(aid in covered, "UNCOVERED_ACCEPTANCE", aid)
        checks = unique_index(acceptance["required_checks"], aid)
        kinds = {check["kind"] for check in checks.values()}
        if acceptance["outcome_type"] == "BUSINESS":
            require(bool(kinds & {"BUSINESS", "INTEGRATION"}), "MISSING_BUSINESS_CHECK", aid)
        if acceptance["outcome_type"] == "EXTERNAL":
            require("EXTERNAL" in kinds and acceptance["capability"] == "REAL", "MISSING_EXTERNAL_CHECK", aid)
        if acceptance["consumer"]["required"]:
            check_id = acceptance["consumer"]["check_id"]
            require(check_id in checks, "MISSING_CONSUMER_CHECK", aid)
            require(checks[check_id]["kind"] in {"BUSINESS", "INTEGRATION", "EXTERNAL"}, "CONSUMER_CHECK_KIND", aid)
        observed = set()
        for eid in acceptance["evidence_ids"]:
            require(eid in evidence, "UNKNOWN_EVIDENCE", eid)
            item = evidence[eid]
            require(item["check_id"] in checks, "UNRELATED_EVIDENCE", eid)
            require(item["kind"] == checks[item["check_id"]]["kind"], "CHECK_KIND_MISMATCH", eid)
            if acceptance["status"] == "PASS":
                if eid not in receipts:
                    receipts[eid] = verify_receipt(item, data["baseline"], path.parent)
                observed.add(item["check_id"])
        if acceptance["status"] == "PASS":
            require(set(checks) <= observed, "MISSING_CHECK_EVIDENCE", aid)
    pending = {tid for tid, task in tasks.items() if task["state"] != "ACCEPTED"}
    continuation = data["continuation"]
    require(set(continuation["remaining_task_ids"]) == pending, "LOST_PENDING_TASKS", sorted(pending))
    next_id = continuation["next_task_id"]
    ready = {tid for tid in pending if tasks[tid]["state"] != "BLOCKED" and not tasks[tid]["blockers"] and all(tasks[dep]["state"] == "ACCEPTED" for dep in tasks[tid]["depends_on"])}
    if next_id is not None:
        require(next_id in ready, "NEXT_TASK_NOT_READY", next_id)
    if continuation["mode"] == "AUTHORIZED_BACKLOG":
        require(bool(continuation["authorization_refs"]), "MISSING_AUTHORIZATION", "continuation")
        require(not ready or next_id in ready, "MISSING_NEXT_TASK", sorted(ready))
    if require_complete:
        require(not pending and all(a["status"] == "PASS" for a in acceptances.values()), "DELIVERY_INCOMPLETE", sorted(pending))
    return {"valid": True, "complete": not pending and all(a["status"] == "PASS" for a in acceptances.values()), "commitments": len(commitments), "acceptances": len(acceptances), "tasks": len(tasks), "pending_tasks": sorted(pending), "verified_receipts": len(receipts)}


def main():
    parser = argparse.ArgumentParser(description="核对完整覆盖、任务状态和真实执行证据")
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    print(json.dumps(validate(args.ledger.resolve(strict=True), args.require_complete), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
