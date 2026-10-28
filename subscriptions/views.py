from datetime import date

from django.conf import settings
from django.http import HttpResponse

from homepage.views import page
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

STATUS_VIEW = {
    "Подписка активна": ("активна", "bg-success"),
    "Подписка приостановлена": ("приостановлена", "bg-secondary"),
    "Подписка истекла": ("истекла", "bg-warning text-dark"),
}


def _load_subscriptions():
    types_list = load_notification_types(TYPES_FILE)
    subscribers_list = load_subscribers(SUBSCRIBERS_FILE)
    return load_subscriptions(
        SUBSCRIPTIONS_FILE,
        types_list,
        subscribers_list,
    )


def subscriptions(request):
    today = date.today()

    items = ""
    for subscription in _load_subscriptions():
        status, badge = STATUS_VIEW[subscription.get_status(today)]
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/subscriptions/{subscription.id}/">
                {subscription.subscriber.name} –
                {subscription.notification_type.name}
            </a>
            <span class="badge {badge}">
                {status}
            </span>
        </li>
        """
    content = f"""
    <h1>Подписки</h1>
    <ul class="list-group">
        {items}
    </ul>
    """
    return HttpResponse(
        page("NotifyHub – подписки", content)
    )


def subscription_detail(request, subscription_id):
    subscription = find_subscription_by_id(
        _load_subscriptions(),
        subscription_id,
    )

    if subscription is None:
        content = """
        <h1 class="text-danger">
            Подписка не найдена
        </h1>
        <a href="/subscriptions/"
           class="btn btn-outline-secondary">
            ← к списку подписок
        </a>
        """
        return HttpResponse(
            page("Подписка не найдена", content),
            status=404,
        )

    status, badge = STATUS_VIEW[subscription.get_status(date.today())]

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                Подписка №{subscription.id}
            </h5>
            <p class="card-text">
                Подписчик: {subscription.subscriber.name}
            </p>
            <p class="card-text">
                Тип уведомлений: {subscription.notification_type.name}
            </p>
            <p class="card-text">
                Канал: {subscription.channel}
            </p>
            <p class="card-text">
                Действует до: {subscription.end_date}
            </p>
            <p class="card-text">
                Статус:
                <span class="badge {badge}">
                    {status}
                </span>
            </p>
            <a href="/subscriptions/"
               class="btn btn-outline-secondary">
                ← к списку подписок
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Подписка №{subscription.id}", content),
        status=200,
    )
