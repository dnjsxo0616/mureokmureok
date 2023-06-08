from django.contrib import admin
from .models import Order
# Register your models here.


class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_date', 'delivery_address', 'product_name', 'payment_status', 'quantity', 'price']
    list_filter = ['payment_status']

admin.site.register(Order)
