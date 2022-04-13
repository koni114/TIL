import pandas as pd
import numpy as np

import pandas as pd
personnel_df = pd.DataFrame({'sequence': [1, 3, np.nan],
                             'name': ['park', 'lee', 'choi'],
                             'age': [30, 20, 40]})

personnel_df.sort_values(["sequence"], ascending=False)
personnel_df.sort_values(["sequence"], na_position="first")
personnel_df.sort_values(["sequence"], na_position="last")

personnel_tuple = [(1, 'park', 30),
                   (3, 'lee', 20),
                   (2, 'choi', 40)]

s = pd.Series([0, 1, 2, 3, 4], index=['a', 'b', 'c', 'd', 'e'])

# 다음 소스 코드를 완성하여 문자열에서 특정 단어가 있으면 True,
# 없으면 False 가 출력되게 만드세요. find 함수는 코루틴으로 작성해야 합니다.

def find(word):
    toggle = True
    while True:
        x = (yield toggle)
        toggle = word in x
        print(f"toggle --> {toggle}")


f = find('Python')
next(f)

print(f.send('Hello, Python!'))
print(f.send('Hello, world!'))
print(f.send('Python Script'))

f.close()
