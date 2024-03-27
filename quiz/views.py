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
    if request.user.is_superuser:
        return render (request,"add_question.html")
    else:
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
        if user is not None:# if the user is logged in
            # A backend authenticated the credentials
            login(request,user)
            return redirect("/")
        else:# if the user is not logged in
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
    if request.user.is_superuser:
        context = {'categories':Category.objects.all()}
        if request.method == 'POST':
            category_name = request.POST.get('category')
            question = request.POST.get('question')
            answer_data=[
                (request.POST.get('answer1'), True),
                (request.POST.get('answer2'), False),
                (request.POST.get('answer3'), False),
                (request.POST.get('answer4'), False),
            ]
            marks = request.POST.get('marks')
            
            category,created=Category.objects.get_or_create(category_name=category_name)
            question = Question(category=category, question=question, marks=marks)
            question.save()
            category.save()
            
            for answer_individual, is_correct in answer_data:
                answer=Answer(question=question,answer=answer_individual,is_correct=is_correct)
                answer.save()
            
            messages.success(request, "Your Question Has Been Successfully Added!")
        return render (request,'question.html',context)
    else: return render (request,'index.html')


#learnig about the app
def get_category(request):
    context = {'categories':Category.objects.all()}
    if request.GET.get('category'):
        return redirect(f"/quiz/?category={request.GET.get('category')}")
    else:return render(request,'quiz_category.html',context)

def quiz(request):
    context = {'category':request.GET.get('category')}
    return render(request, 'take_quiz.html', context)
    
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