from django.urls import path
from . import views


app_name = 'supplies'
urlpatterns = [
    path('', views.supply_index, name='supply_index'),
    path('create/', views.supply_create, name='supply_create'), 
    path('<int:supply_pk>/', views.supply_detail, name='supply_detail'),  
    path('<int:supply_pk>/update/', views.supply_update, name='supply_update'), 
    path('<int:supply_pk>/delete/', views.supply_delete, name='supply_delete'),  
    path('filter/', views.filter_supplies, name='filter_supplies'),
]