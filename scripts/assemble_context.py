#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sqlite3
import subprocess
from datetime import datetime
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


SECTION_RE = re.compile(r"^## (.+?)\r?$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def parse_h2_sections(text: str) -> dict[str, str]:
    matches = list(SECTION_RE.finditer(text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        sections[title] = body
    return sections


def strip_inline_code(text: str) -> str:
    value = text.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        return value[1:-1].strip()
    return value


def parse_keyed_bullets(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        match = re.match(r"^- ([^:]+):\s*(.+)$", line)
        if not match:
            continue
        key = match.group(1).strip().lower()
        values[key] = strip_inline_code(match.group(2))
    return values


def extract_frontmatter_scalars(text: str, field_names: list[str]) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    frontmatter = match.group(1)
    values: dict[str, str] = {}
    for field_name in field_names:
        field_match = re.search(rf"^{re.escape(field_name)}:\s*(.+?)\r?$", frontmatter, re.MULTILINE)
        if not field_match:
            continue
        values[field_name] = strip_inline_code(field_match.group(1))
    return values


def append_named_sections(parts: list[str], title: str, sections: dict[str, str], names: list[str]) -> None:
    selected: list[str] = []
    for name in names:
        body = sections.get(name, "").strip()
        if not body:
            continue
        selected.append(f"### {name}\n\n{body}")
    if not selected:
        return
    parts.append(f"## {title}\n")
    parts.append("\n\n".join(selected))
    parts.append("")


def extract_current_task_anchor(current_task_sections: dict[str, str]) -> dict[str, str]:
    current_state = current_task_sections.get("Current State", "")
    validated_facts = current_task_sections.get("Validated Facts", "")
    values = parse_keyed_bullets(current_state)
    worktree_hint = values.get("worktree state", "") or infer_worktree_hint("\n".join([current_state, validated_facts]).strip())
    anchor = {
        "workspace_id": values.get("workspace id", ""),
        "workspace_root": values.get("workspace root", ""),
        "branch": values.get("branch", ""),
        "git_sha": values.get("head anchor", ""),
        "worktree_hint": worktree_hint,
        "changed_path_count": values.get("changed path count", ""),
    }
    return {key: value for key, value in anchor.items() if value}


def extract_snapshot_anchor(snapshot_path: Path | None) -> dict[str, str]:
    if not snapshot_path or not snapshot_path.exists():
        return {}
    values = extract_frontmatter_scalars(
        read_text(snapshot_path),
        ["id", "title", "workspace_id", "workspace_root", "branch", "git_sha", "created_at", "updated_at"],
    )
    if values:
        values["source"] = snapshot_path.relative_to(ROOT).as_posix()
    worktree_hint = infer_worktree_hint(read_text(snapshot_path))
    if worktree_hint:
        values["worktree_hint"] = worktree_hint
    return values


def merge_anchor_sources(primary: dict[str, str], secondary: dict[str, str]) -> dict[str, str]:
    merged = dict(secondary)
    for key, value in primary.items():
        if value:
            merged[key] = value
    return merged


def infer_worktree_hint(text: str) -> str:
    lower = text.lower()
    dirty_markers = (
        "dirty diff",
        "dirty worktree",
        "dirty work is focused",
        "working tree has expanded",
        "uncommitted mainline",
        "broader than the active round contract",
    )
    clean_markers = (
        "worktree is clean",
        "clean checkout",
        "clean worktree",
    )
    if any(marker in lower for marker in dirty_markers):
        return "dirty"
    if any(marker in lower for marker in clean_markers):
        return "clean"
    return ""


def latest_snapshot(project_dir: Path) -> Path | None:
    snapshot_dir = project_dir / "snapshots"
    if not snapshot_dir.exists():
        return None
    files = sorted(snapshot_dir.glob("*.md"), reverse=True)
    return files[0] if files else None


def run_git_command(workspace_root: str, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", workspace_root, *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "git command failed")
    return completed.stdout.strip()


def inspect_live_workspace(anchor: dict[str, str]) -> dict[str, str]:
    workspace_root = anchor.get("workspace_root", "")
    if not workspace_root:
        return {"status": "anchor_missing"}

    workspace_path = Path(workspace_root)
    if not workspace_path.exists():
        return {"status": "workspace_unavailable", "workspace_root": workspace_root}

    try:
        branch = run_git_command(workspace_root, "rev-parse", "--abbrev-ref", "HEAD")
        git_sha = run_git_command(workspace_root, "rev-parse", "HEAD")
        status_text = run_git_command(workspace_root, "status", "--short", "--branch", "--untracked-files=all")
    except RuntimeError as exc:
        return {
            "status": "workspace_unavailable",
            "workspace_root": workspace_root,
            "error": str(exc),
        }

    status_lines = [line for line in status_text.splitlines() if line.strip()]
    change_lines = status_lines[1:] if status_lines[:1] and status_lines[0].startswith("## ") else status_lines
    worktree_state = "clean" if not change_lines else "dirty"

    return {
        "status": "available",
        "workspace_root": workspace_root,
        "branch": branch,
        "git_sha": git_sha,
        "worktree_state": worktree_state,
        "changed_path_count": str(len(change_lines)),
        "status_short": status_text,
    }


def assess_packet_freshness(
    packet_anchor: dict[str, str],
    current_task_anchor: dict[str, str],
    snapshot_anchor: dict[str, str],
    live_workspace: dict[str, str],
) -> tuple[str, list[str], list[str]]:
    warnings: list[str] = []
    snapshot_warnings: list[str] = []
    live_warnings: list[str] = []
    guidance: list[str] = []

    current_head = current_task_anchor.get("git_sha", "")
    snapshot_head = snapshot_anchor.get("git_sha", "")
    current_branch = current_task_anchor.get("branch", "")
    snapshot_branch = snapshot_anchor.get("branch", "")
    current_hint = current_task_anchor.get("worktree_hint", "")
    snapshot_hint = snapshot_anchor.get("worktree_hint", "")

    if current_head and snapshot_head and current_head != snapshot_head:
        snapshot_warnings.append(
            f"current-task HEAD anchor `{current_head}` does not match latest snapshot git_sha `{snapshot_head}`"
        )
    if current_branch and snapshot_branch and current_branch != snapshot_branch:
        snapshot_warnings.append(
            f"current-task branch `{current_branch}` does not match latest snapshot branch `{snapshot_branch}`"
        )
    if current_hint and snapshot_hint and current_hint != snapshot_hint:
        snapshot_warnings.append(
            f"current-task worktree hint `{current_hint}` does not match latest snapshot worktree hint `{snapshot_hint}`"
        )

    if live_workspace.get("status") != "available":
        warnings.extend(snapshot_warnings)
        if warnings:
            guidance.append("Current memory sources already disagree. Prefer live repo inspection before acting.")
        guidance.append("Live workspace inspection was unavailable. Treat this packet as orientation context only.")
        return "workspace_unavailable", warnings, guidance

    packet_head = packet_anchor.get("git_sha", "")
    packet_branch = packet_anchor.get("branch", "")
    packet_hint = packet_anchor.get("worktree_hint", "")
    live_head = live_workspace.get("git_sha", "")
    live_branch = live_workspace.get("branch", "")
    live_worktree = live_workspace.get("worktree_state", "")

    if packet_head and live_head and packet_head != live_head:
        live_warnings.append(f"packet HEAD anchor `{packet_head}` does not match live workspace HEAD `{live_head}`")
    if packet_branch and live_branch and packet_branch != live_branch:
        live_warnings.append(f"packet branch `{packet_branch}` does not match live workspace branch `{live_branch}`")
    if packet_hint and live_worktree and packet_hint != live_worktree:
        live_warnings.append(
            f"packet worktree hint `{packet_hint}` does not match live workspace state `{live_worktree}`"
        )

    warnings.extend(snapshot_warnings)
    warnings.extend(live_warnings)

    if live_warnings:
        guidance.append("Treat this packet as orientation context only until branch, HEAD, and worktree facts are revalidated.")
        guidance.append("Re-read live git status and the active project governance files before making code changes.")
        return "stale", warnings, guidance

    if snapshot_warnings:
        guidance.append("Packet anchor matches the live workspace, but the latest snapshot is behind current-task state.")
        guidance.append("Use current-task plus live repo checks as truth. Treat the snapshot as historical context.")
        if live_worktree == "dirty":
            return "fresh_snapshot_behind_dirty", warnings, guidance
        return "fresh_snapshot_behind", warnings, guidance

    if live_worktree == "dirty":
        guidance.append("Packet branch and HEAD still match, but the live workspace is dirty. Reconfirm scope before acting.")
        return "live_match_dirty", warnings, guidance

    guidance.append("Packet anchor matches the live workspace. You can trust it as the initial recovery baseline.")
    return "fresh", warnings, guidance


def append_packet_freshness(
    parts: list[str],
    *,
    current_task_anchor: dict[str, str],
    snapshot_anchor: dict[str, str],
    packet_anchor: dict[str, str],
    live_workspace: dict[str, str],
) -> None:
    verdict, warnings, guidance = assess_packet_freshness(
        packet_anchor,
        current_task_anchor,
        snapshot_anchor,
        live_workspace,
    )
    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")

    parts.append("## Packet Freshness\n")
    parts.append(f"- Generated at: `{generated_at}`")
    parts.append(f"- Freshness verdict: `{verdict}`")
    parts.append(f"- Packet anchor source: `{packet_anchor.get('anchor_source', 'unknown')}`")

    if packet_anchor:
        parts.append("- Packet anchor:")
        for label, key in [
            ("workspace id", "workspace_id"),
            ("workspace root", "workspace_root"),
            ("branch", "branch"),
            ("head anchor", "git_sha"),
            ("worktree hint", "worktree_hint"),
        ]:
            value = packet_anchor.get(key, "")
            if value:
                parts.append(f"  - {label}: `{value}`")

    if snapshot_anchor:
        parts.append("- Latest snapshot anchor:")
        for label, key in [
            ("source", "source"),
            ("snapshot id", "id"),
            ("updated_at", "updated_at"),
            ("branch", "branch"),
            ("git_sha", "git_sha"),
            ("worktree hint", "worktree_hint"),
        ]:
            value = snapshot_anchor.get(key, "")
            if value:
                parts.append(f"  - {label}: `{value}`")

    if live_workspace:
        parts.append("- Live workspace:")
        for label, key in [
            ("status", "status"),
            ("workspace root", "workspace_root"),
            ("branch", "branch"),
            ("head", "git_sha"),
            ("worktree", "worktree_state"),
            ("changed path count", "changed_path_count"),
        ]:
            value = live_workspace.get(key, "")
            if value:
                parts.append(f"  - {label}: `{value}`")

    if warnings:
        parts.append("- Anchor warnings:")
        for warning in warnings:
            parts.append(f"  - {warning}")

    if guidance:
        parts.append("- Operator guidance:")
        for item in guidance:
            parts.append(f"  - {item}")

    parts.append("")


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
    current_task_sections: dict[str, str] = {}
    if current_task_path.exists():
        current_task_sections = parse_h2_sections(clean_section_text(current_task_path, strip_heading=True, strip_yaml=False))
    current_task_anchor = extract_current_task_anchor(current_task_sections)
    snapshot_anchor = extract_snapshot_anchor(snapshot_path)
    packet_anchor = merge_anchor_sources(current_task_anchor, snapshot_anchor)
    if current_task_anchor:
        packet_anchor["anchor_source"] = "current-task"
    elif snapshot_anchor:
        packet_anchor["anchor_source"] = "latest-snapshot"
    else:
        packet_anchor["anchor_source"] = "unknown"
    live_workspace = inspect_live_workspace(packet_anchor)

    parts: list[str] = []
    parts.append(f"# Session Context\n")
    parts.append(f"Project: `{args.project_id}`\n")
    append_packet_freshness(
        parts,
        current_task_anchor=current_task_anchor,
        snapshot_anchor=snapshot_anchor,
        packet_anchor=packet_anchor,
        live_workspace=live_workspace,
    )

    if current_task_path.exists():
        append_named_sections(
            parts,
            "Current Task",
            current_task_sections,
            ["Goal", "Current State", "Active Risks", "Next Steps"],
        )

    if blockers_path.exists():
        blocker_sections = parse_h2_sections(clean_section_text(blockers_path, strip_heading=True, strip_yaml=False))
        append_named_sections(parts, "Blockers", blocker_sections, ["Active", "Waiting"])

    if snapshot_path:
        snapshot_sections = parse_h2_sections(clean_section_text(snapshot_path, strip_heading=False, strip_yaml=True))
        parts.append("## Latest Snapshot\n")
        parts.append(f"Source: `{snapshot_path.relative_to(ROOT).as_posix()}`\n")
        parts.append("")
        for name in ["Goal", "Completed Work", "Validated Facts", "Next Steps"]:
            body = snapshot_sections.get(name, "").strip()
            if not body:
                continue
            parts.append(f"### {name}\n\n{body}")
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
