from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest, JsonResponse
from .models import Event, Notification, User


def index(_: HttpRequest, provider_id: str, user_id: str, format: str) -> JsonResponse:
    try:
        user = User.objects.get(provider_id=provider_id, user_id=user_id)
    except User.DoesNotExist:
        return JsonResponse([], safe=False)
    notifications = user.notification_set.all()
    notifications_list = [notification.to_json(format) for notification in notifications]
    return JsonResponse(notifications_list, safe=False)
