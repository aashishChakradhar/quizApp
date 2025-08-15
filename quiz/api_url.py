from django.urls import path
from quiz import api_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'api'

urlpatterns = [
    # for api testing token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Category Endpoints
    path('categories/', api_views.CategoryListAPIView.as_view(), name='category-list'),
    path('categories/create/', api_views.CategoryCreateAPIView.as_view(), name='category-create'),

    # Question Endpoints
    path('questions/', api_views.QuestionListAPIView.as_view(), name='question-list'),
    path('questions/create/', api_views.QuestionCreateAPIView.as_view(), name='question-create'),
    path('questions/submit-test/', api_views.QuestionSubmitAPIView.as_view(), name='question-submit'),
    # (Optional: path for creating questions could go here)
    path('exams/', api_views.ExamListAPIView.as_view(), name='exams'),
    path('exams/<str:exam_id>/questions/',api_views.ExamQuestionAPIView.as_view(), name='take-exam'),
    path('exams/<str:exam_id>/submit/',api_views.QuestionSubmitAPIView.as_view(), name='submit-exam'),
    
    # Record Endpoints
    path('records/', api_views.RecordsListAPIView.as_view(), name='record-list'),
    path('records/create/', api_views.RecordsCreateAPIView.as_view(), name='record-create'),
    path('records/view/',api_views.RecordsViewAPIView.as_view(), name='record-view'),

    # User Endpoints (Admin-only, optional)
    path('users/', api_views.UserListAPIView.as_view(), name='user-list'),
    path('profile/', api_views.ProfileAPIView.as_view(), name='profile'),
    path('update/', api_views.UpdateProfileAPIView.as_view(), name='update-profile'),

    path('register/',api_views.RegistrationAPIView.as_view(), name='create-user')
]
