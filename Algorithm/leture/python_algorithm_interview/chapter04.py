import copy

a = 10
b = a
print(a, b)

a = 11
print(a, b)

a = [1, 2, 3, 4, 5]
b = a
print(b)
a[2] = 4
print(a)
print(b)


a = [1, 2, 3]
a == a
a == list(a)
a is a
a is list(a)

import copy
a == copy.deepcopy(a)
a is copy.deepcopy(a)