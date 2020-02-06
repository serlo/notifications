from django.shortcuts import render
import requests

# Create your views here.
from django.http import HttpRequest, JsonResponse
from .models import Notification, User


def index(_: HttpRequest, provider_id: str, user_id: str, format: str) -> JsonResponse:
    try:
        user = User.objects.get(provider_id=provider_id, user_id=user_id)
    except User.DoesNotExist:
        return JsonResponse([], safe=False)
    notifications = user.notification_set.all()
    event_ids = [n.event.event_id for n in notifications]
    rendered = requests.post(
        url="http://host.docker.internal:9009/event/render/{}".format(format),
        json=event_ids,
    ).json()

    def f(n: Notification):
        temp = n.to_json()
        temp["content"] = rendered[n.event.event_id]["content"]
        return temp

    result = list(map(f, list(notifications)))

    return JsonResponse(result, safe=False)
