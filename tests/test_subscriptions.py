"""Тесты функций работы с подписками на уведомления."""

from datetime import date

from subscribers import add_subscriber
from subscriptions import (
    cancel_subscription,
    check_subscription_status,
    create_subscription,
    days_until_renewal,
    format_notification,
    is_subscription_active,
)

TODAY = date(2026, 9, 24)


def test_check_subscription_status_active():
    status = check_subscription_status(True, date(2026, 12, 31), TODAY)
    assert status == "Подписка активна"


def test_check_subscription_status_paused():
    status = check_subscription_status(False, date(2026, 12, 31), TODAY)
    assert status == "Подписка приостановлена"


def test_check_subscription_status_expired():
    status = check_subscription_status(True, date(2026, 1, 1), TODAY)
    assert status == "Подписка истекла"


def test_days_until_renewal():
    assert days_until_renewal(date(2026, 10, 4), TODAY) == 10


def test_days_until_renewal_expired_is_zero():
    assert days_until_renewal(date(2026, 1, 1), TODAY) == 0


def test_format_notification_contains_name_and_type():
    text = format_notification("Иван", "Акции и скидки", "email", 3)
    assert "Иван" in text
    assert "Акции и скидки" in text
    assert "Внимание!" in text


def test_is_subscription_active_when_empty():
    assert not is_subscription_active([], 1, 1, "email", TODAY)


def test_create_subscription():
    subscribers = {}
    subscriber_id = add_subscriber(subscribers, "Иван", "ivan@example.com")
    subscriptions = []
    create_subscription(
        subscribers, subscriptions, subscriber_id, 1, "email",
        date(2026, 12, 31), TODAY,
    )
    assert is_subscription_active(
        subscriptions, subscriber_id, 1, "email", TODAY
    )


def test_duplicate_active_subscription_forbidden():
    subscribers = {}
    subscriber_id = add_subscriber(subscribers, "Иван", "ivan@example.com")
    subscriptions = []
    create_subscription(
        subscribers, subscriptions, subscriber_id, 1, "email",
        date(2026, 12, 31), TODAY,
    )
    try:
        create_subscription(
            subscribers, subscriptions, subscriber_id, 1, "email",
            date(2026, 12, 31), TODAY,
        )
        assert False, "повторная активная подписка недопустима"
    except ValueError:
        pass


def test_cancel_subscription():
    subscribers = {}
    subscriber_id = add_subscriber(subscribers, "Иван", "ivan@example.com")
    subscriptions = []
    subscription = create_subscription(
        subscribers, subscriptions, subscriber_id, 1, "email",
        date(2026, 12, 31), TODAY,
    )
    assert cancel_subscription(subscriptions, subscription["id"])
    assert not is_subscription_active(
        subscriptions, subscriber_id, 1, "email", TODAY
    )
