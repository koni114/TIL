class Singleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)

        return cls.__instances[cls]


class MyClass(metaclass=Singleton):
    def __init__(self):
        print("This is called by super().__call__")


object1 = MyClass()
object2 = MyClass()

#- 단순 객체의 메소드를 이용하여 구현
import random
class RandomPick:

    def __init__(self):
        self._numbers = [n for n in range(1, 101)]

    def pick(self):
        return sorted([random.choice(self._numbers) for _ in range(10)])

obj = RandomPick()
obj.pick()

#- __call__를 이용하여 클래스 객체를 호출할 수 있도록 overriding
import random
class RandomPick:

    def __init__(self):
        self._numbers = [n for n in range(1, 101)]

    def pick(self):
        return sorted([random.choice(self._numbers) for _ in range(10)])

    def __call__(self):
        return self.pick()

a = RandomPick()
a()                 #- [1, 2, 7, 8, 4, 3..]

#- callable : 객체가 호출가능한지 확인
callable(a)   #- True
callable(obj) #- False