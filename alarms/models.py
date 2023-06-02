from django.db import models
from django.db.models.signals import post_save
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
from django.dispatch import receiver
import json
from datetime import timedelta
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from communities.models import Community, Community_comment

class BroadcastAlarm(models.Model):
    message = models.TextField()
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-broadcast_on']

@receiver(post_save, sender=BroadcastAlarm)
def alarm_handler(sender, instance, created, **kwargs):
     if created:
        # 시간 변환
        broadcast_on_utc = timezone.make_aware(instance.broadcast_on, timezone=timezone.utc)

        # SQLite에서는 타임존 정보를 지원하지 않으므로 제거하여 naive datetime으로 변환
        broadcast_on_naive = timezone.make_naive(broadcast_on_utc)

        # CrontabSchedule 생성 또는 가져오기
        schedule, created = CrontabSchedule.objects.get_or_create(
            hour=broadcast_on_naive.hour,
            minute=broadcast_on_naive.minute,
            day_of_month=broadcast_on_naive.day,
            month_of_year=broadcast_on_naive.month
        )

        # PeriodicTask 생성
        task = PeriodicTask.objects.create(
            crontab=schedule,
            name="broadcast-alarm-" + str(instance.id),
            task="alarms.tasks.broadcast_alarm",
            args=json.dumps((instance.id,))
        )


