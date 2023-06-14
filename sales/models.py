from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import Thumbnail, ResizeToFit
from django.utils import timezone
from datetime import timedelta,datetime
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager
import random
def sale_img_path(instance, filename):
    return f'images/sale/{instance.title}/{filename}'
# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    content = CKEditor5Field('Content', config_name='extends')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_products')
    category = models.CharField(max_length=20)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    photo = models.ImageField(upload_to=sale_img_path)
    Thumbnail = ImageSpecField( 
		source = 'photo', 		  
		processors = [Thumbnail(300, 300)], 
		format = 'JPEG',		   
		options = {'quality': 90}) 
    
    def __str__(self):
        return self.title
    

# 주문정보
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=100)
    product_name = models.CharField(max_length=50)
    payment_status = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    order_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"주문번호 {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        length = 10
        order_number = str(random.randint(0, 9999999999)).zfill(length)
        return order_number
    
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=20)
    score = models.IntegerField()
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def review_images_path(instance, filename):
        return f'reviews/{instance.title}/{filename}'
    image = ProcessedImageField(
        upload_to=review_images_path, 
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
