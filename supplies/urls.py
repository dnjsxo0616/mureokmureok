from django.urls import path
from . import views


app_name = 'supplies'
urlpatterns = [
    path('', views.index, name='index'),
    path('category/<str:category>/', views.filter_supplies, name='filter_supplies'),
    path('create/', views.create, name='create'), 
    path('<int:supply_pk>/', views.detail, name='detail'),  
    path('<int:supply_pk>/update/', views.update, name='update'), 
    path('<int:supply_pk>/delete/', views.delete, name='delete'),  
]