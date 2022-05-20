from konlpy.tag import Mecab

mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
morphs_list = mecab.morphs("안녕하세요, 헤이 테크 블로그의 자연어처리 관련 포스팅입니다. 1234-!5123 @!@!@@$")
print(morphs_list)