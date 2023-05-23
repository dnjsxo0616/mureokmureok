from django.urls import path
from . import views


app_name = "gardens"
urlpatterns = [
    path('create/', views.create, name='create'),
    path('<int:garden_pk>/delete/', views.delete, name='delete'),
    path('<int:garden_pk>/update/', views.update, name='update'),
    path('<int:garden_pk>/comment/', views.comment, name='comment'),
    path('<int:garden_pk>/like_garden/', views.like_garden, name='like_garden'),
    path('listing/', views.listing, name='listing'),
]