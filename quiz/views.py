from django.shortcuts import render,HttpResponse
from datetime import datetime
from quiz.models import Contact, Question
from django.contrib import messages

# Create your views here.
def home(request):
    return render (request,'home.html')
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
        messages.success(request, "Your Message Has Been Sent.")
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
        messages.success(request, "Your Question Has Been Inserted.")
    return render (request,'question.html')