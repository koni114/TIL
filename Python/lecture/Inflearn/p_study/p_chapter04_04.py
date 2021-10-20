"""
파이썬 시퀀스 실습
- 해시 테이블(Hashable)
- Immutable Dict 생성
- 지능형 Set
- Set 선언 최적화
"""

# 해시 테이블 -> 적은 리소스로 많은 데이터를 효율적으로 관리
# Dict -> Key 중복 허용 x, set -> 중복 허용 x

# dict 및 set 심화
# immutable Dict
from types import MappingProxyType  # 읽기 전용의 dictionary 타입 생성 가능

d = {'key1': 'value1'} # 다른 팀원이 해당 d 라는 값을 수정할 여지가 있을 때, 읽기 전용으로 사용할 때 사용

# Read Only
d_frozen = MappingProxyType(d)

print(d, id(d))
print(d_frozen, id(d_frozen), hash(d_frozen)) # hash 값도 지원하지 않음

# 수정 가능
d['key2'] = 'value2'
print(d)

# 수정 불가능
d_frozen['key2'] = 'value2' # does not support item assignment

# set type 도 MappingProxyType 으로 감싸면 변경이 불가능

s1 = {'Apple', 'Orange', 'Apple', 'Orange', 'Kiwi'}
s2 = {'Apple', 'Orange', 'Apple', 'Orange', 'Kiwi'}
s3 = {} # 값이 하나도 없는 경우에는 dictionary 로 설정됨
s4 = set()
s5 = frozenset(s1)

s1.add('Melon')
print(s1)

# fronzenset 에는 값이 추가가 안됨
s5.add('Molon')

# 선언 최적화
# 내부적으로 파이썬은 바이트 코드를 실행 -> 파이썬 언티프리터가 바이트 코드를 실행함
from dis import dis

# 위에 것은 3단계로 되어 있고, 아래 것은 5단계로 되어 있음
# 결과적으로 위에 방법을 사용하는 것이 조금 더 최적화 되어 있음을 확인 가능
print('------')
print(dis('{10}'))
print('------')
print(dis('set([10])'))

# 지능형 집합(Comprehending Set)
print("-----")
from unicodedata import name
print({chr(i) for i in range(0, 256)})
print({name(chr(i), '') for i in range(0, 256)}) # 문자열 자판을 가져온 것