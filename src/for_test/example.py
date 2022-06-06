from konlpy.tag import Mecab, Komoran, Twitter, Okt

text = "안녕하세요. 컴퓨터 전공 4학년 김태원입니다. 010-xxxx-xxxx -.-"
# text = "지미 카터는 민주당 출신 미국 39번째 대통령이다. 지미 카터는 조지아 주  한 마을에서 태어났다. 조지아 공과대학교를 졸업하였다. 그 후 해군에 들어가 전함·원자력·잠수함의 승무원으로 일하였다. "
# text = "조지아 주 한"

# Mecab
print("===================Mecab===================")
mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
m_nouns = mecab.nouns(text)
print('명사 단위:',m_nouns)
m_pos = mecab.pos(text)
print('품사 태깅:',m_pos)
m_morphs = mecab.morphs(text)
print('형태소 단위:',m_morphs)

# Komoran
print("===================Komoran===================")
komoran = Komoran()
k_nouns = komoran.nouns(text)
print('명사 단위:',k_nouns)
k_pos = komoran.pos(text)
print('품사 태깅:',k_pos)
k_morphs = komoran.morphs(text)
print('형태소 단위:', k_morphs)

# Twitter
print("===================Twitter===================")
twitter = Twitter()
t_nouns = twitter.nouns(text)
print('명사 단위:',t_nouns)
t_pos = twitter.pos(text)
print('품사 태깅:',t_pos)
t_morphs = twitter.morphs(text)
print('형태소 단위:', t_morphs)

# Okt
print("===================Okt===================")
okt = Okt()
o_nouns = okt.nouns(text)
print('명사 단위:',o_nouns)
o_pos = okt.pos(text)
print('품사 태깅:',o_pos)
o_morphs = okt.morphs(text, norm=True, stem=True)
print('형태소 단위:', o_morphs)