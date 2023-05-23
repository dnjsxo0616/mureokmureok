
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'plants'
urlpatterns = [
    path('create/', views.create_plant, name = 'create_plant'),
    path('<int:plant_pk>/update/', views.update_plant, name = 'update_plant'),
    path('<int:plant_pk>/delete/', views.delete_plant, name = 'delete_plant'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)