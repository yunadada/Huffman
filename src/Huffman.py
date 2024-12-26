import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import heapq
import time
import os
import zlib

#전역 변수 초기화
file_Name = None
output_Path = None

class Node:
    def __init__(self, frequency=None, text=None, left=None, right=None):
        self.frequency = frequency  # 해당 노드의 빈도수
        self.text = text            # 해당 노드의 문자
        self.left = left            # 왼쪽 자식 노드
        self.right = right          # 오른쪽 자식 노드

    # 빈도수를 비교할 수 있도록 __lt__ 메서드 정의
    def __lt__(self, other):
        return self.frequency < other.frequency

    # 노드의 정보를 문자열로 반환하는 __str__ 메서드 정의
    def __str__(self):
        return f"Node(text: '{self.text}', frequency: {self.frequency}, left: {self.left}, right: {self.right})"

#버튼 클릭시 호출될 함수
def OpenFile(label_FilePath):
    fileName= filedialog.askopenfilename(
        initialdir = "C:/Users/yuna/Desktop/컴퓨터공학/2학년 2학기/어드벤처디자인/최종레벨_허프만",
        title = "파일 선택", 
        filetypes=[('모든 파일', "*.*"), ('텍스트 파일', '*.txt'), ('이진 파일', "*.bin")] 
    )
    if fileName: #사용자가 파일을 선택한 경우
        label_FilePath.config(text=f"{fileName}")
        global file_Name #압축할 파일의 경로가 담긴 전역 변수
        file_Name = fileName

#출력 경로 설정 함수
def SelectOutputPath(label_outputPath):
    outputPath = filedialog.askdirectory(
        initialdir="/",
        title='출력 경로 선택'
    )
    if outputPath:
        label_outputPath.config(text=f"{outputPath}")
        global output_Path #출력 경로가 담긴 전역 변수
        output_Path = outputPath

#텍스트 파일에서 각 문자의 빈도수를 계산
def Caculate_Frequency(file_Name):
    global textFile_content
    content = []

    frequency = {}
    totalCount = 0
    try:
        with open(file_Name, 'r') as file: #읽기 모드로 파일 열기
            while(1):
                ch = file.read(1)
                if not ch:
                    break

                totalCount += 1
                content.append(ch)

                if (ch in frequency): #이미 있는 문자는 빈도수 증가
                    frequency[ch] += 1
                else:  #처음 등장하는 문자는 빈도수를 1로 초기화
                    frequency[ch] = 1
        textFile_content = ''.join(content)
        return(frequency, totalCount)

    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror('에러', '파일을 찾을 수 없습니다.')
        root.quit()
    
#허프만 트리 생성
def Make_HuffmanTree(frequency):
    PQ = []
    
    #딕셔너리를 우선순위 큐로 변환
    for char, frequ in frequency.items():
        node = Node(frequ, char)
        heapq.heappush(PQ, node)

    while len(PQ) > 1:
        p = heapq.heappop(PQ)
        q = heapq.heappop(PQ)
        root = Node()
        root.left = p
        root.right = q
        root.frequency = p.frequency + q.frequency
        heapq.heappush(PQ, root)
    
    return heapq.heappop(PQ)

#접두코드 해시테이블 생성
def Generate_PrefixCode(root, prefix, prefix_code):
    cur = Node()
    cur = root
    
    if cur.left == None and cur.right == None:
        prefix_code[cur.text] = prefix
        return
    if cur.left != None:
        Generate_PrefixCode(cur.left, prefix + '0', prefix_code)
    if cur.right != None:
        Generate_PrefixCode(cur.right, prefix + '1', prefix_code)

#압축률 계산 함수
def EncodeRate(label_Encode_Rate_Value):
    total_bitCost = 0
    for char in frequency:
        if char in prefix_code:
            charFrequency = frequency[char]
            prefixLength = len(prefix_code[char])
            total_bitCost += charFrequency * prefixLength
    result = round((1 - (total_bitCost / (totalCount * 8))) * 100, 3)
    label_Encode_Rate_Value.config(text=f"{result} %")

#압축 수행 함수
def Encode(label_Encode_Rate_Value, label_Encode_Speed_Value, label_B_fileSize, label_A_fileSize, label_textFile, label_encodeFile):
    start_Time = time.time() #시작 시간 기록

    global file_Name, output_Path, textFile_content

    if not file_Name:
        messagebox.showwarning("경고", "압축할 파일을 먼저 선택해주세요.")
        return
    if not output_Path:
        messagebox.showwarning("경고", "출력 경로를 먼저 설정해주세요.")
        return

    #텍스트 파일에서 각 문자의 빈도수 계산
    global frequency, totalCount
    frequency, totalCount = Caculate_Frequency(file_Name)

    #허프만 트리 생성
    root = Node()
    root = Make_HuffmanTree(frequency)

    #접두코드 해시테이블 생성
    global prefix_code
    prefix_code = {} #접두코드를 저장할 빈 딕셔너리(=해시테이블) 생성
    prefix = "" #접두코드를 저장할 빈 문자열
    Generate_PrefixCode(root, prefix, prefix_code)

    #파일 읽기
    buf = []
    try:
        with open(file_Name, 'r') as file: #읽기 모드로 파일 열기
            content = file.read()
            for ch in content:
                if ch in prefix_code:
                    buf.append(prefix_code[ch]) #접두 코드 가져오기
            buf = ''.join(buf)
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror('에러', '파일 읽기 실패')
        root.quit()

    #압축 파일명 지정
    Encode_FileName = os.path.splitext(file_Name)[0] + "_Encode.bin"

    #지정된 경로에 저장
    output_FilePath = os.path.join(output_Path, Encode_FileName)

    # 허프만 코드표를 이진 데이터로 변환하여 파일에 저장(헤더 부분)
    # 1. 허프만 코드표를 이진 코드로 변환
    bin_prefix = ""
    for text, prefix in prefix_code.items():
        text_binary = format(ord(text), '08b') #문자를 8bit 이진 문자열로 변환
        prefix_length = format(len(prefix), '08b') #접두 코드 길이를 8bit 이진 문자열로 변환
        padded_prefix = prefix.ljust(8, '0')  # 접두 코드를 앞에 0을 채워 8비트로 맞춤
        bin_prefix += text_binary + prefix_length + padded_prefix #문자, 접두부 코드 길이, 접두부 코드 자체를 연결
    
    #허프만 코드표 길이를 4바이트로 저장
    code_table_length = len(bin_prefix) // 8

    # 2.이진 코드를 바이트로 변환
    try:
        with open(output_FilePath, 'wb') as f:
            #허프만 코드표 길이 저장(4바이트)
            f.write(code_table_length.to_bytes(4, 'big'))
            
            #헤더 작성
            for i in range(0, len(bin_prefix), 8):
                byte_chunck = bin_prefix[i:i+8]
                byte = int(byte_chunck, 2)
                f.write(byte.to_bytes(1, 'big'))
        
            #실제 압축된 데이터를 파일에 저장(본문 부분)
            for i in range(0, len(buf), 8):
                byte_chunck = buf[i:i+8]
                if len(byte_chunck) < 8:
                    byte_chunck = byte_chunck.ljust(8, '0')
                byte = int(byte_chunck, 2)
                f.write(byte.to_bytes(1, 'big'))

            
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror('에러', f'파일 압축 중 오류가 발생했습니다.\n{str(e)}')
        root.quit()

    end_Time = time.time() #끝 시간 기록
    total_Time = (end_Time - start_Time) * 1000

    #압축 전 파일 크기 출력
    label_B_fileSize.config(text=f"{os.path.getsize(file_Name)} byte")

    #압축 후 파일 크기 출력
    label_A_fileSize.config(text=f"{os.path.getsize(output_FilePath)} byte")

    #압축률 출력
    EncodeRate(label_Encode_Rate_Value)
    
    #압축 속도 출력
    label_Encode_Speed_Value.config(text=f"{total_Time:.2f} ms")

    # 압축전 파일 내용을 출력
    MAX = 5000
    label_textFile.delete('1.0', 'end')  # 기존 텍스트 삭제
    label_textFile.insert('1.0', textFile_content[:MAX])  # 새 텍스트 삽입

    # 압축된 데이터 내용을 출력
    compressed_preview = f"<Header>\n{bin_prefix[:4096]}\n\n<Data>\n{buf[:4096]}"  # 4096비트만 미리보기로 출력
    label_encodeFile.delete('1.0', 'end')  # 기존 텍스트 삭제
    label_encodeFile.insert('1.0', compressed_preview)  # 새 텍스트 삽입

#압축 해제 수행 함수
def Decode(label_Decode_Speed_Value, label_decodeFile):
    global file_Name, output_Path

    if not file_Name:
        messagebox.showwarning("경고", "압축할 파일을 먼저 선택해주세요.")
        return
    if not output_Path:
        messagebox.showwarning("경고", "출력 경로를 먼저 설정해주세요.")
        return
        
    # 파일 확장자 확인
    if not file_Name.endswith('.bin'):
        messagebox.showerror("오류", "선택한 파일의 확장자가 .bin이 아닙니다.")
        return

    try:
        with open(file_Name, 'rb') as file: #읽기 모드로 파일 열기
            start_Time = time.time()
            
            # 허프만 코드표를 참조하여 허프만 트리 구성 (헤더)
            code_table_length = int.from_bytes(file.read(4), 'big') #허프만 코드표의 길이 정보를 가져옴

            #허프만 코드표 읽기
            bin_prefix = file.read(code_table_length)
            bin_prefix = ''.join(format(byte, '08b') for byte in bin_prefix)
            
            root = Node()
            i = 0

            while i < len(bin_prefix):
                # 문자 읽기 (8비트)
                text_binary = bin_prefix[i:i+8]
                char = chr(int(text_binary, 2))
                i += 8

                # 접두 코드 길이 읽기 (8비트)
                prefix_length_binary = bin_prefix[i:i+8]
                prefix_length = int(prefix_length_binary, 2)
                i += 8

                # 접두 코드 읽기 (prefix_length 비트)
                prefix = bin_prefix[i:i+prefix_length]
                i += 8
                
                # 허프만 트리에 삽입
                current = root
                for bit in prefix:
                    if bit == '0':
                        if current.left == None:
                            current.left = Node()
                        current = current.left
                    elif bit == '1':
                        if current.right == None:
                            current.right = Node()
                        current = current.right

                # 노드에 문자 저장
                current.text = char

            #본문 데이터 읽기
            buf = file.read()
            buf = ''.join(format(byte, '08b') for byte in buf)

            #본문 데이터 복원
            decoded_text = []
            cur = root  # 허프만 트리의 루트 노드부터 시작

            # 이진 문자열의 각 비트를 순회하여 복원
            for bit in buf:
                if bit == '0':
                    cur = cur.left  # '0'이면 왼쪽 자식으로 이동
                else:
                    cur = cur.right  # '1'이면 오른쪽 자식으로 이동

                if cur.left == None and cur.right == None:  # 단말 노드인 경우
                    decoded_text.append(cur.text)  # 복원된 문자를 추가
                    cur = root  # 루트 노드로 돌아가 다음 문자 해제
            decoded_text = ''.join(decoded_text)
            
            #압축 해제된 내용을 텍스트 파일로 저장
            Decode_FileName = os.path.splitext(file_Name)[0] + "_Decode.txt" #압축 해제 파일명 지정
            output_FilePath = os.path.join(output_Path, Decode_FileName) #지정된 경로에 저장
            with open(output_FilePath, 'w') as f:
                f.write(decoded_text)
            
            # 압축 해제 속도 출력 (시간 측정)
            end_Time = time.time()
            total_Time = (end_Time - start_Time) * 1000  # 밀리초 단위
            label_Decode_Speed_Value.config(text=f"{total_Time:.2f} ms")

            # 압축 해제된 데이터 내용을 출력
            MAX = 5000
            label_decodeFile.delete('1.0', 'end')  # 기존 텍스트 삭제
            label_decodeFile.insert('1.0', decoded_text[:MAX])  # 새 텍스트 삽입

    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror('에러', f'파일 압축 해제 중 오류가 발생했습니다.\n{str(e)}')
        root.quit()


#LZ77 압축 수행
def LZ77(label_LZ77_Value):
    global file_Name, output_Path

    if not file_Name:
            messagebox.showwarning("경고", "압축할 파일을 먼저 선택해주세요.")
            return
    if not output_Path:
        messagebox.showwarning("경고", "출력 경로를 먼저 설정해주세요.")
        return

    #압축 파일명 지정
    Encode_FileName = os.path.splitext(file_Name)[0] + "_LZ77_Encode.bin"

    #지정된 경로에 저장
    output_FilePath = os.path.join(output_Path, Encode_FileName)

    try:
        with open(file_Name, "r", encoding="utf-8") as file:
            data = file.read()

        compressed_data = zlib.compress(data.encode("utf-8"))

        with open(Encode_FileName, "wb") as file:
            file.write(compressed_data)
        
        label_LZ77_Value.config(text=f"{os.path.getsize(output_FilePath)} byte")

    except Exception as e:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror('에러', f'파일 압축 중 오류가 발생했습니다.\n{str(e)}')
            root.quit()