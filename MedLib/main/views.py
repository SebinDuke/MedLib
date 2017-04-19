from django.shortcuts import render,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist #This may be used instead of Users.DoesNotExist
from django.http import HttpResponse,HttpResponseRedirect
from .medget import medget
from django.views import generic
import re
import medplace
from django.urls import reverse
#for older versoins of Django use:
#from django.core.urlresolvers import reverse
import ast

from .models import Users
from main.forms import SignupForm,LoginForm,SearchForm#,AddTopicForm,AddOpinionForm,

ob=medget()
j = []

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
        topic=SearchForm(request.POST,initial={"topic_text": "c"})
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
                name=signup.cleaned_data.get('name'),
                email=signup.cleaned_data.get('email'),
                pwd=signup.cleaned_data.get('pwd'),
                age=signup.cleaned_data.get('age'),
                sex=signup.cleaned_data.get('sex'),
            )
            p.save()
            request.session['user_id'] = p.id
    return HttpResponseRedirect(reverse('main:index'))

def logInReq(request):
    if request.method == 'POST':
        log=LoginForm(request.POST)
        if log.is_valid():
            try:
                user=Users.objects.get(email=log.cleaned_data.get('email'),pwd=log.cleaned_data.get('pwd'))
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

            age = 21#int(user.age)
            sex = 'male'#user.sex.lower()
            ob.get_data(sex,age)
            lis=[]
            for i in checklist:
                dic={}
                dic['id']=i
                dic['status']='present'
                lis.append(dic)
                dic=None

            #ob.add_symptoms(lis)
            request.session['lis'] = lis
            return HttpResponseRedirect(reverse('main:question'))
            #return HttpResponse(a)
        #ob.get_questions()

def question(request):
    global ob
    #global j
    #j +=1
    i = []
    if request.session.has_key('lis'):
        i = request.session['lis']
        try:
            del request.session['lis']
        except:
            pass
        ob.add_symptoms(i)
        a = ob.get_question()
        return render(request, 'Temp/question.html', {"ques_dict": a})
        #return HttpResponse(a)
    elif not ob.check_risk():
        i = {}
        #id = request.POST.get('id')
        if request.POST.get('yes'):
            i['id'] = str(request.POST['option'])
            i['status'] = 'present'
        elif request.POST.get('no'):
            i['id'] = str(request.POST['option'])
            i['status'] = 'absent'
        elif request.POST.get('dont'):
            i['id'] = str(request.POST['option'])
            i['status'] = 'unknown'
    
        a = []
        a.append(i)
        ob.add_symptoms(a)
        a = ob.get_question()
        #j = i
        return render(request, 'Temp/question.html', {"ques_dict": a})
    else:
        result = {}
        result = ob.get_result()
        return render(request, 'Temp/get_result.html', {"result": result})

def doc_list(request):
    location = request.POST['location']
    loc_dict = ast.literal_eval(location)
    loc_dict1 = {}
    loc_dict1['lat'] = loc_dict['latitude']
    loc_dict1['lng'] = loc_dict['longitude']
    doctor_type = request.POST['doctor_type']
    doctor = doctor_type.split()
    doctor_search = doctor[-2] + doctor[-1]
    plac = medplace.get_places(lat_lng=loc_dict1, doctor_type=doctor_search)
    return render(request, 'Temp/doctor.html', {"doc_list": plac})
    
def logout(request):
   try:
      del request.session['user_id']
   except:
      pass
   return HttpResponseRedirect(reverse('main:index'))
