# 매직 메소드(magic method)
# 클래스안에 정의할 수 있는 스페셜 메소드. 클래스를 int, str, list 등의
# 파이썬의 빌트인 타입(built-in type)과 같은 작동을 하게 해줌

# +, -, >, < 등의 오퍼레이터에 대해서 각각의 데이터 타입에 맞는 메소드로 오버로딩하여
# 백그라운드에서 연산을 함
# __init__, __str__ 과 같이 메소드 이름 앞뒤에 더블 인더스코어("__")를 붙인다

# 클래스를 만들때 항상 사용하는 __init__ 이나 __str__ 는 가장 대표적인 매직 메소드
# 해당 함수를 부르는 가장 좋은 호칭은 "던더 init 던더" 이다

# 우리가 평소에 사용하는 +, - 또한 매직 메소드임
# x + y를 실행하면 x가 가지고 있는 매직 메소드인 "__add__"가 실행
# 결국 백그라운드에서는 "x.__add__(y)"가 실행 : 예제를 통해 확인해보자!

# 1. 먼저 int 타입을 베이스로하는 커스텀 클래스 만들어보자


class MyInt(int):
    pass

# 인스턴스 생성
my_num = MyInt(5)

# 타입 확인
print(type(my_num))

# int의 인스턴스인지 확인
print(isinstance(my_num,int))

# MyInt의 베이스 클래스 확인
print(MyInt.__bases__)

# 덧샘 실행
print(my_num + 5)

# 5 + 5를 실행한 것과 똑같은 결과를 출력
# my_num 이 정말 매직 메소드를 가지고 있는지 확인해보자

print(dir(my_num))

# 2. 매직 메소드를 직접 호출해보자
print(my_num.__add__(5))

# 3. 매직 메소드를 수정하여 리턴 값을 정수가 아닌 문자열로 해보자
class MyInt(int):
    def __add__(self, other):
        return '{} 더하기 {}는 {} 입니다'.format(self.real, other.real, self.real + other.real)

my_num = MyInt(5)
print(my_num + 5)

# 이런 매직 메소드를 알아야 하는 이유는 무엇일까?
# -> 우리가 만드는 클래스에 매직 메소드를 적용해서 사용하기 위함
# 활용도가 큰 예제 하나를 보자

class Food(object):
    def __init__(self, name, price):
        self.name = name
        self.price = price

food_1 = Food('아이스크림', 3000)
print(food_1)

# 출력해 보았더니, 주소값이 리턴된다.
# 4. 좀 더 사용자에게 유용한 값을 return해 주기 위해 __str__ 를 사용해보자!

class Food(object):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return "아이템 : {}, 가격 : {}".format(self.name, self.price)

food_1 = Food('아이스크림', 3000)
print(food_1)

# print 내부에 class 를 넣어 출력했을때 아까와는 다르게, 아이템과 가격이 출력됨을 확인 할 수 있다.

# 5. 이번에는 <, > 를 오버라이딩 해서 해당 클래스의 가격을 비교하도록 만들어보자
# __lt__ 매직 메소드를 수정하여 가격이 비교되도록 만들어보자


class Food(object):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return "아이템 : {}, 가격 : {}".format(self.name, self.price)

    def __lt__(self, other):
        if self.price < other.price:
            return True
        else:
            return False

food_1 = Food('아이스크림', 3000)
food_2 = Food('햄버거', 5000)
food_3 = Food('콜라', 2000)

print(food_1 < food_2)
print(food_2 < food_3)

# 이처럼 매직 메소드 오버라이딩을 통한 응용이 가능하다!

# 여러가지 매직 메소드 예를 보고, 자신이 만든 클래스에는 어떤 매직 메소드를
# 편리하게 사용할 수 있을지 고민해보자!

# +	        object.__add__(self, other)
# -	        object.__sub__(self, other)
# *	        object.__mul__(self, other)
# //	    object.__floordiv__(self, other)
# /	        object.__div__(self, other)
# %	        object.__mod__(self, other)
# **	    object.__pow__(self, other[, modulo])
# >>	    object.__lshift__(self, other)
# <<    	object.__rshift__(self, other)
# &	        object.__and__(self, other)
# ^	        object.__xor__(self, other)
# |	        object.__or__(self, other)

# +=	    object.__iadd__(self, other)
# -=	    object.__isub__(self, other)
# *=	    object.__imul__(self, other)
# /=	    object.__idiv__(self, other)
# //=	    object.__ifloordiv__(self, other)
# %=	    object.__imod__(self, other)
# **=	    object.__ipow__(self, other[, modulo])
# <<=	    object.__ilshift__(self, other)
# >>=	    object.__irshift__(self, other)
# &=	    object.__iand__(self, other)
# ^=	    object.__ixor__(self, other)
# |=	    object.__ior__(self, other)

#  -	    object.__neg__(self)
# +	        object.__pos__(self)
# abs()	    object.__abs__(self)
# ~	        object.__invert__(self)
# complex()	object.__complex__(self)
# int()	    object.__int__(self)
# long()	object.__long__(self)
# float()	object.__float__(self)
# oct()	    object.__oct__(self)
# hex()	    object.__hex__(self)

# <	        object.__lt__(self, other)
# <=	    object.__le__(self, other)
# ==	    object.__eq__(self, other)
# !=	    object.__ne__(self, other)
# >=	    object.__ge__(self, other)
# >	        object.__gt__(self, other)