# login views

import json, re, bcrypt, sys
import logging

from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime

from . import models

# LOG ------------------------------------------------

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('static/adminLog/login.log')
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stderr)  # stderr로 변경
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# LOG ------------------------------------------------

# 로그인 화면
def index(request) :
    if 'user' in request.session :
        return render(request, 'index.html')
    
    else :
        return render(request, 'login/login.html')
    
# 로그 아웃
def logout(request) : 
    logger.info(f'로그아웃 : {request.session["user"]} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]')
    request.session.clear() # 세션 삭제
    
    return render(request, 'login/logoutAlert.html')

# 회원가입 화면
def register(request) :
    return render(request, 'login/register.html')
    
# 회원가입 화면
def priv(request) :
    return render(request, 'login/priv.html')
    
# id 중복 검사
class idInspectionView(View) :
    def post(self, request) :
            id = json.loads(request.body)['id']
            
            # 이미 사번이 있는 경우
            if models.User.objects.filter(id=id).exists():
                return JsonResponse({"message" : "ALREADY_EXISTS"}, status = 400)
            else :
                return JsonResponse({"message" : "SUCCESS"}, status = 201)
            
        
# 로그인 검사
class loginView(View) :
    def post(self, request) :
        try :
            login_data = json.loads(request.body)
            id = login_data['id']
            
            user = models.User.objects.get(id = id)
            
            pw = login_data['pw'].encode('utf-8')
            user_pw = user.pw.encode('utf-8')
            user_name = user.name
            
            if user.is_account_locked() : # 계정이 잠긴지 확인
                logger.info(f'계정 잠김 : {user.id} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]')
                return JsonResponse({"message" : "ACCOUNT_LOCKED"}, status = 403)
            
            else : # 계정이 잠긴게 아니라면
                if not bcrypt.checkpw(pw, user_pw) : # 비밀번호 오류
                    user.increment_failed_attempts() # 실패 횟수 추가
                    
                    if user.is_account_locked() : # 계정이 잠긴지 확인
                        logger.info(f'계정 잠김 : {user.id} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]')
                        return JsonResponse({"message" : "ACCOUNT_LOCKED"}, status = 403)
                    
                    return JsonResponse({"message" : "INVALID_PASSWORD", "count" : user.failed_attempts}, status = 403)
                
                if 'user' not in request.session and 'username' not in request.session :
                    request.session['user'] = id # 세션 추가
                    request.session['username'] = user_name
                    
                    user.reset_failed_attempts() # 실패횟수 초기화
                    logger.info(f'로그인 완료 : {user.id} [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]')
                    return JsonResponse({"redirect_url" : "/main/"}, status = 201)
            
        # 입력 오류 => 하나 이상 비어있을 경우  
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        
        # id가 테이블 존재 X
        except models.User.DoesNotExist :
            return JsonResponse({"message" : "USER_NOT_FOUND"}, status = 404)
        
        except ValueError:
            return JsonResponse({"message" : "VALUE_ERROR"}, status = 400)
            
    
# 회원가입 등록
class registerView(View) :
    def post(self, request) :
        try :
            data = json.loads(request.body)
            
            name = data['name']
            id = data['id']
            pw = data['pw']
            pwVerify = data['pw-verify']
            region = data['region']
            category = data['category']

            # 비밀번호 8 ~ 25글자
            regex_pw = '\S{8,25}'
            if not re.match(regex_pw, pw) :
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400)
            
            # 비밀번호, 비밀번호 일치 X
            if pw != pwVerify :
                return JsonResponse({"message" : "INVALID_PASSWORD_VERIFY"}, status = 400)
            
            # 비밀번호 해싱
            pw = data['pw'].encode('utf-8')
            pw_crypt = bcrypt.hashpw(pw, bcrypt.gensalt()).decode('utf-8')
            
            # db에 추가
            models.User.objects.create(name = name, id = id, pw = pw_crypt, region = region, category = category)
            return JsonResponse({"redirect_url" : "/"}, status = 201)
            
        # 입력 오류 => 하나 이상 비어있을 경우
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)    
        # json 디코드 오류
        except json.JSONDecodeError as e:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status = 400)
            
    
    
