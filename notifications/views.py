from django.shortcuts import render
import requests

# Create your views here.
from django.http import HttpRequest, JsonResponse
from .models import Event, Notification, User


def index(_: HttpRequest, provider_id: str, user_id: str, format: str) -> JsonResponse:
    try:
        user = User.objects.get(provider_id=provider_id, user_id=user_id)
    except User.DoesNotExist:
        return JsonResponse([], safe=False)
    notifications = user.notification_set.all()

    def render(format: str, events_list: list):
        r = requests.post(
            url="http://host.docker.internal:9009/event/render/{}".format(format),
            json=events_list,
        )
        return r.json()

    notifications_list = [
        notification.to_json(format) for notification in notifications
    ]
    events_list = [notification["event"]["id"] for notification in notifications_list]
    contents = render(format, events_list)
    for notification in notifications_list:
        notification["content"] = contents[notification["event"]["id"]]
    return JsonResponse(notifications_list, safe=False)
