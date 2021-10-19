"""
chapter04-02.py
"""
# Tuple Advanced
# Unpacking

print(divmod(100, 9))
print(divmod(*(100, 9)))
print(*(divmod(100, 9)))

x, y, * rest = range(10)
print(x, y, rest)
x, y, * rest = range(2)
print(x, y, rest)
x, y, z, i, *rest = 1, 2, 3, 4, 5
print(x, y, rest)

# Mutable(가변) vs Immutable(불변)
l = (15, 20, 25)
m = [15, 20, 25]

print(l, id(l))
print(m, id(m))

l = l * 2
m = m * 2

print(l, id(l))
print(m, id(m))

# ** 중요!
l *= 2
m *= 2
print(l, id(l))
print(m, id(m))

# sort vs sorted
# sorted : 정렬 후 새로운 객체 반환
f_list = ['orange', 'apple', 'mango', 'papaya', 'lemon', 'strawberry', 'coconut']
print(f"sorted - {sorted(f_list)}")
print(f"sorted - {sorted(f_list, reverse=True)}")
print(f"sorted - {sorted(f_list, key=len)}") # 길이 순으로 정렬
print(f'sorted - {sorted(f_list, key=lambda x: x[-1], reverse=True)}') # x[-1] : 단어 중 가장 끝의 알파벳을 기준으로

print(f_list)
# sort : 정렬 후 객체 직접 변경
print(f"sort - {f_list.sort()}, {f_list}") # 원본 자체가 수정됨. 반환 값은 없음
print(f"sort - {f_list.sort(reverse=True)}, {f_list}")
print(f"sort - {f_list.sort(key=len)}, {f_list}")
print(f"sort - {f_list.sort(key=lambda x: x[-1])}, {f_list}")

# List vs Array 적합한 사용법 설명
# 리스트 기반 : 융통성, 다양한 자료형, 범용적 사용.
# 숫자 기반 : 배열(리스트와 거의 호환)