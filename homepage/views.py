from django.http import HttpResponse

BOOTSTRAP_URL = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)


def page(title, content):
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_URL}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/types/">Типы уведомлений</a>
        <a class="nav-link" href="/subscriptions/">Подписки</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    content = """
    <h1 class="display-4">NotifyHub</h1>
    <p class="lead">Сервис управления подписками на уведомления.</p>
    <p>Основные разделы:</p>
    <a href="/types/" class="btn btn-primary me-2">Типы уведомлений</a>
    <a href="/subscriptions/" class="btn btn-secondary">Подписки</a>
    """
    return HttpResponse(page("NotifyHub", content))
