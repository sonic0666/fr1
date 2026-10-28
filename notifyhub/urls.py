"""Корневая маршрутизация проекта NotifyHub."""

from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("types/", include("notification_types.urls")),
    path("subscriptions/", include("subscriptions.urls")),
]
