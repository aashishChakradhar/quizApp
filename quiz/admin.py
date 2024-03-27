from django.contrib import admin
from quiz.models import *

# Register your models here.

admin.site.register(Contact)
# admin.site.register(Question)

# learning about the quiz app

class AnswerAdmin(admin.StackedInline):
    model=Answer
    
class QuestionAdmin(admin.ModelAdmin):
    inlines=[AnswerAdmin]
    
admin.site.register(Category)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Records)