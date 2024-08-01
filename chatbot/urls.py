from django.urls import path
from chatbot import views

urlpatterns = [
    path('applicant-bot/', views.applicant, name='applicant'),       # 지원자들을 위한 챗봇
]
