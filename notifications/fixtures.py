from typing import List

from .tasks import SubscriberPayload, EventPayload, NotificationPayload

event_payload: EventPayload = {
    "event_id": "1",
    "event_provider": "serlo.org",
    "created_at": "2019-11-11 11:11:11+02:00",
}

subscriber_payload: SubscriberPayload = {
    "subscriber_id": "123",
    "provider_id": "serlo.org",
}

notification_payload: NotificationPayload = {
    "event": event_payload,
    "subscriber": subscriber_payload,
}
