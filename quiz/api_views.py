from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Category, Question, Answer, Records, Exam
from .serializers import CategorySerializer, QuestionSerializer, RecordsSerializer, UserRegistrationSerializer, ExamSerializer

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
        questions = Question.objects.prefetch_related('question_answer').all()
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

class QuestionSubmitAPIView(APIView):
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
                except Question.DoesNotExist:
                    return Response({"error": f"Question not found: {question}"}, status=status.HTTP_404_NOT_FOUND)
                except Answer.DoesNotExist:
                    return Response({"error": f"Answer not found: {answer}"}, status=status.HTTP_404_NOT_FOUND)
            Records.objects.create(
                user=request.user,
                category=category,
                score=totalScore
            )
            return Response({
                "message": "Test submitted successfully.",
                "score": float(totalScore)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ExamListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        exams = Exam.objects.filter(student = request.user)
        serializer = ExamSerializer(exams, many=True)  
        return Response(serializer.data, status=200) 

class ExamQuestionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request, exam_id):
        exam = get_object_or_404(Exam, uid=exam_id, student=request.user)
        questions = Question.objects.filter(category=exam.category)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

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

class RecordsViewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        records = Records.objects.filter(user=request.user).order_by('-created_at')
        serializer = RecordsSerializer(records, many=True)
        return Response(serializer.data, status=200)
        