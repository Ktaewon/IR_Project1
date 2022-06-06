import olefile
import os
import zlib
import struct

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
        
    return text

print(readHWP(os.getcwd() + '/input/full_corpus.hwp'))
