from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from django.utils import timezone
from datetime import timedelta,datetime
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class Garden(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = CKEditor5Field('Content', config_name='extends')
    ex_content = models.TextField(default='Default value')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_gardens')
    hits = models.PositiveIntegerField(default=0)
    address = models.TextField()
    category_Choices = (
        ('전체', '전체'),
        ('식물원', '식물원'),
        ('전시회', '전시회'),
        ('정원센터', '정원센터'),
        ('축제', '축제')
    )
    category = models.CharField(max_length=20, choices=category_Choices)
    def search(cls, query):
        return cls.objects.filter(models.Q(title__icontains=query) | models.Q(address__icontains=query))
    def garden_images_path(instance, filename):
        return f'gardens/{instance.title}/{filename}'
    image = ProcessedImageField(
        upload_to=garden_images_path, 
        processors=[ResizeToFit(800, 800)], 
        format='JPEG', 
        options={'quality': 100}
    )

    site_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name='comments')
    title = models.CharField(max_length=20)
    score = models.IntegerField()
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def comment_images_path(instance, filename):
        return f'comments/{instance.title}/{filename}'
    image = ProcessedImageField(
        upload_to=comment_images_path, 
        processors=[ResizeToFit(800, 800)], 
        format='JPEG', 
        options={'quality': 100}
    )

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