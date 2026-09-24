"""Класс Subscriber и функции работы с коллекцией подписчиков."""

from typing import Optional


class Subscriber:
    """Подписчик сервиса уведомлений."""

    def __init__(
        self,
        subscriber_id: int,
        name: str,
        email: str,
    ) -> None:
        """Создать объект подписчика."""
        self.id = subscriber_id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        """Вернуть строковое представление подписчика."""
        return f"{self.name} ({self.email})"

    @staticmethod
    def validate_email(email: str) -> bool:
        """Функция из ПР1: простейшая валидация email."""
        if "@" not in email:
            return False
        local_part, _, domain_part = email.partition("@")
        if len(local_part) == 0 or "." not in domain_part:
            return False
        return True

    @classmethod
    def from_data(cls, data: dict) -> "Subscriber":
        """Создать подписчика из набора данных, например из JSON."""
        return cls(
            subscriber_id=data["id"],
            name=data["name"],
            email=data["email"],
        )


def add_subscriber(
    subscribers: list[Subscriber],
    name: str,
    email: str,
) -> Subscriber:
    """Создать подписчика, добавить его в коллекцию и вернуть объект.

    Вызывает ValueError, если email не прошёл валидацию.
    """
    if not Subscriber.validate_email(email):
        raise ValueError(f"некорректный email: {email}")
    subscriber_id = max(
        (subscriber.id for subscriber in subscribers), default=0
    ) + 1
    subscriber = Subscriber(subscriber_id, name, email)
    subscribers.append(subscriber)
    return subscriber


def find_subscriber(
    subscribers: list[Subscriber],
    query: str,
) -> list[Subscriber]:
    """Найти подписчиков по имени или адресу электронной почты."""
    query = query.lower()
    return [
        subscriber
        for subscriber in subscribers
        if query in subscriber.name.lower()
        or query in subscriber.email.lower()
    ]


def find_subscriber_by_id(
    subscribers: list[Subscriber],
    subscriber_id: int,
) -> Optional[Subscriber]:
    """Найти подписчика по идентификатору."""
    for subscriber in subscribers:
        if subscriber.id == subscriber_id:
            return subscriber
    return None
