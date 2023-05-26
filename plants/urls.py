
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'plants'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name = 'create'),
    path('<int:plant_pk>/update/', views.update, name = 'update'),
    path('<int:plant_pk>/delete/', views.delete, name = 'delete'),
    path('<int:plant_pk>/', views.detail, name='detail'),
    path('<int:plant_pk>/likes/', views.likes, name='likes'),

    path('recommendation/', views.recommendation, name='recommendation'),
]