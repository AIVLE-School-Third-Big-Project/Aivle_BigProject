# videoLog urls

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('textLog/', views.videoLog, name='videoLog'),
    path('textLog/<path:pathes>/', views.videoLog, name='videoLog'),
    
    path('mediaLog/', views.videoPlayerLog, name='videoPlayerLog'),
    path('mediaLog/<path:pathes>/', views.videoPlayerLog, name='videoPlayerLog'),
]