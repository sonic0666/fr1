from django.urls import path

from . import views

app_name = "notification_types"

urlpatterns = [
    path("", views.notification_types, name="list"),
    path("available/", views.available_types, name="available"),
    path("<int:type_id>/", views.notification_type_detail, name="detail"),
]
