from datetime import date

from django.shortcuts import render

from db.database import get_connection
from db.queries import (
    CHANNELS,
    get_channel_statistics,
    get_popular_types,
    get_subscription,
    get_subscriptions,
    get_type_statistics,
)


def subscriptions(request):
    channel = request.GET.get("channel")
    if channel not in CHANNELS:
        channel = None

    conn = get_connection()
    try:
        subscriptions_list = get_subscriptions(conn, date.today(), channel)
    finally:
        conn.close()

    context = {
        "subscriptions": subscriptions_list,
        "channels": CHANNELS,
        "selected_channel": channel,
    }

    return render(
        request,
        "subscriptions/subscription_list.html",
        context,
    )


def subscription_detail(request, subscription_id):
    conn = get_connection()
    try:
        subscription = get_subscription(conn, subscription_id, date.today())
    finally:
        conn.close()

    context = {
        "subscription": subscription,
    }

    return render(
        request,
        "subscriptions/subscription_detail.html",
        context,
        status=404 if subscription is None else 200,
    )


def statistics(request):
    conn = get_connection()
    try:
        context = {
            "type_statistics": get_type_statistics(conn),
            "channel_statistics": get_channel_statistics(conn),
            "popular_types": get_popular_types(conn),
            "today": date.today(),
        }
    finally:
        conn.close()

    return render(
        request,
        "subscriptions/statistics.html",
        context,
    )
