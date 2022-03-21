# 2021-03-21
# dataFrame 을 JSON 으로 변환

# pandas 에는 DataFrame 이나 Series 를 json 형태로 변환해주는 to_json 이라는
# method 가 있음

import pandas as pd
dict_test = {
    'col1': [1, 2, 3, 4, 5],
    'col2': ['a', 'b', 'c', 'd', 'e'],
    'col3': ['Apple', 'Banana', 'Watermelon', 'Grape', 'Melon']
}
df_test = pd.DataFrame(dict_test)
print(df_test)

json_test = df_test.to_json()
print(json_test)

# json 의 형태는 하나의 column 이 가장 바깥쪽에 있으며,
# 각 컬럼에 존재하는 행(row) 별 값들이 내부 json 형태로 들어가있음

df = pd.DataFrame([['Jay',16,'BBA'],
                   ['Jack',19,'BTech'],
                   ['Mark',18,'BSc']],
                  columns = ['Name','Age','Course'])

js = df.to_json(orient='records')






