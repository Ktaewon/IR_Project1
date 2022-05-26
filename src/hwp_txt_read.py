import os
import olefile
# from bs4 import BeautifulSoup
# import xml.etree.ElementTree as ET

def readHWPandParse(filename:str):
    # os.getcwd() + '/input/full_corpus.hwp'
    f = olefile.OleFileIO(filename) #olefile로 한글파일 열기
    encoded_text = f.openstream('PrvText').read() #PrvText 스트림 안의 내용 꺼내기 (유니코드 인코딩 되어 있음)
    # print(encoded_text)
    
    # for encoded_text in f.openstream('PrvText').readlines():
    #     print(encoded_text)
    #     print(encoded_text.decode('utf-16'))
    decoded_text = encoded_text.decode('UTF-16') #유니코드이므로 UTF-16으로 디코딩
    
    return decoded_text

def readTXTandParseAsDict(filename:str):
    corpus_dict = {}
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        count = 0
        tempbody = ""
        title_find = False
        for line in lines:
            if line.find("<title>") >= 0:
                if title_find == True:
                    corpus_dict[count] = tempbody
                    tempbody = ""
                else:
                    title_find = True
                count += 1
                line = line.replace("<title>", "")
                line = line.replace("</title>", "")
            if not line == "" and not line == "\n":
                tempbody += line
        corpus_dict[count] = tempbody
    #print(corpus_dict)
    return corpus_dict

def readTXTandParseAsList(filename:str):
    corpus_list = [""]
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        count = 0
        tempbody = ""
        title_find = False
        for line in lines:
            if line.find("<title>") >= 0:
                if title_find == True:
                    corpus_list.append(tempbody)
                    tempbody = ""
                else:
                    title_find = True
                line = line.replace("<title>", "")
                line = line.replace("</title>", "")
            if not line == "" and not line == "\n":
                tempbody += line
        corpus_list.append(tempbody)
    #print(corpus_dict)
    return corpus_list

def main():
    corpus = readTXTandParseAsList(os.getcwd() + '/input/full_corpus.txt')
    for i in range(len(corpus)):
        print("[{}] : {}".format(i, corpus[i]))
    
    # decoded_text = readHWPandParse(os.getcwd() + '/input/full_corpus.hwp')
    # print(decoded_text)


    # tree = ET.fromstring(decoded_text)

    # root = tree.getroot() # 해당 트리의 root를 반환
    # print(root.tag)
    # print(root.attrib) 

    # for child in root:
    #     print(child.tag, child.attrib)
    # bs = BeautifulSoup(decoded_text, 'html.parser')
    # print(bs)

    # 5번 글 /안붙어있었음
    # print(bs.find_all('title'))

if __name__ == '__main__':
    main()