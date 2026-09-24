"""Тесты класса Subscriber и функций работы с коллекцией подписчиков."""

from models import Subscriber
from models.subscribers import add_subscriber, find_subscriber


def test_subscriber_creation():
    subscriber = Subscriber(1, "Иван Петров", "ivan.petrov@example.com")

    assert subscriber.id == 1
    assert subscriber.name == "Иван Петров"
    assert subscriber.email == "ivan.petrov@example.com"


def test_subscriber_str():
    subscriber = Subscriber(1, "Иван Петров", "ivan.petrov@example.com")
    assert str(subscriber) == "Иван Петров (ivan.petrov@example.com)"


def test_validate_email_valid():
    assert Subscriber.validate_email("ivan.petrov@example.com")


def test_validate_email_invalid():
    assert not Subscriber.validate_email("not-an-email")


def test_subscriber_from_data():
    data = {"id": 1, "name": "Иван Петров", "email": "ivan@example.com"}
    subscriber = Subscriber.from_data(data)
    assert subscriber.id == 1
    assert subscriber.name == "Иван Петров"


def test_add_subscriber():
    subscribers = []
    add_subscriber(subscribers, "Иван Петров", "ivan.petrov@example.com")
    assert len(subscribers) == 1


def test_add_subscriber_rejects_invalid_email():
    subscribers = []
    try:
        add_subscriber(subscribers, "Иван", "плохой-email")
        assert False, "некорректный email не должен приниматься"
    except ValueError:
        pass


def test_find_subscriber():
    subscribers = []
    add_subscriber(subscribers, "Иван Петров", "ivan.petrov@example.com")
    assert find_subscriber(subscribers, "иван")
