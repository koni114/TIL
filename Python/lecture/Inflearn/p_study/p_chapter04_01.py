"""
시퀀스
- 나열되어 있으면서 순서가 붙어 있는 타입
"""
# 시퀀스형
# 컨테이너(container: 서로 다른 자료형(list, tuple, collections.deque))
# 플랫(Flat: 한개의 자료형(str, bytes, bytearray, array.array, memoryview)

# 가변(mutable, [list, bytearray, array.array, memoryview, deque])
# 불변(immutable, [tuple, str, bytes])

# a = [3, 3.0, 'a']
# print(a)

# 리스트 및 튜플 고급
# 지능형 리스트(Comprehension lists)

chars = '+_)(*&^%$$#@!'
# chars[2] = 'h' # error

code_list1 = []
for s in chars:
    # 유니코드 리스트
    code_list1.append(ord(s))

print(code_list1)

# Comprehension lists
code_list2 = [ord(s) for s in chars]

# Comprehending Lists,  Map + Filter
# 복잡한 filter logic 을 사용할 때, filter + map 함수를 사용하는 경우가 많음
code_list3 = [ord(s) for s in chars if ord(s) > 40]
print(code_list3)

# Map + Filter
code_list4 = list(filter(lambda x: x > 40, map(ord, chars)))
print(code_list4)

print([chr(s) for s in code_list1])
print([chr(s) for s in code_list2])
print([chr(s) for s in code_list3])
print([chr(s) for s in code_list4])

# Generator 생성
# 다음에 내가 반환할 값만 메모리 상에 가지고 있음. -> 메모리 사용량은 극히 작음
# array 는 플랫형으로 한개의 자료형만 저장이 가능

# generator + array 사용 예제
# 만약 마지막 값 이후에 next 함수를 통해 값 호출 시, stopIteration 예외 발생

import array
tuple_g = (ord(s) for s in chars) # ()로 선언
print(tuple_g) # generator
print(type(tuple_g))
print(next(tuple_g))

# numpy package 의 ndarray 는 array 를 사용
array_g = array.array('I', (ord(s) for s in chars))

print(type(array_g))
print(array_g.tolist())

# 제너레이터 예제
# A1, A2, A3 .. ~ D20까지 출력하는 제너레이터를 만들어 출력해보기
for s in ('%s' % c + str(n) for c in ['A', 'B', 'C', 'D'] for n in range(1, 21)):
    print(s)

# 리스트 주의 --> 얕은 복사 vs 깊은 복사
marks1 = [['~'] * 3 for _ in range(4)]
marks2 = [['~'] * 3] * 4
print(marks1)
print(marks2)

marks1[0][1] = 'X'
marks2[0][1] = 'X'

print(marks1)
print(marks2)

# 원인 증명
print([id(i) for i in marks1])
print([id(i) for i in marks2]) # 모든 내부 리스트들이 같은 주소값을 가지는 것을 확인




