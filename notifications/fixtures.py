from typing import List

from .tasks import UserPayload, EventPayload, NotificationPayload

event_payload: EventPayload = {
    "event_id": "1",
    "provider_id": "serlo.org",
    "created_at": "2019-11-11 11:11:11+02:00",
}

create_event_payload: EventPayload = {
    "event_id": "1",
    "provider_id": "serlo.org",
    "created_at": "2019-11-11 11:11:11+02:00",
}

user_payload: UserPayload = {"user_id": "123", "provider_id": "serlo.org"}

create_notification_payload: NotificationPayload = {
    "event": event_payload,
    "user": user_payload,
}
