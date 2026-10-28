from django.urls import path

from . import views

app_name = "notification_types"

urlpatterns = [
    path("", views.type_list, name="list"),
    path("<int:type_id>/", views.type_detail, name="detail"),
]
