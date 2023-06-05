
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'managements'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name = 'create'),
    path('<int:management_pk>/update/', views.update, name = 'update'),
    path('<int:management_pk>/delete/', views.delete, name = 'delete'),
    path('<int:management_pk>/', views.detail, name='detail'),
]