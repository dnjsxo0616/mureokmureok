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
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_gradens')
    # 지도 위도 경도
    latitude = models.FloatField()
    longitude = models.FloatField()

    category_Choices = (
        ('전체', '전체'),
        ('식물원', '식물원'),
        ('전시회', '전시회'),
        ('정원 센터', '정원 센터'),
        ('이벤트', '이벤트')
    )
    category = models.CharField(max_length=20, choices=category_Choices)

    # tag_Choices = (
    #     ('연인', '연인'),
    #     ('가족', '가족'),
    #     ('개인', '개인'),
    #     ('친구', '친구')
    # )
    # tag = models.CharField(max_length=100, choices=tag_Choices)

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
    comment = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def garden_images_path(instance, filename):
        return f'gardens/{instance.title}/{filename}'
    image = ProcessedImageField(
        upload_to=garden_images_path, 
        processors=[ResizeToFit(800, 800)], 
        format='JPEG', 
        options={'quality': 100}
    )

    @property
    def created_time(self):
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
            return self.strftime('%Y-%m-%d')