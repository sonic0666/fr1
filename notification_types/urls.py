from django.urls import path

from . import views

urlpatterns = [
    path("", views.notification_types, name="notification_types"),
    path(
        "<int:type_id>/",
        views.notification_type_detail,
        name="notification_type_detail",
    ),
]
