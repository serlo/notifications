from django.contrib import admin
from django.urls import include, path
from . import views

app_name = "notifications"
urlpatterns = [
    path(
        "<str:content_provider_id>/<str:entity_id>/<str:format>",
        views.index,
        name="index",
    )
]
