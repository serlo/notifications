from datetime import timezone, datetime
from typing import Any

from django.test import TestCase
from django.urls import reverse

from . import models
from . import tasks
from . import fixtures


def normalize_timestamp(timestamp: str) -> str:
    dt = datetime.fromisoformat(timestamp)
    return dt.astimezone(tz=timezone.utc).isoformat(timespec="seconds")


# Create your tests here.
class NotificationIndexViewTests(TestCase):
    def test_no_notifications(self) -> None:
        self.assertResponseForUser(fixtures.user_payload, [])

    def test_one_notification(self) -> None:
        event_payload = fixtures.create_event_payload
        tasks.create_event(event_payload)
        payload = {"event": event_payload, "user": fixtures.user_payload}
        tasks.create_notification(payload)
        self.assertResponseForUser(
            payload["user"],
            [
                {
                    "event": {
                        "event_id": payload["event"]["event_id"],
                        "provider_id": payload["event"]["provider_id"],
                    },
                    "content": "iloveorange",
                    "created_at": normalize_timestamp(payload["event"]["created_at"]),
                }
            ],
        )

    def test_two_notifications(self) -> None:
        event_payload = fixtures.create_event_payload
        tasks.create_event(event_payload)
        payload = {
            "event": fixtures.create_event_payload,
            "user": fixtures.user_payload,
        }
        tasks.create_notification(payload)
        event_payload2: tasks.CreateEventPayload = {
            "event_id": "456",
            "provider_id": "serlo.org",
            "created_at": "2018-08-06T16:53:10+01:00",
        }
        tasks.create_event(event_payload2)
        payload2 = {"event": event_payload2, "user": payload["user"]}
        tasks.create_notification(payload2)
        self.assertResponseForUser(
            fixtures.user_payload,
            [
                {
                    "event": {
                        "event_id": payload["event"]["event_id"],
                        "provider_id": payload["event"]["provider_id"],
                    },
                    "content": "iloveorange",
                    "created_at": normalize_timestamp(payload["event"]["created_at"]),
                },
                {
                    "event": {
                        "event_id": payload2["event"]["event_id"],
                        "provider_id": payload2["event"]["provider_id"],
                    },
                    "content": "iloveorange",
                    "created_at": normalize_timestamp(payload2["event"]["created_at"]),
                },
            ],
        )

    def assertResponseForUser(
        self, user: tasks.UserPayload, notifications: Any
    ) -> None:
        url = reverse(
            "notifications:index",
            kwargs={
                "provider_id": user["provider_id"],
                "user_id": user["user_id"],
                "format": "json",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, notifications)


class TestCreateEvent(TestCase):
    def test_create_event(self) -> None:
        tasks.create_event(fixtures.create_event_payload)
        events = list(models.Event.objects.all())
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].event_id, fixtures.create_event_payload["event_id"])

    def test_create_event_only_once(self) -> None:
        tasks.create_event(fixtures.create_event_payload)
        tasks.create_event(fixtures.create_event_payload)
        events = list(models.Event.objects.all())
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].event_id, fixtures.create_event_payload["event_id"])


class TestCreateNotification(TestCase):
    def test_create_notification_for_nonexistingevent(self) -> None:
        self.assertRaises(
            models.Event.DoesNotExist,
            tasks.create_notification,
            fixtures.create_notification_payload,
        )

    def test_create_notification(self) -> None:
        event_payload = fixtures.create_event_payload
        tasks.create_event(event_payload)
        payload = {"event": event_payload, "user": fixtures.user_payload}
        tasks.create_notification(payload)
        notifications = list(models.Notification.objects.all())
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].user.user_id, payload["user"]["user_id"])

    def test_create_notification_only_once(self) -> None:
        event_payload = fixtures.create_event_payload
        tasks.create_event(event_payload)
        payload = {"event": event_payload, "user": fixtures.user_payload}
        tasks.create_notification(payload)
        tasks.create_notification(payload)
        notifications = list(models.Notification.objects.all())
        self.assertEqual(len(notifications), 1)


class TestReadNotification(TestCase):
    def test_read_notification(self) -> None:
        event_payload = fixtures.create_event_payload
        tasks.create_event(event_payload)
        payload = {"event": event_payload, "user": fixtures.user_payload}
        tasks.read_notification(payload)
        event = models.Event.objects.get(
            event_id=payload["event"]["event_id"],
            provider_id=payload["event"]["provider_id"],
        )
        user = models.User.objects.get(**payload["user"])
        notification = models.Notification.objects.get(event=event, user=user)
        print(notification.seen)
        self.assertEqual(notification.seen, True)
