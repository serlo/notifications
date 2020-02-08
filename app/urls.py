from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("health", views.health, name="health"),
    path("", include("notifications.urls")),
]

if settings.DEBUG:
    urlpatterns.extend([path("pact/", include("pact.urls"))])
