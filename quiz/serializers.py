from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Category, Records, Question, Answer, Exam, Group, ExamSubmit

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'password2']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['uid', 'category_name']

class RecordsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    class Meta:
        model = Records
        fields = ['uid', 'user', 'category', 'score', 'created_at' ]

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['uid', 'answer', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    question_answer = AnswerSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    # user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Question
        fields = ['uid', 'question', 'marks', 'category', 'question_answer']

class StudentGroupSerializer(serializers.ModelSerializer):
    students = serializers.StringRelatedField(many=True)  # show usernames instead of IDs

    class Meta:
        model = Group
        fields = ["uid", "name", "students"]

class ExamSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()  # username
    category = serializers.StringRelatedField()
    groups = StudentGroupSerializer(many=True, read_only=True)  # nested groups

    class Meta:
        model = Exam
        fields = '__all__'

class ExamSubmitSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    exam = serializers.PrimaryKeyRelatedField(queryset=Exam.objects.all())

    class Meta:
        model = ExamSubmit
        fields = '__all__'
