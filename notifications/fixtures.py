from typing import List

from .tasks import (
    UserPayload,
    EventPayload,
    CreateEventPayload,
    CreateNotificationPayload,
)

event_payload: EventPayload = {"id": "234", "provider_id": "serlo.org"}

create_event_payload: CreateEventPayload = {
    "event": event_payload,
    "created_at": "2015-08-06T16:53:10+01:00",
}

user_payload: UserPayload = {"id": "123", "provider_id": "serlo.org"}

create_notification_payload: CreateNotificationPayload = {
    "event": event_payload,
    "user": user_payload,
}
