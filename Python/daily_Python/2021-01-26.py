# 2021.01.26.py
########################################
# test, csv file 불러오기 : pd.read_csv() #
########################################

import pandas as pd
import os
os.getcwd()

df = pd.read_csv('./test_data/test_csv_file.csv')
print(df.shape)

df = pd.read_csv('./test_data/test_text_file.txt', sep="|")
print(df)
print(df.shape)

# 구분자가 tab 이라면, sep  = '\t' 입력

# 파일 불러올 때, index
df = pd.read_csv('./test_data/test_text_file.txt', sep="|", index_col='ID')
df = pd.read_csv('./test_data/test_text_file.txt', sep="|", index_col=0)
print(df)

# 변수 이름(column name) 이 없는 파일 불러올때 이름 부여하기
df = pd.read_csv('./test_data/text_without_column_name.txt', sep="|", names=['ID', 'A', 'B', 'C', 'D'],
                 header=None, index_col='ID')
print(df)

# unicode decode error 발생시, encoding parameter 지정
file = pd.read_csv('directory/file', sep='|', encoding='CP949')
file = pd.read_csv('directory/file', sep='|', encoding='latin')

# 특정 줄은 제외하고 불러오기
csv_2 = pd.read_csv('./test_data/test_text_file.txt', skiprows=[1, 2])

# n 개의 행만 불러오기
csv_3 = pd.read_csv('./test_data/test_text_file.txt', nrows=3)

# 사용자 정의 결측값 기호(custom missing value symbols) : na_values
df = pd.read_csv('./test_data/test_text_file.txt', na_values=['?', '??', 'N/A', 'NA', 'nan'])

# 데이터 유형 설정 : dtype
# pandas 는 데이터셋을 읽어들일 때 '첫번째 행의 데이터' 를 기준으로 각 컬럼별 데이터 유형을 추정해서 자동으로 셋팅함
# 맞지 않는 경우, dtype 옵션으로 사전형으로 각 칼럼 별 데이터 유형을 짝 지어 명시적으로 설정 가능
df = pd.read_csv('./test_data/test_text_file.txt', dtype={'ID': int,
                                                          'LAST_NAME': str,
                                                          'AGE': float})


