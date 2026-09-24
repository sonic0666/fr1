"""Вспомогательные функции ввода данных с обработкой ошибок."""

from datetime import date


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число, повторяя при ошибке."""
    while True:
        raw_value = input(prompt)
        try:
            return int(raw_value)
        except ValueError:
            print("Введите целое число.")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ГГГГ-ММ-ДД."""
    while True:
        raw_value = input(prompt)
        try:
            return date.fromisoformat(raw_value)
        except ValueError:
            print("Введите дату в формате ГГГГ-ММ-ДД, например 2026-12-31.")


def input_channel(prompt: str) -> str:
    """Запросить у пользователя канал доставки (email/push/sms)."""
    allowed = ("email", "push", "sms")
    while True:
        raw_value = input(prompt).strip().lower()
        if raw_value in allowed:
            return raw_value
        print("Введите один из каналов: email, push, sms.")
