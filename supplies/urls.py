from django.urls import path
from . import views


app_name = 'supplies'
urlpatterns = [
    path('create/', views.supply_create, name='supply_create'), 
    path('<int:supplies_pk>/', views.supply_detail, name='supply_detail'),  
    path('<int:supplies_pk>/update/', views.supply_update, name='supply_update'), 
    path('<int:supplies_pk>/delete/', views.supply_delete, name='supply_delete'),  
    path('filter/', views.filter_products, name='filter_products'),
]