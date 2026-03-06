from __future__ import annotations

import json
import sqlite3
from datetime import date


class PaperDB:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self._init_table()

    def _init_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS processed_papers (
                arxiv_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                tags TEXT NOT NULL,
                processed_date TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def is_processed(self, arxiv_id: str) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM processed_papers WHERE arxiv_id = ?", (arxiv_id,)
        ).fetchone()
        return row is not None

    def mark_processed(self, arxiv_id: str, title: str, tags: list[str]):
        self.conn.execute(
            """INSERT OR IGNORE INTO processed_papers (arxiv_id, title, tags, processed_date)
               VALUES (?, ?, ?, ?)""",
            (arxiv_id, title, json.dumps(tags), date.today().isoformat()),
        )
        self.conn.commit()

    def get_all_processed_ids(self) -> set[str]:
        rows = self.conn.execute("SELECT arxiv_id FROM processed_papers").fetchall()
        return {r[0] for r in rows}

    def close(self):
        self.conn.close()
