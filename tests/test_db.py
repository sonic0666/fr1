"""Тесты слоя базы данных: схема, ограничения и импорт из JSON."""

import json
import sqlite3
from pathlib import Path

import pytest

from db import import_json
from db.database import get_connection

SCHEMA_FILE = Path(__file__).resolve().parent.parent / "sql" / "schema.sql"


def test_schema_creates_three_tables(empty_db):
    conn = get_connection()
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"
    ).fetchall()
    conn.close()
    names = {row[0] for row in rows}
    assert {"notification_types", "subscribers", "subscriptions"} <= names


def test_schema_can_be_executed_twice(empty_db):
    conn = get_connection()
    conn.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))
    conn.close()


def test_foreign_keys_are_enforced(sample_db):
    conn = get_connection()
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO subscriptions
                (id, subscriber_id, type_id, channel, end_date, is_active)
            VALUES (100, 999, 1, 'email', '2099-01-01', 1)
            """
        )
    conn.close()


def test_channel_check_constraint(sample_db):
    conn = get_connection()
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO subscriptions
                (id, subscriber_id, type_id, channel, end_date, is_active)
            VALUES (100, 1, 1, 'fax', '2099-01-01', 1)
            """
        )
    conn.close()


def test_import_json_moves_all_records(empty_db, tmp_path, monkeypatch):
    files = {
        "TYPES_FILE": [{"id": 1, "name": "Новости"}],
        "SUBSCRIBERS_FILE": [
            {"id": 1, "name": "Иван", "email": "ivan@example.com"},
            {"id": 2, "name": "Анна", "email": "anna@example.com"},
        ],
        "SUBSCRIPTIONS_FILE": [
            {
                "id": 1,
                "subscriber_id": 2,
                "type_id": 1,
                "channel": "push",
                "end_date": "2099-01-01",
                "is_active": True,
            }
        ],
    }
    for attribute, data in files.items():
        path = tmp_path / f"{attribute}.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        monkeypatch.setattr(import_json, attribute, path)

    import_json.main()

    conn = get_connection()
    counts = [
        conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        for table in ("notification_types", "subscribers", "subscriptions")
    ]
    is_active = conn.execute(
        "SELECT is_active FROM subscriptions WHERE id = 1"
    ).fetchone()[0]
    conn.close()
    assert counts == [1, 2, 1]
    assert is_active == 1


def test_import_rolls_back_on_error(empty_db, tmp_path, monkeypatch):
    types_file = tmp_path / "types.json"
    types_file.write_text(
        json.dumps([{"id": 1, "name": "Новости"}]), encoding="utf-8"
    )
    subscribers_file = tmp_path / "subscribers.json"
    subscribers_file.write_text("[]", encoding="utf-8")
    broken_file = tmp_path / "subscriptions.json"
    broken_file.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "subscriber_id": 42,
                    "type_id": 1,
                    "channel": "email",
                    "end_date": "2099-01-01",
                    "is_active": True,
                }
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(import_json, "TYPES_FILE", types_file)
    monkeypatch.setattr(import_json, "SUBSCRIBERS_FILE", subscribers_file)
    monkeypatch.setattr(import_json, "SUBSCRIPTIONS_FILE", broken_file)

    with pytest.raises(sqlite3.IntegrityError):
        import_json.main()

    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM notification_types").fetchone()
    conn.close()
    assert count[0] == 0


QUERIES_FILE = SCHEMA_FILE.parent / "queries.sql"


def _read_queries():
    text = QUERIES_FILE.read_text(encoding="utf-8")
    parts = [part.strip() for part in text.split("-- ;;")]
    return [part for part in parts if "SELECT" in part]


def test_queries_file_has_at_least_ten_queries():
    assert len(_read_queries()) >= 10


@pytest.mark.parametrize("query", _read_queries())
def test_each_query_in_queries_sql_runs(sample_db, query):
    conn = get_connection()
    conn.execute(query).fetchall()
    conn.close()


def test_query_functions(sample_db):
    from datetime import date

    from db import queries

    today = date(2026, 10, 29)
    conn = get_connection()
    assert queries.count_rows(conn) == {
        "notification_types": 3,
        "subscribers": 2,
        "subscriptions": 4,
    }
    assert queries.count_active_subscriptions(conn, 1, today) == 2
    assert queries.get_notification_type(conn, 99) is None
    assert queries.get_subscription(conn, 99, today) is None
    expired = queries.get_subscription(conn, 2, today)
    assert expired["is_expired"] == 1
    assert expired["end_date"] == date(2020, 1, 1)
    popular = queries.get_popular_types(conn)
    assert [row["name"] for row in popular] == ["Акции и скидки"]
    conn.close()
