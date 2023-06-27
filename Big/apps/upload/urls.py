# upload urls

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   path('uploadIn/', views.uploadIn, name = 'uploadIn'),
   path('uploadOut/', views.uploadOut, name = 'uploadOut'),
   path('uploadWork/', views.uploadWork, name = 'uploadWork'),
   
   path('uploadIn/submit', views.uploadInSubmit, name='uploadInSubmit'),
]
