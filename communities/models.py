from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail


# Create your models here.
def community_img_path(instance, filename):
    return f'images/community/{instance.name}/{filename}'



class Community(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    hits = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to=community_img_path)
    community_photo = ImageSpecField(
        source = 'photo',
        processors = [Thumbnail(300,300)],
        format = 'JPEG',
        options = {'quality': 90}
    )
    need_expert = models.BooleanField(default=False)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_community')
    category = models.CharField(max_length=20)
    
    def __str__(self):
        return self.title


class Community_comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, blank=False, null=False, on_delete=models.CASCADE)
    crated_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=600)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_community_comment')