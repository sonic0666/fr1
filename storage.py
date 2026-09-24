"""Функции сохранения и загрузки данных проекта в формате JSON."""

import json
from datetime import date
from pathlib import Path


def load_subscribers(filename: str) -> dict[int, dict]:
    """Загрузить подписчиков из JSON-файла."""
    path = Path(filename)
    if not path.exists():
        return {}
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return {}
    return {item["id"]: item for item in data}


def save_subscribers(filename: str, subscribers: dict[int, dict]) -> None:
    """Сохранить подписчиков в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            list(subscribers.values()), file, ensure_ascii=False, indent=2
        )


def load_notification_types(filename: str) -> dict[int, dict]:
    """Загрузить каталог типов уведомлений из JSON-файла."""
    path = Path(filename)
    if not path.exists():
        return {}
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return {}
    return {item["id"]: item for item in data}


def save_notification_types(
    filename: str,
    notification_types: dict[int, dict],
) -> None:
    """Сохранить каталог типов уведомлений в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            list(notification_types.values()),
            file,
            ensure_ascii=False,
            indent=2,
        )


def load_subscriptions(filename: str) -> list[dict]:
    """Загрузить список подписок из JSON-файла."""
    path = Path(filename)
    if not path.exists():
        return []
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return []
    for item in data:
        item["end_date"] = date.fromisoformat(item["end_date"])
    return data


def save_subscriptions(filename: str, subscriptions: list[dict]) -> None:
    """Сохранить список подписок в JSON-файл."""
    data = [
        {**item, "end_date": item["end_date"].isoformat()}
        for item in subscriptions
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
