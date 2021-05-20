#- waste_memory.py
import os


class MyObject:
    def __init__(self):
        self.data = os.urandom(100)


def get_data():
    values = []
    for _ in range(100):
        obj = MyObject()
        values.append(obj)
    return values


def run():
    deep_value = []
    for _ in range(100):
        deep_value.append(get_data())
    return deep_value