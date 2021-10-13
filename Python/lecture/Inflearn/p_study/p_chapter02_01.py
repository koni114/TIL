"""
클래스 기반 개발 설명
- 절차 지향 vs 객체 지향
- 객체 지향 프로그래밍 장점
- 클래스 기반 코딩 실습
"""
# chapter02_01
# 객체 지향 프로그래밍(oop) -> 코드의 재사용, 코드 중복 방지, 유지보수가 쉬움
# 규모가 큰 프로젝트(프로그램) -> 함수 중심 -> 데이터가 방대 -> 복잡
# 클래스 중심 -> 데이터가 중심에 있고, 함수의 파라미터가 감소하게 되며 객체로 관리
# 만들고자 하는 프로그래밍의 규모와 근거에 의해서 맞게 코딩하면 됨

"""
다음의 정보를 알고있는지 확인해보세요
1. __str__ vs __repr__의 차이
2. __dict__ 함수란? 
3. 상위 함수인 __str__ 함수가 아닌 __repr__를 호출하려면 어떻게 해야하는지?
4. dir 함수의 쓰임새
"""


# 일반적인 코딩
# 차량1
car_company_1 = 'Ferrari'
car_detail_1 = [
    {'color': 'White'},
    {'horsepower': 400},
    {'price': 8000}
]

# 차량2
car_company_2 = 'Bmw'
car_detail_2 = [
    {'color': 'Black'},
    {'horsepower': 270},
    {'price': 5000}
]

# 각 차량들을 리스트로 선언
# 관리하기가 불편. 인덱스 접근 시 실수 가능성, 삭제가 불편함
car_company = ['Ferrari', 'Bmw']
car_detail = [
              [
                {'color': 'White'},
                {'horsepower': 400},
                {'price': 8000}
              ],
              [
                  {'color': 'Black'},
                  {'horsepower': 270},
                  {'price': 5000}
              ]
            ]


class Car:
    def __init__(self, company, details):
        self.company = company
        self.details = details

    def __str__(self):
        return 'str : {} - {}'.format(self.company, self.details)

    def __repr__(self):
        return 'repr : {} - {}'.format(self.company, self.details)


"""
class 를 print 로 출력하고 싶을 때, special method(magic method)를 활용하면,
여러가지 기능을 추가 할 수 있음.
** __str__ 함수를 선언하면, print 시 필요한 값을 출력할 수 있음
** __repr__ 함수도 str 과 비슷한데, 차이점은
- __str__ 은 reference 에서는 비공식적인, print 로 문자열을 출력하여 사용자 입장에서 표현하고 싶을 때, 
- __repr__ 은 엔지니어 레벨에서 객체의 엄격한 타입을 구체적으로 표현하고 싶은 경우 사용
- __str__ 과 __repr__ 동시에 존재할 때, __str__로 사용됨.(상위..)
- 쉽게 사용자 레벨  vs 개발자 레벨로 구분됨을 기억하자
"""

car_1 = Car('Ferrari', {'color': 'White', 'horsepower': 400, 'price': 8000})
car_2 = Car('Bmw',  {'color': 'Black', 'horsepower': 270, 'price': 5000})
print(car_1)
print(car_2)


"""
__dict__: 클래스 내에 attribute 정보를 확인할 수 있음.
dir 함수를 사용하면, 클래스 내에서 사용가능한 메타 정보 확인 가능
"""
print(car_1.__dict__)
print(dir(car_1))

# 리스트 선언 후, 리스트에 class 객체들을 담아 사용하는 경우는 __repr__ 함수가 호출되므로,
# 결과적으로 __str__, __repr__ 함수를 동시에 선언해서 사용하는 것이 좋음

car_list = [car_1, car_2]
print(car_list)

# 반복문에서는 __str__가 호출되고,
# __repr__를 호출하고 싶다면, repr 함수를 사용
for car in car_list:
    print(repr(car))

