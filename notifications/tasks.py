from notifications.models import Event, Subscriber, Notification
from datetime import datetime
from typing import TypedDict, List


class SubscriberPayload(TypedDict):
    provider_id: str
    subscriber_id: str


class CreateEventPayload(TypedDict):
    event_id: str
    event_provider: str
    created_at: str


class EventPayload(TypedDict):
    event_id: str
    event_provider: str
    created_at: str


class NotificationPayload(TypedDict):
    event: EventPayload
    subscriber: SubscriberPayload


class CreateNotificationPayload(TypedDict):
    event: EventPayload
    subscriber: SubscriberPayload


def create_event(payload: CreateEventPayload) -> Event:
    event = get_event_or_create(payload)
    return event


def create_notification(payload: CreateNotificationPayload) -> Notification:
    subscriber = get_subscriber_or_create(payload["subscriber"])
    event = get_event_or_create(payload["event"])
    notification = get_notification_or_create(
        {"event": event, "subscriber": subscriber}
    )
    return notification


def read_notification(payload: CreateNotificationPayload) -> Notification:
    notification = create_notification(payload)
    notification.seen = True
    notification.save()
    return notification


def get_subscriber_or_create(payload: SubscriberPayload) -> Subscriber:
    subscriber, _ = Subscriber.objects.get_or_create(
        subscriber_id=payload["subscriber_id"], provider_id=payload["provider_id"]
    )
    return subscriber


def get_event_or_create(payload: EventPayload) -> Event:
    event, _ = Event.objects.get_or_create(
        event_id=payload["event_id"],
        event_provider=payload["event_provider"],
        created_at=datetime_from_timestamp(payload["created_at"]),
    )
    return event


def get_notification_or_create(payload: NotificationPayload) -> Notification:
    notification, _ = Notification.objects.get_or_create(
        event=payload["event"], subscriber=payload["subscriber"]
    )
    return notification


def datetime_from_timestamp(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp)
