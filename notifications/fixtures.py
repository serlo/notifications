from typing import List

from .tasks import UserPayload, EventPayload, NotificationPayload

event_payload: EventPayload = {
    "event_id": "234",
    "provider_id": "serlo.org",
    "created_at": "2015-08-06T16:53:10+01:00",
    "content": "iloveorange",
}

create_event_payload = event_payload

user_payload: UserPayload = {"user_id": "123", "provider_id": "serlo.org"}

create_notification_payload: NotificationPayload = {
    "event": event_payload,
    "user": user_payload,
}
