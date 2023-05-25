from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import Thumbnail, ResizeToFit


# Create your models here.


class User(AbstractUser):
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    birthday = models.DateField(null=True)
    image = ProcessedImageField(upload_to='users', 
                                blank=True,
                                processors=[Thumbnail(100,100)],
                                format='JPEG',
                                options={'quality': 80})



class User_title(models.Model):
    name = models.CharField(max_length=20)
    min_points = models.IntegerField()
    max_points = models.IntegerField()



class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    title = models.ForeignKey(User_title, on_delete=models.SET_NULL, null=True)


