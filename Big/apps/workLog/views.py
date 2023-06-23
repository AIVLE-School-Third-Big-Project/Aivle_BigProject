# workLog views

import json
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from datetime import datetime
from . import models
from apps.login.models import User


def workLog(request) : # 작업 일지 Html
    boards = models.WorkLog.objects.all()  # 데이터베이스에서 게시판 데이터 조회
    role = User.objects.get(id=request.session['user']).category

    # 페이징 설정
    paginator = Paginator(boards, 10)  # 한 페이지에 10개의 게시물이 보이도록 설정
    page_number = request.GET.get('page')  # 현재 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 현재 페이지에 해당하는 게시물들을 가져옴

    context = {
        'page_obj': page_obj,
        'role': role,
    }
    
    print(context)
    return render(request, 'workLog/workLog.html', context)

def workLogWrite(request) : # 작업 일지 작성 Html
    return render(request, 'workLog/workLogWrite.html')

def workLogWriteSubmit(request) : # 작업 일지 작성 로직
    if request.method == 'POST':
        title = request.POST.get('title')
        user_id = request.session['user'] # 세션
        in_time = request.POST.get('in_time')
        out_time = request.POST.get('out_time')
        start = request.POST.get('start')
        end = request.POST.get('end')
        work_type = request.POST.get('work_type')
        contents = request.POST.get('contents')
        region = User.objects.get(id = user_id).region # 유저 지역

        # WorkLog 모델에 데이터 저장
        worklog = models.WorkLog(
            title=title,
            day = datetime.now().strftime('%Y-%m-%d'),
            user_id = user_id,
            in_time=in_time,
            out_time=out_time,
            start=start,
            end=end,
            work_type=work_type,
            contents=contents,
            region = region
        )
        worklog.save()

        # 저장 후 작업 완료 페이지로 이동
        return redirect('/main/workLog/')
    
    
def workLogView(request, board_id) :
        board = models.WorkLog.objects.get(pk=board_id)
        role = User.objects.get(id=request.session['user']).category

        context = {
            'board': board,
            'role': role
        }
        
        return render(request, 'workLog/workLogView.html', context)
    
def workLogSearch(request) :
    keyword = request.GET.get('keyword', '')  # 'keyword' 매개변수 값 가져오기 (기본값은 빈 문자열)
    role = User.objects.get(id=request.session['user']).category
    page_obj = models.WorkLog.objects.filter(title__icontains=keyword)


    context = {
        'page_obj': page_obj, 
        'role': role
    }
    return render(request, 'workLog/workLog.html', context)

def workLogApprove(request, board_id) : # 관리자 승인 요청
    try:
        board = models.WorkLog.objects.get(board_id=int(board_id))
        board.approved = True
        board.save()
    except models.WorkLog.DoesNotExist:
        return render(request, 'workLog/DoesNotExist.html') 
    
    return redirect('/main/workLog/view/'+board_id+'/')
    
        