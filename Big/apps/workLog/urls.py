# workLog urls

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.workLog, name = 'workLog'), # 작업 일지
    
    path('write/', views.workLogWrite, name = 'workLogWrite'), # 일지 작성
    path('write/submit/', views.workLogWriteSubmit, name = 'workLogWriteSubmit'), # 일지 Submit
    path('view/<int:board_id>/', views.workLogView, name='workLogView'),   # 게시판 글 클릭 시
    path('search/', views.workLogSearch, name = 'workLogSearch'), # 게시판 글 검색
    path('approve/<str:board_id>/',views.workLogApprove, name = 'workLogApprove')
]
