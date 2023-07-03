# videoLog urls

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('videoLog/', views.videoLog, name='videoLog'),
    path('videoLog/<path:pathes>/', views.videoLog, name='videoLog'),
]