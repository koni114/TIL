# 클래스 메소드와 스테틱 메소드(class method and static method)

# chapter03 에서 배운 인스턴스 메소드는 self인 인스턴스를 인자로 받고 인스턴스 변수와 같이 하나의 인스턴스에만 한정된 데이터를 생성, 변경, 참조
# 클래스 메소드는 self 와는 달리 cls 인 클래스를 인자로 받고 모든 인스턴스가 공유하는 클래스 변수와 같은 데이터(클래스)를 생성, 변경, 참조하기위한
# 메소드라고 생각하면 됨

# 아래 예제를 통해 확인해보자
# 아래 함수는 클래스 변수인 raise_amount를 선언하여 연봉 인상율이 있을때, 모든 인스턴스들에 대해서
# 일괄적으로 적용하기 위하여 선언해 둠

class Employee(object):
    raise_amount = 1.1  # 1 연봉 인상율 클래스 변수

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first.lower() + '.' + last.lower() + '@schoolofweb.net'

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

    def full_name(self):
        return '{} {}'.format(self.first, self.last)

    def get_pay(self):
        return '현재 "{}"의 연봉은 "{}"입니다.'.format(self.full_name(), self.pay)


emp_1 = Employee('Sanghee', 'Lee', 50000)
emp_2 = Employee('Minjung', 'Kim', 60000)

# 연봉 인상 전
print(emp_1.get_pay())
print(emp_2.get_pay())

# 연봉 인상
emp_1.apply_raise()
emp_2.apply_raise()

# 연봉 인상 후
print(emp_1.get_pay())
print(emp_2.get_pay())

# 만약 해당 인상률을 변경하고 싶다면 ?
# 1. 클래스 변수 값을 실행한다.
# 2. 클래스 메소드를 선언하고 실행한다.

# 그렇다면 궂이 클래스 변수를 수정해도 되지만, 클래스 메소드를 선언하는 이유는 무엇일까?
# 그 이유는 값을 특정 로직을 통해 검열하거나 제한을 걸 수 있기 때문이다!

# 클래스 메소드를 선언하면 다음과 같다

class Employee(object):
    raise_amount = 1.1  # 연봉 인상율 클래스 변수

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

    def full_name(self):
        return '{} {}'.format(self.first, self.last)

    def get_pay(self):
        return '현재 "{}"의 연봉은 "{}"입니다.'.format(self.full_name(), self.pay)

    @classmethod
    def change_raise_amounts(cls, amount):
        # 인상율이 "1" 보다 작으면 재입력 요청
        while amount < 1:
            print("[경고] 인상율은 '1'보다 작을 수 없습니다. 다시 입력해 주세요")
            amount = input('[입력] 인상율을 다시 입력하여 주십시오.\n=> ')
            amount = float(amount)
        cls.raise_amount = amount
        print("인상율 {} 가 적용 되었습니다.".format(amount))


# 메소드 데코레이터(@)를 이용하여 클래스 메소드를 정의했다.
# 무결성 검사(인상율은 1보다 작을 수 없음)를 실시 한 후
# 데이터가 1보다 큰 경우에만 클래스 변수를 변경
# 클래스 메소드는 인스턴스 생성자와 같은 용도로 사용하는 경우도 있음

# 다음 예제를 살펴보자

class Person(object):
    def __init__(self, year, month, day, sex):
        self.year = year
        self.month = month
        self.day = day
        self.sex = sex

    def __str__(self):
        return '{}년 {}월 {}일생 {}입니다.'.format(self.year, self.month, self.day, self.sex)


person_1 = Person(1990, 8, 29, '남성')
print(person_1)

# 생년월일과 성별 데이터를 가진 클래스를 사용해 봤다.
# 하지만 항상 "년, 월, 일, 성별"을 인자로 받는 것이 아니라 경우에 따라서는
# 주민등록번호를 인자로 받아 인스턴스를 생성해야 하는 경우가 있다고 하자.
# 그럴 경우에는 어떻게 해야할까?

# 외부 메소드로 선언해서  해당 메소드로 주민등록번호를 분석 결과를
# 다시 해당 클래스로 넣을 수 있다

# 그러나 좀더 세련된 코드를 만들고 싶다면, 클래스 메소드를 이용해
# 선언하면 된다!. 하단 예제와 같다

# -*- coding: utf-8 -*-
class Person(object):
    def __init__(self, year, month, day, sex):
        self.year = year
        self.month = month
        self.day = day
        self.sex = sex

    def __str__(self):
        return '{}년 {}월 {}일생 {}입니다.'.format(self.year, self.month, self.day, self.sex)

    @classmethod
    def ssn_constructor(cls, ssn):
        front, back = ssn.split('-')
        sex = back[0]

        if sex == '1' or sex == '2':
            year = '19' + front[:2]
        else:
            year = '20' + front[:2]

        if (int(sex) % 2) == 0:
            sex = '여성'
        else:
            sex = '남성'

        month = front[2:4]
        day = front[4:6]

        return cls(year, month, day, sex) # cls로 둘러야 함을 잊지 말자!


ssn_1 = '900829-1034356'
ssn_2 = '051224-4061569'

person_1 = Person.ssn_constructor(ssn_1)
print(person_1)

person_2 = Person.ssn_constructor(ssn_2)
print(person_2)

# 스테틱 메소드(static method)
# 인스턴스 메소드의 self, 클래스 메소드의 cls 처럼 인자를 따로 받지 않음
# 단순히 클래스 안에 정의되어 있을 뿐, 일반 함수와 전혀 다를게 없음

class Person(object):
    my_class_var = 'sanghee'

    def __init__(self, year, month, day, sex):
        self.year = year
        self.month = month
        self.day = day
        self.sex = sex

    def __str__(self):
        return '{}년 {}월 {}일생 {}입니다.'.format(self.year, self.month, self.day, self.sex)

    @classmethod
    def ssn_constructor(cls, ssn):
        front, back = ssn.split('-')
        sex = back[0]

        if sex == '1' or sex == '2':
            year = '19' + front[:2]
        else:
            year = '20' + front[:2]

        if (int(sex) % 2) == 0:
            sex = '여성'
        else:
            sex = '남성'

        month = front[2:4]
        day = front[4:6]

        return cls(year, month, day, sex)

    @staticmethod
    def is_work_day(day):
        # weekday() 함수의 리턴값은
        # 월: 0, 화: 1, 수: 2, 목: 3, 금: 4, 토: 5, 일: 6
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True


ssn_1 = '900829-1034356'
ssn_2 = '051224-4061569'

person_1 = Person.ssn_constructor(ssn_1)
print(person_1)

person_2 = Person.ssn_constructor(ssn_2)
print(person_2)

import datetime

# 일요일 날짜 오브젝트 생성
my_date = datetime.date(2016, 10, 9)

# 클래스를 통하여 스태틱 메소드 호출
print(Person.is_work_day(my_date))
# 인스턴스를 통하여 스태틱 메소드 호출
print(person_1.is_work_day(my_date))