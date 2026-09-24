"""Точка запуска приложения «Сервис управления подписками на уведомления»."""

from datetime import date
from pathlib import Path

from models import NotificationType, Subscriber, Subscription
from models.notification_types import (
    add_notification_type,
    find_notification_type,
    find_notification_type_by_id,
    sort_notification_types,
)
from models.subscribers import (
    add_subscriber,
    find_subscriber,
    find_subscriber_by_id,
)
from models.subscriptions import cancel_subscription, create_subscription
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


def show_subscribers(subscribers: list[Subscriber]) -> None:
    """Вывести список подписчиков."""
    if not subscribers:
        print("Подписчиков пока нет.")
        return
    for subscriber in subscribers:
        print(f"{subscriber.id}. {subscriber}")


def show_notification_types(
    notification_types: list[NotificationType],
) -> None:
    """Вывести список типов уведомлений."""
    if not notification_types:
        print("Каталог типов уведомлений пуст.")
        return
    for item in notification_types:
        print(f"{item.id}. {item}")


def show_subscriptions(subscriptions: list[Subscription]) -> None:
    """Вывести список подписок с их текущим статусом."""
    if not subscriptions:
        print("Подписок пока нет.")
        return
    for subscription in subscriptions:
        print(f"{subscription.id}. {subscription}")


def create_new_subscription(
    subscriptions: list[Subscription],
    subscribers: list[Subscriber],
    notification_types: list[NotificationType],
) -> None:
    """Провести пользовательский сценарий оформления подписки."""
    subscriber_id = input_int("Id подписчика: ")
    subscriber = find_subscriber_by_id(subscribers, subscriber_id)
    if subscriber is None:
        print("Подписчик не найден.")
        return

    type_id = input_int("Id типа уведомлений: ")
    notification_type = find_notification_type_by_id(
        notification_types, type_id
    )
    if notification_type is None:
        print("Тип уведомлений не найден.")
        return

    channel = input_channel("Канал (email/push/sms): ")
    end_date = input_date("Дата окончания (ГГГГ-ММ-ДД): ")

    subscription = create_subscription(
        subscriptions, subscriber, notification_type, channel, end_date,
        date.today(),
    )
    if subscription is not None:
        print(f"Подписка оформлена, id={subscription.id}.")
    else:
        print("У подписчика уже есть активная подписка на этот тип и канал.")


def main() -> None:
    """Запустить меню приложения и обработать выбор пользователя."""
    subscribers = load_subscribers(str(SUBSCRIBERS_FILE))
    notification_types = load_notification_types(str(TYPES_FILE))
    subscriptions = load_subscriptions(
        str(SUBSCRIPTIONS_FILE), notification_types, subscribers
    )

    while True:
        print(MENU)
        choice = input("Выберите действие: ")

        if choice == "1":
            show_subscribers(subscribers)
        elif choice == "2":
            name = input("Имя подписчика: ")
            email = input("Email: ")
            try:
                subscriber = add_subscriber(subscribers, name, email)
                save_subscribers(str(SUBSCRIBERS_FILE), subscribers)
                print(f"Подписчик добавлен, id={subscriber.id}.")
            except ValueError as error:
                print(f"Не удалось добавить подписчика: {error}")
        elif choice == "3":
            query = input("Имя или email: ")
            show_subscribers(find_subscriber(subscribers, query))
        elif choice == "4":
            show_notification_types(notification_types)
        elif choice == "5":
            name = input("Название типа уведомлений: ")
            notification_type = add_notification_type(
                notification_types, name
            )
            save_notification_types(str(TYPES_FILE), notification_types)
            print(f"Тип уведомлений добавлен, id={notification_type.id}.")
        elif choice == "6":
            query = input("Название: ")
            show_notification_types(
                find_notification_type(notification_types, query)
            )
        elif choice == "7":
            for item in sort_notification_types(notification_types):
                print(item)
        elif choice == "8":
            create_new_subscription(
                subscriptions, subscribers, notification_types
            )
            save_subscriptions(str(SUBSCRIPTIONS_FILE), subscriptions)
        elif choice == "9":
            subscription_id = input_int("Id подписки: ")
            if cancel_subscription(subscriptions, subscription_id):
                save_subscriptions(str(SUBSCRIPTIONS_FILE), subscriptions)
                print("Подписка приостановлена.")
            else:
                print("Подписка не найдена.")
        elif choice == "10":
            show_subscriptions(subscriptions)
        elif choice == "11":
            subscription_id = input_int("Id подписки: ")
            subscription = next(
                (s for s in subscriptions if s.id == subscription_id), None
            )
            if subscription is None:
                print("Подписка не найдена.")
                continue
            today = date.today()
            print(f"Статус подписки: {subscription.get_status(today)}")
            days_left = subscription.days_until_renewal(today)
            print(f"Дней до окончания подписки: {days_left}")
            if subscription.get_status(today) == "Подписка активна":
                print(subscription.format_notification(today))
            else:
                print("Уведомление не отправлено: подписка неактивна.")
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неизвестный пункт меню, попробуйте снова.")


if __name__ == "__main__":
    main()
