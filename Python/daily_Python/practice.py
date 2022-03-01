import numpy as np
import os
x = np.array([0, 1, 2, 3, 4])
y = np.array([5, 6, 7, 8, 9])
file_name = "xy_savez.npz"
np.savez_compressed(file_name, x=x, y=y)
obj = np.load(file_name)
x = obj['x']
y = obj['y']
print(x)
print(y)


import numpy as np
x = np.array([0.00, 1.00, 2.00, 3.00, 4.00])
y = np.array([5.00, 6.00, 7.00, 8.00, 9.00])

file_name = "xy_save.txt"
np.savetxt(file_name,
           (x, y),
           "%0.2f",
           header="-- xy save start --",
           footer="-- xy save end --")

# 과제 2
# 다음의 데이터를 로드해보시고, 아래와 같은 결과를 도출해보세요
# 2가지 이상의 방법을 통해서 도출해보세요
import numpy as np
x = np.arange(18).reshape(3, 6)

np.hsplit(x, 3)
np.split(x, (2, 4), axis=1)

x = np.arange(18).reshape(3, 6)

np.vsplit(x, 3)
np.split(x, (1, 2), axis=0)

np.eye(4)
x = np.arange(9).reshape(3, 3)
np.diag(np.diag(x))

a = np.arange(4).reshape(2, 2)
a * a
a.dot(a)

c = np.arange(27).reshape(3, 3, 3)
np.trace(c)

d = np.array([[1, 2], [3, 4]])
np.linalg.det(d)

a = np.array(range(4)).reshape(2, 2)
e, v = np.linalg.eig(a)

A = np.array([[3,6], [2,3], [0,0], [0,0]])
s, v, d = np.linalg.svd(A)

a = np.array([[4, 3], [3, 2]])
b = np.array([23, 16])
x = np.linalg.solve(a, b)
np.isclose((a.dot(x)), b)

import pandas as pd
music_df = pd.DataFrame({'music_id': [1, 2, 3, 4, 5],
                         'music_genre': ['rock',
                                         'disco',
                                         'pop',
                                         'rock',
                                         'pop']})

df_result = pd.concat([music_df, pd.get_dummies(music_df['music_genre'],
                                                prefix="genre")], axis=1)

# 아래 주어진 데이터를 기반으로 One-Hot encoding 을 수행하는 예제입니다
music_multi_df = pd.DataFrame({'music_id': [1, 2, 3, 4, 5],
                               'music_genre': ['rock|punk rock|heavy metal',
                                               'hip hop|reggae',
                                               'pop|jazz|blues',
                                               'disco|techo',
                                               'rhythm and blues|blues|jazz']})

# 다음의 지시를 잘 따라하여 도출해보세요
#   1. 수직바(|) 로 구분되어 있는 music_genre 컬럼에서 | 를 기준으로
#      잘라 음악 장르 범주 값들을 원소로 가지는 하나의 집합(set)을 만들어보세요
#      music_genre_set 변수에 저장해야 합니다.
music_genre_iter = (set(x.split("|")) for x in music_multi_df.music_genre)
music_genre_set = set.union(* music_genre_iter)
print(music_genre_set)

#   2. music_multi_df의 행 개수만큼 행과 music_genre_set 의 개수만큼의 열을 가지는 0으로 채워진
#      dataframe 을 만들어보세요
#      해당 dataframe 을 indicator_mat 에 저장해주세요


#   3. indicator_mat 데이터 프레임에 각 행별로 해당하는 음악 장르를 1로 채워 넣어
#      One-Hot encoding 을 완성하세요

#   4. 기존의 music_multi_df dataFrame 과 indicator_mat 를 합쳐서 완성해주세요












