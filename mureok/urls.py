"""mureok URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.home, name='home'),
    path('test/', views.test, name='test'),
    path('search/',views.search, name='search'),
    path('admin/', admin.site.urls),
    path('notices/', include('notices.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('communities/', include('communities.urls')),
    path('supplies/', include('supplies.urls')),
    path('gardens/', include('gardens.urls')),
    path('plants/', include('plants.urls')),
    path('sales/', include('sales.urls')),
    path('managements/', include('managements.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('game/', include('game.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
