from django.conf import settings
from django.http import HttpResponse

from homepage.views import page
from models.notification_types import find_notification_type_by_id
from storage import load_notification_types

TYPES_FILE = str(settings.BASE_DIR / "data" / "notification_types.json")


def type_list(request):
    items = ""
    for item in load_notification_types(TYPES_FILE):
        items += (
            '<li class="list-group-item">'
            f'<a href="/types/{item.id}/">{item.name}</a></li>'
        )
    content = f"""
    <h1>Типы уведомлений</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("NotifyHub – типы уведомлений", content))


def type_detail(request, type_id):
    types_list = load_notification_types(TYPES_FILE)
    item = find_notification_type_by_id(types_list, type_id)
    if item is None:
        content = """
        <h1 class="text-danger">Тип уведомлений не найден</h1>
        <a href="/types/">← к списку типов</a>
        """
        return HttpResponse(page("Тип не найден", content), status=404)
    content = f"""
    <h1>{item.name}</h1>
    <p><strong>ID:</strong> {item.id}</p>
    <a href="/types/">← к списку типов</a>
    """
    return HttpResponse(page(f"{item.name} – NotifyHub", content))
