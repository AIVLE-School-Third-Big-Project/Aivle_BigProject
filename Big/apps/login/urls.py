# login urls

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # 로그인 회원가입 --
    path('', views.index, name = 'login'),
    path('login/submit', views.loginView.as_view(), name = 'loginView'),
    path('register/', views.register, name = 'register'),
    path('register/submit/', views.registerView.as_view(), name = 'registerView'),
    
]
