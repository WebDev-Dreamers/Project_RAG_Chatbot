## 지원자를 위한 Applicant-Chatbot DB 도메인 정보를 추가하기 위해, 데이터 크롤링 및 정제 파일
import re
import requests
import pandas as pd


# 텍스트 정규화
def clean_text(text):
    """
    한글, 영어, 숫자, 공백만 남기고 특수문자를 제거
    """
    text = re.sub(r'[^\?가-힣A-Z0-9\s]', '', text)  # 한글, 영어, 숫자, 공백만 남기기
    text = re.sub(r'\s+', ' ', text)              # 여러 공백을 하나로
    return text


# 홈페이지 FAQ 게시판 크롤링
def crawling():

    """
    홈페이지 FAQ 데이터를 크롤링하여 AIVLE 지원자 QA CSV 파일로 저장
    """
    
    # 세션 객체 생성
    session = requests.Session()

    # 세션 내에서 첫 번째 요청 보내기
    session_url = 'https://aivle.kt.co.kr/home/brd/faq/main?mcd=MC00000056'
    response = session.get(session_url)

    data_list = []

    # 세션을 통해 다른 요청 보내기
    for i in range(8):
        data_url = f'https://aivle.kt.co.kr/home/brd/faq/listJson?ctgrCd=&pageIndex={i}'
        response = session.get(data_url)

        data = response.json()
        
        for ele in data['returnList']:
            category = clean_text(ele['ctgrNm'])                      # QA 카테고리
            content = clean_text(ele['atclTitle'] + ele['atclCts'])   # QA 정보
            
            item = {
                'category': category,
                'content': content
            }
            
            data_list.append(item)

    # 데이터프레임 생성
    data = pd.DataFrame(data_list)

    # 세션 종료
    session.close()

    # 데이터프레임을 CSV 파일로 저장
    csv_filename = 'Applicant_FAQ.csv'
    data.to_csv(csv_filename, index=False, encoding='utf-8-sig')



# 자체 실행
if __name__ == "__main__":
    crawling()