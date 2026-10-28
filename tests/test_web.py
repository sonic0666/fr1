"""Тесты веб-интерфейса: маршруты, коды ответов и страница 404."""

from types import SimpleNamespace

import pytest
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
    assert response.status_code == 404
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
