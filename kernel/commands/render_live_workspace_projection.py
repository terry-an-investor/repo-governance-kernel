#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from kernel.assemble_context import (
    extract_current_task_anchor,
    inspect_live_workspace,
    parse_h2_sections,
    read_text,
    render_live_workspace_projection,
)
from kernel.round_control import assert_anchor_maintenance_command_contract


ROOT = Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a non-durable live workspace projection from the current repo state.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--workspace-root")
    parser.add_argument("--output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    current_task_path = ROOT / "projects" / args.project_id / "current" / "current-task.md"
    current_task_sections = parse_h2_sections(read_text(current_task_path)) if current_task_path.exists() else {}
    anchor = extract_current_task_anchor(current_task_sections)
    if args.workspace_root:
        anchor["workspace_root"] = args.workspace_root

    live_workspace = inspect_live_workspace(anchor)
    if live_workspace.get("status") != "available":
        raise SystemExit(f"live workspace unavailable: {live_workspace}")
    assert_anchor_maintenance_command_contract(
        "render-live-workspace",
        provided_inputs={"project_id"},
    )

    projection = render_live_workspace_projection(
        project_id=args.project_id,
        live_workspace=live_workspace,
        workspace_id=anchor.get("workspace_id", ""),
        generated_at=datetime.now().astimezone().isoformat(timespec="seconds"),
    )

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = ROOT / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(projection, encoding="utf-8")
        print(f"rendered live workspace projection: {output_path}")
    else:
        print(projection, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

