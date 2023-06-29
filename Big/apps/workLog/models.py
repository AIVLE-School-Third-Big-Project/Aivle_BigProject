# workLog models

from django.db import models
from apps.login.models import User

# 작업 일지 게시판
class WorkLog(models.Model):
    board_id = models.AutoField(primary_key=True) # 게시판 테이블 기본키
    title = models.CharField(max_length=50, default='작업 승인 요청') # 제목
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Login 테이블 외래키
    day = models.CharField(max_length = 20) # 게시판 등록 날짜
    
    in_time = models.TimeField() # 작업 입장 시간
    out_time = models.TimeField() # 작업 퇴장 시간
    
    start = models.DateField() # 작업 시작 날짜
    end = models.DateField() # 작업 죵료 날짜
    
    work_type = models.CharField(max_length = 50) # 작업 유형
    contents = models.CharField(max_length = 300) # 작업 상세내용
    
    region = models.CharField(max_length=50, default='')
    approved = models.BooleanField(default=False)  # 승인 여부
