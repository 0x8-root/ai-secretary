import os
import sqlite3
from pathlib import Path

DB_NAME = os.getenv("DB_PATH", "secretary.db")
Path(DB_NAME).parent.mkdir(parents=True, exist_ok=True)


def init_db() -> None:
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                remind_time TEXT NOT NULL,
                priority INTEGER DEFAULT 3,
                task_type TEXT NOT NULL,
                days_of_week TEXT DEFAULT '',
                is_sent INTEGER DEFAULT 0
            )
            """
        )


def add_task(
    title: str,
    remind_time: str,
    task_type: str,
    days_of_week: str = "",
    priority: int = 3,
) -> None:
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """
            INSERT INTO tasks
            (title, remind_time, task_type, days_of_week, priority)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, remind_time, task_type, days_of_week, priority),
        )


def get_pending_tasks(
    current_time: str,
    current_weekday: int,
) -> list[tuple[int, str, int]]:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute(
            """
            SELECT id, title, priority, task_type, days_of_week
            FROM tasks
            WHERE remind_time = ? AND is_sent = 0
            """,
            (current_time,),
        )

        rows = cursor.fetchall()
        result = []

        for task_id, title, priority, task_type, days_of_week in rows:
            if task_type != "weekly" or str(current_weekday) in days_of_week.split(","):
                result.append((task_id, title, priority))

        return result


def cleanup_once_tasks() -> None:
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "DELETE FROM tasks WHERE is_sent = 1 AND task_type = 'once'"
        )


def mark_as_sent(task_id: int) -> None:
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "UPDATE tasks SET is_sent = 1 WHERE id = ?",
            (task_id,),
        )


def reset_recurring_tasks() -> None:
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "UPDATE tasks SET is_sent = 0 WHERE task_type IN ('daily', 'weekly')"
        )


def get_all_tasks() -> list[dict]:
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            """
            SELECT id, title, remind_time, priority,
                   task_type, days_of_week, is_sent
            FROM tasks
            ORDER BY remind_time ASC
            """
        )
        return [dict(row) for row in cursor.fetchall()]


def delete_task(task_id: int) -> None:
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,),
        )