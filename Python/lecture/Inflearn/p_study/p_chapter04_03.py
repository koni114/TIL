"""
해시 테이블(hashtable)
Dict 생성 고급 예제
- key 를 하나로 합치면서 데이터를 합치는 방법 : setdefault
Setdefault 사용법
"""

# open-source 나 package 에서 tuple 을 많이 사용함
# 이 때 tuple 을 Dict 로 변경할 때 key 를 하나로 합치면서 dict 를 만드는 방법이 유용

# 해시 테이블
# key 에 Value 를 저장하는 구조
# 파이썬 언어 자체가 hashtable 구조로 되어 있다고 함
# 파이썬 dict 해쉬 테이블 예
# 키 값의 연산 결과에 따라 직접 접근이 가능한 구조
# key 값을 해싱 함수를 통해 해시 주소 값이 나오고, 이 값을 기반으로 key 에 대한 value 의 위치 참조

# Dict 구조
print(__builtins__.__dict__)

# Hash 값 확인
# hash 함수 사용 시, 가변 값은 불가능
t1 = (10, 20, (30, 40, 50))
t2 = (10, 20, [30, 40, 50])
print(hash(t1)) # 고유한 값의 해시 값 확인 가능
print(hash(t2)) # list 는 해시 함수 사용 불가능

# Dict Setdefault 예제
# 정보 검색이나 분석을 통해서 setdefault 가 많이 사용

# source 를 dict 로 변경
source = (('k1', 'val1'),
          ('k1', 'val2'),
          ('k2', 'val3'),
          ('k2', 'val4'),
          ('k2', 'val5'))

new_dict1 = {}
new_dict2 = {}

# No use setdefault
for k, v in source:
    if k in new_dict1:
        new_dict1[k].append(v)
    else:
        new_dict1[k] = [v]

print(new_dict1)

# use setdefault
for k, v in source:
    new_dict2.setdefault(k, []).append(v)
print(new_dict2)

# 주의 --> 다음과 같이 만들어내면 안됨
#     --> key 중복시 덮어써짐
new_dict3 = {k: v for k, v in source}


