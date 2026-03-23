#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

from assemble_context import extract_current_task_anchor, inspect_live_workspace, parse_h2_sections, read_text


ROOT = Path(__file__).resolve().parent.parent
CURRENT_STATE_SECTION = "Current State"


SECTION_RE = re.compile(r"^## (.+?)\r?$", re.MULTILINE)
BULLET_RE = re.compile(r"^(\s*-\s*)([^:]+):\s*(.+?)\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh the current-task anchor bullets from the live workspace.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--workspace-root")
    return parser.parse_args()


def replace_h2_section(text: str, section_name: str, new_body: str) -> str:
    matches = list(SECTION_RE.finditer(text))
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        if title != section_name:
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        replacement = f"\n\n{new_body.strip()}\n\n"
        return text[:start] + replacement + text[end:]
    raise RuntimeError(f"missing section: {section_name}")


def format_code(value: str) -> str:
    return f"`{value}`" if value else "``"


def update_or_insert_bullet(lines: list[str], label: str, value: str, *, insert_after: str | None = None) -> list[str]:
    rendered = f"- {label}: {format_code(value)}"
    for index, line in enumerate(lines):
        match = BULLET_RE.match(line)
        if not match:
            continue
        current_label = match.group(2).strip().lower()
        if current_label == label.lower():
            lines[index] = rendered
            return lines

    if insert_after:
        for index, line in enumerate(lines):
            match = BULLET_RE.match(line)
            if not match:
                continue
            current_label = match.group(2).strip().lower()
            if current_label == insert_after.lower():
                lines.insert(index + 1, rendered)
                return lines

    insert_index = 0
    for index, line in enumerate(lines):
        if BULLET_RE.match(line):
            insert_index = index + 1
    lines.insert(insert_index, rendered)
    return lines


def refresh_current_state_section(section_text: str, live_workspace: dict[str, str], workspace_root: str) -> str:
    lines = section_text.splitlines()
    refreshed_at = datetime.now().astimezone().isoformat(timespec="seconds")

    lines = update_or_insert_bullet(lines, "Workspace root", workspace_root, insert_after="Workspace id")
    lines = update_or_insert_bullet(lines, "Branch", live_workspace.get("branch", ""), insert_after="Workspace root")
    lines = update_or_insert_bullet(lines, "HEAD anchor", live_workspace.get("git_sha", ""), insert_after="Branch")
    lines = update_or_insert_bullet(
        lines,
        "Worktree state",
        live_workspace.get("worktree_state", ""),
        insert_after="HEAD anchor",
    )
    lines = update_or_insert_bullet(
        lines,
        "Changed path count",
        live_workspace.get("changed_path_count", ""),
        insert_after="Worktree state",
    )
    lines = update_or_insert_bullet(
        lines,
        "Last anchor refresh",
        refreshed_at,
        insert_after="Changed path count",
    )
    return "\n".join(lines).strip()


def main() -> int:
    args = parse_args()
    project_dir = ROOT / "projects" / args.project_id
    current_task_path = project_dir / "current" / "current-task.md"
    if not current_task_path.exists():
        raise SystemExit(f"missing current-task file: {current_task_path}")

    text = read_text(current_task_path)
    sections = parse_h2_sections(text)
    current_state = sections.get(CURRENT_STATE_SECTION, "")
    if not current_state:
        raise SystemExit(f"missing `{CURRENT_STATE_SECTION}` section in {current_task_path}")

    anchor = extract_current_task_anchor(sections)
    if args.workspace_root:
        anchor["workspace_root"] = args.workspace_root
    live_workspace = inspect_live_workspace(anchor)
    if live_workspace.get("status") != "available":
        raise SystemExit(f"live workspace unavailable: {live_workspace}")

    workspace_root = args.workspace_root or anchor.get("workspace_root") or live_workspace.get("workspace_root", "")
    refreshed_current_state = refresh_current_state_section(current_state, live_workspace, workspace_root)
    updated_text = replace_h2_section(text, CURRENT_STATE_SECTION, refreshed_current_state)
    current_task_path.write_text(updated_text, encoding="utf-8")

    print(f"refreshed current-task anchor: {current_task_path}")
    print(f"branch={live_workspace.get('branch', '')}")
    print(f"git_sha={live_workspace.get('git_sha', '')}")
    print(f"worktree_state={live_workspace.get('worktree_state', '')}")
    print(f"changed_path_count={live_workspace.get('changed_path_count', '')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
