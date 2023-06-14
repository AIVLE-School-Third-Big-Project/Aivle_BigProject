# workLog urls

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.workLog, name = 'workLog'), # 작업 일지
    path('request/', views.workLogView.as_view(), name = 'workLogView'), # 작업 일지 Load
    
    path('write/', views.workLogWrite, name = 'workLogWrite'), # 일지 작성
    path('write/request/', views.workLogWriteView.as_view(), name = 'workLogWriteView'), # 일직 Submit
]
