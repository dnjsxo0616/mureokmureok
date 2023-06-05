from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from django.utils import timezone
from datetime import timedelta,datetime
from plants.models import Plant

class Management(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    watering = models.CharField(max_length=20)
    sunlight = models.CharField(max_length=20)
    humidity = models.CharField(max_length=20)
    temperature = models.CharField(max_length=20)
    supply = models.CharField(max_length=50)
    significant = models.CharField(max_length=50)
    score = models.IntegerField(default=0)