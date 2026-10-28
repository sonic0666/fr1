"""Настройка Django для тестов веб-интерфейса."""

import os
import sqlite3
from pathlib import Path

import django
import pytest
from django.test.utils import setup_test_environment

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notifyhub.settings")
django.setup()
setup_test_environment()


ROOT_DIR = Path(__file__).resolve().parent.parent
SCHEMA_FILE = ROOT_DIR / "sql" / "schema.sql"


@pytest.fixture
def empty_db(tmp_path, monkeypatch):
    """Пустая БД со схемой проекта; db.database.DB_PATH указывает на неё."""
    db_path = tmp_path / "test.sqlite"
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))
    conn.commit()
    conn.close()
    monkeypatch.setattr("db.database.DB_PATH", db_path)
    return db_path


@pytest.fixture
def sample_db(empty_db):
    """БД с тестовыми данными, не зависящими от текущей даты."""
    conn = sqlite3.connect(empty_db)
    conn.executemany(
        "INSERT INTO notification_types (id, name) VALUES (?, ?)",
        [
            (1, "Акции и скидки"),
            (2, "Новости сервиса"),
            (3, "Системные оповещения"),
        ],
    )
    conn.executemany(
        "INSERT INTO subscribers (id, name, email) VALUES (?, ?, ?)",
        [
            (1, "Иван Петров", "ivan@example.com"),
            (2, "Анна Смирнова", "anna@example.com"),
        ],
    )
    conn.executemany(
        """
        INSERT INTO subscriptions
            (id, subscriber_id, type_id, channel, end_date, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (1, 1, 1, "email", "2099-12-31", 1),
            (2, 1, 2, "push", "2020-01-01", 1),
            (3, 2, 1, "email", "2099-06-01", 1),
            (4, 2, 3, "sms", "2099-01-01", 0),
        ],
    )
    conn.commit()
    conn.close()
    return empty_db
