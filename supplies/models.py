from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field

def supply_img_path(instance, filename):
    return f'images/supply/{instance.name}/{filename}'
# Create your models here.

class Supply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    supply_name = models.CharField(max_length=500)  
    category_choices = (
        ('pot', '화분'),
        ('fertilizer', '비료'),
        ('nutrition', '영양제'),
        ('decoration', '데코레이션'),
        ('sprinkler', '물뿌리개'),
    )
    category = models.CharField(max_length=20, choices=category_choices) 
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_supply')
    price = models.IntegerField()
    content = CKEditor5Field('Content', config_name='extends')
    photo = models.ImageField(upload_to=supply_img_path)
    Thumbnail = ImageSpecField( 
		source = 'photo', 		   # 원본 ImageField 명
		processors = [Thumbnail(300, 300)], # 처리할 작업목록
		format = 'JPEG',		   # 최종 저장 포맷
		options = {'quality': 90}) # 저장 옵션


    tags = TaggableManager(blank=True)

    def save(self, *args, **kwargs):
        self.tags = ','.join(self.tags)

        super().save(*args, **kwargs)

    def get_tags_list(self):
        return self.tags.split(',')