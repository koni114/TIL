# p_chapter02_02.py
"""
클래스 상세 설명
- 클래스 변수 vs 인스턴스 변수
- 클래스 메소드 실습
- 네임스페이스의 이해
"""


class Car:
    """
    Car class
    Author : Jaebig
    Date : 2021.10.12
    """
    # 클래스 변수(모든 인스턴스가 공유)
    # 클래스 내에 공통적으로 참조하는 변수
    car_count = 0

    def __init__(self, company, details):
        self.company = company
        self.details = details
        self.car_count = 10
        Car.car_count += 1

    def __str__(self):
        return 'str : {} - {}'.format(self.company, self.details)

    def __repr__(self):
        return 'repr : {} - {}'.format(self.company, self.details)

    def __del__(self):
        Car.car_count -= 1

    def detail_info(self):
        print('Current ID : {}'.format(id(self)))
        print('Car Detail Info : {} {}'.format(self.company, self.details.get('price')))


car_1 = Car('Ferrari', {'color': 'White', 'horsepower': 400, 'price': 8000})
car_2 = Car('Bmw',  {'color': 'Black', 'horsepower': 270, 'price': 5000})

"""
self 의 의미
- 첫 번째 인자로 반드시 넘어오게 됨. 
- 특정 클래스를 기반으로 생성된 인스턴스의 내부 고유 객체를 의미
"""

# ID 확인
print(id(car_1))
print(id(car_2))

print(car_1.company == car_2.company)
print(car_2 is car_2)

# dir & __dict__ 확인
# 모든 클래스는 object 를 상속받기 때문에 meta 정보를 확인 가능하며, 마지막에 company, details 확인 가능
print(dir(car_1))
print(dir(car_2))

# 내 namespace 만, 값까지 확인하고 싶을 때, __dict__ 매직 메서드 사용해서 확인
print(car_1.__dict__)
print(car_2.__dict__)

# Docstring
# 해당 class 의 documentation 정보를 확인
# 필수적인 것은 아니나, 개발에 대한 노하우가 늘어나는 것 중에 하나
print(car_1.__doc__)
print(car_2.__doc__)

# 클래스 메소드 실행
# 위에서 id 함수를 실행하여 확인한 car_1 의 값과 detail_info 함수를 통해 확인한 id 값이 같음을 확인할 수 있음
car_1.detail_info()
car_2.detail_info()

print(car_1.__class__)
print(car_2.__class__)
print(car_1.__class__ == car_2.__class__)
print(id(car_1.__class__) == id(car_2.__class__)) # ** True

# 당연히 에러가 발생함 -> self 인자를 넘기지 않았기 때문
Car.detail_info() # error

# 다음과 같이 사용 가능!
car_1.detail_info()
Car.detail_info(car_1)

car_2.detail_info()
Car.detail_info(car_2)

# 클래스 변수는 __dict__ 메소드 내에서는 보이지 않음
# why? __dict__ 변수는 namespace(인스턴스) 공간 내의 값들을 출력하기 때문
print(car_1.__dict__)
print(car_1.car_count)
print(Car.car_count)
print(dir(car_1))

# dir 은 class 변수까지 다나옴
# 즉 인스턴스 변수는 앞에 '_'를 붙이는 것이 PEP 가이드임을 기억하자

del car_2
# 삭제 확인
print(car_1.car_count)
print(Car.car_count)

# 인스턴스 네임스페이스에 없으면 상위에서 검색
# 즉, 동일한 이름으로 변수 생성 가능(인스턴스 검색 후, 없으면 상위(클래스 변수)를 찾음)
