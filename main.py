"""
Сервис управления подписками на уведомления.
Начальный сценарий (ПР1): проверка одной подписки пользователя
на конкретный тип уведомлений.
"""

from datetime import date

subscriber_name = "Иван Петров"
subscriber_email = "ivan.petrov@example.com"
notification_type = "Акции и скидки"
delivery_channel = "email"
subscription_active = True
subscription_end_date = date(2026, 12, 31)
today = date.today()


def validate_email(email):
    """Простейшая валидация email: наличие '@' и '.' после него."""
    if "@" not in email:
        return False
    local_part, _, domain_part = email.partition("@")
    if len(local_part) == 0 or "." not in domain_part:
        return False
    return True


def check_subscription_status(is_active, end_date, current_date):
    """
    Определяет текстовый статус подписки на основе флага активности
    и срока действия.
    """
    if not is_active:
        return "Подписка приостановлена"
    if current_date > end_date:
        return "Подписка истекла"
    return "Подписка активна"


def days_until_renewal(end_date, current_date):
    """
    Считает количество дней до окончания подписки.
    Если срок уже истёк, возвращает 0 (преобразование типов: timedelta -> int).
    """
    delta = end_date - current_date
    days_left = int(delta.days)
    if days_left < 0:
        return 0
    return days_left


def format_notification(name, notif_type, channel, days_left):
    """Формирует текст уведомления для подписчика."""
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



print("=== Сервис управления подписками на уведомления ===")
print(f"Подписчик: {subscriber_name}")
print(f"Email: {subscriber_email}")

email_is_valid = validate_email(subscriber_email)
print(f"Email корректен: {email_is_valid}")

status = check_subscription_status(subscription_active, subscription_end_date, today)
print(f"Статус подписки: {status}")

remaining_days = days_until_renewal(subscription_end_date, today)
print(f"Дней до окончания подписки: {remaining_days}")

if email_is_valid and status == "Подписка активна":
    notification_text = format_notification(
        subscriber_name, notification_type, delivery_channel, remaining_days
    )
    print(notification_text)
else:
    print("Уведомление не отправлено: подписка неактивна или email некорректен")
