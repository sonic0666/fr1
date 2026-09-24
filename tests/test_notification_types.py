"""Тесты функций работы с каталогом типов уведомлений."""

from notification_types import (
    add_notification_type,
    find_notification_type,
    sort_notification_types,
)


def test_add_notification_type():
    types = {}
    add_notification_type(types, "Акции и скидки")
    assert len(types) == 1


def test_find_notification_type():
    types = {}
    add_notification_type(types, "Акции и скидки")
    assert find_notification_type(types, "акции")


def test_sort_notification_types():
    types = {}
    add_notification_type(types, "Системные оповещения")
    add_notification_type(types, "Акции и скидки")
    ordered = sort_notification_types(types)
    assert ordered[0]["name"] == "Акции и скидки"
