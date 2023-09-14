from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta,datetime
from django_ckeditor_5.fields import CKEditor5Field
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
# Create your models here.

def notice_img_path(instance, filename):
    return f'images/notice/{instance.title}/{filename}'


class Notice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = CKEditor5Field('Content', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hits = models.PositiveIntegerField(default=0)
    thumbnail = models.ImageField(upload_to=notice_img_path)
    community_thumbnail = ImageSpecField(
        source = 'thumbnail',
        processors = [Thumbnail(300,300)],
        format = 'JPEG',
        options = {'quality': 90}
    )