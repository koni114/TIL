#- intertools practice
import itertools

it = itertools.chain([1,2,3], [4,5,6])
print(list(it))
# --> [1, 2, 3, 4, 5, 6]

it = itertools.repeat('Hi', 3)
print(list(it))
#- ['Hi', 'Hi', 'Hi']

it =itertools.cycle([1, 2])
result = [next(it) for _ in range(10)]
print(result)
#-[1, 2, 1, 2, 1, 2, 1, 2, 1, 2]

it1, it2, it3 = itertools.tee(['하나', '둘'], 3)
print(list(it1))
print(list(it2))
print(list(it3))

#- ['하나', '둘']
#- ['하나', '둘']
#- ['하나', '둘']

keys = ['하나', '둘', '셋']
values = [1, 2]
normal = list(zip(keys, values))
print(f'zip: {normal}')
#- zip: [('하나', 1), ('둘', 2)]

it = itertools.zip_longest(keys, values, fillvalue=None)
longest = list(it)
print(f"zip longest: {longest}")
#- zip longest: [('하나', 1), ('둘', 2), ('셋', None)]

values = [i for i in range(1, 10)]
first_value = itertools.islice(values, 5)
print(list(first_value))
#- [1, 2, 3, 4, 5]

middle_odds = itertools.islice(values, 2, 8, 2)
print(list(middle_odds))
#- [3, 5, 7]

values = list(range(1, 10))
less_than_seven = lambda x: x < 7
it = itertools.takewhile(less_than_seven, values)
print(list(it))
#- [1, 2, 3, 4, 5, 6]

import random
value = [random.randint(1, 10) for _ in range(10)]
less_than_seven = lambda x: x < 7
it = itertools.takewhile(less_than_seven, value)
print(list(it))
#- value : [1, 10, 10, 2, 9, 1, 6, 1, 8, 7]
#- [1]

it = itertools.dropwhile(less_than_seven, value)
print(list(it))
#- value: [1, 10, 10, 2, 9, 1, 6, 1, 8, 7]
#- [10, 10, 2, 9, 1, 6, 1, 8, 7]


#- filterfalse
#- filter 내장 함수의 반대 --> false 에 해당하는 모든 원소를 돌려줌
value = [random.randint(1, 10) for _ in range(10)]
evens = lambda x: x % 2 == 0
filter_result = filter(evens, values)
print('Filter: ', list(filter_result))

filter_false_result = itertools.filterfalse(evens, values)
print("Filter false: ", list(filter_false_result))

values = list(range(10))
sum_reduce = itertools.accumulate(values)
print("합계 : ", list(sum_reduce))

def sum_module_20(first, second):
    output = first + second
    return output % 20

module_reduce = itertools.accumulate(values, sum_module_20)
print('20으로 나눈 나머지의 합계:', list(module_reduce))

#- product
#- 하나 이상의 이터레이터에 들어 있는 데카르트 곱을 반환

it = itertools.permutations([1, 2, 3, 4], 2)
print(list(it))

it = itertools.combinations([1, 2, 3, 4], 2)
print(list(it))

it = itertools.combinations_with_replacement([1, 2, 3, 4], 2)
print(list(it))