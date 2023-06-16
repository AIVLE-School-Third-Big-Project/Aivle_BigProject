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
    
    # menu
    path('about/', views.about, name = 'about'),
    path('service/', views.service, name = 'about'),
    path('project/', views.project, name = 'about'),
    
    # pages drop down menu
    path('feature/', views.feature, name = 'about'),
    path('team/', views.team, name = 'team'),
    path('faq/', views.faq, name = 'faq'),
    path('testimonial/', views.testimonial, name = 'testimonial'),
    path('404/', views.NotFound, name = '404'),
    path('contact/', views.contact, name = 'contact'),
]
