"""Класс NotificationType и функции работы с каталогом типов."""

from typing import Optional


class NotificationType:
    """Тип уведомлений (категория рассылки)."""

    def __init__(self, type_id: int, name: str) -> None:
        """Создать объект типа уведомлений."""
        self.id = type_id
        self.name = name

    def __str__(self) -> str:
        """Вернуть строковое представление типа уведомлений."""
        return self.name


def add_notification_type(
    notification_types: list[NotificationType],
    name: str,
) -> NotificationType:
    """Создать тип уведомлений, добавить его в коллекцию и вернуть."""
    type_id = max(
        (item.id for item in notification_types), default=0
    ) + 1
    notification_type = NotificationType(type_id, name)
    notification_types.append(notification_type)
    return notification_type


def find_notification_type(
    notification_types: list[NotificationType],
    query: str,
) -> list[NotificationType]:
    """Найти типы уведомлений, в названии которых встречается query."""
    query = query.lower()
    return [
        item for item in notification_types if query in item.name.lower()
    ]


def find_notification_type_by_id(
    notification_types: list[NotificationType],
    type_id: int,
) -> Optional[NotificationType]:
    """Найти тип уведомлений по идентификатору."""
    for item in notification_types:
        if item.id == type_id:
            return item
    return None


def sort_notification_types(
    notification_types: list[NotificationType],
) -> list[NotificationType]:
    """Вернуть типы уведомлений, отсортированные по названию."""
    return sorted(notification_types, key=lambda item: item.name)
