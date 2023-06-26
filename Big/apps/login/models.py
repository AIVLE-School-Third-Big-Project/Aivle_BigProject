from django.db import models
from django.utils import timezone

 # login_user
class User(models.Model):
    name = models.CharField(max_length=15, default='KT사원')
    id = models.IntegerField(primary_key=True)
    pw = models.CharField(max_length=1000)
    region = models.CharField(max_length=50)
    category = models.CharField(max_length=50) # 관리자 or 작업자
    failed_attempts = models.IntegerField(default=0) # 실패 횟수
    locked_until = models.DateTimeField(null=True, blank=True) # 계정 장금 시간
    
    def increment_failed_attempts(self): # 로그인 실패시 횟수 증가
        self.failed_attempts += 1 # 1회 +
        if self.failed_attempts >= 5: # 5회 실패시
            self.locked_until = timezone.now() + timezone.timedelta(minutes=1) # 10분 잠금
        self.save()

    def reset_failed_attempts(self): # 로그인 실패 횟수 초기화 -> 로그인 성공하면...
        self.failed_attempts = 0
        self.locked_until = None
        self.save()

    def is_account_locked(self): # 계정이 잠겨있는지
        return self.locked_until and self.locked_until > timezone.now()
    
    