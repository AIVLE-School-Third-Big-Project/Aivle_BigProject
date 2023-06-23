# login urls

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # 로그인 회원가입 --
    path('', views.index, name = 'login'), # 로그인 화면
    path('login/submit/', views.loginView.as_view(), name = 'loginView'), # 로그인 검사
    path('logout/', views.logout, name ='logout'),
    
    path('register/', views.register, name = 'register'), # 회원가입
    path('register/id_inspection/', views.idInspectionView.as_view(), name = 'register'),
    path('register/submit/', views.registerView.as_view(), name = 'registerView'), # 회원가입 검사
    path('register/priv/', views.priv, name='priv')
]
