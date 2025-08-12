from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import random
import uuid

# Create your models here.
# class Contact(models.Model):
#     fname = models.CharField(max_length=25)
#     lname = models.CharField(max_length=25)
#     phone = models.CharField(max_length=10)
#     email = models.CharField(max_length=50)
#     comment = models.TextField()
#     date = models.DateField()
        
#     def __str__(self):
#         return self.fname

# learning about the quiz app
class BaseModel(models.Model):
    uid=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    class Meta:
        abstract=True

class Category(BaseModel):
    category_name = models.CharField(max_length=15, default='Uncatogarized')
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.category_name
    
class Records(BaseModel):
    category=models.ForeignKey(Category,related_name='category_records',on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    score=models.DecimalField(default=0, max_digits=6, decimal_places=3, validators=[MinValueValidator(0), MaxValueValidator(100.000)])
    
    
class Question(BaseModel):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    question=models.CharField(max_length=100)
    marks=models.IntegerField(default=5)
    
    def __str__(self):
        return self.question
    
    def get_answers(self):
        answer_objs = list(Answer.objects.filter(question=self))
        random.shuffle(answer_objs)
        data=[]
        
        for answer_obj in answer_objs:
            data.append({
                'answer':answer_obj.answer,
                'is_correct': answer_obj.is_correct,
            })
        return data

class Answer(BaseModel):
    question=models.ForeignKey(Question,related_name='question_answer', on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.CharField(max_length=50)
    is_correct=models.BooleanField(default=False)
    def __str__(self):
        return self.answer
    
class Group(BaseModel):
    user = models.ForeignKey(User, related_name="group_user", on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Exam(BaseModel):
    teacher = models.ForeignKey(User, related_name = "creator", on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name="examinee", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    deadline = models.DateField()
    submitted = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.title}  ({self.group})"
