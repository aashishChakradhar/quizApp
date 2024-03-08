from django.shortcuts import render,HttpResponse
# from quiz.models
# Create your views here.
def home(request):
    return render (request,'home.html')
def question(request):
    return render (request,'question.html')
def about(request):
    return render (request,'about.html')