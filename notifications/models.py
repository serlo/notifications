from django.db import models

# Create your models here.
from typing import List, TypedDict
import uuid


class SubscriberJson(TypedDict):
    provider_id: str
    subscriber_id: str


class EventJson(TypedDict):
    event_id: str
    event_provider: str
    created_at: str


class NotificationJson(TypedDict):
    event: EventJson
    subsriber: SubscriberJson
    seen: bool


class Event(models.Model):
    event_id = models.CharField(max_length=200)
    event_provider = models.CharField(max_length=200)
    created_at = models.DateTimeField()

    def to_json(self) -> EventJson:
        return {
            "event_id": self.event_id,
            "event_provider": self.event_provider,
            "created_at": self.created_at.isoformat(timespec="seconds"),
        }


class Subscriber(models.Model):
    subscriber_id = models.CharField(max_length=200)
    provider_id = models.CharField(max_length=200)

    def to_json(self) -> SubscriberJson:
        return {"provider_id": self.provider_id, "user_id": self.subscriber_id}


class Notification(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)

    def to_json(self) -> NotificationJson:
        return {"event": self.event, "subscribers": self.subscriber, "seen": self.seen}
