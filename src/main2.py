from konlpy.tag import Mecab
from math import log10
import os

mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")

# tf (Term Frequency): 해당 문서에서 특정 단어의 빈도 수
def tf(t, d):
    return d.count(t)

# w (weight of term): log frequency weighting
def w_tf(t, d):
    tf_tmp = tf(t,d)
    if tf_tmp > 0:
        return 1 + log10(tf_tmp)
    else:
        return 0

# df (Document Frequency): 특정 단어가 등장한 문서의 수
def df(t, D):
    count = 0
    for d in D:
        if t in d:
            count += 1
    return count

def idf(t, D):
    N = len(D)
    return log10(1 + N/(df(t, D)))

def w_tfidf(t, d, D):
    return w_tf(t, d) * idf(t, D)

def tfidf(t, d, D):
    return tf(t, d) * idf(t, D)

class Term:
    def __init__(self, term):
        self.term = term
        self.posting_list = None
        self.tail = None

class Posting: 
    def __init__(self, docID, tf_idf, next=None): #data 만 입력시 next 초기값은 None이다. 
        self.docID = docID #다음 데이터 주소 초기값 = None
        self.tf_idf = tf_idf
        self.w_td = tf_idf
        self.next = next
        
# inverted index 출력
def printPostingList(term_dictionary):
    f = open(os.getcwd() + "/output/posting_lists.txt", "w", encoding="utf-8-sig")
    for term in term_dictionary:
        node = term_dictionary[term].next
        print("[{}] -> ".format(term), end = '')
        f.write("[{}] -> ".format(term))
        while node.next: #node.next =None이 아닐 경우. 즉, node의 next가 있는 경우 실행 
            print("({0}, {1}) -> ".format(node.docID, node.tf_idf), end = '') 
            f.write("({0}, {1}) -> ".format(node.docID, node.tf_idf))
            node=node.next
        print("({0}, {1});".format(node.docID, node.tf_idf))
        f.write("({0}, {1});\n".format(node.docID, node.tf_idf))
    f.close()


def makePostingList(D): # D : CORPUS
    term_dictionary = {}
    # term 마다 (doc번호, tf-idf값)
    morphs_D = [mecab.morphs(d) for d in D]
    for docId, doc in enumerate(morphs_D):
        for term in set(doc):
            w_td = w_tfidf(term, doc, morphs_D)
            if term not in term_dictionary:
                term_dictionary[term] = Term(term)
                term_dictionary[term].next = Posting(docId, w_td)
                term_dictionary[term].tail = term_dictionary[term].next
            else:
                term_dictionary[term].tail.next = Posting(docId, w_td)
                term_dictionary[term].tail = term_dictionary[term].tail.next
    # TO-DO : 출력하는 함수 짜기
    
    #pprint.pprint(term_dictionary)
    return term_dictionary

def consineScore(q, D, term_dict):
    N = len(D)
    scores = [0 for i in range(N)]
    length = [0 for i in range(N)]
    query_terms = mecab.morphs(q)
    for t in set(query_terms):
        w_tq = w_tfidf(t, q, [q]) #w_tf(t, q)
        print(t, w_tq)
        if t in term_dict:
            node = term_dict[t].next
            while node.next:
                scores[node.docID] += node.w_td * w_tq
                node = node.next
            scores[node.docID] += node.w_td * w_tq
    print(scores)
    return scores
    #for each d 
        

# 문서 입력
CORPUS = ["""<title>1. 지미 카터</title>
제임스 얼 지미 카터 주니어는 민주당 출신 미국 39번째 대통령이다. 지미 카터는 조지아 주 한 마을에서 태어났다. 조지아 공과대학교를 졸업하였다. 그 후 해군에 들어가 전함·원자력·잠수함의 승무원으로 일하였다.""",
"""<title>2. 체첸 공화국</title> 
체첸 공화국 또는 줄여서 체첸은 러시아의 공화국이다. 체첸에서 사용되는 언어는 체첸어와 러시아어이다. 체첸어는 캅카스제어 중, 북동 캅카스제어로 불리는 그룹에 속하는데 인구시어와 매우 밀접한 관계에 있다.
""",
"""<title>3. 백남준</title> 
192.168.10.1 https://naver.com
백남준은 한국 태생의 미국 미술작가, 작곡가, 전위 예술가이다. 여러 가지 매체로 예술 활동을 하였고 특히 비디오 아트라는 새로운 예술을 창안하여 발전시켰다는 평가를 받는 예술가로서 '비디오 아트의 창시자'로 알려져 있다. 
"""
]

# 토큰나이징 & 역인덱싱 & tf-idf weight 계산
term_dict = makePostingList(CORPUS)
printPostingList(term_dict)

# 쿼리 들어옴
query = ["체첸 공화국 만세 체첸 러시아 민주당에서 예술활동, 아티스트"]

# 쿼리 토크나이징 & 점수 계산
scores =consineScore(query[0], CORPUS, term_dict)

