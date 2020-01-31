from django.db import models

# Create your models here.


class Event(models.Model):
    event_id = models.CharField(max_length=200)
    provider_id = models.CharField(max_length=200)
    created_at = models.DateTimeField()


class User(models.Model):
    user_id = models.CharField(max_length=200)
    provider_id = models.CharField(max_length=200)


class Notification(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)

