from __future__ import annotations

import sqlite3
from datetime import datetime, timezone


class Store:
    """Post history: used for dedup, topic rotation and auditing."""

    def __init__(self, path: str):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                topic TEXT NOT NULL,
                text TEXT NOT NULL,
                status TEXT NOT NULL,       -- published | dry_run | failed
                external_id TEXT,
                error TEXT,
                created_at TEXT NOT NULL
            )"""
        )
        self.conn.commit()

    def add(self, platform, topic, text, status, external_id=None, error=None) -> None:
        self.conn.execute(
            "INSERT INTO posts (platform, topic, text, status, external_id, error, created_at)"
            " VALUES (?,?,?,?,?,?,?)",
            (platform, topic, text, status, external_id, error,
             datetime.now(timezone.utc).isoformat()),
        )
        self.conn.commit()

    def recent_texts(self, platform: str, limit: int = 15) -> list[str]:
        rows = self.conn.execute(
            "SELECT text FROM posts WHERE platform=? AND status!='failed'"
            " ORDER BY id DESC LIMIT ?",
            (platform, limit),
        ).fetchall()
        return [r[0] for r in rows]

    def count(self, platform: str) -> int:
        return self.conn.execute(
            "SELECT COUNT(*) FROM posts WHERE platform=? AND status!='failed'", (platform,)
        ).fetchone()[0]

    def history(self, limit: int = 20):
        return self.conn.execute(
            "SELECT created_at, platform, status, text FROM posts ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
