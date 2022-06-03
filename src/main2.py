from konlpy.tag import Mecab
from math import log10
import os
from hwp_txt_read import readTXTandParseAsList

mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
STOPWORDS = ['고','으면','을','의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다','에서', '다', ',', '.', '·']

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

# idf (): 
def idf(t, D):
    N = len(D)
    #return log10(1 + N/(df(t, D)))
    return log10(N/(df(t, D)))

# tf-idf weight
def w_tfidf(t, d, D):
    return w_tf(t, d) * idf(t, D)

# tf-idf: 
def tfidf(t, d, D):
    return tf(t, d) * idf(t, D)

# dictionary에 들어갈 Term
class Term:
    def __init__(self, term):
        self.term = term
        self.posting_list = None
        self.tail = None

# Term에 대한 Posting Linked list를 위한 Posting
class Posting: 
    def __init__(self, docID, tf_idf, next=None): #data 만 입력시 next 초기값은 None이다. 
        self.docID = docID #다음 데이터 주소 초기값 = None
        self.tf_idf = tf_idf
        self.w_td = tf_idf
        self.next = next
        
# inverted index 출력 & 파일 저장
def printPostingList(term_dictionary):
    f = open(os.getcwd() + "/output/posting_lists.txt", "w", encoding="utf-8-sig")
    for term in term_dictionary:
        node = term_dictionary[term].next
        #print("[{}] -> ".format(term), end = '')
        f.write("[{}] -> ".format(term))
        while node.next: #node.next =None이 아닐 경우. 즉, node의 next가 있는 경우 실행 
            #print("({0}, {1}) -> ".format(node.docID, node.tf_idf), end = '') 
            f.write("({0}, {1}) -> ".format(node.docID, node.tf_idf))
            node=node.next
        #print("({0}, {1});".format(node.docID, node.tf_idf))
        f.write("({0}, {1});\n".format(node.docID, node.tf_idf))
    f.close()

def delete_stopwords(morphs, stopwords):
    after = [t for t in morphs if t not in stopwords]
    return after

# Inverted Index 생성 함수 & tf-idf weight 계산
def makePostingList(D): # D : CORPUS
    term_dictionary = {}
    # TO-DO : (1) 형태소 분석 전 데이터 정제 필요
    # TO-DO : (2) 형태소 분석 후 데이터 정제 필요
    #             1) Lemmatization 2) Stemming 필요?
    # TO-DO : (3) tf-idf 머가 맞는지 잘 모르겠음 -> 강의 듣고 다시 해야 할 듯...
    
    morphs_D = [delete_stopwords(mecab.morphs(d), STOPWORDS) for d in D]
    length = [len(d) for d in morphs_D]
    print(morphs_D)
    # term 마다 (doc번호, tf-idf값)
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
    return term_dictionary, length

# term-at-a-time 방식의 cosine 점수 계산 함수
def consineScore(q, D, term_dict, length):
    N = len(D)
    scores = {i: 0 for i in range(N)}
    query_terms =  delete_stopwords(mecab.morphs(q), STOPWORDS)
    print(query_terms)
    for t in set(query_terms):
        #w_tq = w_tfidf(t, q, [q]) #w_tf(t, q)
        #w_tq = w_tf(t, q)
        w_tq = 1
        print(t, w_tq)
        if t in term_dict:
            node = term_dict[t].next
            while node.next:
                scores[node.docID] += node.w_td * w_tq
                node = node.next
            scores[node.docID] += node.w_td * w_tq
    
    # TO-DO : (3) arr length 만큼 나누는 코드 필요
    #             근데 이게 무슨 소린지 이해 X
    #             강의 다시 보고 이어서 진행 하기
    # -> 일단 아래 처럼 하긴 함
    # -> 길이가 긴 doc이랑 길이가 짧은 doc이랑 차별두면 안되니까
    # -> 해당 doc의 전체 길이로 나눠주는 느낌?
    for i in range(1, len(CORPUS)):
        scores[i] /= length[i]
    print(scores)
    return scores
    
        

# 문서 입력
CORPUS = readTXTandParseAsList(os.getcwd() + '/input/full_corpus.txt')
# CORPUS = ["""<title>1. 지미 카터</title>
# 제임스 얼 지미 카터 주니어는 민주당 출신 미국 39번째 대통령이다. 지미 카터는 조지아 주 한 마을에서 태어났다. 조지아 공과대학교를 졸업하였다. 그 후 해군에 들어가 전함·원자력·잠수함의 승무원으로 일하였다.""",
# """<title>2. 체첸 공화국</title> 
# 체첸 공화국 또는 줄여서 체첸은 러시아의 공화국이다. 체첸에서 사용되는 언어는 체첸어와 러시아어이다. 체첸어는 캅카스제어 중, 북동 캅카스제어로 불리는 그룹에 속하는데 인구시어와 매우 밀접한 관계에 있다.
# """,
# """<title>3. 백남준</title> 
# 백남준은 한국 태생의 미국 미술작가, 작곡가, 전위 예술가이다. 여러 가지 매체로 예술 활동을 하였고 특히 비디오 아트라는 새로운 예술을 창안하여 발전시켰다는 평가를 받는 예술가로서 '비디오 아트의 창시자'로 알려져 있다. 
# """
# ]

# 토큰나이징 & 역인덱싱 & tf-idf weight 계산
term_dict, length = makePostingList(CORPUS)
printPostingList(term_dict)


while True:
    # 쿼리 들어옴
    query = [input("검색어를 입력해주세요(종료하려면 q나 Q를 입력해주세요): ")]
    #query = ["체첸 공화국 만세 체첸 러시아 민주당에서 예술가, 아티스트, 작곡가"]
    
    if query[0] == "q" or query[0] == "Q":
        break

    # 쿼리 토크나이징 & 점수 계산
    scores =consineScore(query[0], CORPUS, term_dict, length)


    print(sorted(scores.items(), key = lambda item: item[1], reverse = True)[:5])

