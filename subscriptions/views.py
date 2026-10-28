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


def _load_all():
    types_list = load_notification_types(TYPES_FILE)
    subscribers_list = load_subscribers(SUBSCRIBERS_FILE)
    subscriptions_list = load_subscriptions(
        SUBSCRIPTIONS_FILE, types_list, subscribers_list
    )
    return subscriptions_list


def subscription_list(request):
    items = ""
    for item in _load_all():
        state = "активна" if item.is_active else "приостановлена"
        items += (
            '<li class="list-group-item">'
            f'<a href="/subscriptions/{item.id}/">№{item.id}</a> – '
            f"{item.subscriber.name}, {item.notification_type.name} "
            f"({item.channel}), {state}</li>"
        )
    content = f"""
    <h1>Подписки</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("NotifyHub – подписки", content))


def subscription_detail(request, subscription_id):
    item = find_subscription_by_id(_load_all(), subscription_id)
    if item is None:
        content = """
        <h1 class="text-danger">Подписка не найдена</h1>
        <a href="/subscriptions/">← к списку подписок</a>
        """
        return HttpResponse(page("Подписка не найдена", content), status=404)
    state = "активна" if item.is_active else "приостановлена"
    content = f"""
    <h1>Подписка №{item.id}</h1>
    <p><strong>Подписчик:</strong> {item.subscriber.name}</p>
    <p><strong>Тип уведомлений:</strong> {item.notification_type.name}</p>
    <p><strong>Канал:</strong> {item.channel}</p>
    <p><strong>Действует до:</strong> {item.end_date}</p>
    <p><strong>Статус:</strong> {state}</p>
    <a href="/subscriptions/">← к списку подписок</a>
    """
    return HttpResponse(page(f"Подписка №{item.id}", content))
