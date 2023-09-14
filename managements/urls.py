from django.urls import path
from . import views

app_name = 'managements'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name = 'create'),
    path('<int:management_pk>/update/', views.update, name = 'update'),
    path('<int:management_pk>/delete/', views.delete, name = 'delete'),
    path('<int:management_pk>/', views.detail, name='detail'),
    path('<int:management_pk>/calenderentry_create/',views.calenderentry_create, name='calenderentry_create'),
    path('<int:management_pk>/calenderentrys/<int:calenderentry_pk>/calenderentry_update/',views.calenderentry_update, name='calenderentry_update'),
    path('<int:management_pk>/calenderentrys/<int:calenderentry_pk>/calenderentry_delete/',views.calenderentry_delete, name='calenderentry_delete'), 
]