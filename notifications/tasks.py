from notifications.models import Event, User, Notification
from datetime import datetime
from typing import TypedDict, List


class UserPayload(TypedDict):
    provider_id: str
    user_id: str


class CreateEventPayload(TypedDict):
    event_id: str
    provider_id: str
    created_at: str


class EventPayload(TypedDict):
    event_id: str
    provider_id: str
    created_at: str


class NotificationPayload(TypedDict):
    event: EventPayload
    user: UserPayload


class CreateNotificationPayload(TypedDict):
    event: EventPayload
    user: UserPayload


def create_event(payload: CreateEventPayload) -> Event:
    event = get_event_or_create(payload)
    return event


def create_notification(payload: CreateNotificationPayload) -> Notification:
    user = get_user_or_create(payload["user"])
    event = get_event_or_create(payload["event"])
    notification = get_notification_or_create({"event": event, "user": user})
    return notification


def read_notification(payload: CreateNotificationPayload) -> Notification:
    notification = create_notification(payload)
    notification.seen = True
    notification.save()
    return notification


def get_user_or_create(payload: UserPayload) -> User:
    user, _ = User.objects.get_or_create(
        user_id=payload["user_id"], provider_id=payload["provider_id"]
    )
    return user


def get_event_or_create(payload: EventPayload) -> Event:
    event, _ = Event.objects.get_or_create(
        event_id=payload["event_id"],
        provider_id=payload["provider_id"],
        created_at=datetime_from_timestamp(payload["created_at"]),
    )
    return event


def get_notification_or_create(payload: NotificationPayload) -> Notification:
    notification, _ = Notification.objects.get_or_create(
        event=payload["event"], user=payload["user"]
    )
    return notification


def datetime_from_timestamp(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp)
