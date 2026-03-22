#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "index" / "memory.sqlite"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n") or text.startswith("---\r\n"):
        parts = re.split(r"^---\r?\n.*?\r?\n---\r?\n", text, maxsplit=1, flags=re.DOTALL)
        if len(parts) == 2:
            return parts[1].strip()
    return text.strip()


def strip_top_heading(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).strip()
    return text.strip()


def clean_section_text(path: Path, strip_heading: bool = True, strip_yaml: bool = False) -> str:
    text = read_text(path)
    if strip_yaml:
        text = strip_frontmatter(text)
    if strip_heading:
        text = strip_top_heading(text)
    return text.strip()


def latest_snapshot(project_dir: Path) -> Path | None:
    snapshot_dir = project_dir / "snapshots"
    if not snapshot_dir.exists():
        return None
    files = sorted(snapshot_dir.glob("*.md"), reverse=True)
    return files[0] if files else None


def fetch_memory_rows(project_id: str, limit: int) -> list[sqlite3.Row]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute(
            """
            SELECT id, type, title, summary_text, source_file
            FROM memory_items
            WHERE project_id = ?
              AND type IN ('decision', 'failure', 'constraint', 'pattern', 'handoff')
            ORDER BY updated_at DESC, id ASC
            LIMIT ?
            """,
            (project_id, limit),
        ).fetchall()


def main() -> None:
    parser = argparse.ArgumentParser(description="Assemble a fresh-session context packet.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--memory-limit", type=int, default=10)
    parser.add_argument("--output")
    args = parser.parse_args()

    project_dir = ROOT / "projects" / args.project_id
    current_task_path = project_dir / "current" / "current-task.md"
    blockers_path = project_dir / "current" / "blockers.md"
    snapshot_path = latest_snapshot(project_dir)
    rows = fetch_memory_rows(args.project_id, args.memory_limit)

    parts: list[str] = []
    parts.append(f"# Session Context\n")
    parts.append(f"Project: `{args.project_id}`\n")

    if current_task_path.exists():
        parts.append("## Current Task\n")
        parts.append(clean_section_text(current_task_path, strip_heading=True, strip_yaml=False))
        parts.append("")

    if blockers_path.exists():
        parts.append("## Blockers\n")
        parts.append(clean_section_text(blockers_path, strip_heading=True, strip_yaml=False))
        parts.append("")

    if snapshot_path:
        parts.append("## Latest Snapshot\n")
        parts.append(f"Source: `{snapshot_path.relative_to(ROOT).as_posix()}`\n")
        parts.append(clean_section_text(snapshot_path, strip_heading=False, strip_yaml=True))
        parts.append("")

    if rows:
        parts.append("## Durable Memory\n")
        for row in rows:
            if row["type"] == "handoff":
                continue
            parts.append(f"- `{row['type']}` `{row['id']}`: {row['title']}")
            if row["summary_text"]:
                parts.append(f"  {row['summary_text']}")
            parts.append(f"  Source: `{row['source_file']}`")
        parts.append("")

    output = "\n".join(parts).strip() + "\n"

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = ROOT / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
