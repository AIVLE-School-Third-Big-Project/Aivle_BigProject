# notice urls

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name = 'notice'),
    path('view/<int:board_id>/', views.noticeView, name='noticeView'),
    
    path('write/', views.noticeWrite, name = 'noticeWrite'),
    path('write/submit/', views.noticeWriteSubmit.as_view(), name = 'noticeWriteSubmit'),
    
    path('search/', views.noticeSearch, name = 'noticeSearch'), 
    
    path('edit/<int:board_id>/', views.noticeEdit, name = 'noticeEdit'),
]