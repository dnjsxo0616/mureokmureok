from django.urls import path
from . import views

app_name = "game"
urlpatterns = [
    path('', views.index, name='index'),
    path('play/', views.play_puzzle, name='play_puzzle'),
    path('solved/', views.solved_puzzles, name='solved_puzzles'),
]