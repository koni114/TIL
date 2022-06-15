"""

"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def df2_isin_df1(df1, df2, group_var):
    """
        두 개의 dataFrame 이 있을 때,(df1, df2)
        df2[group_var] 에 존재하는 모든 CASE 의 df1[group_var] 를 slicing 하는 예제
    :param df1: df2[group_var] 에 존재하는 row 를 slicing 하기 위한 dataFrame
    :param df2: df1 을 slicing 하기위한 dataFrame
    :param group_var:
    :return:
        slicing 한 df1 dataFrame
    """
    result_df = df1.loc[np.all(np.isin(list(df1[group_var].itertuples(index=False, name=None)),
                                       list(df2[group_var].itertuples(index=False, name=None))), axis=1), :]
    return result_df


# 함수 테스트 해보기
pd.set_option("display.max_columns", 100)

# test data 만들기
df = pd.read_csv("rfriend-python-study/data/train.csv")

train_data, test_data = train_test_split(df,
                                         test_size=0.2,
                                         train_size=0.8,
                                         random_state=100,
                                         shuffle=True)

result_df = df2_isin_df1(train_data, test_data, ["Sex", "Age"])




















