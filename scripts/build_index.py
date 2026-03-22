#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "index" / "memory.sqlite"


FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", re.DOTALL)


def find_memory_files() -> list[Path]:
    roots = [
        ROOT / "projects",
        ROOT / "cross-project",
    ]
    files: list[Path] = []
    for base in roots:
        if not base.exists():
            continue
        files.extend(path for path in base.rglob("*.md") if path.is_file())
    return sorted(files)


def split_frontmatter(text: str) -> tuple[str | None, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    return match.group(1), match.group(2).strip()


def parse_scalar(value: str):
    lowered = value.lower()
    if lowered == "[]":
        return []
    if lowered == "null":
        return None
    if lowered in {"true", "false"}:
        return lowered == "true"
    return value


def parse_frontmatter(block: str | None) -> dict:
    if not block:
        return {}

    data: dict[str, object] = {}
    current_key: str | None = None
    current_list_item: dict[str, str] | None = None

    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            item_text = line[4:].strip()
            if ":" in item_text:
                item_key, item_value = item_text.split(":", 1)
                current_list_item = {item_key.strip(): item_value.strip()}
                data[current_key].append(current_list_item)
            else:
                current_list_item = None
                data[current_key].append(item_text)
            continue
        if line.startswith("- ") and current_key:
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            item_text = line[2:].strip()
            if ":" in item_text:
                item_key, item_value = item_text.split(":", 1)
                current_list_item = {item_key.strip(): item_value.strip()}
                data[current_key].append(current_list_item)
            else:
                current_list_item = None
                data[current_key].append(item_text)
            continue
        if line.startswith("    ") and current_key and current_list_item is not None and ":" in line.strip():
            nested_key, nested_value = line.strip().split(":", 1)
            current_list_item[nested_key.strip()] = nested_value.strip()
            continue

        if ":" not in line:
            continue

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        current_key = key

        if value == "":
            data[key] = []
            continue

        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [] if not inner else [part.strip() for part in inner.split(",")]
            continue

        data[key] = parse_scalar(value)

    return data


def infer_scope_kind(path: Path) -> str:
    parts = path.relative_to(ROOT).parts
    if not parts:
        return "unknown"
    if parts[0] == "projects":
        return "project"
    if parts[0] == "cross-project":
        return "cross_project"
    return "unknown"


def make_summary(body: str) -> str:
    lines = [
        line.strip()
        for line in body.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    return lines[0] if lines else ""


def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;

        DROP TABLE IF EXISTS memory_items;
        DROP TABLE IF EXISTS memory_paths;
        DROP TABLE IF EXISTS memory_evidence_refs;
        DROP TABLE IF EXISTS memory_links;
        DROP TABLE IF EXISTS memory_fts;

        CREATE TABLE memory_items (
          id TEXT PRIMARY KEY,
          type TEXT,
          title TEXT,
          status TEXT,
          scope_kind TEXT,
          project_id TEXT,
          workspace_id TEXT,
          workspace_root TEXT,
          branch TEXT,
          git_sha TEXT,
          summary_text TEXT,
          body_text TEXT,
          source_file TEXT,
          confidence TEXT,
          created_at TEXT,
          updated_at TEXT
        );

        CREATE TABLE memory_paths (
          memory_id TEXT NOT NULL,
          path TEXT NOT NULL
        );

        CREATE TABLE memory_evidence_refs (
          memory_id TEXT NOT NULL,
          evidence_type TEXT,
          ref TEXT NOT NULL
        );

        CREATE TABLE memory_links (
          src_memory_id TEXT NOT NULL,
          link_type TEXT NOT NULL,
          dst_memory_id TEXT NOT NULL
        );

        CREATE VIRTUAL TABLE memory_fts USING fts5(
          id UNINDEXED,
          title,
          summary_text,
          body_text
        );
        """
    )


def parse_evidence_refs(raw_value) -> list[dict[str, str]]:
    if not isinstance(raw_value, list):
        return []

    parsed: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for entry in raw_value:
        if isinstance(entry, dict):
            ref = str(entry.get("ref") or "").strip()
            if not ref:
                continue
            parsed.append(
                {
                    "type": str(entry.get("type") or "").strip(),
                    "ref": ref,
                }
            )
            current = None
            continue
        if not isinstance(entry, str):
            continue
        stripped = entry.strip()
        if stripped.startswith("type:"):
            if current:
                parsed.append(current)
            current = {"type": stripped.split(":", 1)[1].strip()}
            continue
        if stripped.startswith("ref:"):
            if current is None:
                current = {}
            current["ref"] = stripped.split(":", 1)[1].strip()
            continue

    if current:
        parsed.append(current)
    return parsed


def parse_string_list(raw_value) -> list[str]:
    if isinstance(raw_value, list):
        return [str(item).strip() for item in raw_value if str(item).strip()]
    if raw_value is None:
        return []
    value = str(raw_value).strip()
    return [value] if value else []


def insert_file(conn: sqlite3.Connection, path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    frontmatter_text, body = split_frontmatter(text)
    meta = parse_frontmatter(frontmatter_text)

    item_id = str(meta.get("id") or path.stem)
    item_type = str(meta.get("type") or "note")
    title = str(meta.get("title") or path.stem)
    status = str(meta.get("status") or "active")
    scope_kind = infer_scope_kind(path)
    project_id = str(meta.get("project_id") or "")
    workspace_id = str(meta.get("workspace_id") or "")
    workspace_root = str(meta.get("workspace_root") or "")
    branch = str(meta.get("branch") or "")
    git_sha = str(meta.get("git_sha") or "")
    confidence = str(meta.get("confidence") or "")
    created_at = str(meta.get("created_at") or "")
    updated_at = str(meta.get("updated_at") or "")
    summary_text = make_summary(body)
    source_file = str(path.relative_to(ROOT)).replace("\\", "/")

    conn.execute(
        """
        INSERT INTO memory_items (
          id, type, title, status, scope_kind, project_id, workspace_id,
          workspace_root, branch, git_sha, summary_text, body_text, source_file,
          confidence, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            item_id,
            item_type,
            title,
            status,
            scope_kind,
            project_id,
            workspace_id,
            workspace_root,
            branch,
            git_sha,
            summary_text,
            body,
            source_file,
            confidence,
            created_at,
            updated_at,
        ),
        )

    for scope_path in parse_string_list(meta.get("paths")):
        conn.execute(
            "INSERT INTO memory_paths (memory_id, path) VALUES (?, ?)",
            (item_id, str(scope_path)),
        )

    for evidence in parse_evidence_refs(meta.get("evidence_refs", [])):
        ref = evidence.get("ref")
        if not ref:
            continue
        conn.execute(
            "INSERT INTO memory_evidence_refs (memory_id, evidence_type, ref) VALUES (?, ?, ?)",
            (item_id, evidence.get("type", ""), ref),
        )

    for dst_id in parse_string_list(meta.get("supersedes")):
        conn.execute(
            "INSERT INTO memory_links (src_memory_id, link_type, dst_memory_id) VALUES (?, ?, ?)",
            (item_id, "supersedes", dst_id),
        )

    for dst_id in parse_string_list(meta.get("superseded_by")):
        conn.execute(
            "INSERT INTO memory_links (src_memory_id, link_type, dst_memory_id) VALUES (?, ?, ?)",
            (item_id, "superseded_by", dst_id),
        )

    conn.execute(
        """
        INSERT INTO memory_fts (id, title, summary_text, body_text)
        VALUES (?, ?, ?, ?)
        """,
        (item_id, title, summary_text, body),
    )


def main() -> None:
    files = find_memory_files()
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    with sqlite3.connect(DB_PATH) as conn:
        ensure_schema(conn)
        for path in files:
            insert_file(conn, path)
        conn.commit()

        item_count = conn.execute("SELECT COUNT(*) FROM memory_items").fetchone()[0]
        path_count = conn.execute("SELECT COUNT(*) FROM memory_paths").fetchone()[0]
        evidence_count = conn.execute("SELECT COUNT(*) FROM memory_evidence_refs").fetchone()[0]
        link_count = conn.execute("SELECT COUNT(*) FROM memory_links").fetchone()[0]
        fts_count = conn.execute("SELECT COUNT(*) FROM memory_fts").fetchone()[0]

    print(
        json.dumps(
            {
                "db_path": str(DB_PATH),
                "files_indexed": len(files),
                "memory_items": item_count,
                "memory_paths": path_count,
                "memory_evidence_refs": evidence_count,
                "memory_links": link_count,
                "memory_fts": fts_count,
            },
            ensure_ascii=True,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
