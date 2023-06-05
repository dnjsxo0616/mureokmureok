from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from django.utils import timezone
from datetime import timedelta,datetime
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
def community_img_path(instance, filename):
    return f'images/community/{instance.title}/{filename}'


class Community(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = CKEditor5Field('Content', config_name='extends')
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
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def count_likes_user(self):
        return self.like_users.count()
    
    @property
    def created_time(self):
        if self.created_at is None:
            return False

        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return False


class Community_comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, blank=False, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=600)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_community_comment')

    def count_likes_user(self):
        return self.like_users.count()
    
    @property
    def created_time(self):
        if self.created_at is None:
            return False

        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return False