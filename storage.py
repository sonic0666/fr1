"""Функции сохранения и загрузки объектов проекта в формате JSON."""

import json
from datetime import date
from pathlib import Path

from models import NotificationType, Subscriber, Subscription
from models.notification_types import find_notification_type_by_id
from models.subscribers import find_subscriber_by_id


def _read_json_list(filename: str) -> list[dict]:
    """Прочитать JSON-файл со списком записей, устойчиво к ошибкам."""
    path = Path(filename)
    if not path.exists():
        return []
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def _write_json_list(filename: str, data: list[dict]) -> None:
    """Записать список записей в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_subscribers(filename: str) -> list[Subscriber]:
    """Загрузить подписчиков из JSON-файла и создать объекты Subscriber."""
    return [
        Subscriber.from_data(item) for item in _read_json_list(filename)
    ]


def save_subscribers(filename: str, subscribers: list[Subscriber]) -> None:
    """Сохранить объекты Subscriber в JSON-файл."""
    data = [
        {
            "id": subscriber.id,
            "name": subscriber.name,
            "email": subscriber.email,
        }
        for subscriber in subscribers
    ]
    _write_json_list(filename, data)


def load_notification_types(filename: str) -> list[NotificationType]:
    """Загрузить типы уведомлений и создать объекты NotificationType."""
    return [
        NotificationType(item["id"], item["name"])
        for item in _read_json_list(filename)
    ]


def save_notification_types(
    filename: str,
    notification_types: list[NotificationType],
) -> None:
    """Сохранить объекты NotificationType в JSON-файл."""
    data = [
        {"id": item.id, "name": item.name} for item in notification_types
    ]
    _write_json_list(filename, data)


def load_subscriptions(
    filename: str,
    notification_types: list[NotificationType],
    subscribers: list[Subscriber],
) -> list[Subscription]:
    """Загрузить подписки, связав их с Subscriber и NotificationType."""
    subscriptions = []
    for item in _read_json_list(filename):
        notification_type = find_notification_type_by_id(
            notification_types, item["type_id"]
        )
        subscriber = find_subscriber_by_id(
            subscribers, item["subscriber_id"]
        )
        if notification_type is None or subscriber is None:
            continue
        subscription = Subscription(
            item["id"],
            subscriber,
            notification_type,
            item["channel"],
            date.fromisoformat(item["end_date"]),
            item["is_active"],
        )
        subscriptions.append(subscription)
    return subscriptions


def save_subscriptions(
    filename: str,
    subscriptions: list[Subscription],
) -> None:
    """Сохранить подписки, заменив ссылки на объекты идентификаторами."""
    data = [
        {
            "id": subscription.id,
            "subscriber_id": subscription.subscriber.id,
            "type_id": subscription.notification_type.id,
            "channel": subscription.channel,
            "end_date": subscription.end_date.isoformat(),
            "is_active": subscription.is_active,
        }
        for subscription in subscriptions
    ]
    _write_json_list(filename, data)
