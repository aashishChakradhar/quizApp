from django.contrib import admin
from django.urls import path
from quiz import views

'''
    'name=' is used for reverse linking which is efficient for dynamic routing
'''
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('create-user', views.create_user, name='create_user'),
    path('delete-user', views.delete_user, name='delete_user'),
    path('view-user', views.view_user, name='view_user'),
    
    # path('index', views.index, name='index'),
    path('about', views.about, name='about_us'),
    path('change-password', views.change_password, name='change_password'),
    path('reset-password', views.reset_password, name='reset_password'),
    
    path('add-category',views.add_category,name='add_category'),
    path('add-question', views.add_question, name='add_question'),
    path('delete-category', views.delete_category, name='delete_category'),
    path('delete-question',views.delete_question,name='delete_question'),
    
    # learning about the quiz app
    path('get-category',views.get_category,name='get_category'),
    path('api/get-quiz/',views.get_quiz,name='get_quiz'), #not webpage in program but to check the question in json format
    path('quiz/',views.take_quiz,name='take_quiz'),
    
    path('view-record',views.view_record,name='view_record'),
    path('view-category',views.view_category,name='view_category'),
    path('view-question',views.view_question,name='view_question'),
]