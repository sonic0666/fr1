"""Тесты веб-интерфейса: маршруты, коды ответов и страница 404."""

import pytest
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
    assert reverse("index") == "/"
    assert reverse("notification_types") == "/types/"
    assert reverse("notification_type_detail", args=[1]) == "/types/1/"
    assert reverse("subscriptions") == "/subscriptions/"
    assert reverse("subscription_detail", args=[2]) == "/subscriptions/2/"
