from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from quiz.models import *
import random

# Create your views here.

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

def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        return render (request,"index.html")
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

def add_category(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            category_name = request.POST.get('new_category')
            category = Category(category_name=category_name)
        return render (request,'add_category.html')
    else: return render (request,'index.html')
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
            category, created = Category.objects.get_or_create(category_name=category_name)
            question,created = Question.objects.get_or_create(category=category, question=question, marks=marks)
            
            for answer_individual, is_correct in answer_data:
                answer=Answer(question=question,answer=answer_individual,is_correct=is_correct)
                answer.save()
            messages.success(request, "Your Question Has Been Successfully Added!")
        return render (request,'add_question.html',context)
    else: return render (request,'permission.html')


def delete_category(request):
    if request.user.is_superuser:
        context = {'categories':Category.objects.all()}
        if request.GET.get('category'):
            category_name = request.GET.get('category')
            instance = Category.objects.filter(category_name=category_name)
            if instance.exists():
                instance.delete()
                return HttpResponse("Category deleted successfully!")
            else:
                return HttpResponse("Category does not exist!")
        return render(request,"get_category.html",context)
    else: return HttpResponse('Delete Fail: User is not a superuser')
def delete_question(request):
    if request.user.is_superuser:
        context = {'questions':Question.objects.all()}
        if request.GET.get('question'):
            question_del = request.GET.get('question')
            instance = Question.objects.filter(question=question_del)
            if instance.exists():
                instance.delete()
                return HttpResponse("Question deleted successfully!")
            else:
                return HttpResponse("Question does not exist!")
        return render(request,"get_question.html",context)
    else: return HttpResponse('Delete Fail: User is not a superuser')

#learnig about the app
def get_category(request):
    context = {'categories':Category.objects.all()}
    if request.GET.get('category'):
        return redirect(f"/quiz/?category={request.GET.get('category')}")
    else:return render(request,'get_category.html',context)

def take_quiz(request):
    context = {'category':request.GET.get('category')}
    if request.method=='POST':
        category_name = request.POST.get('category_record')
        current_user = request.user
        score=10
        # checks if category already exist
        category, created = Category.objects.get_or_create(category_name=category_name)
        # save the new record
        records = Records.objects.create(category=category, user_name=current_user, score=score)
        return redirect(f"/index")
    return render(request, 'get_quiz.html',context)

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

def get_record(request):
    try:
        current_user = request.user
        all_records = Records.objects.all()
        filter_record = all_records.filter(user_name=current_user)
        context = {'records': filter_record}
        return render(request, 'records.html', context)
    except Exception as e:
        print(e)
    return HttpResponse('No records found!')
