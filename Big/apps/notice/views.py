import json, re, bcrypt

from datetime import datetime
from django.views import View
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from apps.login.models import User

from . import models

def index(req):
    role = User.objects.get(id=req.session['user']).category # 사용자 역할
    # 페이징 설정
    
    boards = models.Post.objects.order_by('-id')  # 작성일 기준으로 내림차순 정렬
    paginator = Paginator(boards, 10)  # 한 페이지에 10개의 게시물이 보이도록 설정
    page_number = req.GET.get('page')  # 현재 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 현재 페이지에 해당하는 게시물들을 가져옴
    
    
    return render(req, "notice/notice.html", {
        'page_obj': page_obj,
        'role': role,
    })


def noticeView(req, board_id):
    role = User.objects.get(id=req.session['user']).category # 사용자 역할
    
    post = models.Post.objects.get(id=board_id) #filter
    return render(req, "notice/noticeView.html", {
        "post": post,
        "role": role,
    })


  
def noticeEdit(request, board_id):
    if request.method == 'GET':
        post = models.Post.objects.get(id=board_id)
        return render(request, "notice/noticeEdit.html", {
            "post": post
        })
    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        name = request.session['username']
        created = datetime.now().strftime("%Y-%m-%d")
            
        post = models.Post.objects.get(id=board_id)
        post.title = title
        post.content = content
        post.name = name
        post.created = str(created)
        post.save()
            
        return redirect("/main/notice/view/{}".format(board_id))

    
def noticeWrite(request) :
    return render(request, 'notice/noticeWrite.html')

class noticeWriteSubmit(View):
    def post(self, request):

        title = request.POST.get('title')
        content = request.POST.get('content')
        name = request.session['username']
        created = datetime.now().strftime("%Y-%m-%d")

        models.Post.objects.create(title=title, content=content, name=name, created=str(created))
            
        redirect_url = "/main/notice/"
        return redirect(redirect_url)


def noticeSearch(request) : # 공지사항 검색
    keyword = request.GET.get('keyword', '')  # 'keyword' 매개변수 값 가져오기 (기본값은 빈 문자열)
    role = User.objects.get(id=request.session['user']).category
    page_obj = models.Post.objects.filter(title__icontains=keyword)

    context = {
        'page_obj': page_obj, 
        'role': role
    }
    
    return render(request, 'notice/notice.html', context)





