# big urls

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.login.urls')),
    
    # 메인 --
    path('main/', views.main, name = 'main'),
    path('main/workLog/',include('apps.workLog.urls')),
    
    #about
    path('about/', views.about, name = 'about'),
    
    #공지
    path('main/notice/', include('apps.notice.urls')),
    
    #빈페이지
    path('project/', views.project, name = 'project'),
    
    # pages drop down menu
    # 영상로그
    path('main/videoLog/', include('apps.videoLog.urls')),
    
    # upload drop down menu
    path('main/upload/', include('apps.upload.urls')),
    
    #개인정보처리방침
    path('privacy/', views.privacy, name = 'privacy'),
    
    # 이용약관
    path('userAcc/', views.useAcc, name = 'useAcc')
]
