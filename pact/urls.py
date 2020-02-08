from django.urls import path

from . import views

app_name = "pact"
urlpatterns = [
    path("set-state/", views.set_state, name="set_state",),
    path("execute-message/", views.execute_message, name="execute_message"),
]
