# Big views
from django.shortcuts import render

# 메인 화면
def main(request) :
    return render(request, 'index.html')

# menu
def about(request) :
    return render(request, 'about.html')

def service(request) :
    return render(request, 'service.html')

def project(request) :
    return render(request, 'project.html')

# pages drop down menu
def feature(request) :
    return render(request, 'feature.html')

def team(request) :
    return render(request, 'team.html')

def faq(request) :
    return render(request, 'faq.html')

def testimonial(request) :
    return render(request, 'testimonial.html')

def NotFound(request) :
    return render(request, '404.html')

def contact(request) :
    return render(request, 'contact.html')
