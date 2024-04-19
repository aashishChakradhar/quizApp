from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
from quiz.models import *
import random
import quiz.check as check #custom model containing verification related models

# Create your views here.

# login and sign up related views
def loginUser(request):
    # user: student, admin
    # password: student, admin
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            # check if user is valid
            user = authenticate(username=username, password=password)
            if user is not None:# if the user is logged in
                login(request,user)
                return redirect("/")
            else:# if the user is not logged in
                raise ValueError("Error: Invalid Credentials")
        except ValueError as e:
            messages.error(request,str(e))
            return render (request,"signin.html")
        except Exception as e:
            messages.error(request,f"Error: {str(e)}")
            return render (request,"signin.html")
    else:
        return render (request,'signin.html')
def logoutUser(request):
    try:
        logout(request)
        messages.success(request,"Successfully Logged out")
    except Exception as e:
        messages.error(request,f"Error: {str(e)}")
    return redirect ('/login')

def create_user(request):
    if request.method == "POST":
        # for teacher and student
        try:
            # read input from form
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            firstName = request.POST.get('firstName')
            lastName = request.POST.get('lastName')
            status = request.POST.get('status')
            
            # checks the status of user to be created
            if (status.lower() == 'admin'):
                is_superuser =True 
                is_staff =True
            elif (status.lower() == 'teacher'):
                is_superuser =False 
                is_staff =True
            elif (status.lower() == 'student'):
                is_superuser =False 
                is_staff =False
            
            # check validation
            if(not check.valid_name(firstName)):
                raise ValueError("Error: Invalid First Name")
            if(not check.valid_name(lastName)):
                raise ValueError("Error: Invalid Last Name")
            if(not check.valid_email(email)):
                raise ValueError("Error: Invalid Email")
            if(not check.valid_username(username)):
                raise ValueError("Error: Invalid Username")

            # creating user
            user = User.objects.create_user(username,email,password,is_superuser=is_superuser)
            
            # additional user details
            user.first_name=firstName
            user.last_name=lastName
            user.is_staff = is_staff
            user.save()
            
            if request.user.is_anonymous:
            # login the created user
                user = authenticate(username=username, password=password)
                if user is not None:# if the user is logged in
                    login(request,user)
                    return redirect("/")
                else:# if the user is not logged in
                    return render (request,"signin.html")
            
            # display success messages    
            if(is_superuser):messages.success(request, "Admin Created Successfully")
            elif(is_staff):messages.success(request, "Teacher Created Successfully")
            elif(not is_staff):messages.success(request, "Student Created Successfully")
                
        except ValueError as e:
            messages.error(request,str(e))
        except Exception as e:
            messages.error(request, str(e))
        return render (request,'create_user.html')
    else:
        return render (request,'create_user.html')
def delete_user(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        if request.user.is_superuser:
            if request.method == "POST":
                try:
                    del_user = request.POST.get('username')
                    users = User.objects.get(username = del_user)
                    users.delete()
                    messages.success(request, "User deleted successfully")
                except User.DoesNotExist:
                    messages.error(request, "User does not exist")
                return redirect("delete_user")
            else:
                users = User.objects.filter(is_superuser = False)
                context = {"users": users}
                return render(request, "delete_user.html",context)
        else:
            return redirect('home')

# basic pages of website
def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        return render (request,"index.html")
def about(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        user_name = request.user
        context = {
            'details':User.objects.filter(username=user_name)
        }
        return render (request,'about.html',context)

# change password of own account
def change_password(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        if request.method == "POST":
            try:
                old_password = request.POST.get('old_password')
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                if request.user.check_password(old_password): #checks old password
                    if(confirm_password == new_password): # matches new password
                        request.user.set_password(new_password) # set new password
                        request.user.save()
                        update_session_auth_hash(request, request.user) #keeps user loggedin
                        messages.success(request, "Your Password Has Been Changed Successfully!")
                        return redirect('index')
                    else:
                        raise ValueError("Error: Passwords Do Not Match")
                else:
                    raise ValueError("Error: Invalid Old Password")
            except ValueError as e:
                messages.error(request,str(e))
                return render (request,'contact.html')
            except Exception as e:
                messages.error(request,str(e))
                return render (request,'contact.html')
        else:
            return render (request,'contact.html')
# reset the password
def reset_password(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        if request.user.is_superuser:
            if request.method == "POST":
                try:
                    username = request.POST.get('username')
                    new_password = "happy123"
                    user = User.objects.get(username = username)
                    user.set_password(new_password) # set new password
                    user.save()
                    messages.success(request, f"Password for {username} Has Been Successfully Reset to: {new_password}")
                    return redirect('index') # goto homepage
                except User.DoesNotExist:
                    messages.error(request, f"Error: User {username} does not exist")
                except Exception as e:
                    messages.error(request,str(e))
                return render (request,'reset_password.html')
            else:
                return render (request,'reset_password.html')
        else:
            messages.error(request, "Reset Password Fail: User is not a Superuser")
            return render (request,'index.html')

# main operations related to working of quiz app
def get_category(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        context = {'categories':Category.objects.all()}
        if request.GET.get('category'):
            return redirect(f"/quiz/?category={request.GET.get('category')}")
        else:return render(request,'get_category.html',context)
def take_quiz(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        context = {'category':request.GET.get('category')}
        try:
            if request.method=='POST':
                category_name = request.POST.get('category_record')
                current_user = request.user

                total_attempted_marks = request.POST.get('total_attempted_marks')
                total_marks_obtained = request.POST.get('total_marks_obtained')
                total_percentage = request.POST.get('total_percentage')
                # score=request.POST.get('score')
                # checks if category already exist
                category, created = Category.objects.get_or_create(category_name=category_name)
                # save the new record
                records = Records.objects.create(category=category, user_name=current_user, score=total_percentage)
                messages.success(request,"Your Score Has Been Successfully Added!")
                return redirect(f"/get-category")
            return render(request, 'get_quiz.html',context)
        except Exception as e:
            messages.error(request,str(e))
            return render(request, 'get_quiz.html',context)

#for reading datas from question form
def get_quiz(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        try:
            question_objs=Question.objects.all()
            if request.GET.get('category'):
                question_objs=question_objs.filter(category__category_name__icontains=request.GET.get('category'))
            question_objs=list(question_objs)    
            
            data=[]
            random.shuffle(question_objs)
            count = 0
            for question_obj in question_objs:
                count += 1 
                if count <= 10:
                    data.append({
                        "uid":question_obj.uid,
                        "category":question_obj.category.category_name,
                        "question":question_obj.question,
                        "marks":question_obj.marks,
                        "answer":question_obj.get_answers(),
                    })
                else: break
                
            payload = {'status':True,'data': data}
            return JsonResponse(payload)
        except Exception as e:
            messages.error(request, str(e))
            return render(request,"index.html")

# only admin operations
# adding stuff
def add_category(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        if request.user.is_superuser:
            if request.method == 'POST':
                category_name = request.POST.get('new_category')
                category, created = Category.objects.get_or_create(category_name=category_name)
                messages.success(request, "Add Success: Category Added Successfully")
            return render (request,'add_category.html')
        else:
            messages.error(request, "Add Fail: User is not a superuser")
            return render (request,'permission.html')
def add_question(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        if request.user.is_superuser:
            try:
                context = {'categories':Category.objects.all()}
                if request.method == 'POST':
                    category_name = request.POST.get('category')
                    question = request.POST.get('question')
                    answer_data=[
                        (request.POST.get('answer1'), True),
                        (request.POST.get('answer2'), False),
                        (request.POST.get('answer3'), False),
                        (request.POST.get('answer4'), False),
                    ]
                    marks = request.POST.get('marks')
                    category, created = Category.objects.get_or_create(category_name=category_name)
                    question,created = Question.objects.get_or_create(category=category, question=question, marks=marks)
                    
                    for answer_individual, is_correct in answer_data:
                        answer=Answer(question=question,answer=answer_individual,is_correct=is_correct)
                        answer.save()
                    messages.success(request, "Your Question Has Been Successfully Added!")
                return render (request,'add_question.html',context)
            except Exception as e:
                messages.error(request, str(e))
                return render (request,'add_question.html',context)
        else:
            messages.error(request, "Add Fail: User is not a Superuser")
            return render (request,'index.html')

# deleting stuff
def delete_category(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        if request.user.is_superuser:
            context = {'categories':Category.objects.all()}
            if request.GET.get('category'):
                category_name = request.GET.get('category')
                instance = Category.objects.filter(category_name=category_name)
                if instance.exists():
                    instance.delete()
                    messages.success(request, "Your Category Has Been Successfully Deleted!")
                else:
                    messages.error(request, "Category Doesnot Exists!")
            return render(request,"get_category.html",context)
        else: 
            messages.error(request, "Delete Fail: User is not a superuser")
            return render(request,"permission.html")
def delete_question(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        if request.user.is_superuser:
            context = {'questions':Question.objects.all()}
            if request.GET.get('question'):
                question_del = request.GET.get('question')
                instance = Question.objects.filter(question=question_del)
                if instance.exists():
                    instance.delete()
                    messages.success(request, "Your Question Has Been Successfully Deleted!")
                else:
                    messages.error(request, "Question Doesnot Exist!")
            return render(request,"delete_question.html",context)
        else: 
            messages.error(request, "Delete Fail: User is not a superuser")
            return render(request,"permission.html")

# viewing stuff
def view_record(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        try:
            if request.user.is_superuser:
                if request.method=="POST":
                    user= request.POST.get('user')
                    category_form= request.POST.get('category')
                    time= request.POST.get('time')
                    if (user == 'all' and category_form == 'all'):
                        all_records=Records.objects.all()
                    elif(user == 'all' and category_form != 'all'):
                        all_records = Records.objects.filter(category = category_form)
                    elif(user != 'all' and category_form == 'all'):
                        all_records = Records.objects.filter(user_name=user) 
                    else:
                        all_records = Records.objects.filter(user_name=user, category = category_form)
                    context = {
                        'records':all_records,
                        'users':User.objects.all(),
                        'categories': Category.objects.all(),
                    }
                else:
                    context = {
                        'records':Records.objects.all(),
                        'users':User.objects.all(),
                        'categories': Category.objects.all(),
                    }
            else:
                current_user = request.user
                filter_records=Records.objects.filter(user_name = current_user)
                context = {'records': filter_records}
            return render(request, 'view_record.html', context)
        except Exception as e:
            messages.error(request,str(e))
            return render(request,"index.html")
def view_category(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        try:
            all_category = Category.objects.all()
            context = {'categories': all_category}
            return render(request, 'view_category.html', context)
        except Exception as e:
            messages.error(request,str(e))
            return render(request,"index.html")
def view_question(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        if request.user.is_superuser:
            try:
                all_question = Question.objects.all()
                context = {'questions': all_question}
                return render(request, 'view_question.html', context)
            except Exception as e:
                messages.error(request, str(e))
            return render(request, 'index.html')
        else: 
            messages.error(request, "View Fail: User is not a superuser")
            return render(request,"permission.html")
