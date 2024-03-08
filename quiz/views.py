from django.shortcuts import render,HttpResponse
# from quiz.models
# Create your views here.
def home(request):
    return render (request,'home.html')