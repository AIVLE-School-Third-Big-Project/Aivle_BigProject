# Big views
from django.shortcuts import render

# 메인 화면
def main(request) :
    return render(request, 'index.html',)

# about
def about(request) :
    return render(request, 'about.html')

#아직 빈페이지
def project(request) :
    return render(request, 'project.html')


# 영상 로그
def log(request) :
    return render(request, 'log.html')

#개인정보처리방침
def privacy(request) :
    return render(request, 'privacy.html')

def priv(request) :
    return render(request, 'priv.html')

# 이용약관
def useAcc(request) :
    return render(request, 'useAcc.html')