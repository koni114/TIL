# numpy 배열 외부 파일로 저장하기(save)
# 외부 파일을 배열로 불러오기(load)

# np.save() : 1개의 배열을 NumPy format 의 바이너리 파일로 저장
import numpy as np
import os
x = np.arange(5)
abs_path = "/Users/heojaehun/gitRepo/TIL/Python/daily_Python/test_data"
np_file_name = "x_save"
full_file_name = os.path.join(abs_path, np_file_name)
np.save(full_file_name, x)

# np.load() : np.save() 로 저장된 *.npy 파일을 배열로 불러오기
x_save_load = np.load(full_file_name + '.npy')
print(x_save_load)

# np.savez() : 여러개의 배열을 1개의 압축되지 않은 *.npz 포맷 파일로 저장하기
x = np.array([0, 1, 2, 3, 4])
y = np.array([5, 6, 7, 8, 9])
npz_file_name = 'xy_save'
full_file_name = os.path.join(abs_path, npz_file_name)
np.savez(full_file_name, x=x, y=y)

# np.load() : np.savez() 로 저장된 *.npz 파일을 배열로 불러오기
xy_save_load = np.load(full_file_name + ".npz")
type(xy_save_load)  # NpzFile type
print(xy_save_load['x'])
print(xy_save_load['y'])

# np.load() 함수로 연 파일을 더이상 사용할 일이 없으면 메모리 효율 관리를 위해 file.close() 로
# 닫아주어야 함. .close() 로 닫은 상태에서 indexing 을 하려면 open error 발생
xy_save_load.close()

try:
    xy_save_load['x']
except AttributeError as e:
    print(e)

# np.savez_compressed() : 여러개의 배열을 1개의 압축된 *.npz 포맷 파일로 저장하기
x = np.array([0, 1, 2, 3, 4])
y = np.array([5, 6, 7, 8, 9])
npz_file_name = 'xy_savez_compressed'
full_file_name = os.path.join(abs_path, npz_file_name)
np.savez_compressed(full_file_name, x=x, y=y)

# np.load() : np.save_compressed() 로 저장된 압축된 *.npz 파일을 배열로 불러오기

xy_savez_compress_load = np.load(full_file_name + ".npz")
type(xy_savez_compress_load)
print(xy_savez_compress_load['x'])
print(xy_savez_compress_load['y'])
xy_savez_compress_load.close()

# np.savetext() : 여러개의 배열을 텍스트 파일로 저장하기
# np.loadtext() : 텍스트 파일을 배열로 불러오기
# header, footer 로 '#' 으로 시작하는 부가설명을 추가할 수 있음
# fmt 로 format 지정 가능. 아래 예에서는 소수점 2자리까지만 고정된 자리수로 표현

x = np.array([0, 1, 2, 3, 4])
y = np.array([5, 6, 7, 8, 9])
text_file_name = 'xy.txt'
full_file_name = os.path.join(abs_path, text_file_name)
np.savetxt(full_file_name,
           (x, y),  # x,y equal sized 1D arrays
           header='--xy save start--',
           footer='--xy save end--',
           fmt='%1.2f'
           )

xy_savetxt_load = np.loadtxt(full_file_name)
print(xy_savetxt_load)

# numpy 배열을 여러개의 하위 배열로 분할하기
# (1) 한 개의 배열을 수직 축(열 방향, column-wise) 로 여러 개의 하위 배열로 분할
import numpy as np

x = np.arange(18).reshape(3, 6)

# 아래의 4가지 함수 모두 동일한 결과 반환
# - np.hsplit(x, 3)
# - np.hsplit(x, (2, 4))
# - np.split(x, 3, axis=1)
# - np.split(x, (2, 4), axis=1)

x1, x2, x3 = np.hsplit(x, 3)
print(x1)
print(x2)
print(x3)

np.hsplit(x, (2, 4))  # (2, 4)는 자르는 기준 축

# (1) 한 개의 배열을 수평 축(행 방향, row-wise)으로 여러 개의 하위 배열로 분할
x = np.arange(18).reshape(3, 6)
print(x)

# - np.vsplit(x, 3)
# - np.vsplit(x, (2, 4))
# - np.split(x, 3, axis=0)
# - np.split(x, (2, 4), axis=0)

np.vsplit(x, 3)
np.vsplit(x, (1, 2))
np.split(x, 3, axis=0)
np.split(x, (1, 2), axis=0)

# 선형대수 함수(Linear Algebra)
# 단위행렬(Unit matrix): np.eye(n)
import numpy as np

unit_mat_4 = np.eye(4)
print(unit_mat_4)

# 대각행렬(Diagonal matrix): np.diag(x)
import numpy as np

x = np.arange(9).reshape(3, 3)
print(x)
print(np.diag(x))
print(np.diag(np.diag(x)))

# 내적(Dot product, Inner product): np.dot(a, b)
a = np.arange(4).reshape(2, 2)
print(a)
print(a * a)

# 대각합(Trace): np.trace(x)
b = np.arange(16).reshape(4, 4)
np.trace(b)

# 3차원 행렬에 대해서도 대각합 가능
c = np.arange(27).reshape(3, 3, 3)
np.trace(c)

# 행렬식(Matrix Determinant): np.linalg.det(x)
# 역행렬이 존재하는지의 여부를 확인
# 행렬식이 0이 아니면 역행렬이 존재. 이 행렬식이 0이면 역행렬이 존재하지 않음
d = np.array([[1, 2], [3, 4]])
np.linalg.det(d)

# 역행렬(Inverse of a matrix): np.linalg.inv(x)
# A*B, B*A 모두 순서에 상관없이 곱했을 때 단위 행렬이 나오는 n차 정방행렬이 있다면 역행렬 존재
# 역행렬은 가우스 소거법, 혹은 여인수(cofactor method) 로 풀 수 있음

a = np.array(range(4)).reshape(2, 2)
a_inv = np.linalg.inv(a)
a.dot(a_inv)  # 단위 행렬 출력

# 고유값(Eigenvalue), 고유벡터(Eigenvector): w, v = np.linalg.eig(x)
# 정방행렬 A에 대해서 Ax = λx 가 성립하는 0이 아닌 벡터 x가 존재할 때 상수 λ 를 행렬 A의 고유값,
# x 를 이에 대응하는 고유벡터 (eigenvector) 라고 함

e = np.array([[4, 2], [3, 5]])
w, v = np.linalg.eig(e)
print(w)  # lambda
print(v)  # eigen-vector

# 특이값 분해 (Singular Value Decomposition): u, s, vh = np.linalg.svd(A)
# 행렬을 대각화하는 방법
# 정방행렬 뿐만 아니라, m x n 행렬에 대해 적용 가능
# 특이값 분해는 차원축소, 데이터 압축 등에 사용할 수 있음
A = np.array([[3, 6], [2, 3], [0, 0], [0, 0]])
print(A)
u, s, vh = np.linalg.svd(A)

# 연립방정식 해 풀기 (Solve a linear matrix equation): np.linalg.solve(a, b)
# 4x0 + 3x1 = 23
# 3x0 + 2x1 = 16
# 위의 연립방정식을 어떻게 행렬로 입력하고, np.linalg.solve(a, b)에 입력하는지 확인
a = np.array([[4, 3], [3, 2]])
b = np.array([23, 16])
x = np.linalg.solve(a, b)

# 결과 확인
np.allclose(np.dot(a, x), b)

# 최소자승 해 풀기(Compute the Least-squares solution): m, c = np.linalg.lstsq(A, y, rcond=None)
# 회귀모형 적합시 최소자승법(Least-square method) 으로 잔차 제곱합을 최소화하는 회귀계수 추정
x = np.array([0, 1, 2, 3])
y = np.array([-1, 0.2, 0.9, 2.1])
A = np.vstack([x, np.ones(len(x))]).T
m, c = np.linalg.lstsq(A, y, rcond=None)[0]
print(m, c)

import matplotlib.pyplot as plt

plt.plot(x, y, 'o', label='Original data', markersize=10)
plt.plot(x, m * x + c, 'r', label='fitted line')
plt.legend()
plt.show()

# 다수개의 범주형 자료로 가변수 만들기(dummy variable)
# (1) 하나의 cell 당 값이 한개씩 들어있는 범주형 자료를 가지고 가변수 만들기

import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas import Series

music_df = pd.DataFrame({'music_id': [1, 2, 3, 4, 5],
                         'music_genre': ['rock',
                                         'disco',
                                         'pop',
                                         'rock',
                                         'pop']})

music_dummy_mat = pd.get_dummies(music_df['music_genre'])
music_df.join(music_dummy_mat.add_prefix('genre_s'))

# (2) 하나의 cell 에 범주 값이 여러 개씩 들어있는 범주형 자료를 가지고 가변수 만들기
music_multi_df = DataFrame({'music_id': [1, 2, 3, 4, 5],
                            'music_genre': ['rock|punk rock|heavy metal',
                                            'hip hop|reggae',
                                            'pop|jazz|blues',
                                            'disco|techo',
                                            'rhythm and blues|blues|jazz']})

# | 로 구분되어 있는 여러개의 범주 값들을 split() 문자열 메소드로 사용하여 분리 한 후,
# set.union() 함수를 사용하여 각 음악 장르 범주 값들을 원소로 가지는 하나의 집합 생성
music_genre_iter = (set(x.split("|")) for x in music_multi_df.music_genre)
music_genre_set = sorted(set.union(*music_genre_iter))

# 다음 np.zeros() 함수를 사용하여 music_multi_df 의 행 개수만큼 행과
# music_genre_set 의 개수만큼 열을 가지는 '0'으로 채워진 데이터프레임을 만들어봄
indicator_mat = pd.DataFrame(np.zeros((len(music_multi_df), len(music_genre_set))),
                             columns=music_genre_set)

# for 문을 통해 row 별로 music_genre 의 값을 순회하면서 split() 메소드를 분리한 다음,
# 각 음악별로 해당 장르를 방금 위에서 '0'으로 자리를 채워두었던 indicator_mat 데이터프레임의 행, 열을 참조하여
# 해당 위치에 '1'의 값 입력

for i, genre in enumerate(music_multi_df.music_genre):
    indicator_mat.loc[i, genre.split("|")] = 1

# 마지막으로, 음악 장르 가변수의 앞 머리에 'genre_' 라는 접두사를 붙이고
music_indicator_mat = music_multi_df.join(indicator_mat.add_prefix('genre_'))
print(music_indicator_mat)

## groupby() 로 그룹별 집계하기(data aggregation by groups)
# 1. 전체 데이터를 그룹별로 나누고(split)
# 2. 각 그룹별로 집계함수를 적용(apply)
# 3. 그룹별 집계 결과를 하나로 합침(combine)

# 실습 데이터 바다 해산물 전복(abalone) 공개 데이터셋 사용
pd.set_option('display.max_columns', 30)
abalone_df = pd.read_csv('./test_data/abalone.txt',
                         sep=',',
                         names=['sex', 'length', 'diameter', 'height',
                                'whole_weight', 'shucked_weight', 'viscera_weight',
                                'shell_weight', 'rings'],
                         header=None)

abalone_df.head()
np.sum(pd.isnull(abalone_df))
abalone_df.describe()

# 전복 성별 그룹별로 전복의 전체 무게 변수에 대해서 GroupBy 집계
# 집단별 크기는 grouped.size(),
# 집단별 합계는 grouped.sum()
# 집단별 평균은 grouped.mean()

grouped = abalone_df['whole_weight'].groupby(abalone_df['sex'])
grouped.size()
grouped.sum()
grouped.mean()

# 모든 연속형 변수에 대해서 성별 집계 수행
abalone_df.groupby(abalone_df['sex']).mean()
abalone_df.groupby('sex').mean()

# 길이(length) 라는 새로운 범주형 변수를 추가
# length 의 중앙값(median) 보다 길면, length_long, 작으면 length_short 로 구분하는 범주형 변수
# length_cat 컬럼 생성
abalone_df['length_cat'] = np.where(abalone_df.length > np.median(abalone_df.length),
                                    'length_long',
                                    'length_short')

# 성별 그룹(sex) 와 범주(length_cat) 그룹별로 GroupBy 를 사용해 평균 구하기
mean_by_sex_length = abalone_df['whole_weight'].groupby([abalone_df['sex'], abalone_df['length_cat']]).mean()
mean_by_sex_length.unstack()

abalone_df.groupby(['sex', 'length_cat'])['whole_weight'].mean()

207 - 145
12
25
25

145 + 37