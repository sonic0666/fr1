from django.urls import path

from . import views

app_name = "subscriptions"

urlpatterns = [
    path("", views.subscriptions, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:subscription_id>/", views.subscription_detail, name="detail"),
]
