from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import os
from hwp_txt_read import readTXTandParseAsList

documents = readTXTandParseAsList(os.getcwd() + '/input/full_corpus.txt')

# TF-IDF 점수 변환 모델 준비
tf_idf_model = TfidfVectorizer().fit(documents)

# 단어 이름 리스트 순서대로 반환(0번으로 지정된 토큰부터)
word_id_list = sorted(tf_idf_model.vocabulary_.items(), key=lambda x: x[1], reverse=False)
word_list = [x[0] for x in word_id_list]

# 용이한 시각화를 위하여 데이터프레임 변환
tf_idf_df = pd.DataFrame(tf_idf_model.transform(documents).toarray(), columns = word_list, index = [ f'd{x}' for x in range(0, len(documents))])

print(tf_idf_df)
