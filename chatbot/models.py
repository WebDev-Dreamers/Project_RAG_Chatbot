from django.db import models

# Create your models here.

# 대화 주제
class Subject(models.Model):
    title = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# 대화 내용 (질의 응답 정보)
class Conversation(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='conversations')
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)

    def __str__(self):
        return self.subject