#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

from kernel.build_index import parse_frontmatter, parse_string_list, split_frontmatter
from kernel.runtime_paths import resolve_index_path, resolve_project_state_root, resolve_repo_root

ROOT = resolve_repo_root()
DB_PATH = resolve_index_path()


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


def preface_before_first_h2(text: str) -> str:
    match = SECTION_RE.search(text)
    if not match:
        return text.strip()
    return text[: match.start()].strip()


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


def parse_bullet_list(text: str) -> list[str]:
    items: list[str] = []
    current_lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped.startswith("- "):
            if current_lines:
                items.append("\n".join(current_lines).strip())
            current_lines = [stripped[2:].strip()]
            continue
        if current_lines and stripped:
            current_lines.append(stripped)
    if current_lines:
        items.append("\n".join(current_lines).strip())
    return items


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


def is_placeholder_body(text: str) -> bool:
    normalized = " ".join(text.strip().lower().split())
    return normalized in {
        "",
        "- none recorded yet.",
        "none recorded yet.",
        "- _none_",
        "_none_",
    }


def append_control_block(parts: list[str], title: str, preface: str, sections: dict[str, str], names: list[str]) -> None:
    selected: list[str] = []
    preface = preface.strip()
    if preface and not is_placeholder_body(preface):
        selected.append(preface)
    for name in names:
        body = sections.get(name, "").strip()
        if is_placeholder_body(body):
            continue
        selected.append(f"### {name}\n\n{body}")
    if not selected:
        return
    parts.append(f"## {title}\n")
    parts.append("\n\n".join(selected))
    parts.append("")


CURRENT_TASK_ANCHOR_LABEL_ALIASES = {
    "workspace_id": ("workspace id",),
    "workspace_root": ("workspace root",),
    "branch": ("branch observed at last refresh", "branch"),
    "git_sha": ("head observed at last refresh", "head anchor"),
    "worktree_hint": ("worktree observed at last refresh", "worktree state"),
    "changed_path_count": ("changed path count observed at last refresh", "changed path count"),
    "last_anchor_refresh": ("last anchor refresh",),
}


def current_task_anchor_value(values: dict[str, str], key: str) -> str:
    for label in CURRENT_TASK_ANCHOR_LABEL_ALIASES.get(key, (key,)):
        value = values.get(label, "")
        if value:
            return value
    return ""


def current_task_has_workspace_snapshot(anchor: dict[str, str]) -> bool:
    return any(
        anchor.get(key, "").strip()
        for key in ["branch", "git_sha", "worktree_hint", "changed_path_count", "last_anchor_refresh"]
    )


def extract_current_task_anchor(current_task_sections: dict[str, str]) -> dict[str, str]:
    current_state = current_task_sections.get("Current State", "")
    values = parse_keyed_bullets(current_state)
    anchor = {
        "workspace_id": current_task_anchor_value(values, "workspace_id"),
        "workspace_root": current_task_anchor_value(values, "workspace_root"),
        "branch": current_task_anchor_value(values, "branch"),
        "git_sha": current_task_anchor_value(values, "git_sha"),
        "worktree_hint": current_task_anchor_value(values, "worktree_hint"),
        "changed_path_count": current_task_anchor_value(values, "changed_path_count"),
        "last_anchor_refresh": current_task_anchor_value(values, "last_anchor_refresh"),
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


def render_live_workspace_projection(
    *,
    project_id: str,
    live_workspace: dict[str, str],
    workspace_id: str = "",
    generated_at: str | None = None,
) -> str:
    timestamp = generated_at or datetime.now().astimezone().isoformat(timespec="seconds")
    lines = [
        "# Live Workspace Projection",
        "",
        "- Project: " + (f"`{project_id}`" if project_id else "``"),
        "- Generated at: " + (f"`{timestamp}`" if timestamp else "``"),
        "- Status: " + (f"`{live_workspace.get('status', '')}`" if live_workspace.get("status", "") else "``"),
    ]
    if workspace_id:
        lines.append(f"- Workspace id: `{workspace_id}`")
    if live_workspace.get("workspace_root", ""):
        lines.append(f"- Workspace root: `{live_workspace.get('workspace_root', '')}`")
    if live_workspace.get("branch", ""):
        lines.append(f"- Branch: `{live_workspace.get('branch', '')}`")
    if live_workspace.get("git_sha", ""):
        lines.append(f"- HEAD: `{live_workspace.get('git_sha', '')}`")
    if live_workspace.get("worktree_state", ""):
        lines.append(f"- Worktree state: `{live_workspace.get('worktree_state', '')}`")
    if live_workspace.get("changed_path_count", ""):
        lines.append(f"- Changed path count: `{live_workspace.get('changed_path_count', '')}`")
    if live_workspace.get("error", ""):
        lines.append(f"- Error: `{live_workspace.get('error', '')}`")

    status_short = str(live_workspace.get("status_short") or "").strip()
    if status_short:
        lines.extend(
            [
                "",
                "## Git Status",
                "",
                "```text",
                status_short,
                "```",
            ]
        )
    return "\n".join(lines).strip() + "\n"


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
    current_refreshed_at = current_task_anchor.get("last_anchor_refresh", "")

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
    packet_anchor_source = packet_anchor.get("anchor_source", "")

    branch_mismatch = bool(packet_branch and live_branch and packet_branch != live_branch)
    head_mismatch = bool(packet_head and live_head and packet_head != live_head)
    worktree_hint_mismatch = bool(packet_hint and live_worktree and packet_hint != live_worktree)

    if head_mismatch:
        if packet_anchor_source == "current-task" and current_refreshed_at:
            live_warnings.append(
                f"packet HEAD anchor `{packet_head}` reflects the last current-task refresh at `{current_refreshed_at}`, while live workspace HEAD is `{live_head}`"
            )
        elif packet_anchor_source == "latest-snapshot":
            live_warnings.append(
                f"packet HEAD anchor `{packet_head}` reflects the latest snapshot anchor, while live workspace HEAD is `{live_head}`"
            )
        elif packet_anchor_source == "current-task-locator":
            live_warnings.append(
                f"packet HEAD anchor `{packet_head}` was borrowed from the latest snapshot because current-task only supplied workspace locator fields, while live workspace HEAD is `{live_head}`"
            )
        else:
            live_warnings.append(
                f"packet HEAD anchor `{packet_head}` reflects historical packet anchor metadata, while live workspace HEAD is `{live_head}`"
            )
    if branch_mismatch:
        live_warnings.append(f"packet branch `{packet_branch}` does not match live workspace branch `{live_branch}`")
    if worktree_hint_mismatch:
        live_warnings.append(
            f"packet worktree hint `{packet_hint}` reflects historical current-task anchor metadata, while live workspace state is `{live_worktree}`"
        )

    warnings.extend(snapshot_warnings)
    warnings.extend(live_warnings)

    if branch_mismatch:
        guidance.append("Treat this packet as orientation context only until branch, HEAD, and worktree facts are revalidated.")
        guidance.append("Re-read live git status and the active project governance files before making code changes.")
        return "stale", warnings, guidance

    if head_mismatch or worktree_hint_mismatch:
        if packet_anchor_source == "current-task":
            guidance.append("Current-task anchor metadata is historical orientation data from the last refresh, not a self-updating live commit identity.")
        elif packet_anchor_source == "current-task-locator":
            guidance.append("Current-task now contributes only workspace locator fields; packet HEAD and worktree hints come from the latest snapshot until live repo inspection revalidates them.")
        elif packet_anchor_source == "latest-snapshot":
            guidance.append("Packet HEAD and worktree hints came from the latest snapshot, not from a live-updating current-task anchor.")
        else:
            guidance.append("Packet anchor metadata is historical orientation data, not a self-updating live commit identity.")
        guidance.append("Use the live workspace block as the canonical code-state truth when branch alignment still holds.")
        if snapshot_warnings:
            guidance.append("The latest snapshot is also behind the live workspace. Treat both snapshot and current-task anchors as historical.")
            if live_worktree == "dirty":
                return "live_revalidated_snapshot_behind_dirty", warnings, guidance
            return "live_revalidated_snapshot_behind", warnings, guidance
        if live_worktree == "dirty":
            guidance.append("The live workspace is still dirty after revalidation. Reconfirm scope before acting.")
            return "live_revalidated_dirty", warnings, guidance
        guidance.append("Live workspace revalidation succeeded on the current branch. You can trust the packet narrative with live repo facts layered on top.")
        return "live_revalidated", warnings, guidance

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
    packet_anchor_source = packet_anchor.get("anchor_source", "unknown")
    parts.append(f"- Packet anchor source: `{packet_anchor_source}`")

    if packet_anchor:
        parts.append("- Packet anchor:")
        anchor_labels = [
            ("workspace id", "workspace_id"),
            ("workspace root", "workspace_root"),
        ]
        if packet_anchor_source == "current-task":
            anchor_labels.extend(
                [
                    ("branch observed at last refresh", "branch"),
                    ("head observed at last refresh", "git_sha"),
                    ("worktree observed at last refresh", "worktree_hint"),
                    ("changed path count observed at last refresh", "changed_path_count"),
                    ("last anchor refresh", "last_anchor_refresh"),
                ]
            )
        else:
            anchor_labels.extend(
                [
                    ("branch", "branch"),
                    ("head", "git_sha"),
                    ("worktree hint", "worktree_hint"),
                    ("changed path count", "changed_path_count"),
                    ("last anchor refresh", "last_anchor_refresh"),
                ]
            )
        for label, key in anchor_labels:
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


def load_control_sections(path: Path) -> tuple[str, dict[str, str]]:
    if not path.exists():
        return "", {}
    cleaned = clean_section_text(path, strip_heading=True, strip_yaml=False)
    return preface_before_first_h2(cleaned), parse_h2_sections(cleaned)


def load_active_task_contract_records(project_dir: Path, round_id: str) -> list[dict[str, object]]:
    if not round_id.strip():
        return []
    directory = project_dir / "memory" / "task-contracts"
    if not directory.exists():
        return []

    records: list[dict[str, object]] = []
    for path in sorted(directory.glob("*.md")):
        text = read_text(path)
        frontmatter_text, _body = split_frontmatter(text)
        meta = parse_frontmatter(frontmatter_text)
        if str(meta.get("status") or "").strip() != "active":
            continue
        if str(meta.get("round_id") or "").strip() != round_id.strip():
            continue
        sections = parse_h2_sections(clean_section_text(path, strip_heading=False, strip_yaml=True))
        records.append(
            {
                "id": str(meta.get("id") or path.stem).strip(),
                "title": str(meta.get("title") or path.stem).strip(),
                "created_at": str(meta.get("created_at") or "").strip(),
                "paths": parse_string_list(meta.get("paths")),
                "summary": str(sections.get("Summary", "")).strip(),
                "intent": str(sections.get("Intent", "")).strip(),
                "allowed_changes": parse_bullet_list(str(sections.get("Allowed Changes", ""))),
                "forbidden_changes": parse_bullet_list(str(sections.get("Forbidden Changes", ""))),
                "completion_criteria": parse_bullet_list(str(sections.get("Completion Criteria", ""))),
                "source_file": path.relative_to(ROOT).as_posix(),
            }
        )
    records.sort(key=lambda record: str(record.get("created_at") or record.get("id") or ""))
    return records


def append_active_task_contracts(parts: list[str], records: list[dict[str, object]]) -> None:
    if not records:
        return
    parts.append("## Active Task Contracts\n")
    for record in records:
        parts.append(f"- `{record['id']}`: {record['title']}")
        summary = str(record.get("summary") or "").strip()
        if summary:
            parts.append(f"  - summary: {summary}")
        intent = str(record.get("intent") or "").strip()
        if intent:
            parts.append(f"  - intent: {intent}")
        paths = [str(item).strip() for item in record.get("paths", []) if str(item).strip()]
        if paths:
            parts.append(f"  - paths: {', '.join(paths)}")
        allowed_changes = [str(item).strip() for item in record.get("allowed_changes", []) if str(item).strip()]
        if allowed_changes:
            parts.append(f"  - allowed: {allowed_changes[0]}")
        completion_criteria = [str(item).strip() for item in record.get("completion_criteria", []) if str(item).strip()]
        if completion_criteria:
            parts.append(f"  - completion: {completion_criteria[0]}")
        parts.append(f"  - source: `{record['source_file']}`")
    parts.append("")


def main() -> None:
    parser = argparse.ArgumentParser(description="Assemble a fresh-session context packet.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--memory-limit", type=int, default=10)
    parser.add_argument("--output")
    args = parser.parse_args()

    project_dir = resolve_project_state_root(args.project_id, ROOT)
    active_objective_path = project_dir / "control" / "active-objective.md"
    active_round_path = project_dir / "control" / "active-round.md"
    pivot_log_path = project_dir / "control" / "pivot-log.md"
    exception_ledger_path = project_dir / "control" / "exception-ledger.md"
    current_task_path = project_dir / "current" / "current-task.md"
    blockers_path = project_dir / "current" / "blockers.md"
    snapshot_path = latest_snapshot(project_dir)
    rows = fetch_memory_rows(args.project_id, args.memory_limit)
    current_task_sections: dict[str, str] = {}
    if current_task_path.exists():
        current_task_sections = parse_h2_sections(clean_section_text(current_task_path, strip_heading=True, strip_yaml=False))
    active_objective_preface, active_objective_sections = load_control_sections(active_objective_path)
    active_round_preface, active_round_sections = load_control_sections(active_round_path)
    pivot_log_preface, pivot_log_sections = load_control_sections(pivot_log_path)
    exception_preface, exception_sections = load_control_sections(exception_ledger_path)
    current_task_anchor = extract_current_task_anchor(current_task_sections)
    snapshot_anchor = extract_snapshot_anchor(snapshot_path)
    packet_anchor = merge_anchor_sources(current_task_anchor, snapshot_anchor)
    if current_task_has_workspace_snapshot(current_task_anchor):
        packet_anchor["anchor_source"] = "current-task"
    elif snapshot_anchor:
        packet_anchor["anchor_source"] = "latest-snapshot"
    elif current_task_anchor:
        packet_anchor["anchor_source"] = "current-task-locator"
    else:
        packet_anchor["anchor_source"] = "unknown"
    live_workspace = inspect_live_workspace(packet_anchor)
    active_round_values = parse_keyed_bullets(active_round_preface)
    active_task_contracts = load_active_task_contract_records(
        project_dir,
        active_round_values.get("round id", ""),
    )

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

    append_control_block(
        parts,
        "Active Objective",
        active_objective_preface,
        active_objective_sections,
        ["Problem", "Success Criteria", "Non-Goals", "Current Risks"],
    )

    append_control_block(
        parts,
        "Active Round",
        active_round_preface,
        active_round_sections,
        ["Scope", "Deliverable", "Validation Plan", "Active Risks", "Blockers"],
    )

    append_active_task_contracts(parts, active_task_contracts)

    append_control_block(
        parts,
        "Pivot Lineage",
        pivot_log_preface,
        pivot_log_sections,
        ["Active Lineage", "Recent Pivots"],
    )

    append_control_block(
        parts,
        "Exception Ledger",
        exception_preface,
        exception_sections,
        ["Active", "Invalidated"],
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

