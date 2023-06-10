from django.db import models

 # login_user
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    pw = models.CharField(max_length=1000)
    region = models.CharField(max_length=50)
    category = models.CharField(max_length=50)