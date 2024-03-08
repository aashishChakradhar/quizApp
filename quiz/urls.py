from django.contrib import admin
from django.urls import path
from quiz import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('question', views.question, name='question'),
    path('contact', views.contact, name='contact'),
]