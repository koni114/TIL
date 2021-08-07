##- pandas DataFrame concat
# pd.concat(objs,                #- Series, DataFrame
#           axis,                #- 0: 위+아래 합치기, 1: 왼쪽 + 오른쪽 합치기
#           join,                #- join type, 'outer', 'inner'
#           ignore_index=,       #- False: 기존 index 유지, True: 기존 index 무시
#           keys=,               #- 계층적 index 사용하려면 keys 튜플 입력
#           levels=,             #- None
#           names=,              #- index의 name 부여시 사용
#           verify_integrity=,   #- index 중복 확인
#           copy=)               #- 복사

import pandas as pd
df_1 = pd.DataFrame({'A': ['A0','A1', 'A2'],
                     'B': ['B0','B1', 'B2'],
                     'C': ['C0', 'C1', 'C2']},
                    index=[1,2,3])

df_2 = pd.DataFrame({'A': ['A3','A4', 'A5'],
                     'B': ['B3','B4', 'B5'],
                     'C': ['C3', 'C3', 'C3']},
                    index=[4,5,6])

df_3 = pd.concat([df_1, df_2])
print(df_3)