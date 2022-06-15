"""
두 개의 dataFrame 이 있을 때,(df1, df2)
df2[group_var] 에 존재하는 모든 CASE 의 df1[group_var] 를 slicing 하는 예제
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

pd.set_option("display.max_columns", 100)

# test data 만들기
df = pd.read_csv("rfriend-python-study/data/train.csv")

train_data, test_data = train_test_split(df,
                                         test_size=0.2,
                                         train_size=0.8,
                                         random_state=100,
                                         shuffle=True)

group_var = ["Sex", "Age"]

len(train_data[group_var].drop_duplicates())
len(test_data[group_var].drop_duplicates())

l1 = list(train_data[group_var].itertuples(index=False, name=None))
l2 = list(test_data[group_var].itertuples(index=False, name=None))

len(train_data.index)
len(np.isin(l1, l2, axis=))

train_data.loc[np.in1d(l1, l2), :]