#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from assemble_context import extract_current_task_anchor, inspect_live_workspace, parse_h2_sections, read_text
from round_control import assert_anchor_maintenance_command_contract, expected_current_task_control_values


ROOT = Path(__file__).resolve().parent.parent
CURRENT_STATE_SECTION = "Current State"


SECTION_RE = re.compile(r"^## (.+?)\r?$", re.MULTILINE)
BULLET_RE = re.compile(r"^(\s*-\s*)([^:]+):\s*(.+?)\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh the current-task control bullets and workspace locator fields."
    )
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


def update_or_insert_bullet(
    lines: list[str],
    label: str,
    value: str,
    *,
    insert_after: str | None = None,
    aliases: tuple[str, ...] = (),
) -> list[str]:
    rendered = f"- {label}: {format_code(value)}"
    accepted_labels = {label.lower(), *(alias.lower() for alias in aliases)}
    for index, line in enumerate(lines):
        match = BULLET_RE.match(line)
        if not match:
            continue
        current_label = match.group(2).strip().lower()
        if current_label in accepted_labels:
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


def remove_bullets(lines: list[str], labels: tuple[str, ...]) -> list[str]:
    blocked = {label.lower() for label in labels}
    filtered: list[str] = []
    for line in lines:
        match = BULLET_RE.match(line)
        if match and match.group(2).strip().lower() in blocked:
            continue
        filtered.append(line)
    return filtered


def refresh_current_state_section(
    section_text: str,
    workspace_root: str,
    control_values: dict[str, str],
) -> str:
    lines = section_text.splitlines()
    lines = remove_bullets(
        lines,
        (
            "Branch",
            "Branch observed at last refresh",
            "HEAD anchor",
            "HEAD observed at last refresh",
            "Worktree state",
            "Worktree observed at last refresh",
            "Changed path count",
            "Changed path count observed at last refresh",
            "Last anchor refresh",
        ),
    )

    lines = update_or_insert_bullet(lines, "Objective id", control_values.get("objective id", ""), insert_after="Project")
    lines = update_or_insert_bullet(
        lines,
        "Active round id",
        control_values.get("active round id", ""),
        insert_after="Objective id",
    )
    lines = update_or_insert_bullet(lines, "Phase", control_values.get("phase", ""), insert_after="Active round id")
    lines = update_or_insert_bullet(lines, "Workspace root", workspace_root, insert_after="Workspace id")
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
    control_values = expected_current_task_control_values(args.project_id)
    assert_anchor_maintenance_command_contract(
        "refresh-anchor",
        provided_inputs={"project_id"},
    )
    refreshed_current_state = refresh_current_state_section(current_state, workspace_root, control_values)
    updated_text = replace_h2_section(text, CURRENT_STATE_SECTION, refreshed_current_state)
    current_task_path.write_text(updated_text, encoding="utf-8")

    print(f"refreshed current-task anchor: {current_task_path}")
    print(f"objective_id={control_values.get('objective id', '')}")
    print(f"active_round_id={control_values.get('active round id', '')}")
    print(f"phase={control_values.get('phase', '')}")
    print(f"workspace_root={workspace_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
