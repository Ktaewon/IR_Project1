from konlpy.tag import Mecab
from math import log10, sqrt
import os
from hwp_txt_read import readTXTandParseAsList
import heapq

mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
# STOPWORDS = []
# 불용어 제거를 위한 리스트
STOPWORDS = [ 
                '로', '고', '으면', '을', '의', 
                '가', '이', '은', '들', '는',
                '좀', '잘', '걍', '과', '도', 
                '를', '으로', '자', '에', '와',
                '며', '하다', '에서', '다', '하',
                '있', '였', '었', '여', '이다',
                "했", '였으며', 
                ',', '.', '·', '’', '‘',
                ';', '"', '(', ')', '[', ']',
                '》', '《']

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

# idf (inverse document frequency): 특정 단어가 등장한 문서의 수를 뒤집은 값 + log취함
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

# 불용어 제거 함수
def delete_stopwords(morphs, stopwords):
    after = [t for t in morphs if t not in stopwords]
    return after

# Inverted Index 생성 함수 & tf-idf weight 계산
def makePostingList(D): # D : CORPUS
    term_dictionary = {}
    # TO-DO : (1) 형태소 분석 전 데이터 정제 필요
    # TO-DO : (2) 형태소 분석 후 데이터 정제 필요
    #             1) Lemmatization 2) Stemming 필요?
    morphs_D = [delete_stopwords(mecab.morphs(d), STOPWORDS) for d in D]
    
    # for l2 normalization
    length = [0 for i in range(len(D))]
    
    # for i in range(len(morphs_D)):
    #     print(f'{i} : \n{morphs_D[i]}')

    # term 마다 (doc번호, tf-idf값)
    for docId, doc in enumerate(morphs_D):
        for term in set(doc):
            w_td = w_tfidf(term, doc, morphs_D)
            length[docId] += w_td * w_td
            if term not in term_dictionary:
                term_dictionary[term] = Term(term)
                term_dictionary[term].next = Posting(docId, w_td)
                term_dictionary[term].tail = term_dictionary[term].next
            else:
                term_dictionary[term].tail.next = Posting(docId, w_td)
                term_dictionary[term].tail = term_dictionary[term].tail.next
    length = [sqrt(l) for l in length]
    return term_dictionary, length

# term-at-a-time 방식의 cosine 점수 계산 함수
def consineScore(q, D, term_dict, length):
    N = len(D)
    scores = {i: 0 for i in range(N)}
    query_terms =  delete_stopwords(mecab.morphs(q), STOPWORDS)
    print(query_terms)
    for t in set(query_terms):
        #w_tq = w_tfidf(t, q, [q])  -> 0이 되므로 사용X
        #w_tq = w_tf(t, q)  -> 대부분의 쿼리에서 같은 단어가 반복되는 일 없으므로 1로 설정
        w_tq = 1
        print(t, w_tq)
        if t in term_dict:
            node = term_dict[t].next
            while node.next:
                scores[node.docID] += node.w_td * w_tq
                node = node.next
            scores[node.docID] += node.w_td * w_tq

    # top k개 selction을 위한 Max Heap
    # python의 heapq(MIN HEAP) 응용
    max_heap = []
    # 정규화 작업 - L2 norm
    for i in range(1, len(CORPUS)):
        scores[i] /= length[i]
        heapq.heappush(max_heap, (-scores[i], scores[i], i))  # (우선 순위, 값, docID)
        
    # 완성된 Max Heap 반환
    return max_heap    

# 문서 입력
CORPUS = readTXTandParseAsList(os.getcwd() + '/input/full_corpus.txt')

# 토큰나이징 & 역인덱싱 & tf-idf weight 계산
term_dict, length = makePostingList(CORPUS)
printPostingList(term_dict)


while True:
    # 쿼리 들어옴
    query = [input("검색어를 입력해주세요(종료하려면 q나 Q를 입력해주세요): ")]
    #query = ["체첸 공화국 만세 체첸 러시아 민주당에서 예술가, 아티스트, 작곡가"]
    
    if query[0] == "q" or query[0] == "Q":
        print("프로그램을 종료합니다.")
        break

    # 쿼리 토크나이징 & 점수 계산
    scores_max_heap =consineScore(query[0], CORPUS, term_dict, length)

    # Top K개 뽑기
    #   - Sorting Version
    #   print(sorted(scores.items(), key = lambda item: item[1], reverse = True)[:5])
    
    #   - Max Heap Version : TOP K개 Selection - Max Heap pop이용
    k = 5 # 이번 프로그램에서는 top 5개 뽑음
    result = []
    for _ in range(k):
        result.append(heapq.heappop(scores_max_heap)[2])
    print(result)

