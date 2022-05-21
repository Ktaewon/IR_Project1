from konlpy.tag import Mecab
from math import log10

mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")

# DF (Document Frequency): 특정 단어가 등장한 문서의 수
def df(t, d):
    pass

# t is token
# d is document == tokens
def f(t, d):
    return d.count(t)

def tf(t, d):
    return 0.5 + 0.5*f(t,d)/max([f(w,d) for w in d])

def idf(t, D):
    # D is documents == document list
    numerator = len(D)
    denominator = 1 + len([ True for d in D if t in d])
    return log10(numerator/denominator)

def tfidf(t, d, D):
    return tf(t,d)*idf(t, D)

def tfidfScorer(D):
    morphs_D = [mecab.morphs(d) for d in D]
    result = []
    for d in morphs_D:
        result.append([(t, tfidf(t, d, morphs_D)) for t in d])
    return result

# 문서 입력
D = ["""<title>1. 지미 카터</title>
제임스 얼 지미 카터 주니어는 민주당 출신 미국 39번째 대통령이다. 지미 카터는 조지아 주 한 마을에서 태어났다. 조지아 공과대학교를 졸업하였다. 그 후 해군에 들어가 전함·원자력·잠수함의 승무원으로 일하였다.""",
"""<title>2. 체첸 공화국</title> 
체첸 공화국 또는 줄여서 체첸은 러시아의 공화국이다. 체첸에서 사용되는 언어는 체첸어와 러시아어이다. 체첸어는 캅카스제어 중, 북동 캅카스제어로 불리는 그룹에 속하는데 인구시어와 매우 밀접한 관계에 있다.
""",
"""<title>3. 백남준</title> 
백남준은 한국 태생의 미국 미술작가, 작곡가, 전위 예술가이다. 여러 가지 매체로 예술 활동을 하였고 특히 비디오 아트라는 새로운 예술을 창안하여 발전시켰다는 평가를 받는 예술가로서 '비디오 아트의 창시자'로 알려져 있다. 
"""
]

# 토큰나이징
for i, doc in enumerate(tfidfScorer(D)):
    print('====== document[%d] ======' % i)
    print(doc)

# 역인덱싱

# 쿼리 들어옴
q = "체첸 공화국"

# 쿼리 토크나이징

# 점수 계산
scores = []