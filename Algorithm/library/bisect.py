"""
정렬된 시퀀스 검색 시, bisect 를 사용해라
- 리스트에서 index 함수를 사용하여 특정 값 검색시 리스트 길이에 선형으로 비례하는 시간이 필요
-
"""
#- bisect 를 사용하지 않는 경우,
data = list(range(10**5))
index = data.index(91234)
assert index == 91234

def find_closest(sequence, goal):
    for idx, value in enumerate(sequence):
        if goal < value:
            return idx
    raise ValueError(f"범위를 벗어남 : {goal}")

index = find_closest(data, 91234.56)
assert index == 91235

#- 파이썬 내장 bisect 모듈은 순서가 정해져 있는 리스트에 대해서 이런 유형의 검사를 효과적으로 수행함
#- bisect_left 함수를 사용하면 정렬된 원소로 이루어진 시퀀스에 대해서 이진 검색을 효율적으로 수행
#- bisect_left 가 반환하는 인덱스는 리스트에 찾는 값의 원소가 존재하는 경우 이 원소의 인덱스이며,
#- 리스트에 찾는 값의 원소가 존재하지 않는 경우 정렬 순서상 해당 값을 삽입해야 할 자리의 인덱스

from bisect import bisect_left
index = bisect_left(data, 91234)
print(index)

index = bisect_left(data, 91234.56)
print(index)

index = bisect_left(data, 91234.23)
print(index)