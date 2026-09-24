"""Функции для работы с подписчиками сервиса."""


def validate_email(email: str) -> bool:
    """Функция из ПР1: простейшая валидация email."""
    if "@" not in email:
        return False
    local_part, _, domain_part = email.partition("@")
    if len(local_part) == 0 or "." not in domain_part:
        return False
    return True


def add_subscriber(
    subscribers: dict[int, dict],
    name: str,
    email: str,
) -> int:
    """Добавить подписчика и вернуть его id.

    Вызывает ValueError, если email не прошёл валидацию.
    """
    if not validate_email(email):
        raise ValueError(f"некорректный email: {email}")
    subscriber_id = max(subscribers, default=0) + 1
    subscribers[subscriber_id] = {
        "id": subscriber_id,
        "name": name,
        "email": email,
    }
    return subscriber_id


def find_subscriber(
    subscribers: dict[int, dict],
    query: str,
) -> dict[int, dict]:
    """Найти подписчиков по имени или адресу электронной почты."""
    query = query.lower()
    return {
        subscriber_id: data
        for subscriber_id, data in subscribers.items()
        if query in data["name"].lower() or query in data["email"].lower()
    }
