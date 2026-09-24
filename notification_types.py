"""Функции для работы с каталогом типов уведомлений."""


def add_notification_type(
    notification_types: dict[int, dict],
    name: str,
) -> int:
    """Добавить тип уведомлений в каталог и вернуть его id."""
    type_id = max(notification_types, default=0) + 1
    notification_types[type_id] = {"id": type_id, "name": name}
    return type_id


def find_notification_type(
    notification_types: dict[int, dict],
    query: str,
) -> dict[int, dict]:
    """Найти типы уведомлений, в названии которых встречается query."""
    query = query.lower()
    return {
        type_id: data
        for type_id, data in notification_types.items()
        if query in data["name"].lower()
    }


def sort_notification_types(
    notification_types: dict[int, dict],
) -> list[dict]:
    """Вернуть типы уведомлений, отсортированные по названию."""
    return sorted(
        notification_types.values(), key=lambda item: item["name"]
    )
