from django.urls import path
from . import views

app_name = 'sales'
urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('detail/<int:product_pk>', views.detail, name="detail"),
    path('view-cart/', views.view_cart, name="view_cart"),
    path('add-to-cart/<int:product_pk>/',views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('<int:product_pk>/review/create/', views.create_review, name='create_review'),
]