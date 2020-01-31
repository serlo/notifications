from django.contrib import admin
from django.urls import include, path
from . import views

app_name = "notifications"
urlpatterns = [
    path("<str:provider_id>/<str:user_id>/<str:format>", views.index, name="index")
]
