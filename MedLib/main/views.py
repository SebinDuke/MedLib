from django.shortcuts import render,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist #This may be used instead of Users.DoesNotExist
from django.http import HttpResponse,HttpResponseRedirect
from .medget import medget
from django.views import generic
import re

from django.urls import reverse
#for older versoins of Django use:
#from django.core.urlresolvers import reverse


from .models import Users
from main.forms import SignupForm,LoginForm,SearchForm#,AddTopicForm,AddOpinionForm,

ob=medget()
def index(request):
    if request.session.has_key('user_id'):
        uid=request.session['user_id']
        try:
            user=Users.objects.get(pk=uid)
            return render(request, 'Temp/logged.html',{'user_id':user})
        except Users.DoesNotExist:
            return HttpResponse("UserName not found")
    else:
        return render(request, 'Temp/main.html')

def login(request):
    return render(request, 'Temp/login.html')

def signup(request):
    return render(request, 'Temp/signup.html')

def search_checkup(request):
    return render(request, 'Temp/search_checkup.html')

def search(request):
    if request.method == 'POST':
        topic=SearchForm(request.POST)
        if topic.is_valid():

            #t=Topic.objects.get(topic_text=topic.cleaned_data.get('topic_text'))
            top_li = Topic.objects.all()
            li=[]
            for t in top_li:
                if re.search(topic.cleaned_data.get('topic_text'),t.topic_text,re.IGNORECASE):
                    li.append(t)
            if request.session.has_key('user_id'):
                uid = request.session['user_id']
                user = Users.objects.get(pk=uid)
                return render(request, 'Temp/searchresults.html', {'user_id':user,"list": li})
            else:
                return render(request, 'Temp/searchresultL.html', {"list": li})
        else:
            return HttpResponse("Form not valid")
    else:
        return HttpResponse("not POST")

def search1(request):
    if request.method == 'POST':
        topic=SearchForm(request.POST)
        if topic.is_valid():
            sim_str=topic.cleaned_data.get('topic_text')
            checklist=sim_str.split(",")
            #checklist = topic.cleaned_data.get('symptom')

            try:
                checklist.append(request.POST['symptom1'])
            except:
                pass
            try:
                checklist.append(request.POST['symptom2'])
            except:
                pass
            try:
                checklist.append(request.POST['symptom3'])
            except:
                pass
            try:
                checklist.append(request.POST['symptom4'])
            except:
                pass
            try:
                checklist.append(request.POST['symptom5'])
            except:
                pass
            try:
                checklist.append(request.POST['symptom6'])
            except:
                pass
            try:
                checklist.append(request.POST['symptom7'])
            except:
                pass
            #return HttpResponse(checklist)

            li=ob.search_symptoms(checklist)
            l = len(li)
            return render(request, 'Temp/symtoms.html', {"list": li,"len":l})


            #return HttpResponse((' ').join(li))
            #t=Topic.objects.get(topic_text=topic.cleaned_data.get('topic_text'))

        else:
            return HttpResponse("Form not valid")
    else:
        return HttpResponse("not POST")


def register(request):
    if request.method == 'POST':
        signup=SignupForm(request.POST)
        if signup.is_valid():
            p=Users(
                user_name=signup.cleaned_data.get('username'),
                first_name=signup.cleaned_data.get('firstname'),
                last_name=signup.cleaned_data.get('lastname'),
                email=signup.cleaned_data.get('email'),
                pwd=signup.cleaned_data.get('pwd'),
                age=signup.cleaned_data.get('age'),
                height=signup.cleaned_data.get('height'),
                weight=signup.cleaned_data.get('weight'),
                country=signup.cleaned_data.get('country'),
            )
            p.save()
            request.session['user_id'] = p.id
    return HttpResponseRedirect(reverse('main:index'))

def logInReq(request):
    if request.method == 'POST':
        log=LoginForm(request.POST)
        if log.is_valid():
            try:
                user=Users.objects.get(user_name=log.cleaned_data.get('username'),pwd=log.cleaned_data.get('pwd'))
                request.session['user_id'] = user.id
                return HttpResponseRedirect(reverse('main:index'))
            except Users.DoesNotExist:
                return HttpResponse("WRONG USERNAME OR PASSWORD")


"""
class LoggedIn(generic.DetailView):
	model = Users
	template_name = 'Temp/logged.html'
	context_object_name = 'user_id'
"""

def quest(request):
    global ob
    if request.method == 'POST':
        l=request.POST['len']
        checklist=[]
        for i in range(int(l)):
            try:
                checklist.append(request.POST['symptom'+str(i)])
            except:
                pass
        #return HttpResponse(checklist)
        if request.session.has_key('user_id'):
            uid = request.session['user_id']
            try:
                user = Users.objects.get(pk=uid)
            except ObjectDoesNotExist:
                HttpResponse("Object not found")

            age=user.age
            sex=user.sex
            ob.get_data(sex,age)
            lis=[]
            for i in checklist:
                dic={}
                dic['id']=i
                dic['status']='present'
                lis.append(dic)
                dic=None

            ob.add_symptoms(lis)
            return HttpResponse("yoyo")
        #ob.get_questions()

def logout(request):
   try:
      del request.session['user_id']
   except:
      pass
   return HttpResponseRedirect(reverse('main:index'))
