# notice urls

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.notice, name = 'notice'),
    path('view/', views.noticeView, name = 'noticeView'),
    path('write/', views.noticeWrite, name = 'noticeWrite'),
    path('edit/', views.noticeEdit, name = 'noticeEdit'),
]