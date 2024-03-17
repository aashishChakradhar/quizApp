from django.db import models

# Create your models here.
class Contact(models.Model):
    fname = models.CharField(max_length=25)
    lname = models.CharField(max_length=25)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=50)
    comment = models.TextField()
    date = models.DateField()

class Question(models.Model):
    category = models.CharField(max_length=20, default = 'None')
    question = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=20)
    option_1 = models.CharField(max_length=20)
    option_2 = models.CharField(max_length=20)
    option_3 = models.CharField(max_length=20)