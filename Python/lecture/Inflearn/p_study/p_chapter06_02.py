"""
병행성
- 제너레이터 실습
- Yield 실습
- Itertools 실습
"""
# chapter06-02.py
# 병행성 vs 병렬성
# 병행성은 한 컴퓨터가 여러 일을 동시에 수행하는 것을 의미함
# - thread 는 하나지만, 여러 일을 하는 것처럼 수행되는 것
# 병렬성은 여러 컴퓨터가 여러 작업을 동시에 수행하는 것을 의미함

# generator ex1
def generator_ex1():
    print('start')
    yield 'A Point' # 네이버 크롤링
    print('Continue')
    yield 'B Point' # 구글 크롤링
    print('end')

temp = iter(generator_ex1())
print(temp) # generator

print(next(temp)) # A Point 출력 후 멈춤
print(next(temp)) # B Point 출력 후 멈춤
print(next(temp)) # end 호출 후 StopIteration

# 이러한 과정이 동시에 여러 일을 단일 코딩에서 수행 할 수 있게 하는 매커니즘
# for 문에서 반복 가능한 generator.
for v in generator_ex1():
    print(v)

# generator Ex2
# 두 개의 차이를 꼭 기억하자
temp2 = [x * 3 for x in generator_ex1()]
temp3 = (x * 3 for x in generator_ex1())

print(temp2)
print(temp3) # 생성된 값을 다시 generator 로 만듬 -> for 문에서 호출!

# Generator Ex3(중요 함수)
# count, takewhile, filterfalse, accumulate, chain, product, groupby..

# 무한대로 값을 만들어보고 싶을 때: itertools.count
import itertools
gen1 = itertools.count(1, 2.5)

# 조건
# takewhile(func1, func2)
# func1 을 만족할 때까지 func2 generator or iterator 순환
gen2 = itertools.takewhile(lambda n: n < 1000, itertools.count(1, 2.5))
for v in gen2:
    print(v)

# 필터의 반대조건 : filterfalse
gen3 = itertools.filterfalse(lambda n: n < 3, [1, 2, 3, 4, 5])
for v in gen3:
    print(v)

# 누적 합계
gen4 = itertools.accumulate([x for x in range(1, 101)])
for v in gen4:
    print(v)

# 연결1 : chain
# 앞, 뒤를 연결해서 하나로 뽑아내고 싶을 떄
gen5 = itertools.chain('ABCDE', range(1, 11, 2))
print(list(gen5))

# 연결2 : chain + enumerate
gen6 = itertools.chain(enumerate('ABCDE'))
print(list(gen6))

# 개별
gen7 = itertools.product('ABCDE')
print(list(gen7))

# repeat n : 5x5 의 순서쌍 n 출력
gen8 = itertools.product('ABCDE', repeat=2)
print(list(gen8))

# 그룹화
# 중복되는 문자를 그룹핑해서 출력
gen9 = itertools.groupby('AAAABBCCCCCDDEE')
# print(list(gen9)) # itertools._grouper object 로 되어 있음
for chr, group in gen9:
    print(chr, " : ", list(group))

