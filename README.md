# IR_Project1
한글 정보 검색 엔진 만들기 프로젝트/Information Retreival engine creation project for korean

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
        - "<title>1. 이순신</title> 이순신은 조선 중기의 무신이었다. 본관은 덕수, 자는 여해, 시호는 충무였으며, 한성 출신이었다. ...생략..."
- 실행
    
    ```bash
    source myvenv/Scripts/activate
    python src/main_mecab.py
    ```
     
