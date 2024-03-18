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
    # path('question', views.question, name='question'),
    
    # learning about the quiz app
    path('quiz',views.quiz,name='quiz'),
    path('take-quiz',views.takequiz,name='take_quiz'),
    path('api/get-quiz/',views.get_quiz,name='get_quiz')
]