from django.contrib import admin
from .models import Question,UserData,QuestionData
# Register your models here.


admin.site.register(Question)
admin.site.register(UserData)
admin.site.register(QuestionData)
