from django.contrib import admin
from django.urls import path
from quiz import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('question', views.question, name='question'),
]