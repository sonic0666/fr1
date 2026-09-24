"""Тесты функций работы с подписчиками."""

from subscribers import add_subscriber, find_subscriber, validate_email


def test_validate_email_valid():
    assert validate_email("ivan.petrov@example.com")


def test_validate_email_invalid():
    assert not validate_email("not-an-email")


def test_add_subscriber():
    subscribers = {}
    add_subscriber(subscribers, "Иван Петров", "ivan.petrov@example.com")
    assert len(subscribers) == 1


def test_add_subscriber_rejects_invalid_email():
    subscribers = {}
    try:
        add_subscriber(subscribers, "Иван", "плохой-email")
        assert False, "некорректный email не должен приниматься"
    except ValueError:
        pass


def test_find_subscriber():
    subscribers = {}
    add_subscriber(subscribers, "Иван Петров", "ivan.petrov@example.com")
    assert find_subscriber(subscribers, "иван")
