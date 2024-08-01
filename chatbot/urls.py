from django.urls import path
from chatbot import views

urlpatterns = [
    path('applicant-bot/', views.applicant, name='applicant'),       # 지원자들을 위한 챗봇
    path('student-bot/', views.student, name='student'),             # 수강생들을 위한 챗봇
]