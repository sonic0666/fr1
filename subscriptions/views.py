from django.conf import settings
from django.shortcuts import render

from models.subscriptions import find_subscription_by_id
from storage import (
    load_notification_types,
    load_subscribers,
    load_subscriptions,
)

DATA_DIR = settings.BASE_DIR / "data"
TYPES_FILE = str(DATA_DIR / "notification_types.json")
SUBSCRIBERS_FILE = str(DATA_DIR / "subscribers.json")
SUBSCRIPTIONS_FILE = str(DATA_DIR / "subscriptions.json")


def _load_subscriptions():
    types_list = load_notification_types(TYPES_FILE)
    subscribers_list = load_subscribers(SUBSCRIBERS_FILE)
    return load_subscriptions(
        SUBSCRIPTIONS_FILE,
        types_list,
        subscribers_list,
    )


def subscriptions(request):
    context = {
        "subscriptions": _load_subscriptions(),
    }

    return render(
        request,
        "subscriptions/subscription_list.html",
        context,
    )


def subscription_detail(request, subscription_id):
    subscription = find_subscription_by_id(
        _load_subscriptions(),
        subscription_id,
    )

    context = {
        "subscription": subscription,
    }

    return render(
        request,
        "subscriptions/subscription_detail.html",
        context,
        status=404 if subscription is None else 200,
    )
