from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

# Create your models here.
class Garden(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_gradens')
    location_garden = models.CharField(max_length=200)

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
        return f'products/{instance.title}/{filename}'
    image = ProcessedImageField(
        upload_to=garden_images_path, 
        processors=[ResizeToFit(800, 800)], 
        format='JPEG', 
        options={'quality': 100}
    )

    site_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)