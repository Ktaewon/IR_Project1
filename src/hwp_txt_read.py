import os
import olefile
import zlib
import struct
# from bs4 import BeautifulSoup
# import xml.etree.ElementTree as ET

def readHWP(filename:str):
    # os.getcwd() + '/input/full_corpus.hwp'
    f = olefile.OleFileIO(filename) #olefile로 .hwp 파일 열기
    
    # OLE 파일이 가진 stream 리스트
    dirs = f.listdir()

    # hwp 파일인지 확인
    if ["FileHeader"] not in dirs or ["\x05HwpSummaryInformation"] not in dirs:
        raise Exception("Not a HWP format.")
    
    # 문서 포맷 압축 여부 확인
    header_data = f.openstream("FileHeader").read()
    is_compressed = (header_data[36] & 1) == 1
    
    # Body Sections 불러오기
    nums = []
    for d in dirs:
        if d[0] == "BodyText":
            nums.append(int(d[1][len("Section"):]))
    sections = ["BodyText/Section" + str(x) for x in sorted(nums)]
    
    # 전체 text 추출
    text = ""
    for section in sections:
        encoded_bodytext = f.openstream(section)
        encoded_data = encoded_bodytext.read()
        if is_compressed: # 압축된 경우 해제
            unpacked_encoded_data = zlib.decompress(encoded_data, -15)
        else:
            unpacked_encoded_data = encoded_data
    
        # 각 Section 내 text 추출    
        section_text = ""
        i = 0
        size = len(unpacked_encoded_data)
        while i < size:
            header = struct.unpack_from("<I", unpacked_encoded_data, i)[0]
            rec_type = header & 0x3ff
            rec_len = (header >> 20) & 0xfff
            if rec_type in [67]:
                rec_data = unpacked_encoded_data[i+4:i+4+rec_len]
                section_text += rec_data.decode('utf-16')
                section_text += "\n"
            i += 4 + rec_len
        text += section_text
        text += "\n"
    
    f.close()
    # 디코딩된 text 반환
    return text


def readHWPandParseAsList(filename:str):
    corpus_list = [""]
    # os.getcwd() + '/input/full_corpus.hwp'
    lines = readHWP(filename).strip().split('\r\n')
    print(lines)
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
            tempbody += f'{line}\n'
    corpus_list.append(tempbody)
    
    return corpus_list

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
    corpus = readHWPandParseAsList(os.getcwd() + '/input/full_corpus.hwp')
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