"""Точка запуска приложения «Сервис управления подписками на уведомления»."""

from datetime import date
from pathlib import Path

from notification_types import (
    add_notification_type,
    find_notification_type,
    sort_notification_types,
)
from subscribers import add_subscriber, find_subscriber
from subscriptions import (
    cancel_subscription,
    check_subscription_status,
    create_subscription,
    days_until_renewal,
    format_notification,
)
from storage import (
    load_notification_types,
    load_subscribers,
    load_subscriptions,
    save_notification_types,
    save_subscribers,
    save_subscriptions,
)
from utils import input_channel, input_date, input_int

DATA_DIR = Path(__file__).parent / "data"
SUBSCRIBERS_FILE = DATA_DIR / "subscribers.json"
TYPES_FILE = DATA_DIR / "notification_types.json"
SUBSCRIPTIONS_FILE = DATA_DIR / "subscriptions.json"

MENU = """
=== Сервис управления подписками на уведомления ===

1. Показать подписчиков
2. Добавить подписчика
3. Найти подписчика
4. Показать типы уведомлений
5. Добавить тип уведомлений
6. Найти тип уведомлений
7. Отсортировать типы уведомлений
8. Оформить подписку
9. Отменить подписку
10. Показать подписки
11. Показать уведомление по подписке
0. Выход
"""


def show_subscribers(subscribers: dict[int, dict]) -> None:
    """Вывести список подписчиков."""
    if not subscribers:
        print("Подписчиков пока нет.")
        return
    for subscriber in subscribers.values():
        print(
            f"{subscriber['id']}. {subscriber['name']} "
            f"({subscriber['email']})"
        )


def show_notification_types(notification_types: dict[int, dict]) -> None:
    """Вывести список типов уведомлений."""
    if not notification_types:
        print("Каталог типов уведомлений пуст.")
        return
    for item in notification_types.values():
        print(f"{item['id']}. {item['name']}")


def show_subscriptions(
    subscriptions: list[dict],
    subscribers: dict[int, dict],
    notification_types: dict[int, dict],
) -> None:
    """Вывести список подписок с их текущим статусом."""
    if not subscriptions:
        print("Подписок пока нет.")
        return
    today = date.today()
    for subscription in subscriptions:
        subscriber = subscribers.get(subscription["subscriber_id"])
        notif_type = notification_types.get(subscription["type_id"])
        subscriber_name = subscriber["name"] if subscriber else "неизвестно"
        type_name = notif_type["name"] if notif_type else "неизвестно"
        status = check_subscription_status(
            subscription["is_active"], subscription["end_date"], today
        )
        print(
            f"{subscription['id']}. {subscriber_name} -> {type_name} "
            f"({subscription['channel']}): {status}"
        )


def main() -> None:
    """Запустить меню приложения и обработать выбор пользователя."""
    subscribers = load_subscribers(str(SUBSCRIBERS_FILE))
    notification_types = load_notification_types(str(TYPES_FILE))
    subscriptions = load_subscriptions(str(SUBSCRIPTIONS_FILE))

    while True:
        print(MENU)
        choice = input("Выберите действие: ")

        if choice == "1":
            show_subscribers(subscribers)
        elif choice == "2":
            name = input("Имя подписчика: ")
            email = input("Email: ")
            try:
                subscriber_id = add_subscriber(subscribers, name, email)
                save_subscribers(str(SUBSCRIBERS_FILE), subscribers)
                print(f"Подписчик добавлен, id={subscriber_id}.")
            except ValueError as error:
                print(f"Не удалось добавить подписчика: {error}")
        elif choice == "3":
            query = input("Имя или email: ")
            show_subscribers(find_subscriber(subscribers, query))
        elif choice == "4":
            show_notification_types(notification_types)
        elif choice == "5":
            name = input("Название типа уведомлений: ")
            type_id = add_notification_type(notification_types, name)
            save_notification_types(str(TYPES_FILE), notification_types)
            print(f"Тип уведомлений добавлен, id={type_id}.")
        elif choice == "6":
            query = input("Название: ")
            show_notification_types(
                find_notification_type(notification_types, query)
            )
        elif choice == "7":
            for item in sort_notification_types(notification_types):
                print(item["name"])
        elif choice == "8":
            subscriber_id = input_int("Id подписчика: ")
            type_id = input_int("Id типа уведомлений: ")
            channel = input_channel("Канал (email/push/sms): ")
            end_date = input_date("Дата окончания (ГГГГ-ММ-ДД): ")
            try:
                create_subscription(
                    subscribers, subscriptions, subscriber_id, type_id,
                    channel, end_date, date.today(),
                )
                save_subscriptions(str(SUBSCRIPTIONS_FILE), subscriptions)
                print("Подписка оформлена.")
            except (KeyError, ValueError) as error:
                print(f"Не удалось оформить подписку: {error}")
        elif choice == "9":
            subscription_id = input_int("Id подписки: ")
            if cancel_subscription(subscriptions, subscription_id):
                save_subscriptions(str(SUBSCRIPTIONS_FILE), subscriptions)
                print("Подписка приостановлена.")
            else:
                print("Подписка не найдена.")
        elif choice == "10":
            show_subscriptions(subscriptions, subscribers, notification_types)
        elif choice == "11":
            subscription_id = input_int("Id подписки: ")
            subscription = next(
                (s for s in subscriptions if s["id"] == subscription_id),
                None,
            )
            if subscription is None:
                print("Подписка не найдена.")
                continue
            subscriber = subscribers.get(subscription["subscriber_id"])
            notif_type = notification_types.get(subscription["type_id"])
            today = date.today()
            status = check_subscription_status(
                subscription["is_active"], subscription["end_date"], today
            )
            print(f"Статус подписки: {status}")
            days_left = days_until_renewal(subscription["end_date"], today)
            print(f"Дней до окончания подписки: {days_left}")
            if subscriber and notif_type and status == "Подписка активна":
                print(
                    format_notification(
                        subscriber["name"],
                        notif_type["name"],
                        subscription["channel"],
                        days_left,
                    )
                )
            else:
                print(
                    "Уведомление не отправлено: подписка неактивна "
                    "или данные не найдены"
                )
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неизвестный пункт меню, попробуйте снова.")


if __name__ == "__main__":
    main()
