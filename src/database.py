import sqlite3
from typing import List
from .models import ServiceResult


class DatabaseManager:
    """Handles SQLite persistence for health check outcomes."""

    def __init__(self, db_path: str = "sitepulse.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Creates the required tables if they do not exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS check_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL,
                    status_code INTEGER,
                    latency_ms REAL,
                    is_healthy INTEGER,
                    error_message TEXT,
                    timestamp TEXT
                )
            """)
            conn.commit()

    def save_result(self, result: ServiceResult):
        """Saves a single health check result."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO check_logs 
                (name, url, status_code, latency_ms, is_healthy, error_message, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                result.name,
                result.url,
                result.status_code,
                result.latency_ms,
                1 if result.is_healthy else 0,
                result.error_message,
                result.timestamp
            ))
            conn.commit()

    def get_recent_history(self, limit: int = 15) -> List[ServiceResult]:
        """Fetches the latest check logs ordered by timestamp descending."""
        results: List[ServiceResult] = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, url, status_code, latency_ms, is_healthy, error_message, timestamp
                FROM check_logs
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            for row in rows:
                results.append(ServiceResult(
                    name=row[0],
                    url=row[1],
                    status_code=row[2],
                    latency_ms=row[3],
                    is_healthy=bool(row[4]),
                    error_message=row[5],
                    timestamp=row[6]
                ))
        return results

    def get_stats(self) -> dict:
        """Calculates basic availability statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), SUM(is_healthy), AVG(latency_ms) FROM check_logs")
            total, healthy, avg_latency = cursor.fetchone()
            total = total or 0
            healthy = healthy or 0
            avg_latency = avg_latency or 0.0

            uptime_pct = (healthy / total * 100) if total > 0 else 100.0
            return {
                "total_checks": total,
                "healthy_checks": healthy,
                "failed_checks": total - healthy,
                "uptime_percentage": round(uptime_pct, 2),
                "avg_latency_ms": round(avg_latency, 2)
            }
