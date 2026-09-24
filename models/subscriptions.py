"""Класс Subscription и функции работы с коллекцией подписок."""

from datetime import date
from typing import Optional

from .notification_types import NotificationType
from .subscribers import Subscriber


def check_subscription_status(is_active, end_date, current_date):
    """Функция из ПР1: статус подписки по флагу активности и сроку."""
    if not is_active:
        return "Подписка приостановлена"
    if current_date > end_date:
        return "Подписка истекла"
    return "Подписка активна"


class Subscription:
    """Подписка подписчика на тип уведомлений по определённому каналу."""

    def __init__(
        self,
        subscription_id: int,
        subscriber: Subscriber,
        notification_type: NotificationType,
        channel: str,
        end_date: date,
        is_active: bool = True,
    ) -> None:
        """Создать объект подписки."""
        self.id = subscription_id
        self.subscriber = subscriber
        self.notification_type = notification_type
        self.channel = channel
        self.end_date = end_date
        self.is_active = is_active

    def cancel(self) -> None:
        """Приостановить подписку."""
        self.is_active = False

    def days_until_renewal(self, current_date: date) -> int:
        """Функция из ПР1: количество дней до окончания подписки."""
        delta = self.end_date - current_date
        days_left = int(delta.days)
        if days_left < 0:
            return 0
        return days_left

    def get_status(self, current_date: date) -> str:
        """Определить текущий статус подписки на указанную дату."""
        return check_subscription_status(
            self.is_active, self.end_date, current_date
        )

    def format_notification(self, current_date: date) -> str:
        """Функция из ПР1: формирует текст уведомления для подписчика."""
        days_left = self.days_until_renewal(current_date)
        urgency = "Внимание! " if days_left <= 7 else ""
        return (
            f"{urgency}Здравствуйте, {self.subscriber.name}! "
            f"Ваша подписка на рассылку «{self.notification_type.name}» "
            f"по каналу {self.channel} истекает через {days_left} дн."
        )

    def __str__(self) -> str:
        """Вернуть строковое представление подписки с учётом статуса."""
        status = self.get_status(date.today())
        return (
            f"{self.subscriber.name} -> {self.notification_type.name} "
            f"({self.channel}): {status}"
        )


def is_subscription_active(
    subscriptions: list[Subscription],
    subscriber: Subscriber,
    notification_type: NotificationType,
    channel: str,
    current_date: date,
) -> bool:
    """Проверить, есть ли активная подписка на тип и канал."""
    for subscription in subscriptions:
        same_target = (
            subscription.subscriber is subscriber
            and subscription.notification_type is notification_type
            and subscription.channel == channel
        )
        if same_target and subscription.get_status(current_date) == (
            "Подписка активна"
        ):
            return True
    return False


def create_subscription(
    subscriptions: list[Subscription],
    subscriber: Subscriber,
    notification_type: NotificationType,
    channel: str,
    end_date: date,
    current_date: date,
) -> Optional[Subscription]:
    """Оформить подписку, если на этот тип и канал нет активной.

    Возвращает None, если активная подписка уже существует.
    """
    if is_subscription_active(
        subscriptions, subscriber, notification_type, channel, current_date
    ):
        return None
    subscription_id = max(
        (item.id for item in subscriptions), default=0
    ) + 1
    subscription = Subscription(
        subscription_id, subscriber, notification_type, channel, end_date
    )
    subscriptions.append(subscription)
    return subscription


def cancel_subscription(
    subscriptions: list[Subscription],
    subscription_id: int,
) -> bool:
    """Найти подписку по идентификатору и приостановить её."""
    for subscription in subscriptions:
        if subscription.id == subscription_id:
            subscription.cancel()
            return True
    return False
