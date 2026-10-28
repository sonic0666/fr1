"""Тесты веб-интерфейса: маршруты, коды ответов и страница 404."""

from types import SimpleNamespace

import pytest
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from django.test import Client
from django.test.utils import override_settings
from django.urls import reverse


@pytest.fixture
def client():
    return Client()


@pytest.mark.parametrize(
    "url",
    ["/", "/types/", "/types/1/", "/subscriptions/", "/subscriptions/1/"],
)
def test_pages_open(client, url):
    response = client.get(url)
    assert response.status_code == 200
    assert "bootstrap" in response.content.decode("utf-8")


def test_missing_notification_type_returns_404(client):
    response = client.get("/types/9999/")
    assert response.status_code == 404
    assert "Тип уведомлений не найден" in response.content.decode("utf-8")


def test_missing_subscription_returns_404(client):
    response = client.get("/subscriptions/9999/")
    assert response.status_code == 404
    assert "Подписка не найдена" in response.content.decode("utf-8")


def test_custom_404_page_for_unknown_url(client):
    with override_settings(DEBUG=False):
        response = client.get("/nonexistent/")
    names = [template.name for template in response.templates]
    assert response.status_code == 404
    assert "404.html" in names
    assert "404 – страница не найдена" in response.content.decode("utf-8")


def test_url_names_build_expected_paths():
    assert reverse("homepage:index") == "/"
    assert reverse("notification_types:list") == "/types/"
    assert reverse("notification_types:detail", args=[1]) == "/types/1/"
    assert reverse("subscriptions:list") == "/subscriptions/"
    assert reverse("subscriptions:detail", args=[2]) == "/subscriptions/2/"


def test_homepage_uses_base_template(client):
    response = client.get("/")
    names = [template.name for template in response.templates]
    assert "homepage/index.html" in names
    assert "base.html" in names
    assert "includes/navigation.html" in names


def test_type_list_uses_card_include(client):
    response = client.get("/types/")
    names = [template.name for template in response.templates]
    assert "notification_types/type_list.html" in names
    assert "notification_types/includes/type_card.html" in names
    assert 'href="/types/1/"' in response.content.decode("utf-8")


def test_subscription_pages_use_status_include(client):
    for url in ("/subscriptions/", "/subscriptions/1/"):
        response = client.get(url)
        names = [template.name for template in response.templates]
        assert "subscriptions/includes/subscription_status.html" in names


@pytest.mark.parametrize(
    "is_active, is_expired, text",
    [
        (True, False, "Активна"),
        (True, True, "Истекла"),
        (False, False, "Приостановлена"),
        (False, True, "Приостановлена"),
    ],
)
def test_subscription_status_include(is_active, is_expired, text):
    subscription = SimpleNamespace(is_active=is_active, is_expired=is_expired)
    html = render_to_string(
        "subscriptions/includes/subscription_status.html",
        {"subscription": subscription},
    )
    assert text in html


@pytest.mark.parametrize(
    "path",
    [
        "homepage/css/style.css",
        "homepage/js/main.js",
        "homepage/img/logo.png",
    ],
)
def test_static_files_are_found(path):
    assert finders.find(path)


def test_base_template_links_static_files(client):
    html = client.get("/").content.decode("utf-8")
    assert "/static/homepage/css/style.css" in html
    assert "/static/homepage/js/main.js" in html
    assert "/static/homepage/img/logo.png" in html
    assert 'id="current-year"' in html


def test_page_function_is_removed():
    import homepage.views

    assert not hasattr(homepage.views, "page")


def test_type_list_uses_length_filter(client):
    html = client.get("/types/").content.decode("utf-8")
    assert "Всего типов:" in html


def test_subscription_list_from_database(client, sample_db):
    response = client.get("/subscriptions/")
    html = response.content.decode("utf-8")
    assert response.status_code == 200
    assert "Иван Петров" in html
    assert "Акции и скидки" in html
    assert "31.12.2099" in html
    assert html.count("subscription-card") == 4


def test_subscription_list_filtered_by_channel(client, sample_db):
    html = client.get("/subscriptions/?channel=push").content.decode("utf-8")
    assert html.count("subscription-card") == 1
    assert "Подписка №2" in html


def test_subscription_list_ignores_unknown_channel(client, sample_db):
    html = client.get("/subscriptions/?channel=fax").content.decode("utf-8")
    assert html.count("subscription-card") == 4


def test_subscription_statuses_from_database(client, sample_db):
    assert "Активна" in client.get("/subscriptions/1/").content.decode()
    assert "Истекла" in client.get("/subscriptions/2/").content.decode()
    assert "Приостановлена" in client.get("/subscriptions/4/").content.decode()


def test_sql_injection_in_channel_is_harmless(client, sample_db):
    url = "/subscriptions/?channel=email'%20OR%20'1'='1"
    html = client.get(url).content.decode("utf-8")
    assert html.count("subscription-card") == 4


def test_type_detail_counts_active_subscriptions(client, sample_db):
    html = client.get("/types/1/").content.decode("utf-8")
    assert "активных подписок: 2" in html
    html = client.get("/types/2/").content.decode("utf-8")
    assert "активных подписок нет" in html


def test_homepage_shows_row_counts(client, sample_db):
    html = client.get("/").content.decode("utf-8")
    assert "типов уведомлений – 3" in html
    assert "подписчиков – 2" in html
    assert "подписок – 4" in html


def test_available_types_page_without_parameters(client, sample_db):
    response = client.get("/types/available/")
    assert response.status_code == 200
    assert "Иван Петров" in response.content.decode("utf-8")


def test_available_types_excludes_subscribed(client, sample_db):
    url = "/types/available/?subscriber=1&date=2026-10-29"
    html = client.get(url).content.decode("utf-8")
    assert "Новости сервиса" in html
    assert "Системные оповещения" in html
    assert "Акции и скидки</a>" not in html


def test_available_types_depends_on_date(client, sample_db):
    url = "/types/available/?subscriber=1&date=2019-01-01"
    html = client.get(url).content.decode("utf-8")
    assert "Новости сервиса" not in html


@pytest.mark.parametrize(
    "query",
    [
        "subscriber=abc&date=2026-10-29",
        "subscriber=1&date=not-a-date",
        "subscriber=1",
        "subscriber=999&date=2026-10-29",
    ],
)
def test_available_types_rejects_bad_input(client, sample_db, query):
    response = client.get("/types/available/?" + query)
    assert response.status_code == 400


def test_statistics_page(client, sample_db):
    response = client.get("/subscriptions/statistics/")
    html = response.content.decode("utf-8")
    assert response.status_code == 200
    assert "Статистика подписок" in html
    assert "Популярные типы" in html
    assert "<li>Акции и скидки – 2</li>" in html


def test_statistics_url_name():
    assert reverse("subscriptions:statistics") == "/subscriptions/statistics/"
    assert reverse("notification_types:available") == "/types/available/"
