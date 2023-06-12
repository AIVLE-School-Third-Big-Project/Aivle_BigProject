# workLog urls

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.workLog, name = 'workLog'),
    path('session/', views.workLogView.as_view(), name = 'workLogView')
]
