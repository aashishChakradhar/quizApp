from django.contrib import admin
from django.urls import path
from quiz import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('signup', views.register, name='signup'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('add_category',views.add_category,name='add_category'),
    path('add_question', views.add_question, name='add_question'),
    
    # learning about the quiz app
    path('get-category',views.get_category,name='get_category'),
    path('api/get-quiz/',views.get_quiz,name='get_quiz'),
    path('quiz/',views.quiz,name='quiz'),
]