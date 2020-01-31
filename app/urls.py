from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # TODO: only load in dev
    path("pact/", include("pact.urls")),
    path("notifications/", include("notifications.urls")),
]
