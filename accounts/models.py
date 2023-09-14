from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import Thumbnail, ResizeToFit
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    def __str__(self):
        return self.name


class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    points = models.IntegerField(default=0)
    title = models.ForeignKey(User_title, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username