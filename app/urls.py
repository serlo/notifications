from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health", views.health, name="health",),
    # TODO: only load in dev
    path("pact/", include("pact.urls")),
    path("", include("notifications.urls")),
]
