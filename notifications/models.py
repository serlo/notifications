from django.db import models
from typing import TypedDict

# Create your models here.
class UserJson(TypedDict):
    user_id: str
    provider_id: str


class EventJson(TypedDict):
    event: dict
    created_at: str


class NotificationJson(TypedDict):
    event: EventJson
    user: UserJson
    seen: bool


class Event(models.Model):
    event_id = models.CharField(max_length=200)
    provider_id = models.CharField(max_length=200)
    created_at = models.DateTimeField()

    def to_json(self) -> EventJson:
        return {"event_id": self.event_id, "provider_id": self.provider_id}


class User(models.Model):
    user_id = models.CharField(max_length=200)
    provider_id = models.CharField(max_length=200)

    def to_json(self) -> UserJson:
        return {"user_id": self.user_id, "provider_id": self.provider_id}


class Notification(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)

    def to_json(self) -> NotificationJson:
        return {
            "event": self.event.to_json(),
            "content": "iloveorange",
            "created_at": self.event.created_at.isoformat(timespec="seconds"),
        }
