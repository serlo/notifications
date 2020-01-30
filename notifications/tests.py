from django.test import TestCase
from . import models
from . import tasks
from . import fixtures

# Create your tests here.
class TestCreateEvent(TestCase):
    def test_create_event(self) -> None:
        tasks.create_event(fixtures.event_payload)
        events = list(models.Event.objects.all())
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].event_id, fixtures.event_payload["event_id"])

    def test_create_event_once(self) -> None:
        tasks.create_event(fixtures.event_payload)
        tasks.create_event(fixtures.event_payload)
        events = list(models.Event.objects.all())
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].event_id, fixtures.event_payload["event_id"])


class TestCreateNotification(TestCase):
    def test_create_notification(self) -> None:
        tasks.create_notification(fixtures.notification_payload)
        notifications = list(models.Notification.objects.all())
        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            notifications[0].subscriber.subscriber_id,
            fixtures.notification_payload["subscriber"]["subscriber_id"],
        )

    def test_create_notification_once(self) -> None:
        tasks.create_notification(fixtures.notification_payload)
        tasks.create_notification(fixtures.notification_payload)
        notifications = list(models.Notification.objects.all())
        self.assertEqual(len(notifications), 1)


class TestReadNotification(TestCase):
    def test_read_notification(self) -> None:
        read_notification = tasks.read_notification(fixtures.notification_payload)
        self.assertEqual(read_notification.seen, True)
