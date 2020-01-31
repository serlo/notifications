from django.test import TestCase
from . import models
from . import tasks
from . import fixtures

# Create your tests here.
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
    def test_create_notification(self) -> None:
        tasks.create_notification(fixtures.create_notification_payload)
        notifications = list(models.Notification.objects.all())
        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            notifications[0].user.user_id,
            fixtures.create_notification_payload["user"]["user_id"],
        )

    def test_create_notification_only_once(self) -> None:
        tasks.create_notification(fixtures.create_notification_payload)
        tasks.create_notification(fixtures.create_notification_payload)
        notifications = list(models.Notification.objects.all())
        self.assertEqual(len(notifications), 1)


class TestReadNotification(TestCase):
    def test_read_notification(self) -> None:
        tasks.read_notification(fixtures.create_notification_payload)
        event = models.Event.objects.get(
            **fixtures.create_notification_payload["event"]
        )
        user = models.User.objects.get(**fixtures.create_notification_payload["user"])
        notification = models.Notification.objects.get(event=event, user=user)
        self.assertEqual(notification.seen, True)
