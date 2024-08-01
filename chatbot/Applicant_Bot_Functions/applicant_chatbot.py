## 지원자들을 위한 Applicant Chatbot 파일
from langchain_openai import OpenAIEmbeddings              # Word Embedding
from langchain_chroma import Chroma                        # Vector DB : Chroma DB
from langchain.chat_models import ChatOpenAI               # LLM 모델 : GPT
from langchain.chains import ConversationalRetrievalChain  # 대화형 검색 Chain
from langchain.memory import ConversationBufferMemory      # Buffer Memory


# 대화 Buffer Memory 초기화
def new_memory():
    """
    대화 메모리 생성 -> 다른 주제의 대화를 시작할 때 메모리를 초기화
    """
    memory = ConversationBufferMemory(memory_key="chat_history", 
                                      input_key="question", 
                                      output_key="answer",
                                      return_messages=True)
    return memory


# 지원자를 위한 RAG Chatbot 생성 (Memory -> 대화 흐름)
def applicant_chatbot(memory):
    """
    RAG Chatbot 생성 (Memory -> 대화 흐름)
    """
    # Word Embedding -> Chroma DB (Vector DB) 구성
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    database = Chroma(persist_directory="./VectorDB/Applicant", embedding_function=embeddings)

    # GPT 3.5 LLM 모델
    llm = ChatOpenAI(model="gpt-3.5-turbo")

    # Cosin 유사도 기반 Vector DB 검색
    k = 3
    retriever = database.as_retriever(search_kwargs={"k": k})
    
    # ConversationalRetrievalQA 체인 생성
    chatbot = ConversationalRetrievalChain.from_llm(llm=llm, 
                                                    retriever=retriever, 
                                                    memory=memory,               # 대화 흐름 Buffer Memory
                                                    return_source_documents=True, 
                                                    output_key="answer")

    return chatbot