from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserData,Question,QuestionData
from django.contrib.auth import authenticate, login, logout
import os,subprocess,sys
from datetime import datetime,timedelta,date
from django.http import HttpResponse
import tempfile			
import time			
from random import random
from ctd import settings
base=settings.BASE_DIR
# Create your views here.

adminpassword = "forcelogin"
start = timedelta(hours =0+6,minutes = 22,seconds = 0)        #Start time to be set as 4:00 for seniors and 3:30 for juniors   24 hour format
end = timedelta(hours =12+7,minutes = 00,seconds = 30)         #End time to be set as 6:00 for both     24 hour format

start_seconds_left = start.total_seconds()

end_seconds_left = end.total_seconds()

def time_passed():
    current_time = datetime.now().time()
    print current_time      #testing purpose
    seconds_passed = current_time.second + current_time.minute*60 + current_time.hour*3600
    return seconds_passed

def timer(request):
    present_time = time_passed()
    if present_time<start_seconds_left :
        timeleft = start_seconds_left-present_time
        return HttpResponse(timeleft)
    elif present_time>end_seconds_left:
         return HttpResponse("0")
    else:
        timeleft = end_seconds_left-present_time
        return HttpResponse(timeleft)
 
            
def home(request):
    if time_passed()<start_seconds_left:
        return render(request,'Index.html')
    elif time_passed()>end_seconds_left:
        return leaderboard(request)
    else:
        return render (request,'Signup.html')
        
def about(request):
    if time_passed()<start_seconds_left:
        return render(request,'About.html')
    elif time_passed()>end_seconds_left:
        return leaderboard(request)
    else:
        return render (request,'Signup.html')
    
def showteam(request):
    if time_passed()<start_seconds_left:
        return render(request,'Team.html')
    elif time_passed()>end_seconds_left:
        return leaderboard(request)
    else:
        return render (request,'Signup.html')

def signup(request):
    if time_passed()<start_seconds_left:
        return render(request,'Index.html')
    elif time_passed()>end_seconds_left:
        return leaderboard(request)
    elif (request.method == "POST") :
        if (User.objects.filter(username=str(request.POST['username']))).exists():
            return render (request,'Signup.html',{'message':'The username already exists'})   
        else:
            username=request.POST['username']
            password=request.POST['password']
            temp=User.objects.create_user(username=username,password=password,email=request.POST['email'])
            UserData.objects.create(name1=str(request.POST['name1']),name2=str(request.POST['name2']), user=temp)
            user=authenticate(username=username,password=password)
            login(request,user)
            os.mkdir(os.path.join(base,"judge","user",str(request.user.id)))
            os.mkdir(os.path.join(base,"judge","error",str(request.user.id)))
            os.mkdir(os.path.join(base,"judge","input",str(request.user.id)))
            q=Question.objects.all()
            return render(request,'Hub.html',{'questions':q})
    else:
        return render (request,'Signup.html') 

def call_login_page(request):
    if time_passed()<start_seconds_left:
        return render(request,'Index.html')
    elif time_passed()>end_seconds_left:
        return leaderboard(request)
    else:
        return render(request,'Loginpage.html')
        
def log_in(request):
    if time_passed()<start_seconds_left:
        return render(request,'Index.html')
    elif time_passed()>end_seconds_left:
        return leaderboard(request)
    else:
        username = request.POST['username']
        password = request.POST['password']
        adminpass = request.POST['adminpass']
        if request.method == "POST":
            if adminpass == adminpassword:
                user = authenticate(username = username,password = password)
                if user is not None:
                    login(request,user)
                    q = Question.objects.all()
                    return render(request,'Hub.html',{'questions':q})
                else:
                    return render(request,'Loginpage.html',{'message':'invalid username or password'})
            else:
                return render(request,'Loginpage.html',{'message':'invalid admin password'})
        
    
def question_view(request):
    if time_passed()<start_seconds_left:
        return render(request,'Index.html')
    elif time_passed()>end_seconds_left:
        return leaderboard(request)
    elif request.user.is_authenticated():
        q=Question.objects.all()
        return render(request,'Hub.html',{'questions':q})
                      # To display question hub
    else:
        return render(request,'Loginpage.html')
        
def question_list(request,question_id):
    if time_passed()<start_seconds_left:
        return render(request,'Index.html')
    elif time_passed()>end_seconds_left:
        return leaderboard(request)
    elif request.user.is_authenticated():
        q=Question.objects.get(pk=question_id)
        if(QuestionData.objects.filter(user=request.user,question=q)).exists():
            print "The QuestionData object already exists"
        else:
            os.mkdir(os.path.join(base,"judge","user",str(request.user.id),str(question_id)))
            QuestionData.objects.create(user=request.user,question=q)                                                                     
        return render(request,'Editor.html',{'question':q})	############
    else:
        return render(request,'Loginpage.html')
        
def return_editor_page(request,question_id):
    if time_passed()<start_seconds_left:
        return render(request,'Index.html')
    elif time_passed()>end_seconds_left:
        return leaderboard(request)
    elif request.user.is_authenticated():
        q = Question.objects.get(pk=question_id)
        return render(request,'Editor.html',{'question':q})   ##############
    else:
        return render(request,'Loginpage.html')
        
def code_test(request,question_id):
    if time_passed()<start_seconds_left:
        return render(request,'Index.html')
    elif time_passed()>end_seconds_left:
        return leaderboard(request)
    elif request.user.is_authenticated:
        if request.method == "POST" :
            language = request.POST['language']
            flag = request.POST['flag']
            print flag         
            try:    
                code = request.FILES['doc'].read()
            except:
                code = request.POST['user_code']	
        loadbuffer = ""
        reload(sys)
        sys.setdefaultencoding('utf-8')
        location = base+"/judge/user/"+str(request.user.id)+"/"+str(question_id)+"/"+str(request.user.id)+"_"+str(question_id)+"."+language
        if flag == "loadbuffer":
            print location
            if os.path.exists(location):
                if os.path.isfile(location):
                    fileobject = open(location,"r")
                    print location
                    loadbuffer = fileobject.read()
                    fileobject.close()
                else :
                    print "No file"
            else:
                print "path dosent exists"
            return HttpResponse(loadbuffer)
        
        if code != "":
            fileobject = open(location,"w")
            fileobject.write(code)
            fileobject.close()
        if flag == "save":
            return HttpResponse("Your file is saved")
        elif flag == "compile":
            if language == "c":
                cmd = ['gcc', location]
            else:
                cmd = ['g++', location]
            error = terminalfunc(cmd,location)
            if error == "":
                error = "Compilation Successful"
            return HttpResponse(error)
        elif flag=="run":
            if request.method == "POST":
                status = request.POST['status']
                custom = request.POST['custom']
            if status == '1':                       # Making the input file in case of custom input
                inputlocation = base+"/judge/input/"+str(request.user.id)+"/"+str(request.user.id)+"_"+str(question_id)+".in"
                fileobject = open(inputlocation, "w")
                fileobject.write(custom)
                fileobject.close()
            cmd=['python',base+'/judge/customj.py',str(request.user.id)+"_"+str(question_id)+"."+language,str(status)]
            outputfile = terminalfunc(cmd,location)
                                                    # call the judge and pass the input.Get the result and pass it to the html template
            if "Compile Time Error" in outputfile:               # If compile time error 
                if language == "c":
                    cmd = ['gcc', location]
                else:
                    cmd = ['g++', location]
                outputfile = terminalfunc(cmd,location)
                outputfile = "Compile Time Error<br>"+outputfile
            return HttpResponse(outputfile)
        else:
            tempuser = UserData.objects.get(user=request.user)
            tempuser.subid = tempuser.subid + 1
            cmd=['python',base+'/judge/jmain.py',str(request.user.id)+"_"+str(question_id)+"."+language]
            with tempfile.TemporaryFile() as tempf:
                output = subprocess.Popen(cmd, stdout=tempf, stderr=tempf, stdin=tempf)
                output.wait()
                tempf.seek(0)
                outputfile = tempf.read()
            score = outputfile.count('1')
            score = score*20
            print score 
            subdata = QuestionData.objects.get(user=request.user,question=Question.objects.get(pk=question_id))
            if subdata.score < score :           #if score obtained is more than the last time
                tempuser.totaltime = tempuser.totaltime-subdata.timereq
                timetaken = (datetime.now()-tempuser.start).seconds
                subdata.timereq = timetaken                         #update time
                tempuser.totaltime = tempuser.totaltime+subdata.timereq
                tempuser.score = tempuser.score-subdata.score
                subdata.score = score                               #update score
                tempuser.score = tempuser.score+subdata.score
                tempuser.save()
                subdata.save()
            print outputfile            #For testing purpose
            if "-9999" in outputfile:
                return render (request,'Submitpage.html',{'question':question_id,'out1':'C','out2':'C','out3':'C','out4':'C','out5':'C'})

            elif "7" in outputfile:
                return render (request,'Submitpage.html',{'question':question_id,'out1':'A','out2':'A','out3':'A','out4':'A','out5':'A'})
            else:
                outputfile = outputfile.replace('1','R')
                outputfile = outputfile.replace('-99','W')
                outputfile = outputfile.replace('5','T')
            outputfile = outputfile.replace(' ','')
            return render (request,'Submitpage.html',{'question':question_id,'out1':outputfile[1],'out2':outputfile[3],'out3':outputfile[5],'out4':outputfile[7],'out5':outputfile[9]})
    else:
        return render(request,'Loginpage.html')      
            
def leaderboard(request):
    board = UserData.objects.all().order_by('-score','totaltime')
    return render (request,'Leaderboard.html',{'object':board})
    
def log_out(request):
    logout(request)
    return leaderboard(request)
            
def terminalfunc(cmd,location):
    with tempfile.TemporaryFile() as tempf:
        output = subprocess.Popen(cmd, stdout=tempf, stderr=tempf, stdin=tempf)
        output.wait()
        tempf.seek(0)
        outputfile = tempf.read()
    outputfile = outputfile.replace(location, '<br>')
    outputfile = outputfile.replace("\n", "<br>")
    return outputfile
            
#R  right answer
#T  TLE
#W  Wrong answer
#C  Compile time error
#A  abnormal termination    
    
