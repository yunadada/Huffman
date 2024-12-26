import tkinter as tk
from tkinter import filedialog
import os
import Huffman

root = tk.Tk()
root.title('허프만 압축 프로그램')

# 제목 레이블
title = tk.Label(root, text="허프만 압축 프로그램", font=('Helvetica', 18, 'bold'))
title.pack()

frame = tk.Frame(root, bg='#d3d3d3', padx=20, pady=20)
frame.pack(padx=20, pady=20)

#파일 선택 프레임
frame1 = tk.Frame(frame, bg='#d3d3d3')
frame1.pack(padx=20, pady=10)

btn_Openfile = tk.Button(frame1, text='파일 선택', command=lambda: Huffman.OpenFile(label_FilePath), bg='black', fg='white', width=13, pady=6)
btn_Openfile.pack(side='left', padx=5)

label_FilePath = tk.Label(frame1, text='선택된 파일 : 없음', bg='white', bd=0.5, relief='solid', padx=10, pady=10, width=90)
label_FilePath.pack(side='right', padx=5)

#출력 경로 설정 프레임
frame2 = tk.Frame(frame, bg='#d3d3d3')
frame2.pack(padx=20, pady=10)

btn_outputPath = tk.Button(frame2, text='출력 경로 설정', command=lambda: Huffman.SelectOutputPath(label_outputPath), bg='black', fg='white', width=13, pady=6)
btn_outputPath.pack(side='left', padx=5)

label_outputPath = tk.Label(frame2, text='지정된 경로 : 없음', bg='white', bd=0.5, relief='solid', padx=10, pady=10, width=90)
label_outputPath.pack(side='left', padx=5)

#압축 및 압축 해제 버튼 프레임
frame3 = tk.Frame(frame, bg='#d3d3d3')
frame3.pack(pady=(0, 10))

btn_Encode = tk.Button(frame3, text="허프만 압축", command=lambda: Huffman.Encode(label_Encode_Rate_Value, label_Encode_Speed_Value, label_B_fileSize, label_A_fileSize, label_textFile, label_encodeFile), bg='#0165DF', fg='white', width=15, pady=5, font=('Helvetica', 11, 'bold'))
btn_Encode.pack(side='left', padx=10, pady=10)

btn_LZ77 = tk.Button(frame3, text="LZ77 압축", command=lambda: Huffman.LZ77(label_LZ77_Value), bg='green', fg='white', width=15, pady=5, padx=5, font=('Helvetica', 11, 'bold'))
btn_LZ77.pack(side='left', padx=10, pady=10)

btn_Decode = tk.Button(frame3, text="압축 해제", command=lambda: Huffman.Decode(label_Decode_Speed_Value, label_decodeFile), bg='#F56939', fg='white', width=15, pady=5, font=('Helvetica', 11, 'bold'))
btn_Decode.pack(side='right', padx=10, pady=10)

#파일 내용 출력
frame4 = tk.Frame(frame, bg='#d3d3d3')
frame4.pack(pady=(10, 25))

label_textFile = tk.Text(frame4, bg='white', width=50, height=25, padx=11, pady=9)
label_textFile.pack(side='left', padx=10)
label_textFile.insert('1.0', '압축 전 파일 내용')

label_encodeFile = tk.Text(frame4, bg='white', width=50, height=25, padx=11, pady=9, wrap='word')
label_encodeFile.pack(side='left', padx=10)
label_encodeFile.insert('1.0', '압축 후 파일 내용')

label_decodeFile = tk.Text(frame4, bg='white', width=50, height=25, padx=11, pady=9)
label_decodeFile.pack(side='left', padx=10)
label_decodeFile.insert('1.0', '압축 해제 후 파일 내용')

#결과 출력 프레임 - 파일 크기
frame5 = tk.Frame(frame, bg='#d3d3d3')
frame5.pack(pady=(10, 0))

label_Before_fs = tk.Label(frame5, text='압축 전 파일 크기', bg='black',fg='white', padx=11, pady=9)
label_Before_fs.pack(side='left')

label_B_fileSize = tk.Label(frame5, text='-', bg='white', width=20, pady=9)
label_B_fileSize.pack(side='left')

label_After_fs = tk.Label(frame5, text='압축 후 파일 크기', bg='black',fg='white', padx=11, pady=9)
label_After_fs.pack(side='left')

label_A_fileSize = tk.Label(frame5, text='-', bg='white', width=20, pady=9)
label_A_fileSize.pack(side='left')

label_LZ77 = tk.Label(frame5, text='LZ77 압축 후 파일 크기', bg='black',fg='white', padx=11, pady=9)
label_LZ77.pack(side='left')

label_LZ77_Value = tk.Label(frame5, text='-', bg='white', width=20, pady=9)
label_LZ77_Value.pack(side='left')

#결과 출력 프레임 - 압축률, 속도
frame6 = tk.Frame(frame, bg='#d3d3d3')
frame6.pack(pady=(10, 25))

label_Encode_Rate = tk.Label(frame6, text='압축률', bg='black',fg='white', padx=11, pady=9)
label_Encode_Rate.pack(side='left')

label_Encode_Rate_Value = tk.Label(frame6, text='-', bg='white', width=20, pady=9)
label_Encode_Rate_Value.pack(side='left')

label_Encode_Speed = tk.Label(frame6, text='압축 속도', bg='black',fg='white', padx=11, pady=9)
label_Encode_Speed.pack(side='left')

label_Encode_Speed_Value = tk.Label(frame6, text='-', bg='white', width=20, pady=9)
label_Encode_Speed_Value.pack(side='left')

label_Decode_Speed = tk.Label(frame6, text='압축 해제 속도', bg='black',fg='white', padx=11, pady=9)
label_Decode_Speed.pack(side='left')

label_Decode_Speed_Value = tk.Label(frame6, text='-', bg='white', width=20, pady=9)
label_Decode_Speed_Value.pack(side='left')

btn_Exit = tk.Button(frame, text="프로그램 종료", bg='white', command=root.quit, padx=8, pady=3)
btn_Exit.pack(pady=(10, 0))
        
root.mainloop()