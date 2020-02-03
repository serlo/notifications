from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import logging
import json

from notifications.tasks import create_event, create_notification
from notifications.worker import execute_message as execute
from notifications.models import Notification

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def set_state(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    consumer = data["consumer"]
    state = data["state"]
    if consumer == "serlo.org" and state == "no notifications exist":
        Notification.objects.all().delete()
        return JsonResponse({})
    if (
        consumer == "serlo.org"
        and state == "a notifications for user 123 and event 234 exists"
    ):
        create_event(
            {
                "event": {"provider_id": "serlo.org", "id": "234"},
                "created_at": "2015-08-06T16:53:10+01:00",
                "source": {"provider_id": "serlo.org"},
            }
        )
        create_notification(
            {
                "event": {"provider_id": "serlo.org", "id": "234"},
                "user": {"provider_id": "serlo.org", "id": "123"},
                "created_at": "2015-08-06T16:53:10+01:00",
                "source": {"provider_id": "serlo.org"},
            }
        )
    if consumer == "serlo.org" and state == "one event with id 123 exists":
        create_event(
            {
                "event": {"provider_id": "serlo.org", "id": "123"},
                "user": {"provider_id": "serlo.org", "id": "234"},
                "created_at": "2015-08-06T16:53:10+01:00",
                "source": {"provider_id": "serlo.org"},
            }
        )
    return JsonResponse({})


@csrf_exempt
def execute_message(request: HttpRequest) -> JsonResponse:
    payload = json.loads(request.body)
    execute(payload)
    return JsonResponse({})
