from django.urls import path

from . import views

app_name = "subscriptions"

urlpatterns = [
    path("", views.subscription_list, name="list"),
    path("<int:subscription_id>/", views.subscription_detail, name="detail"),
]
