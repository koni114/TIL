# pandas 파생변수 생성하는 방법 정리하기.
import pandas as pd
import numpy as np
import os

pd.set_option('display.max_columns', None)

os.getcwd()
file_path = "./test_data/retail-data/all/online-retail-dataset.csv"

df = pd.read_csv(file_path)

# 1. 기존 컬럼을 활용해서 새로운 컬럼 생성하기(단순 추가)
df["total_price"] = df["Quantity"] * df["UnitPrice"]

# 2. case 별로 조건을 설정하여 새로운 컬럼 생성하기(function(lambda) + apply)
def country_level(row):
    if row["Country"] == "France":
        return 1
    elif row["Country"] == "USA":
        return 2
    else:
        return 3


df["country_level"] = df.apply(country_level, axis=1)
df.columns
# 3. case 별로 조건을 설정하여 조건에 해당하는 경우 특정 컬럼의 값을 가져오기(func, apply)
# 3.1 apply
def country_level_check(row):
    if row["Country"] == "United Kingdom":
        return row["country_level"]
    elif row["Country"] == "France":
        return 100
    else:
        return row["CustomerID"]


df["country_level_check_1"] = df.apply(country_level_check, axis=1)

# 3.2 np.select
df["country_level_check_2"] = np.select([df.Country == "United Kingdom", df.Country == "France"],
                       [df.country_level, 100],
                       default=df.CustomerID)

# 3.3 np.where
df["country_level_check_3"] = np.where(df.Country == 'United Kingdom', df.country_level,
                                       np.where(df.Country == 'France', 100, df.CustomerID))



# apply 와 np.select, np.where 를 사용하여 적용 가능하나, np.where/select 가 성능이 훨씬 좋음.

