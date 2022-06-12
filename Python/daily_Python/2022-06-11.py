"""
python nan, None 정복하기.
"""
# pandas DataFrame 에 None 데이터를 넣으면 NaN 객체로 자동 변환이 됨

import pandas as pd
df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [None, 3, 4]],
                  columns=["a", "b", "c"],
                  index=["aa", "bb", "cc"])

# df 를 출력하면 NaN 으로 변경된 것을 확인할 수 있음
print(df)

# None 은 다른 프로그래밍 언어에서의 NULL 임. 즉 아무것도 없는 데이터를 의미함
# 파이썬은 모든 데이터가 객체로 이루어져 있으므로, None 역시 NoneType 이라는 객체로 이루어져 있고
# 싱글턴으로 동작함(싱글턴이란 오직 하나의 인스턴스만 생성하여 사용하는 것)

# NaN은 Not a Number 의 약자로 정의되거나, 표현되지 않는 부동소수점 값으로 Python 에서는 float 타입이 됨
# 무한대끼리의 나눗셈, 무한대 끼리의 덧셈 등을 통해 NaN을 생성할 수 있음
# NaN이 피연산자로 포함되는 어떠한 연산도 결과는 NaN이 됨

print(float("nan") == float("nan"))  # False
print(float("nan") is float("nan"))  # False
print(None is None)  # True
print(None == None)  # True

# 위 결과는 None 과 NaN 의 싱글턴 여부, 값 구분 방식에 대해 나타낸다.( ** 중요)
# `is` 연산자는 해당 객체의 주소, 포인터를 비교하므로, 하나만 생성하는 None 의 비교는 언제나 True
# NaN의 경우 float 객체를 생성한 것이므로 위 코드는 두 개의 float('nan') 객체가 생성된 것으로 False 가 됨

# == 연산자는 값 자체를 비교하므로 None 연산은 True.
# NaN 의 경우 값 비교 자체가 불가능하므로 False(정의되거나 표현되는 값이 아님)

# 결과적으로 3가지 방식을 통해, NaN 여부를 확인할 수 있음
# (1) == 연산자가 False
# (2) math.isnan(x)
# (3) pd.isnull(x)

import math
import pandas as pd
import numpy as np

x = float("nan")
type(x)               # float
print(x == x)         # False
print(math.isnan(x))  # True
print(pd.isnull(x))   # True

y = None
type(y)
print(y == y)         # True
print(math.isnan(y))  # Error . --> TypeError. must be real number, not NoneType
print(pd.isnull(y))   # True

z = np.nan
type(z)               # float
print(z == z)         # False
print(math.isnan(z))  # True
print(pd.isnull(z))   # True

def is_nan_or_none(x):
    if x is None:
        return True
    if type(x) == float:
        if x != x and math.isnan(x) and pd.isnull(x):
            return True

    return False

