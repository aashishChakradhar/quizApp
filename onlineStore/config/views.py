from django.shortcuts import render,HttpResponse
# from home.models import Contact

# Create your views here.

def home(request):
    return render(request,'home.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def services(request):
    return render(request,'services.html')