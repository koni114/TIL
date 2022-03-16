# 2022-03-16
# pd.Series, np.ndarray, list 중 가장 size 가 적은 것은?
# --> pd.Series, np.ndarray, list 로 type 구분하기
import sys

import numpy as np
import pandas as pd

# Python list
my_odd_nums = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
ls = list(range(0, 20))

# Numpy array
my_odd_array = np.array([1, 3, 5, 7, 9, 11, 13, 15, 17, 19])
my_odd_ndarray = np.arange(0, 20)

# Pandas series
my_series = pd.Series(my_odd_nums)
se = pd.Series(my_odd_ndarray)

"""
데이터 자체의 사이즈는 커지면 커질수록 np.array < list < pd.Series 순으로 나타남.
"""

print(f"List : {sys.getsizeof(ls)} bytes")
print(f"np.array : {sys.getsizeof(my_odd_ndarray)} bytes")
print(f"pd.series : {sys.getsizeof(se)} bytes")

#- list, np.ndarray, pd.Series 타입 구분하기
ls = list(range(0, 20))
ls_ndarray = np.arange(0, 20)
se = pd.Series(my_odd_ndarray)

print(f"type(ls) == list :  {type(ls) == list}")
print(f"type(ls) == np.ndarray : {type(ls) == np.ndarray}")
print(f"type(ls) == pd.Series : {type(ls) == pd.Series}")

print(f"type(ls_ndarray) == list :  {type(ls_ndarray) == list}")
print(f"type(ls_ndarray) == np.ndarray : {type(ls_ndarray) == np.ndarray}")
print(f"type(ls_ndarray) == pd.Series : {type(ls_ndarray) == pd.Series}")

print(f"type(se) == list :  {type(se) == list}")
print(f"type(se) == np.ndarray : {type(se) == np.ndarray}")
print(f"type(se) == pd.Series : {type(se) == pd.Series}")