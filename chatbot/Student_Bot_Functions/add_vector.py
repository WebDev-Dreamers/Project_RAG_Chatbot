## 수강생들을 위한 지원자 FAQ 게시판 정보를 저장한 Chroma DB 구성 파일
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
import pandas as pd


def add_vectorDB():

    """
    CSV 파일에서 데이터를 읽어와 Chroma DB에 추가합니다.
    """

    # OpenAIEmbeddings 인스턴스 생성
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

    # Chroma 벡터 DB 인스턴스 생성
    database = Chroma(persist_directory="./VectorDB/Student", embedding_function=embeddings)
    
    # CSV 파일 불러오기
    csv_filename = 'Student_FAQ.csv'
    data = pd.read_csv(csv_filename, encoding='utf-8-sig')

    # CSV 데이터를 리스트로 변환
    text_list = data['content'].tolist()
    meta_list = [{'category': category} for category in data['category'].tolist()]
        
    # 모든 QA 리스트를 Document로 구성
    documents = [Document(metadata=meta_list[i], page_content=text_list[i]) for i in range(len(text_list))]

    # Document를 DB에 추가
    database.add_documents(documents)
    
    print('Vector DB에 새로운 Data가 추가되었습니다.')


# 자체 실행
if __name__ == "__main__":
    add_vectorDB()