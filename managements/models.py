from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail

from plants.models import Plant, PlantImage

def management_img_path(instance, filename):
    return f'images/management/{instance.plant}/{filename}'


class Management(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    photo = models.ImageField(upload_to=management_img_path)
    management_photo = ImageSpecField(
        source = 'photo',
        processors = [Thumbnail(300,300)],
        format = 'JPEG',
        options = {'quality': 90}
    )


class CalenderEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    management = models.ForeignKey(Management, on_delete=models.CASCADE)
    watering = models.CharField(max_length=20)
    sunlight = models.CharField(max_length=20)
    humidity = models.CharField(max_length=20)
    temperature = models.CharField(max_length=20)



