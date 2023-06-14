# workLog views

import json
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from . import models

def workLog(request) : # 작업 일지 Html
    return render(request, 'workLog/workLog.html')

def workLogWrite(request) : # 작업 일지 작성 Html
    return render(request, 'workLog/workLogWrite.html')

class workLogView(View) : # 작업 일지 요청
    def get(self, request) :
        work_log_data = models.WorkLog.objects.all() # 작업 일지 테이블 전부 로드
        json_data = json.dumps(list(work_log_data.values())) # Json 객체로 변환
        
        # json 객체로 Response
        return JsonResponse(json_data, status = 201, safe=False) # list -> safe = False
    
class workLogWriteView(View) : # 작업 일지 작성
    def post(self, request) :
        work_data = json.loads(request.body) # 폼 데이터
        user_id = request.session['user'] # 세션 ID
        
        try :
            models.WorkLog.objects.create( # 테이블에 insert
                user_id     =user_id,
                day         =work_data['day'],
                in_time     =work_data['in_time'],
                out_time    =work_data['out_time'],
                start       =work_data['start'],
                end         =work_data['end'],
                work_type   =work_data['work_type'],
                contents =  work_data['contents']
            )
            
            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
        
        except json.JSONDecodeError :
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status = 400)
        
        except TypeError :  # 잘못된 유형의 값을 필드에 할당
            return JsonResponse({"message" : "TYPE_ERROR"}, status = 400)
        
        except ValueError : # 부적절한 값을 인자로 
            return JsonResponse({"message" : "VALUE_ERROR"}, status = 400)