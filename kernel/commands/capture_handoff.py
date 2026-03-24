#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh current-task control state, render a live workspace projection, create a snapshot, and assemble a packet."
    )
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--slug")
    parser.add_argument("--title")
    parser.add_argument("--memory-limit", type=int, default=10)
    parser.add_argument("--artifact-dir")
    parser.add_argument("--workspace-root")
    return parser.parse_args()


def run_script(script_name: str, script_args: list[str]) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(SCRIPTS / script_name), *script_args]
    return subprocess.run(
        command,
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    args = parse_args()
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    slug = args.slug or f"handoff-{timestamp}"

    if args.artifact_dir:
        artifact_dir = Path(args.artifact_dir)
        if not artifact_dir.is_absolute():
            artifact_dir = ROOT / artifact_dir
    else:
        artifact_dir = ROOT / "artifacts" / args.project_id / "handoff-captures" / slug
    artifact_dir.mkdir(parents=True, exist_ok=True)

    refresh_args = ["--project-id", args.project_id]
    if args.workspace_root:
        refresh_args.extend(["--workspace-root", args.workspace_root])
    refresh = run_script("refresh_current_task_anchor.py", refresh_args)
    if refresh.returncode != 0:
        sys.stderr.write(refresh.stderr or refresh.stdout)
        return refresh.returncode
    (artifact_dir / "refresh.log").write_text(refresh.stdout, encoding="utf-8")

    live_workspace_path = artifact_dir / "live-workspace.md"
    live_workspace_args = ["--project-id", args.project_id, "--output", str(live_workspace_path)]
    if args.workspace_root:
        live_workspace_args.extend(["--workspace-root", args.workspace_root])
    live_workspace = run_script("render_live_workspace_projection.py", live_workspace_args)
    if live_workspace.returncode != 0:
        sys.stderr.write(live_workspace.stderr or live_workspace.stdout)
        return live_workspace.returncode
    (artifact_dir / "live-workspace.log").write_text(live_workspace.stdout, encoding="utf-8")

    snapshot_path = artifact_dir / "snapshot.md"
    snapshot_args = [
        "--project-id",
        args.project_id,
        "--slug",
        slug,
        "--output",
        str(snapshot_path),
    ]
    if args.title:
        snapshot_args.extend(["--title", args.title])
    snapshot = run_script("create_snapshot.py", snapshot_args)
    if snapshot.returncode != 0:
        sys.stderr.write(snapshot.stderr or snapshot.stdout)
        return snapshot.returncode
    (artifact_dir / "snapshot.log").write_text(snapshot.stdout, encoding="utf-8")

    packet_path = artifact_dir / "session-context.md"
    assemble_args = [
        "--project-id",
        args.project_id,
        "--memory-limit",
        str(args.memory_limit),
        "--output",
        str(packet_path),
    ]
    assembled = run_script("assemble_context.py", assemble_args)
    if assembled.returncode != 0:
        sys.stderr.write(assembled.stderr or assembled.stdout)
        return assembled.returncode
    (artifact_dir / "assemble.log").write_text(assembled.stdout, encoding="utf-8")

    summary_lines = [
        f"captured handoff: {artifact_dir}",
        f"live workspace: {live_workspace_path}",
        f"snapshot: {snapshot_path}",
        f"packet: {packet_path}",
    ]
    summary = "\n".join(summary_lines) + "\n"
    (artifact_dir / "summary.txt").write_text(summary, encoding="utf-8")
    sys.stdout.write(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

