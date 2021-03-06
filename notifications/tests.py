from datetime import timezone, datetime
from requests.models import Response
from typing import Any
from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.urls import reverse

from . import models
from . import tasks
from . import fixtures
from .tasks import CreateNotificationPayload, ReadNotificationPayload


def normalize_timestamp(timestamp: str) -> str:
    dt = datetime.fromisoformat(timestamp)
    return dt.astimezone(tz=timezone.utc).isoformat(timespec="seconds")


class NotificationIndexViewTests(TestCase):
    def test_no_notifications(self) -> None:
        self.assertResponseForUser(fixtures.user_payload, [])

    def test_one_notification(self) -> None:
        mock_response = Response()
        mock_response.status_code = 200
        setattr(
            mock_response,
            "json",
            MagicMock(return_value={"234": {"content": "iloveorange"}}),
        )
        mocked_post = MagicMock(return_value=mock_response)

        with patch("requests.post", mocked_post):
            event_payload = fixtures.create_event_payload
            tasks.create_event(event_payload)
            payload: CreateNotificationPayload = {
                "event": event_payload["event"],
                "user": fixtures.user_payload,
            }
            tasks.create_notification(payload)
            self.assertResponseForUser(
                payload["user"],
                [
                    {
                        "event": {
                            "id": payload["event"]["id"],
                            "provider_id": payload["event"]["provider_id"],
                        },
                        "content": "iloveorange",
                        "created_at": normalize_timestamp(event_payload["created_at"]),
                    }
                ],
            )

    def test_two_notifications(self) -> None:
        mock_response = Response()
        mock_response.status_code = 200
        setattr(
            mock_response,
            "json",
            MagicMock(
                return_value={
                    "234": {"content": "iloveorange",},
                    "456": {"content": "iloveapple",},
                }
            ),
        )
        mocked_post = MagicMock(return_value=mock_response)

        with patch("requests.post", mocked_post):
            event_payload = fixtures.create_event_payload
            tasks.create_event(event_payload)
            payload: CreateNotificationPayload = {
                "event": fixtures.create_event_payload["event"],
                "user": fixtures.user_payload,
            }
            tasks.create_notification(payload)
            event_payload2: tasks.CreateEventPayload = {
                "event": {"id": "456", "provider_id": "serlo.org"},
                "created_at": "2018-08-06T16:53:10+01:00",
            }
            tasks.create_event(event_payload2)
            payload2: CreateNotificationPayload = {
                "event": event_payload2["event"],
                "user": payload["user"],
            }
            tasks.create_notification(payload2)
            self.assertResponseForUser(
                fixtures.user_payload,
                [
                    {
                        "event": {
                            "id": payload["event"]["id"],
                            "provider_id": payload["event"]["provider_id"],
                        },
                        "content": "iloveorange",
                        "created_at": normalize_timestamp(event_payload["created_at"]),
                    },
                    {
                        "event": {
                            "id": payload2["event"]["id"],
                            "provider_id": payload2["event"]["provider_id"],
                        },
                        "content": "iloveapple",
                        "created_at": normalize_timestamp(event_payload2["created_at"]),
                    },
                ],
            )

    def assertResponseForUser(
        self, user: tasks.UserPayload, notifications: Any
    ) -> None:
        url = reverse(
            "notifications:index",
            kwargs={
                "lang": "en",
                "provider_id": user["provider_id"],
                "user_id": user["id"],
                "format": "html",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, notifications)


class CreateEventTaskTests(TestCase):
    def test_create_event(self) -> None:
        tasks.create_event(fixtures.create_event_payload)
        events = list(models.Event.objects.all())
        self.assertEqual(len(events), 1)
        self.assertEqual(
            events[0].event_id, fixtures.create_event_payload["event"]["id"]
        )

    def test_create_event_only_once(self) -> None:
        tasks.create_event(fixtures.create_event_payload)
        tasks.create_event(fixtures.create_event_payload)
        events = list(models.Event.objects.all())
        self.assertEqual(len(events), 1)
        self.assertEqual(
            events[0].event_id, fixtures.create_event_payload["event"]["id"]
        )


class CreateNotificationTaskTests(TestCase):
    def test_create_notification_for_nonexistingevent(self) -> None:
        self.assertRaises(
            models.Event.DoesNotExist,
            tasks.create_notification,
            fixtures.create_notification_payload,
        )

    def test_create_notification(self) -> None:
        event_payload = fixtures.create_event_payload
        tasks.create_event(event_payload)
        payload: CreateNotificationPayload = {
            "event": event_payload["event"],
            "user": fixtures.user_payload,
        }
        tasks.create_notification(payload)
        notifications = list(models.Notification.objects.all())
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].user.user_id, payload["user"]["id"])

    def test_create_notification_only_once(self) -> None:
        event_payload = fixtures.create_event_payload
        tasks.create_event(event_payload)
        payload: CreateNotificationPayload = {
            "event": event_payload["event"],
            "user": fixtures.user_payload,
        }
        tasks.create_notification(payload)
        tasks.create_notification(payload)
        notifications = list(models.Notification.objects.all())
        self.assertEqual(len(notifications), 1)


class ReadNotificationTaskTests(TestCase):
    def test_read_notification(self) -> None:
        event_payload = fixtures.create_event_payload
        tasks.create_event(event_payload)
        payload: ReadNotificationPayload = {
            "event": event_payload["event"],
            "user": fixtures.user_payload,
        }
        tasks.read_notification(payload)
        event = models.Event.objects.get(
            event_id=payload["event"]["id"], provider_id=payload["event"]["provider_id"]
        )
        user = models.User.objects.get(
            user_id=payload["user"]["id"], provider_id=payload["user"]["provider_id"]
        )
        notification = models.Notification.objects.get(event=event, user=user)
        self.assertEqual(notification.seen, True)
