# 아스키코드
print(ord('A'))
print(ord('0'))
print(chr(48))
print(chr(65))

import sys
print(sys.maxsize)
print(-sys.maxsize)
float('inf')
float('-inf')

#- if + dict 조합
#- 다음은 dict의 key를 조회
dic = {1: 100, 10: 1000}
if 1 in dic:
    print("helloworld")

#- deque 선언시 다음을 조심
from collections import deque
print(deque([1, 2, 3]))
print(deque([[1, 2, 3]]))

#- ifelse one row에 작성하기
sum = []
1 if not sum else 100

#- sorted lambda 사용
test = [[1, 10, 20, 30],  [2, 30, 20, 10], [2, 30, 30, 30]]
sorted_test = sorted(test, key=lambda x: (-x[0], x[1], -x[2], x[3]))
print(sorted_test)
