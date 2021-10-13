"""
chapter02-03
-

"""


class Car:
    """
    Car class
    Author : Jaebig
    Date : 2021.10.12
    Description : Class, Static, Instance method
    """
    # 클래스 변수(모든 인스턴스가 공유)
    # 클래스 내에 공통적으로 참조하는 변수
    price_per_raise = 1.0

    def __init__(self, company, details):
        self.company = company
        self.details = details
        self.car_count = 10

    def __str__(self):
        return 'str : {} - {}'.format(self.company, self.details)

    def __repr__(self):
        return 'repr : {} - {}'.format(self.company, self.details)

    # Instance Method
    # self: 객체의 고유한 속성 값을 사용
    def detail_info(self):
        print('Current ID : {}'.format(id(self)))
        print('Car Detail Info : {} {}'.format(self.company, self.details.get('price')))

    # Instance Method
    def get_price(self):
        return f'Before Car Price -> company {self.company}, price : {self.details.get("price")}'

    def get_price_calc(self):
        return f'After Car Price -> company {self.company}, price : {self.details.get("price") * Car.price_per_raise}'

    # Class Method
    # cls --> Car 라고 생각하면 됨
    @classmethod
    def raise_price(cls, per):
        if per <= 1.0:
            print('Plz Enter 1 Or more')
            return
        cls.price_per_raise = per
        print(f'Succeed! price increased : {per}')

    # static method : 특별한 파라미터를 받지 않음
    @staticmethod
    def is_bmw(inst):
        if inst.company == 'Bmw':
            return 'OK! This car is {}'.format(inst.company)
        return 'Sorry, this car is not Bmw'


car_1 = Car('Ferrari', {'color': 'White', 'horsepower': 400, 'price': 8000})
car_2 = Car('Bmw',  {'color': 'Black', 'horsepower': 270, 'price': 5000})

# 전체 정보
car_1.detail_info()
car_2.detail_info()

# 가격정보(직접 접근)
print(car_1.details.get('price')) # 일반적으로 이렇게 접근하는 것은 좋지 않음
print(car_2.details.get('price'))

# 가격정보(인상 전)
print(car_1.get_price())
print(car_2.get_price())

# 가격정보(인상 후)
Car.price_per_raise = 1.4
print(car_1.get_price_calc())
print(car_2.get_price_calc())

# 위의 Car.price_per_raise 에 직접 접근하는 것은 좋지 않음
# 클래스 메소드를 사용하여 price_per_raise 에 값을 할당

Car.raise_price(1)
Car.raise_price(1.6)

# Static Method
# 클래스 밖으로 빼기는 애매하며, 클래스 내에 공통적으로 함수를 사용하는 경우 Static Method 사용 가능
# Static Method 를 궂이 사용해야 하는지는 논란의 여지가 많음

# 인스턴스로 호출
print(car_1.is_bmw(car_1))
print(car_2.is_bmw(car_2))

# 클래스로 호출
print(Car.is_bmw(car_1))
print(Car.is_bmw(car_2))