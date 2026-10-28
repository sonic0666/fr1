"""Подключение к базе данных SQLite проекта."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "notifyhub.sqlite"


def get_connection() -> sqlite3.Connection:
    """Создать соединение: строки как словари, внешние ключи включены."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
