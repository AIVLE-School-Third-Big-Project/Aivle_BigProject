# workLog views

import json, sys
import logging

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from apps.login.models import User
from datetime import datetime
from . import models
from django.views import View

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('log/workLog.log')
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stderr)  # stderr로 변경
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

def workLog(request) : # 작업 일지 Html
    boards = models.WorkLog.objects.all()  # 데이터베이스에서 게시판 데이터 조회
    role = User.objects.get(id=request.session['user']).category

    # 페이징 설정
    boards = models.WorkLog.objects.order_by('-board_id')  # 작성일 기준으로 내림차순 정렬
    paginator = Paginator(boards, 10)  # 한 페이지에 10개의 게시물이 보이도록 설정
    page_number = request.GET.get('page')  # 현재 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 현재 페이지에 해당하는 게시물들을 가져옴

    context = {
        'page_obj': page_obj,
        'role': role,
    }
    
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

        logger.info(f'게시글 작성 : {request.session["user"]} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]')
        # 저장 후 작업 완료 페이지로 이동
        return redirect('/main/workLog/')
    
    
def workLogView(request, board_id) : # 게시글 클릭 시
    board = models.WorkLog.objects.get(pk=board_id)
    role = User.objects.get(id=request.session['user']).category
    login_user = request.session['user']

    context = { 
        'board': board,
        'role': role, # 로그인한 유저의 역할
        'login_user': int(login_user), # 로그인 id
    }
        
    return render(request, 'workLog/workLogView.html', context)
   

class workLogViewDelete(View): # 게시글 삭제
    def post(self, request, board_id) :
        try:
            board = models.WorkLog.objects.get(pk=board_id)
            board.delete()
            
            logger.info(f'{board.user_id}의 {board_id} 게시글 삭제 : {request.session["user"]} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]')
            return JsonResponse({'message': 'DELETE_SUCCESS'}, status=204)
        
        except ObjectDoesNotExist: # 게시글 존재 X
            return JsonResponse({'message': 'DELETE_FAILED'}, status=404)
    
        
def workLogSearch(request) : # 작업일지 검색
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
        
        logger.info(f'{board.user_id}의 {board_id} 작업 승인 : {request.session["user"]} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]')
    except models.WorkLog.DoesNotExist:
        return render(request, 'workLog/DoesNotExist.html') 
    
    return redirect('/main/workLog/view/'+board_id+'/')


def workLogEdit(request, board_id) : # 게시판 수정
    try:
        board = models.WorkLog.objects.get(board_id=board_id)
        context = {
            'board': board,
        }
        
    except models.WorkLog.DoesNotExist:
        return render(request, 'workLog/DoesNotExist.html')
    
    return render(request, 'workLog/workLogEdit.html', context)


def workLogEditSubmit(request, board_id) : # 테이블 수정
    if request.method == 'POST':
        title = request.POST.get('title')
        in_time = request.POST.get('in_time')
        out_time = request.POST.get('out_time')
        start = request.POST.get('start')
        end = request.POST.get('end')
        work_type = request.POST.get('work_type')
        contents = request.POST.get('contents')
  
        try:
            board = models.WorkLog.objects.get(board_id=board_id)
            board.title = title
            board.day = datetime.now().strftime('%Y-%m-%d')
            board.in_time = in_time
            board.out_time = out_time
            board.start = start
            board.end = end
            board.work_type = work_type
            board.contents = contents
            board.save()
            
            logger.info(f'{board.user_id}의 {board_id} 게시글 수정 : {request.session["user"]} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]')
            return redirect('/main/workLog/')
        
        except models.WorkLog.DoesNotExist:
            return render(request, 'workLog/DoesNotExist.html') 
    
    
        