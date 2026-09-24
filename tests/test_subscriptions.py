"""Тесты класса Subscription и функций работы с коллекцией подписок."""

from datetime import date

from models import NotificationType, Subscriber
from models.subscriptions import (
    cancel_subscription,
    check_subscription_status,
    create_subscription,
    is_subscription_active,
)

TODAY = date(2026, 9, 24)


def _make_subscriber() -> Subscriber:
    return Subscriber(1, "Иван Петров", "ivan.petrov@example.com")


def _make_type() -> NotificationType:
    return NotificationType(1, "Акции и скидки")


def test_check_subscription_status_active():
    status = check_subscription_status(True, date(2026, 12, 31), TODAY)
    assert status == "Подписка активна"


def test_check_subscription_status_paused():
    status = check_subscription_status(False, date(2026, 12, 31), TODAY)
    assert status == "Подписка приостановлена"


def test_check_subscription_status_expired():
    status = check_subscription_status(True, date(2026, 1, 1), TODAY)
    assert status == "Подписка истекла"


def test_subscription_creation():
    subscriber = _make_subscriber()
    notification_type = _make_type()
    subscriptions = []

    subscription = create_subscription(
        subscriptions, subscriber, notification_type, "email",
        date(2026, 12, 31), TODAY,
    )

    assert subscription is not None
    assert subscription.subscriber is subscriber
    assert subscription.notification_type is notification_type
    assert subscription.is_active


def test_subscription_days_until_renewal():
    subscriber = _make_subscriber()
    notification_type = _make_type()
    subscription = create_subscription(
        [], subscriber, notification_type, "email", date(2026, 10, 4), TODAY,
    )
    assert subscription.days_until_renewal(TODAY) == 10


def test_subscription_format_notification():
    subscriber = _make_subscriber()
    notification_type = _make_type()
    subscription = create_subscription(
        [], subscriber, notification_type, "email", date(2026, 9, 27), TODAY,
    )
    text = subscription.format_notification(TODAY)
    assert "Иван Петров" in text
    assert "Акции и скидки" in text
    assert "Внимание!" in text


def test_subscription_cancel():
    subscriber = _make_subscriber()
    notification_type = _make_type()
    subscription = create_subscription(
        [], subscriber, notification_type, "email", date(2026, 12, 31), TODAY,
    )
    subscription.cancel()
    assert subscription.get_status(TODAY) == "Подписка приостановлена"


def test_is_subscription_active_when_empty():
    subscriber = _make_subscriber()
    notification_type = _make_type()
    assert not is_subscription_active(
        [], subscriber, notification_type, "email", TODAY
    )


def test_duplicate_active_subscription_forbidden():
    subscriber = _make_subscriber()
    notification_type = _make_type()
    subscriptions = []
    create_subscription(
        subscriptions, subscriber, notification_type, "email",
        date(2026, 12, 31), TODAY,
    )
    second = create_subscription(
        subscriptions, subscriber, notification_type, "email",
        date(2026, 12, 31), TODAY,
    )
    assert second is None


def test_cancelled_subscription_frees_channel():
    subscriber = _make_subscriber()
    notification_type = _make_type()
    subscriptions = []
    first = create_subscription(
        subscriptions, subscriber, notification_type, "email",
        date(2026, 12, 31), TODAY,
    )
    first.cancel()
    second = create_subscription(
        subscriptions, subscriber, notification_type, "email",
        date(2026, 12, 31), TODAY,
    )
    assert second is not None


def test_cancel_subscription_by_id():
    subscriber = _make_subscriber()
    notification_type = _make_type()
    subscriptions = []
    subscription = create_subscription(
        subscriptions, subscriber, notification_type, "email",
        date(2026, 12, 31), TODAY,
    )
    assert cancel_subscription(subscriptions, subscription.id)
    assert subscription.get_status(TODAY) == "Подписка приостановлена"
