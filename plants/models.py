from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill
from taggit.managers import TaggableManager


# Create your models here.
class Plant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    content = models.TextField()
    preferences = models.CharField(max_length=20)
    allergy = models.CharField(max_length=20)
    flowering = models.CharField(max_length=20)
    season = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    watering = models.CharField(max_length=20)
    sunlight = models.CharField(max_length=20)
    humidity = models.CharField(max_length=20)
    temperature = models.CharField(max_length=20)
    meaning = models.CharField(max_length=20)
    birthflower = models.CharField(max_length=20)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_plants')
    tags = TaggableManager()


class PlantImage(models.Model):
    def default_image():
        return "default_image_path.jpg"
    
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="plant_images")
    image = ProcessedImageField(
        upload_to="plants/images",
        processors=[ResizeToFill(600, 600)],
        format="JPEG",
        options={"quality": 90},
        blank = False,
        default=default_image,
    )