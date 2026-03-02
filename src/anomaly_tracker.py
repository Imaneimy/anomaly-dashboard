"""
Anomaly Tracker — stores and queries test anomalies in SQLite.
Simulates a JIRA-like ticket database for Big Data testing.
"""

import sqlite3
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class Anomaly:
    title: str
    description: str
    severity: str          # CRITICAL | HIGH | MEDIUM | LOW
    status: str            # OPEN | IN_PROGRESS | RESOLVED | CLOSED | WONT_FIX
    project: str
    component: str         # ETL | DATALAKE | SQL | API
    detected_by: str       # test ID or tester name
    anomaly_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8].upper())
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    resolved_at: Optional[str] = None
    sprint: str = "Sprint-01"
    tags: str = ""


class AnomalyTracker:
    """CRUD operations for anomaly tickets."""

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS anomalies (
                anomaly_id   TEXT PRIMARY KEY,
                title        TEXT NOT NULL,
                description  TEXT,
                severity     TEXT NOT NULL,
                status       TEXT NOT NULL DEFAULT 'OPEN',
                project      TEXT NOT NULL,
                component    TEXT NOT NULL,
                detected_by  TEXT,
                created_at   TEXT,
                updated_at   TEXT,
                resolved_at  TEXT,
                sprint       TEXT,
                tags         TEXT
            );

            CREATE TABLE IF NOT EXISTS comments (
                comment_id  TEXT PRIMARY KEY,
                anomaly_id  TEXT REFERENCES anomalies(anomaly_id),
                author      TEXT,
                body        TEXT,
                created_at  TEXT
            );
        """)
        self.conn.commit()

    # ── CRUD ────────────────────────────────────────────────────────────────

    def create(self, anomaly: Anomaly) -> str:
        self.conn.execute("""
            INSERT INTO anomalies VALUES (
                :anomaly_id, :title, :description, :severity, :status,
                :project, :component, :detected_by, :created_at, :updated_at,
                :resolved_at, :sprint, :tags
            )
        """, anomaly.__dict__)
        self.conn.commit()
        return anomaly.anomaly_id

    def update_status(self, anomaly_id: str, new_status: str) -> bool:
        resolved_at = datetime.now().isoformat() if new_status in ("RESOLVED", "CLOSED") else None
        cursor = self.conn.execute("""
            UPDATE anomalies
               SET status = ?, updated_at = ?, resolved_at = ?
             WHERE anomaly_id = ?
        """, (new_status, datetime.now().isoformat(), resolved_at, anomaly_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def add_comment(self, anomaly_id: str, author: str, body: str) -> None:
        self.conn.execute("""
            INSERT INTO comments VALUES (?, ?, ?, ?, ?)
        """, (str(uuid.uuid4())[:8], anomaly_id, author, body, datetime.now().isoformat()))
        self.conn.commit()

    def get(self, anomaly_id: str) -> Optional[Dict]:
        row = self.conn.execute(
            "SELECT * FROM anomalies WHERE anomaly_id = ?", (anomaly_id,)
        ).fetchone()
        return dict(row) if row else None

    def list_all(self, status: str = None, severity: str = None,
                 component: str = None) -> List[Dict]:
        query = "SELECT * FROM anomalies WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if severity:
            query += " AND severity = ?"
            params.append(severity)
        if component:
            query += " AND component = ?"
            params.append(component)
        query += " ORDER BY created_at DESC"
        return [dict(r) for r in self.conn.execute(query, params).fetchall()]

    def get_stats(self) -> Dict[str, Any]:
        """KPI summary for the dashboard."""
        total = self.conn.execute("SELECT COUNT(*) FROM anomalies").fetchone()[0]
        by_status = {
            r[0]: r[1]
            for r in self.conn.execute(
                "SELECT status, COUNT(*) FROM anomalies GROUP BY status"
            ).fetchall()
        }
        by_severity = {
            r[0]: r[1]
            for r in self.conn.execute(
                "SELECT severity, COUNT(*) FROM anomalies GROUP BY severity"
            ).fetchall()
        }
        by_component = {
            r[0]: r[1]
            for r in self.conn.execute(
                "SELECT component, COUNT(*) FROM anomalies GROUP BY component"
            ).fetchall()
        }
        open_critical = self.conn.execute(
            "SELECT COUNT(*) FROM anomalies WHERE status='OPEN' AND severity='CRITICAL'"
        ).fetchone()[0]
        return {
            "total": total,
            "by_status": by_status,
            "by_severity": by_severity,
            "by_component": by_component,
            "open_critical": open_critical,
        }
