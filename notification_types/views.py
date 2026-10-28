from datetime import date

from django.shortcuts import render

from db.database import get_connection
from db.queries import (
    count_active_subscriptions,
    get_available_types,
    get_notification_type,
    get_notification_types,
    get_subscriber,
    get_subscribers,
)


def notification_types(request):
    conn = get_connection()
    try:
        types_list = get_notification_types(conn)
    finally:
        conn.close()

    context = {
        "notification_types": types_list,
    }

    return render(
        request,
        "notification_types/type_list.html",
        context,
    )


def notification_type_detail(request, type_id):
    conn = get_connection()
    try:
        notification_type = get_notification_type(conn, type_id)
        active_count = 0
        if notification_type is not None:
            active_count = count_active_subscriptions(
                conn,
                type_id,
                date.today(),
            )
    finally:
        conn.close()

    context = {
        "notification_type": notification_type,
        "active_count": active_count,
    }

    return render(
        request,
        "notification_types/type_detail.html",
        context,
        status=404 if notification_type is None else 200,
    )


def available_types(request):
    """Типы, на которые подписчик ещё не подписан на выбранную дату."""
    subscriber_value = request.GET.get("subscriber", "")
    date_value = request.GET.get("date", "")
    error = None
    result = None
    subscriber = None

    conn = get_connection()
    try:
        subscribers_list = get_subscribers(conn)
        if subscriber_value or date_value:
            try:
                subscriber_id = int(subscriber_value)
                on_date = date.fromisoformat(date_value)
            except ValueError:
                error = "Выберите подписчика и укажите дату."
            else:
                subscriber = get_subscriber(conn, subscriber_id)
                if subscriber is None:
                    error = "Подписчик не найден."
                else:
                    result = get_available_types(conn, subscriber_id, on_date)
    finally:
        conn.close()

    context = {
        "subscribers": subscribers_list,
        "selected_subscriber": subscriber_value,
        "selected_date": date_value or date.today().isoformat(),
        "subscriber": subscriber,
        "result": result,
        "error": error,
    }

    return render(
        request,
        "notification_types/available_types.html",
        context,
        status=400 if error else 200,
    )
