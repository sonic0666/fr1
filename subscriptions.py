"""Функции для работы с подписками на уведомления."""

from datetime import date


def check_subscription_status(is_active, end_date, current_date):
    """Функция из ПР1: статус подписки по флагу активности и сроку."""
    if not is_active:
        return "Подписка приостановлена"
    if current_date > end_date:
        return "Подписка истекла"
    return "Подписка активна"


def days_until_renewal(end_date, current_date):
    """Функция из ПР1: количество дней до окончания подписки."""
    delta = end_date - current_date
    days_left = int(delta.days)
    if days_left < 0:
        return 0
    return days_left


def format_notification(name, notif_type, channel, days_left):
    """Функция из ПР1: формирует текст уведомления для подписчика."""
    if days_left <= 7:
        urgency = "Внимание! "
    else:
        urgency = ""
    message = (
        f"{urgency}Здравствуйте, {name}! "
        f"Ваша подписка на рассылку «{notif_type}» по каналу {channel} "
        f"истекает через {days_left} дн."
    )
    return message


def is_subscription_active(
    subscriptions: list[dict],
    subscriber_id: int,
    type_id: int,
    channel: str,
    current_date: date,
) -> bool:
    """Проверить, есть ли активная подписка на тип уведомлений и канал."""
    for subscription in subscriptions:
        same_target = (
            subscription["subscriber_id"] == subscriber_id
            and subscription["type_id"] == type_id
            and subscription["channel"] == channel
        )
        if not same_target:
            continue
        status = check_subscription_status(
            subscription["is_active"], subscription["end_date"], current_date
        )
        if status == "Подписка активна":
            return True
    return False


def create_subscription(
    subscribers: dict[int, dict],
    subscriptions: list[dict],
    subscriber_id: int,
    type_id: int,
    channel: str,
    end_date: date,
    current_date: date,
) -> dict:
    """Оформить подписку подписчика на тип уведомлений по каналу.

    Вызывает KeyError, если подписчик не найден, и ValueError,
    если на этот тип и канал уже есть активная подписка.
    """
    if subscriber_id not in subscribers:
        raise KeyError(f"подписчик с id={subscriber_id} не найден")
    if is_subscription_active(
        subscriptions, subscriber_id, type_id, channel, current_date
    ):
        raise ValueError(
            "у подписчика уже есть активная подписка на этот тип и канал"
        )

    subscription_id = max(
        (item["id"] for item in subscriptions), default=0
    ) + 1
    subscription = {
        "id": subscription_id,
        "subscriber_id": subscriber_id,
        "type_id": type_id,
        "channel": channel,
        "end_date": end_date,
        "is_active": True,
    }
    subscriptions.append(subscription)
    return subscription


def cancel_subscription(
    subscriptions: list[dict],
    subscription_id: int,
) -> bool:
    """Приостановить подписку по идентификатору."""
    for subscription in subscriptions:
        if subscription["id"] == subscription_id:
            subscription["is_active"] = False
            return True
    return False
