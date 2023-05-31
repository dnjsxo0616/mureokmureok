from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from django.utils import timezone
from datetime import timedelta,datetime
from django_ckeditor_5.fields import CKEditor5Field

def sale_img_path(instance, filename):
    return f'images/sale/{instance.title}/{filename}'
# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    content = CKEditor5Field('Content', config_name='extends')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_products')
    category = models.CharField(max_length=20)
    purchase_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='purchase_products', through='Purchase')
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to=sale_img_path)
    Thumbnail = ImageSpecField( 
		source = 'photo', 		  
		processors = [Thumbnail(300, 300)], 
		format = 'JPEG',		   
		options = {'quality': 90}) 


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=80, verbose_name='상품명')
    quantity = models.IntegerField(default=1)
    price = models.PositiveIntegerField(verbose_name='결제금액')
    purchase_date = models.DateTimeField(auto_now_add=True)
    delivery_state = models.CharField(max_length=20)




class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product', blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '{} // {}'.format(self.user, self.products.name)


