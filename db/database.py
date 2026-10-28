"""Подключение к базе данных SQLite проекта."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "notifyhub.sqlite"


def get_connection() -> sqlite3.Connection:
    """Создать соединение с базой данных и включить внешние ключи."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
