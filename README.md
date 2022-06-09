# IR_Project1
한글 정보 검색 엔진 만들기 프로젝트/Information Retreival engine creation project for korean

- 정보검색 수업 과제로 수행한 프로젝트입니다
- tf, idf, tf-idf를 적용하여 입력된 Query에 가장 일치하는 상위 5개의 문서 ID를 알려주는 프로그램입니다.
- 형태소 분석 라이브러리 : KoNLPy 0.6.0 - Mecab, Okt 사용
- 실행환경
    - OS : Window 11
    - Langauge : python 3.8.10
    - 실행 환경 : python 가상환경(venv)
- 자세한 내용은 아래 Notion 링크의 문서 또는 report 디렉토리를 참고해주세요.
- 실행 흐름(flow)
    - ![image](https://user-images.githubusercontent.com/33050476/172857653-97eaf341-02c8-4142-ac27-64103674ed84.png){: width="70%" height="70%"}


### 노션 링크
https://taewon98.notion.site/31dd3436a6e24a93994d58083daadb84

### 실행 방법(How to run)
- koNLPy 설치방법
    - [Installation — KoNLPy 0.6.0 documentation](https://konlpy.org/en/latest/install/)
        - 여기서 window 참고
    - 윈도우의 경우 Mecab 클래스 기본적으로는 지원 X
    - 다른 방법으로 Mecab 클래스 사용
        - [konlpy mecab 설치 window (velog.io)](https://velog.io/@jyong0719/konlpy-mecab-%EC%84%A4%EC%B9%98-window)
        - 경로 설정 주의하기(주황색 부분)
        
- Window PC에 KoNLPy 라이브러리가 설치 완료 되었다는 전제 하에,
    
    ```bash
    git clone https://github.com/Ktaewon/IR_Project1.git
    cd IR_Project1
    ```
- input 디렉토리 생성 및 corpus.txt 삽입
  
    ```bash
    mkdir input
    # input 디렉토리에 full_corpus.txt 넣어주세요
    ```
    - 형식
        ```
        <title>1. 이순신</title> 
        이순신은 조선 중기의 무신이었다. 본관은 덕수, 자는 여해, 시호는 충무였으며, 한성 출신이었다. 
        ...생략...
        <title>2. 세종</title>
        ...생략...```
- 실행
    
    ```bash
    source myvenv/Scripts/activate
    python src/main_mecab.py
    ```
     
