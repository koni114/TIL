import itertools
gen1 = itertools.count(1, 2.5)
for a in gen1:
    print(a)

import itertools
gen2 = itertools.takewhile(lambda x: x < 5, [1, 2, 3, 4, 5, 6])
print(list(gen2))

gen3 = itertools.filterfalse(lambda x: x < 5, list(range(10)))
list(gen3)

gen4 = itertools.accumulate([x for x in range(1, 101)])
list(gen4)

gen7 = itertools.product('ABCDE', repeat=2)
print(list(gen7))

gen9 = itertools.groupby('AAAABBCCCCDDEEEE')
for chr, group in gen9:
    print(chr, " : ", list(group))
