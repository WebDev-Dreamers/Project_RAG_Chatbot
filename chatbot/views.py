# 지원자 Chatbot을 위한 함수들
from django.http import JsonResponse
from chatbot.models import *

# 지원자, 수강생들을 위한 RAG Chatbot 모듈
from chatbot.Applicant_Bot_Functions.applicant_chatbot import new_memory, applicant_chatbot
from chatbot.Student_Bot_Functions.student_chatbot import new_memory, student_chatbot


# Chatbot 메모리
memory = None

# 지원자들을 위한 챗봇
def applicant(request):

    global memory

    # GET 요청 -> 최초 URL 접속
    if request.method == 'GET':

        memory = new_memory()                # 새롭게 URL 접속 시, 대화 흐름 초기화    

        # 과거 모든 대화 주제 데이터 전송
        subjects = Subject.objects.all()
        subject_titles = [subject.title for subject in subjects]

        context = {
            'subjects' : subject_titles,
        }

        return JsonResponse(context)

    # Post 요청 -> Question에 해당하는 Answer 제공
    else:

        chatbot = applicant_chatbot(memory)  # 지원자를 위한 RAG Chatbot 생성 (지원자 Vector DB 검색)
        
        # 질의에 해당하는 Chatbot 답변
        question = request.POST.get('question')
        answer = chatbot(question)

        # 답변을 생성한 출처 데이터 확인하기
        print(answer['source_documents'])

        # Frontend로 전달할 데이터 (질의 / 응답)
        context = {
            'question' : question,
            'answer' : answer['answer']
        }

        return JsonResponse(context)




# 수강생들을 위한 챗봇
def student(request):

    global memory

    # GET 요청 -> 최초 URL 접속
    if request.method == 'GET':

        memory = new_memory()                # 새롭게 URL 접속 시, 대화 흐름 초기화    

        # 과거 모든 대화 주제 데이터 전송
        subjects = Subject.objects.all()
        subject_titles = [subject.title for subject in subjects]

        context = {
            'subjects' : subject_titles,
        }

        return JsonResponse(context)

    # Post 요청 -> Question에 해당하는 Answer 제공
    else:

        chatbot = student_chatbot(memory)  # 수강생들을 위한 RAG Chatbot 생성 (지원자 Vector DB 검색)
        
        # 질의에 해당하는 Chatbot 답변
        question = request.POST.get('question')
        answer = chatbot(question)

        # 답변을 생성한 출처 데이터 확인하기
        print(answer['source_documents'])

        # Frontend로 전달할 데이터 (질의 / 응답)
        context = {
            'question' : question,
            'answer' : answer['answer']
        }

        return JsonResponse(context)