from django.urls import path
from . import views


app_name = "gardens"
urlpatterns = [
    path('create/', views.create, name='create'),
    path('', views.index, name='index'),
    path('<int:garden_pk>/delete/', views.delete, name='delete'),
    path('<int:garden_pk>/update/', views.update, name='update'),
    path('<int:garden_pk>/like_garden/', views.like_garden, name='like_garden'),
    path('listing/', views.listing, name='listing'),
    path('<int:garden_pk>/', views.detail, name='detail'),
    path('<int:garden_pk>/comment/', views.comment, name='comment'),
    path('<int:product_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('location/', views.location, name='location')
]