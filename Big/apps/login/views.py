# login views

import json, re, bcrypt

from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse

from . import models

# 로그인 화면
def index(request) :
    return render(request, 'login/login.html')

# 회원가입 화면
def register(request) :
    return render(request, 'login/register.html')
    
# 로그인 검사
class loginView(View) :
    def post(self, request) :
        try :
            login_data = json.loads(request.body)
            id = login_data['id']
            
            user = models.User.objects.get(id = id)
            
            pw = login_data['pw'].encode('utf-8')
            user_pw = user.pw.encode('utf-8')
            
            if not bcrypt.checkpw(pw, user_pw) : # 비밀번호 오류
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400)
            
            if 'user' not in request.session :
                request.session['user'] = id # 세션 추가
            return JsonResponse({"redirect_url" : "/main/"}, status = 201)
            
        # 입력 오류 => 하나 이상 비어있을 경우  
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        
        # id가 테이블 존재 X
        except models.User.DoesNotExist :
            return JsonResponse({"message" : "USER_NOT_FOUND"}, status = 400)
            
    
# 회원가입 등록
class registerView(View) :
    def post(self, request) :
        try :
            data = json.loads(request.body)
            
            id = data['id']
            pw = data['pw']
            region = data['region']
            category = data['category']
            
            # 이미 사번이 있는 경우
            if models.User.objects.filter(id=id).exists():
                return JsonResponse({"message" : "ALREADY_EXISTS"}, status = 400)

            # 비밀번호 8 ~ 25글자
            regex_pw = '\S{8,25}'
            if not re.match(regex_pw, pw) :
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400)
            
            # 비밀번호 해싱
            pw = data['pw'].encode('utf-8')
            pw_crypt = bcrypt.hashpw(pw, bcrypt.gensalt()).decode('utf-8')
            
            # db에 추가
            models.User.objects.create(id = id, pw = pw_crypt, region = region, category = category)
            return JsonResponse({"message" : "SUCCESS"}, status = 201)
            
        # 입력 오류 => 하나 이상 비어있을 경우
        except KeyError :
            return JsonResponse({"message" : "KEY_EROOR"}, status = 400)    
        # json 디코드 오류
        except json.JSONDecodeError as e:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status = 400)
            
    
    
