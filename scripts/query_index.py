#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "index" / "memory.sqlite"


def quote_fts_term(term: str) -> str:
    return '"' + term.replace('"', '""') + '"'


def build_fts_query(text: str) -> str:
    terms = [part.strip() for part in text.split() if part.strip()]
    if not terms:
        return ""
    return " AND ".join(quote_fts_term(term) for term in terms)


def build_query(args: argparse.Namespace) -> tuple[str, list[str]]:
    params: list[str] = []
    fts_query = build_fts_query(args.text) if args.text else ""

    if fts_query:
        sql = """
        WITH fts_matches AS (
          SELECT id, bm25(memory_fts) AS fts_rank
          FROM memory_fts
          WHERE memory_fts MATCH ?
        )
        SELECT DISTINCT
          mi.id,
          mi.type,
          mi.title,
          mi.project_id,
          mi.workspace_id,
          mi.branch,
          mi.git_sha,
          mi.source_file,
          mi.summary_text,
          fts_matches.fts_rank
        FROM memory_items mi
        JOIN fts_matches ON fts_matches.id = mi.id
        LEFT JOIN memory_paths mp ON mp.memory_id = mi.id
        WHERE 1=1
        """
        params.append(fts_query)
    else:
        sql = """
        SELECT DISTINCT
          mi.id,
          mi.type,
          mi.title,
          mi.project_id,
          mi.workspace_id,
          mi.branch,
          mi.git_sha,
          mi.source_file,
          mi.summary_text,
          NULL AS fts_rank
        FROM memory_items mi
        LEFT JOIN memory_paths mp ON mp.memory_id = mi.id
        WHERE 1=1
        """

    if args.project_id:
        sql += " AND mi.project_id = ?"
        params.append(args.project_id)
    if args.workspace_id:
        sql += " AND mi.workspace_id = ?"
        params.append(args.workspace_id)
    if args.item_type:
        sql += " AND mi.type = ?"
        params.append(args.item_type)
    if args.path_contains:
        sql += " AND mp.path LIKE ?"
        params.append(f"%{args.path_contains}%")

    if fts_query:
        sql += " ORDER BY fts_matches.fts_rank ASC, mi.updated_at DESC, mi.id ASC LIMIT ?"
    else:
        sql += " ORDER BY mi.updated_at DESC, mi.id ASC LIMIT ?"
    params.append(args.limit)
    return sql, params


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the repo-governance-kernel SQLite index.")
    parser.add_argument("--project-id")
    parser.add_argument("--workspace-id")
    parser.add_argument("--type", dest="item_type")
    parser.add_argument("--path-contains")
    parser.add_argument("--text")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    sql, params = build_query(args)

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = [dict(row) for row in conn.execute(sql, params).fetchall()]

    print(json.dumps({"count": len(rows), "results": rows}, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
