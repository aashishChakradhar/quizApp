from django.db import models
import random
import uuid

# Create your models here.
class Contact(models.Model):
    fname = models.CharField(max_length=25)
    lname = models.CharField(max_length=25)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    comment = models.TextField()
    date = models.DateField()
    # def __init__(self,fname,lname,phone,comment,email,date):
    #     self.fname=fname.upper()
    #     self.lname=lname.upper()
    #     self.phone=phone
    #     self.email=email
    #     self.comment=comment.upper()
    #     self.date=date
        
    def __str__(self):
        return self.fname
    
# class Question(models.Model):
#     category = models.CharField(max_length=20, default = 'None')
#     question = models.CharField(max_length=100)
#     correct_answer = models.CharField(max_length=20)
#     option_1 = models.CharField(max_length=20)
#     option_2 = models.CharField(max_length=20)
#     option_3 = models.CharField(max_length=20)
#     def __str__(self):
#         return self.category

# learning about the quiz app
class BaseModel(models.Model):
    uid=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    class Meta:
        abstract=True

class Category(BaseModel):
    category_name = models.CharField(max_length=15, default='Uncatogarized')
    def __str__(self):
        return self.category_name
    
class Question(BaseModel):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
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
    answer = models.CharField(max_length=50)
    is_correct=models.BooleanField(default=False)
    def __str__(self):
        return self.answer