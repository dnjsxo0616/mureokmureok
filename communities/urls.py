from django.urls import path
from . import views

app_name = 'communities'
urlpatterns = [
    path('', views.index, name='index'),
    path('category/<str:category>/', views.filter_communities, name='filter_communities'),
    path('create/',views.create, name='create'),
    path('search/', views.search, name='search'),
    path('<int:community_pk>/',views.detail, name='detail'),
    path('<int:community_pk>/update/',views.update,name='update'),
    path('<int:community_pk>/delete/',views.delete,name='delete'),
    path('<int:community_pk>/likes/',views.community_likes, name='likes'),
    path('<int:community_pk>/community_comment_create/',views.community_comment_create, name='community_comment_create'),
    path('<int:community_pk>/community_comments/<int:community_comment_pk>/community_comment_update/',views.community_comment_update, name='community_comment_update'),
    path('<int:community_pk>/community_comments/<int:community_comment_pk>/community_comment_delete/',views.community_comment_delete, name='community_comment_delete'),
    path('<int:community_pk>/community_comments/<int:community_comment_pk>/community_comment_likes/',views.community_comment_likes, name='community_comment_likes'),
]