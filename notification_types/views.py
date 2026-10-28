from datetime import date

from django.conf import settings
from django.shortcuts import render

from models.notification_types import find_notification_type_by_id
from storage import (
    load_notification_types,
    load_subscribers,
    load_subscriptions,
)

DATA_DIR = settings.BASE_DIR / "data"
TYPES_FILE = str(DATA_DIR / "notification_types.json")
SUBSCRIBERS_FILE = str(DATA_DIR / "subscribers.json")
SUBSCRIPTIONS_FILE = str(DATA_DIR / "subscriptions.json")


def notification_types(request):
    types_list = load_notification_types(TYPES_FILE)

    context = {
        "notification_types": types_list,
    }

    return render(
        request,
        "notification_types/type_list.html",
        context,
    )


def notification_type_detail(request, type_id):
    types_list = load_notification_types(TYPES_FILE)
    notification_type = find_notification_type_by_id(types_list, type_id)

    active_count = 0
    if notification_type is not None:
        subscribers_list = load_subscribers(SUBSCRIBERS_FILE)
        subscriptions_list = load_subscriptions(
            SUBSCRIPTIONS_FILE,
            types_list,
            subscribers_list,
        )
        today = date.today()
        active_count = sum(
            1
            for subscription in subscriptions_list
            if subscription.notification_type is notification_type
            and subscription.get_status(today) == "Подписка активна"
        )

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
