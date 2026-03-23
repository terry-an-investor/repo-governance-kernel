#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

from assemble_context import (
    extract_current_task_anchor,
    extract_frontmatter_scalars,
    inspect_live_workspace,
    latest_snapshot,
    parse_h2_sections,
    read_text,
)


ROOT = Path(__file__).resolve().parent.parent
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a project snapshot from current-task state.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title")
    parser.add_argument("--output")
    return parser.parse_args()


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def clean_section_markdown(text: str) -> str:
    return text.strip() if text.strip() else "_none recorded_"


def parse_frontmatter_block(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    return extract_frontmatter_scalars(text, ["id", "title", "project_id", "workspace_id", "workspace_root", "branch", "git_sha"])


def build_snapshot_frontmatter(
    *,
    project_id: str,
    title: str,
    slug: str,
    anchor: dict[str, str],
    paths: list[str],
) -> str:
    timestamp = datetime.now().astimezone()
    snapshot_id = f"snap-{timestamp.strftime('%Y-%m-%d-%H%M')}-{slug}"
    lines = [
        "---",
        f"id: {snapshot_id}",
        "type: handoff",
        f"title: {yaml_quote(title)}",
        f"project_id: {project_id}",
        f"workspace_id: {anchor.get('workspace_id', '')}",
        f"workspace_root: {anchor.get('workspace_root', '')}",
        f"branch: {anchor.get('branch', '')}",
        f"git_sha: {anchor.get('git_sha', '')}",
        "paths:",
    ]
    if paths:
        for path in paths:
            lines.append(f"  - {path}")
    else:
        lines.append("  - .")
    lines.extend(
        [
            "thread_ids: []",
            f"created_at: {timestamp.isoformat(timespec='seconds')}",
            f"updated_at: {timestamp.isoformat(timespec='seconds')}",
            "tags:",
            "  - handoff",
            f"  - {project_id}",
            f"  - {slug}",
            "---",
            "",
        ]
    )
    return "\n".join(lines)


def render_blockers(blocker_sections: dict[str, str]) -> str:
    parts: list[str] = []
    for name in ["Active", "Waiting", "Cleared"]:
        body = blocker_sections.get(name, "").strip()
        if not body:
            continue
        parts.append(f"### {name}\n\n{body}")
    return "\n\n".join(parts).strip() or "_none recorded_"


def main() -> int:
    args = parse_args()
    project_dir = ROOT / "projects" / args.project_id
    current_task_path = project_dir / "current" / "current-task.md"
    blockers_path = project_dir / "current" / "blockers.md"
    snapshot_seed_path = latest_snapshot(project_dir)

    if not current_task_path.exists():
        raise SystemExit(f"missing current-task file: {current_task_path}")

    current_task_text = read_text(current_task_path)
    current_task_sections = parse_h2_sections(current_task_text)
    blocker_sections = parse_h2_sections(read_text(blockers_path)) if blockers_path.exists() else {}
    snapshot_seed_sections = parse_h2_sections(read_text(snapshot_seed_path)) if snapshot_seed_path else {}
    current_task_anchor = extract_current_task_anchor(current_task_sections)
    snapshot_seed_frontmatter = parse_frontmatter_block(read_text(snapshot_seed_path)) if snapshot_seed_path else {}
    anchor = dict(snapshot_seed_frontmatter)
    for key, value in current_task_anchor.items():
        if value:
            anchor[key] = value
    live_workspace = inspect_live_workspace(anchor)
    if live_workspace.get("status") == "available":
        anchor["workspace_root"] = live_workspace.get("workspace_root", anchor.get("workspace_root", ""))
        anchor["branch"] = live_workspace.get("branch", anchor.get("branch", ""))
        anchor["git_sha"] = live_workspace.get("git_sha", anchor.get("git_sha", ""))

    title = args.title or f"{args.project_id} snapshot {args.slug.replace('-', ' ')}"
    important_files = current_task_sections.get("Important Files", "")
    paths = [line.split("`")[1] for line in important_files.splitlines() if line.strip().startswith("- `") and "`" in line]
    relative_paths: list[str] = []
    workspace_root = anchor.get("workspace_root", "")
    for path in paths:
        if workspace_root and path.startswith(workspace_root):
            relative = path.removeprefix(workspace_root).lstrip("/").replace("\\", "/")
            relative_paths.append(relative or ".")
        else:
            relative_paths.append(path.replace("\\", "/"))

    frontmatter = build_snapshot_frontmatter(
        project_id=args.project_id,
        title=title,
        slug=args.slug,
        anchor=anchor,
        paths=relative_paths[:12],
    )

    sections = [
        ("Goal", current_task_sections.get("Goal", "")),
        ("Completed Work", snapshot_seed_sections.get("Completed Work", "")),
        ("Validated Facts", current_task_sections.get("Validated Facts", "")),
        ("Rejected Approaches", snapshot_seed_sections.get("Rejected Approaches", "")),
        ("Blockers", render_blockers(blocker_sections)),
        ("Important Files", current_task_sections.get("Important Files", "")),
        ("Next Steps", current_task_sections.get("Next Steps", "")),
    ]

    body_parts: list[str] = [frontmatter]
    for section_name, section_body in sections:
        body_parts.append(f"## {section_name}\n")
        body_parts.append(clean_section_markdown(section_body))
        body_parts.append("")

    output = "\n".join(body_parts).strip() + "\n"

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = ROOT / output_path
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
        output_path = project_dir / "snapshots" / f"{timestamp}-{args.slug}.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    print(f"created snapshot: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
