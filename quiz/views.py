from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from quiz.models import Contact, Question

# Create your views here.

def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render (request,"index.html")

def loginUser(request):
    # user: @ashish00
    # password: 123@Happy@123
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
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

def question(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        question = request.POST.get('question')
        correct_answer = request.POST.get('correct_answer')
        option_1 = request.POST.get('option_1')
        option_2 = request.POST.get('option_2')
        option_3 = request.POST.get('option_3')
        question = Question(category=category, question=question, correct_answer=correct_answer, option_1=option_1, option_2=option_2,option_3=option_3)
        question.save()
        messages.success(request, "Your Question Has Been Successfully Added!")
    return render (request,'question.html')