from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from quiz.models import *
import random

# Create your views here.

def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render (request,"index.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        user = User.objects.create_user(username, email, password)
        user.first_name=firstName
        user.last_name=lastName
        user.save()
    return render (request,'register.html')

def loginUser(request):
    # user: @ashish00
    # password: 123@Happy@123
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # check if user is valid
        user = authenticate(username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request,user)
            return redirect("/")
        else:
            # No backend authenticated the credentials
            return render (request,"login.html")
    return render (request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect ('/login')

def about(request):
    return render (request,'about.html')

def contact(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        contact = Contact(fname = fname, lname = lname, email = email, phone=phone, comment = comment, date = datetime.today())
        contact.save()
        messages.success(request, "Your Message Has Been Revieved!")
    return render (request,'contact.html')

def add_question(request):
    context = {'categories':Category.objects.all()}
    if request.method == 'POST':
        
        
        category_name = request.POST.get('category')
        question = request.POST.get('question')
        answer1=request.POST.get('answer1')
        answer2=request.POST.get('answer2')
        answer3=request.POST.get('answer3')
        answer4=request.POST.get('answer4')
        marks = request.POST.get('marks')
        
        
        # basemodel=BaseModel()
        category,created=Category.objects.get_or_create(category_name=category_name)
        question = Question(category=category, question=question, marks=marks)
        
        answer1=Answer(question=question,answer=answer1,is_correct=True)
        answer2=Answer(question=question,answer=answer2,is_correct=False)
        answer3=Answer(question=question,answer=answer3,is_correct=False)
        answer4=Answer(question=question,answer=answer4,is_correct=False)
        
        # basemodel.save()
        question.save()
        category.save()
        answer1.save()
        answer2.save()
        answer3.save()
        answer4.save()
        
        messages.success(request, "Your Question Has Been Successfully Added!")
    return render (request,'question.html',context)


#learnig about the app
def home(request):
    context = {'categories':Category.objects.all()}
    if request.GET.get('category'):
        return redirect(f"/quiz/?category={request.GET.get('category')}")
    else:return render(request,'home.html',context)

def quiz(request):
    context = {'category':request.GET.get('category')}
    return render(request, 'quiz.html', context)
    
#for createing an api
def get_quiz(request):
    try:
        question_objs=Question.objects.all()
        if request.GET.get('category'):
            question_objs=question_objs.filter(category__category_name__icontains=request.GET.get('category'))
        question_objs=list(question_objs)    
        data=[]
        random.shuffle(question_objs)
        
        for question_obj in question_objs:
            data.append({
                "uid":question_obj.uid,
                "category":question_obj.category.category_name,
                "question":question_obj.question,
                "marks":question_obj.marks,
                "answer":question_obj.get_answers(),
            })
            
        payload = {'status':True,'data': data}
        return JsonResponse(payload)
    except Exception as e:
        print(e)
    return HttpResponse('Error Occured')