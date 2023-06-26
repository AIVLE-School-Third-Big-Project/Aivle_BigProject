# workLog urls

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.workLog, name = 'workLog'), # 작업 일지
    
    path('write/', views.workLogWrite, name = 'workLogWrite'), # 일지 작성
    path('write/submit/', views.workLogWriteSubmit, name = 'workLogWriteSubmit'), # 일지 Submit
    
    path('view/<int:board_id>/', views.workLogView, name='workLogView'),   # 게시판 글 클릭 시
    path('view/delete/<int:board_id>/', views.workLogViewDelete.as_view(), name='workLogViewDelete'),   # 게시판 삭제
    path('search/', views.workLogSearch, name = 'workLogSearch'), # 게시판 글 검색
    path('approve/<str:board_id>/', views.workLogApprove, name = 'workLogApprove'), # 일지 승인
    
    path('edit/<int:board_id>/', views.workLogEdit, name = 'workLogEdit'), # 일지 수정 페이지
    path('edit/<int:board_id>/submit/', views.workLogEditSubmit, name = 'workLogEditSubmit') # 일지 테이블 수정
    
]
