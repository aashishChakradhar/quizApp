from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Category, Question, Answer, Records, Exam, Group
from .serializers import  StudentGroupSerializer, UserSerializer,CategorySerializer, QuestionSerializer,RecordsSerializer, UserRegistrationSerializer, ExamSerializer,ExamSubmitSerializer
import random
from datetime import datetime

class RegistrationAPIView(APIView):
    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        data = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            for user in users
        ]
        return Response(data, status=200)

class ProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self,request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=200)

class CategoryCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class QuestionListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        questions = list(Question.objects.prefetch_related('question_answer').all())
        random.shuffle(questions)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=200)

class QuestionCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class RecordsListAPIView(APIView):
    def get(self, request):
        records = Records.objects.select_related('user').all()
        serializer = RecordsSerializer(records, many=True)
        return Response(serializer.data, status=200)

class RecordsCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RecordsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# For students
class RecordsViewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        records = Records.objects.filter(user=request.user).order_by('-created_at')[:15]
        serializer = RecordsSerializer(records, many=True)
        return Response(serializer.data, status=200)

class ExamListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        group = Group.objects.filter(students = request.user)
        exams = Exam.objects.filter(groups__in = group, active = True).distinct()
        serializer = ExamSerializer(exams, many=True)  
        return Response(serializer.data, status=200) 

class ExamQuestionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request, exam_id):
        exam = get_object_or_404(Exam, uid=exam_id, groups__students=request.user)
        questions = list(Question.objects.filter(category=exam.category))
        random.shuffle(questions)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class ExamSubmitAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data.get('answers',[])
            if not data:
                Records.objects.create(
                    user=request.user,
                    category=None,
                    score=0
                )
                return Response({"error": "No answers submitted."}, status=status.HTTP_200_OK)
            totalScore = 0
            category = None
            questionCount = 0
            markCount = 0
            for item in data:
                questionId = item.get("question")
                answerId = item.get("selected_answer")
                try:
                    question = Question.objects.get(uid = questionId)
                    answer = Answer.objects.get(uid = answerId)
                    if answer.question != question:
                        return Response({"error": "Answer does not match question."}, status=status.HTTP_400_BAD_REQUEST)
                    if answer.is_correct:
                        totalScore += question.marks
                    if category is None:
                        category = question.category
                    markCount += question.marks
                    questionCount += 1
                except Question.DoesNotExist:
                    return Response({"error": f"Question not found: {question}"}, status=status.HTTP_404_NOT_FOUND)
                except Answer.DoesNotExist:
                    return Response({"error": f"Answer not found: {answer}"}, status=status.HTTP_404_NOT_FOUND)
            percent = (totalScore/markCount) * 100
            Records.objects.create(
                user=request.user,
                category=category,
                score=percent
            )
            return Response({
                "message": "Test submitted successfully.",
                "score": float(totalScore)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# for teachers
class CreateStudentGroupAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        data = [
            {
                'uid': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
            for user in users
        ]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        user_ids = request.data.get("students", [])
        group_name = request.data.get("name")

        if not group_name:
            return Response({"error": "Group name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        group = Group.objects.create(name=group_name)
        
        if user_ids:
            users = User.objects.filter(id__in=user_ids)
            group.students.set(users)
        
        serializer = StudentGroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CreateExamAPIView(APIView):
    #  permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        groups = Group.objects.all()

        category_serializer = CategorySerializer(categories, many=True)
        group_serializer = StudentGroupSerializer(groups, many=True)

        return Response({
            "categories": category_serializer.data,
            "groups": group_serializer.data
        }, status=200)
    
    def post(self, request):
        """
        Create a new exam with title, category, groups, total_points.
        Expected payload:
        {
            "title": "Exam Title",
            "category": "<category_id>",
            "groups": ["<group_id1>", "<group_id2>"],  # Can be multiple
            "total_points": 50
        }
        """
        data = request.data
        title = data.get("title")
        category_id = data.get("category")
        group_ids = data.get("groups", [])
        total_points = data.get("total_points", 0)
        deadline_str = data.get("deadline")

        try:
            deadline = datetime.strptime(deadline_str, "%d-%m-%Y").date()
        except ValueError:
            return Response({"error": "Invalid date format for deadline. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        if not title or not category_id or not group_ids:
            return Response({"error": "Title, category, and groups are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch related objects
        try:
            category = Category.objects.get(uid=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        groups = Group.objects.filter(uid__in=group_ids)
        if not groups.exists():
            return Response({"error": "One or more groups not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create exam
        exam = Exam.objects.create(
            title=title,
            category=category,
            teacher=request.user,
            total_points=total_points,
            deadline = deadline
        )
        exam.groups.set(groups)
        exam.save()

        serializer = ExamSerializer(exam)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
