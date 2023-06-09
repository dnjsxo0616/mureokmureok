from django.urls import path
from . import views

app_name = 'sales'
urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('<int:product_pk>/update/', views.update, name="update"),
    path('<int:product_pk>/delete/', views.delete, name="delete"),
    path('<int:product_pk>/like/', views.like, name='like'),
    path('detail/<int:product_pk>', views.detail, name="detail"),
    path('filter/', views.filter, name="filter"),
    # path('sort/', views.sort, name="sort"),

    path('cart/', views.cart, name="cart"),
    path('add-to-cart/<int:product_pk>/',views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_pk>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('<int:product_pk>/review/create/', views.create_review, name='create_review'),
    path('<int:product_pk>/reviews/<int:review_pk>/delete_review/', views.delete_review, name='delete_review'),
    path('<int:product_pk>/reviews/<int:review_pk>/update_review/', views.update_review, name='update_review'),

    path('order_payment/<int:order_pk>/', views.order_payment, name="order_payment"),
    path('delete_order/<int:order_pk>/', views.delete_order, name='delete_order'),


    path('create_order/', views.create_order, name='create_order'),
    path('create_ordernow/<int:product_pk>', views.create_ordernow, name='create_ordernow'),

    path('order_complete', views.order_complete, name='order_complete'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),

    path('order_list/', views.order_list, name='order_list'),
]