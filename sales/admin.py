from django.contrib import admin
from .models import Order, Product
# Register your models here.


class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_date', 'delivery_address', 'product_name', 'payment_status', 'quantity', 'price']
    list_filter = ['payment_status']

admin.site.register(Order)

class ProductAdmin(admin.ModelAdmin):
    exclude = ('like_users',)  # 'like_users' 필드를 제외하고 표시

admin.site.register(Product, ProductAdmin)