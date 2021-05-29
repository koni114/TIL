import itertools

# itertools.chain

c = itertools.chain([1,2,3], [4,5,6])
print(list(c))

# itertools.repeat
c = itertools.repeat([1,2,3], 2)
print(list(c))

# itertools.cycle
c = itertools.cycle([1,2])
for _ in range(10):
    print(next(c))

# itertools.tee
it1, it2, it3 = itertools.tee([1,2,3], 3)
print(list(it1))

# itertools.zip_longest
a = [1,2]
b = ['a', 'b', 'c']
list(itertools.zip_longest(a, b, fillvalue='haha'))

# itertools.islice
values = list(range(10))
list(itertools.islice(values, 2, 8, 2))

# itertools.takewhile
less_than_seven = lambda x: x < 7
list(itertools.takewhile(less_than_seven, values))


# itertools.dropwhile
less_than_seven = lambda x: x < 7
list(itertools.dropwhile(less_than_seven, values))

# itertools.filterfalse
list(itertools.filterfalse(less_than_seven, values))

# itertools.accumulate

# itertools.product

# itertools.permutations
list(itertools.permutations([1,2,3,4,5], 2))
# itertools.combinations

# itertools.combinations_with_replacement