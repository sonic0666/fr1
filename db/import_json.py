"""Однократный перенос данных проекта из JSON-файлов в SQLite."""

import json
import sqlite3
from pathlib import Path

from db.database import get_connection

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TYPES_FILE = DATA_DIR / "notification_types.json"
SUBSCRIBERS_FILE = DATA_DIR / "subscribers.json"
SUBSCRIPTIONS_FILE = DATA_DIR / "subscriptions.json"


def load_json(filename: Path) -> list[dict]:
    """Прочитать JSON-файл со списком записей."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_notification_types(conn: sqlite3.Connection) -> None:
    """Перенести типы уведомлений в таблицу notification_types."""
    notification_types = load_json(TYPES_FILE)
    conn.executemany(
        """
        INSERT INTO notification_types (
            id,
            name
        )
        VALUES (?, ?)
        """,
        [
            (
                item["id"],
                item["name"],
            )
            for item in notification_types
        ],
    )


def import_subscribers(conn: sqlite3.Connection) -> None:
    """Перенести подписчиков в таблицу subscribers."""
    subscribers = load_json(SUBSCRIBERS_FILE)
    conn.executemany(
        """
        INSERT INTO subscribers (
            id,
            name,
            email
        )
        VALUES (?, ?, ?)
        """,
        [
            (
                subscriber["id"],
                subscriber["name"],
                subscriber["email"],
            )
            for subscriber in subscribers
        ],
    )


def import_subscriptions(conn: sqlite3.Connection) -> None:
    """Перенести подписки в таблицу subscriptions."""
    subscriptions = load_json(SUBSCRIPTIONS_FILE)
    conn.executemany(
        """
        INSERT INTO subscriptions (
            id,
            subscriber_id,
            type_id,
            channel,
            end_date,
            is_active
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                subscription["id"],
                subscription["subscriber_id"],
                subscription["type_id"],
                subscription["channel"],
                subscription["end_date"],
                int(subscription["is_active"]),
            )
            for subscription in subscriptions
        ],
    )


def main() -> None:
    """Выполнить импорт: сначала справочники, затем подписки."""
    conn = get_connection()
    try:
        import_notification_types(conn)
        import_subscribers(conn)
        import_subscriptions(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
