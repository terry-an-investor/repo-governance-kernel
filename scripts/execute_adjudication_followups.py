#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from audit_control_state import audit_project_control_state
from round_control import load_all_adjudications, parse_bullet_list, project_dir, select_open_round_record


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute the safe automatic portion of adjudication follow-ups.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--adjudication-id")
    parser.add_argument("--round-title")
    parser.add_argument("--round-scope-item", action="append", default=[])
    parser.add_argument("--round-scope-path", action="append", default=[])
    parser.add_argument("--round-deliverable")
    parser.add_argument("--round-validation-plan")
    parser.add_argument("--round-risk", action="append", default=[])
    parser.add_argument("--round-blocker", action="append", default=[])
    parser.add_argument("--round-status-note", default="")
    return parser.parse_args()


def select_adjudication_record(project_id: str, adjudication_id: str | None) -> tuple[Path, dict[str, object], dict[str, str]]:
    records = load_all_adjudications(project_id)
    if not records:
        raise SystemExit(f"no adjudication records found for project `{project_id}`")
    if adjudication_id:
        for record in records:
            _path, meta, _sections = record
            if str(meta.get("id") or "").strip() == adjudication_id.strip():
                return record
        raise SystemExit(f"adjudication `{adjudication_id}` not found for project `{project_id}`")
    return records[0]


def scaffold_constitution(path: Path, adjudication_id: str) -> None:
    text = "\n".join(
        [
            "# Constitution",
            "",
            f"Scaffolded from adjudication `{adjudication_id}`.",
            "Replace placeholders with real project law before treating this file as authoritative governance.",
            "",
            "## Product Boundaries",
            "",
            "_pending authoring_",
            "",
            "## Architecture Invariants",
            "",
            "_pending authoring_",
            "",
            "## Quality Bar",
            "",
            "_pending authoring_",
            "",
            "## Validation Rules",
            "",
            "_pending authoring_",
            "",
            "## Forbidden Shortcuts",
            "",
            "_pending authoring_",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def scaffold_exception_ledger(path: Path) -> None:
    text = "\n".join(
        [
            "# Exception Ledger",
            "",
            "## Active",
            "",
            "- None recorded yet.",
            "",
            "## Retired",
            "",
            "- None recorded yet.",
            "",
            "## Invalidated By Pivot",
            "",
            "- None recorded yet.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def resolve_round_bootstrap(
    args: argparse.Namespace,
    adjudication_meta: dict[str, object],
) -> dict[str, object]:
    cli_scope_items = [item.strip() for item in args.round_scope_item if item.strip()]
    cli_scope_paths = [item.strip() for item in args.round_scope_path if item.strip()]
    cli_risks = [item.strip() for item in args.round_risk if item.strip()]
    cli_blockers = [item.strip() for item in args.round_blocker if item.strip()]
    return {
        "title": (args.round_title or "").strip() or str(adjudication_meta.get("round_title") or "").strip(),
        "scope_items": cli_scope_items or [str(item).strip() for item in adjudication_meta.get("round_scope_items", []) if str(item).strip()],
        "scope_paths": cli_scope_paths or [str(item).strip() for item in adjudication_meta.get("round_scope_paths", []) if str(item).strip()],
        "deliverable": (args.round_deliverable or "").strip() or str(adjudication_meta.get("round_deliverable") or "").strip(),
        "validation_plan": (args.round_validation_plan or "").strip() or str(adjudication_meta.get("round_validation_plan") or "").strip(),
        "risks": cli_risks or [str(item).strip() for item in adjudication_meta.get("round_risks", []) if str(item).strip()],
        "blockers": cli_blockers or [str(item).strip() for item in adjudication_meta.get("round_blockers", []) if str(item).strip()],
        "status_note": (args.round_status_note or "").strip() or str(adjudication_meta.get("round_status_note") or "").strip(),
    }


def maybe_execute_open_round(args: argparse.Namespace, adjudication_meta: dict[str, object]) -> tuple[bool, str]:
    bootstrap = resolve_round_bootstrap(args, adjudication_meta)
    open_round_record, open_round_issues = select_open_round_record(args.project_id)
    if open_round_issues:
        return False, "; ".join(open_round_issues)
    if open_round_record is not None:
        _path, round_meta, _sections = open_round_record
        open_round_id = str(round_meta.get("id") or "").strip()
        open_round_objective_id = str(round_meta.get("objective_id") or "").strip()
        adjudication_objective_id = str(adjudication_meta.get("objective_id") or "").strip()
        if adjudication_objective_id and open_round_objective_id == adjudication_objective_id:
            return True, f"open round `{open_round_id}` already exists for objective `{adjudication_objective_id}`"
        return False, f"open round `{open_round_id}` already exists for a different objective `{open_round_objective_id}`"

    required_present = all(
        [
            str(bootstrap["title"]).strip(),
            bool([item for item in bootstrap["scope_items"] if str(item).strip()]),
            str(bootstrap["deliverable"]).strip(),
            str(bootstrap["validation_plan"]).strip(),
        ]
    )
    if not required_present:
        return False, "missing structured round bootstrap inputs in adjudication or CLI"

    cmd = [
        sys.executable,
        str(SCRIPTS / "open_round.py"),
        "--project-id",
        args.project_id,
        "--title",
        str(bootstrap["title"]).strip(),
        "--deliverable",
        str(bootstrap["deliverable"]).strip(),
        "--validation-plan",
        str(bootstrap["validation_plan"]).strip(),
    ]
    for item in bootstrap["scope_items"]:
        if str(item).strip():
            cmd.extend(["--scope-item", str(item).strip()])
    for item in bootstrap["scope_paths"]:
        if str(item).strip():
            cmd.extend(["--scope-path", str(item).strip()])
    for item in bootstrap["risks"]:
        if str(item).strip():
            cmd.extend(["--risk", str(item).strip()])
    for item in bootstrap["blockers"]:
        if str(item).strip():
            cmd.extend(["--blocker", str(item).strip()])
    if str(bootstrap["status_note"]).strip():
        cmd.extend(["--status-note", str(bootstrap["status_note"]).strip()])

    completed = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return False, completed.stderr.strip() or completed.stdout.strip() or "open-round failed"
    return True, completed.stdout.strip()


def main() -> int:
    args = parse_args()
    project_path = project_dir(args.project_id)
    if not project_path.exists():
        raise SystemExit(f"project directory not found: {project_path}")

    adjudication_path, adjudication_meta, adjudication_sections = select_adjudication_record(args.project_id, args.adjudication_id)
    adjudication_id = str(adjudication_meta.get("id") or adjudication_path.stem).strip()
    followups = parse_bullet_list(adjudication_sections.get("Required Follow-Up Transitions", ""))
    if not followups:
        raise SystemExit(f"adjudication `{adjudication_id}` has no follow-up transitions")

    applied: list[str] = []
    noop: list[str] = []
    blocked: list[str] = []

    for followup in followups:
        normalized = " ".join(followup.strip().lower().split())
        if "control/constitution.md" in normalized:
            constitution_path = project_path / "control" / "constitution.md"
            if constitution_path.exists():
                noop.append(f"`{followup}` -> constitution already exists")
            else:
                scaffold_constitution(constitution_path, adjudication_id)
                applied.append(f"`{followup}` -> created `{constitution_path.relative_to(ROOT).as_posix()}`")
            continue

        if "control/exception-ledger.md" in normalized:
            ledger_path = project_path / "control" / "exception-ledger.md"
            if ledger_path.exists():
                noop.append(f"`{followup}` -> exception ledger already exists")
            else:
                scaffold_exception_ledger(ledger_path)
                applied.append(f"`{followup}` -> created `{ledger_path.relative_to(ROOT).as_posix()}`")
            continue

        if "open one bounded round" in normalized or "open a bounded round" in normalized:
            success, detail = maybe_execute_open_round(args, adjudication_meta)
            if success:
                if "already exists" in detail:
                    noop.append(f"`{followup}` -> {detail}")
                else:
                    applied.append(f"`{followup}` -> executed open-round")
            else:
                blocked.append(f"`{followup}` -> {detail}")
            continue

        if "rerun audit-control-state" in normalized:
            continue

        blocked.append(f"`{followup}` -> no automatic executor is defined for this follow-up")

    audit_after = audit_project_control_state(args.project_id)
    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "adjudication_id": adjudication_id,
                "adjudication_path": str(adjudication_path),
                "applied": applied,
                "noop": noop,
                "blocked": blocked,
                "audit_after": audit_after,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
