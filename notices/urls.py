from django.urls import path
from . import views


app_name = "notices"
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:notice_pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:notice_pk>/delete/', views.delete, name='delete'),
    path('<int:notice_pk>/update/', views.update, name='update'),
]