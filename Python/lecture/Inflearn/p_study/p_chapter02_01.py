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

car_1 = Car('Ferrari', {'color': 'White', 'horsepower':400, 'price': 8000})

