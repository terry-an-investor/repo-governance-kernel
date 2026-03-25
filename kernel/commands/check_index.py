#!/usr/bin/env python3
from __future__ import annotations

import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "index" / "memory.sqlite"


def main() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        tables = [
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            ).fetchall()
        ]
        item_count = conn.execute("SELECT COUNT(*) FROM memory_items").fetchone()[0]
        path_count = conn.execute("SELECT COUNT(*) FROM memory_paths").fetchone()[0]
        evidence_count = conn.execute("SELECT COUNT(*) FROM memory_evidence_refs").fetchone()[0]
        link_count = conn.execute("SELECT COUNT(*) FROM memory_links").fetchone()[0]
        fts_count = conn.execute("SELECT COUNT(*) FROM memory_fts").fetchone()[0]
        evidence_preview = conn.execute(
            """
            SELECT memory_id, evidence_type, ref
            FROM memory_evidence_refs
            ORDER BY memory_id, ref
            LIMIT 10
            """
        ).fetchall()

    print(
        json.dumps(
            {
                "db_path": str(DB_PATH),
                "tables": tables,
                "memory_items": item_count,
                "memory_paths": path_count,
                "memory_evidence_refs": evidence_count,
                "memory_links": link_count,
                "memory_fts": fts_count,
                "evidence_preview": evidence_preview,
            },
            ensure_ascii=True,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

