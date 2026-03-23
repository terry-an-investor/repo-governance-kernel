#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from audit_control_state import audit_project_control_state
from round_control import load_all_adjudications, parse_bullet_list, project_dir


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


def maybe_execute_open_round(args: argparse.Namespace) -> tuple[bool, str]:
    required_present = all(
        [
            (args.round_title or "").strip(),
            bool([item for item in args.round_scope_item if item.strip()]),
            (args.round_deliverable or "").strip(),
            (args.round_validation_plan or "").strip(),
        ]
    )
    if not required_present:
        return False, "missing explicit round bootstrap inputs"

    cmd = [
        sys.executable,
        str(SCRIPTS / "open_round.py"),
        "--project-id",
        args.project_id,
        "--title",
        args.round_title.strip(),
        "--deliverable",
        args.round_deliverable.strip(),
        "--validation-plan",
        args.round_validation_plan.strip(),
    ]
    for item in args.round_scope_item:
        if item.strip():
            cmd.extend(["--scope-item", item.strip()])
    for item in args.round_scope_path:
        if item.strip():
            cmd.extend(["--scope-path", item.strip()])
    for item in args.round_risk:
        if item.strip():
            cmd.extend(["--risk", item.strip()])
    for item in args.round_blocker:
        if item.strip():
            cmd.extend(["--blocker", item.strip()])
    if args.round_status_note.strip():
        cmd.extend(["--status-note", args.round_status_note.strip()])

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
            success, detail = maybe_execute_open_round(args)
            if success:
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
