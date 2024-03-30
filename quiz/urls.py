from django.contrib import admin
from django.urls import path
from quiz import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('signup', views.register, name='signup'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('add-category',views.add_category,name='add_category'),
    path('add-question', views.add_question, name='add_question'),
    
    # learning about the quiz app
    path('get-category',views.get_category,name='get_category'),
    path('get-records',views.get_record,name='get_records'),
    path('api/get-quiz/',views.get_quiz,name='get_quiz'), #not webpage in program but to check the question in json format
    path('quiz/',views.quiz,name='quiz'),
]