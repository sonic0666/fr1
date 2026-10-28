from datetime import date

from django.conf import settings
from django.http import HttpResponse

from homepage.views import page
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
    items = ""
    for item in load_notification_types(TYPES_FILE):
        link = f'<a href="/types/{item.id}/">{item.name}</a>'
        items += f'<li class="list-group-item">{link}</li>'
    content = f"""
    <h1>Типы уведомлений</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("NotifyHub – типы уведомлений", content))


def notification_type_detail(request, type_id):
    types_list = load_notification_types(TYPES_FILE)

    notification_type = find_notification_type_by_id(types_list, type_id)

    if notification_type is None:
        content = """
        <h1 class="text-danger">Тип уведомлений не найден</h1>
        <a href="/types/" class="btn btn-outline-secondary">
            ← к списку типов
        </a>
        """
        return HttpResponse(
            page("Тип уведомлений не найден", content),
            status=404,
        )

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
    status = f"активных подписок: {active_count}"
    badge = "bg-success" if active_count else "bg-secondary"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{notification_type.name}</h5>

            <p class="card-text">
                <strong>ID:</strong> {notification_type.id}
            </p>

            <p class="card-text">
                Подписчики на сегодня:
                <span class="badge {badge}">
                    {status}
                </span>
            </p>

            <a href="/types/"
               class="btn btn-outline-secondary">
                ← к списку типов
            </a>
        </div>
    </div>
    """

    return HttpResponse(
        page(notification_type.name, content),
        status=200,
    )
