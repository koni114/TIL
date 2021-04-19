import collections

Employee = collections.namedtuple('Person', ['name', 'id'])
employee1 = Employee('Dave', '4011')
print(employee1)
print(type(employee1))

Employee = collections.namedtuple('Person', 'name, id')
employee1 = Employee('Dave', '4011')
print(employee1)
print(type(employee1))

Employee = collections.namedtuple('Employee', ['name', 'id'])
employee1 = Employee('Dave', '4011')
print(employee1)
print(type(employee1))

from typing import NamedTuple
class Employee(NamedTuple):
    name: str
    id: int = 3 #- default 값 선언 가능

employee1 = Employee('Guido', 2)
print(employee1)
print(employee1.name, employee1.id)