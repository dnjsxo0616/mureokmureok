from django.db import models
from django.db.models.signals import post_save
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
from django.dispatch import receiver
import json
from datetime import timedelta
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.conf import settings


class BroadcastAlarm(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)
    class Meta:
        ordering = ['-broadcast_on']

@receiver(post_save, sender=BroadcastAlarm)
def alarm_handler(sender, instance, created, **kwargs):
     if created:
        schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.broadcast_on.hour, minute = instance.broadcast_on.minute, day_of_month = instance.broadcast_on.day, month_of_year = instance.broadcast_on.month)
        task = PeriodicTask.objects.create(crontab=schedule, name="broadcast-notification-"+str(instance.id), task="notifications_app.tasks.broadcast_notification", args=json.dumps((instance.id,)))

