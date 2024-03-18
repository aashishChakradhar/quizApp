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

# def question(request):
#     # if request.method == 'POST':
#     #     category = request.POST.get('category')
#     #     question = request.POST.get('question')
#     #     correct_answer = request.POST.get('correct_answer')
#     #     option_1 = request.POST.get('option_1')
#     #     option_2 = request.POST.get('option_2')
#     #     option_3 = request.POST.get('option_3')
#     #     question = Question(category=category, question=question, correct_answer=correct_answer, option_1=option_1, option_2=option_2,option_3=option_3)
#     #     question.save()
#     #     messages.success(request, "Your Question Has Been Successfully Added!")
#     return render (request,'question.html')


#learnig about the app
def quiz(request):
    context = {'categories':Category.objects.all()}
    if request.GET.get('category'):
        return redirect(f"/quiz/?category={request.GET.get('category')}")
    return render(request,'quiz.html',context)

def takequiz(request):
    
    return render(request, 'take_quiz.html')
    
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
                "Category":question_obj.category.category_name,
                "Question":question_obj.question,
                "Marks":question_obj.marks,
                "Answer":question_obj.get_answers(),
            })
            
        payload = {'status':True,'data': data}
        return JsonResponse(payload)
    except Exception as e:
        print(e)
    return HttpResponse('Error Occured')