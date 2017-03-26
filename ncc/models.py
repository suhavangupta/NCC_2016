from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.utils import timezone
import django   


# Create your models here.

class UserData(models.Model):
    name1 = models.CharField(max_length=30,blank=False)
    name2 = models.CharField(max_length=30,blank=True)  
    score = models.IntegerField(default=0)
    subid = models.IntegerField(default=0)
    start = models.DateTimeField(default=django.utils.timezone.now)
    totaltime = models.IntegerField(default = 0)          
    user = models.OneToOneField(User)
    def __str__(self):
        return (self.name1)
        
class Question(models.Model):
    question_name = models.CharField(max_length=100,blank=False)
    question_text = models.CharField(max_length=3000,blank=False)
    def __str__(self):
        return (self.question_name)
        
class QuestionData(models.Model):
    score = models.IntegerField(default=0)
    timereq = models.IntegerField(default = 0)
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)

