from konlpy.tag import Mecab, Komoran, Twitter, Okt

#text = "안녕하세요. 컴퓨터 전공 4학년 김태원입니다. 010-xxxx-xxxx -.-"
text = "카이 설치하느라 이틀 걸렸고 이건 고통이다."

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

# Twitter
print("===================Twitter===================")
okt = Okt()
o_nouns = okt.nouns(text)
print('명사 단위:',o_nouns)
o_pos = okt.pos(text)
print('품사 태깅:',o_pos)
o_morphs = okt.morphs(text, norm=True, stem=True)
print('형태소 단위:', o_morphs)