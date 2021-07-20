import sys
import pprint

pprint.pprint(locals())

a = [1, 2, 3, 4, 5]
list(enumerate(a))
divmod(5, 3)

#- print 함수는 항상 줄바꿈을 함
print("A1", "A2")
print("A1", "A2", sep=',')
print("A1", "A2", end=' ')
a = ['A', 'B']
print(" ".join(a))
#- f-string 을 통한 출력 방법이 좋음: 3.6+ 에서만 지원
idx, fruit = 1, "Apple"
print(f"{idx + 1}: {fruit}")