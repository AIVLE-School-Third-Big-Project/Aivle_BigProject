from django.db import models

 # 공지사항 db
class Post(models.Model):
   title = models.CharField(max_length=100)
   content = models.TextField()
   name = models.CharField(max_length=10)
   created = models.CharField(max_length=15)
   
