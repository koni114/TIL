# 클래스와 인스턴스
'''
 파이썬의 모든 것은 오브젝트
 오브젝트는, 여러가지 데이터와 함수를 담은 하나의 데이터 구조를 칭함
 파이썬에서 이 오브젝트들은 퍼스트 클래스 오브젝트
 (first-class : 인자로써 전달할 수 있고, return 받을 수 있는 형태)

'''

# 논리적인 데이터 집합인 오브젝트를 만들어 필요한 데이터 access 하는 방법
# 1. 사전을 사용하는 경우,
student = {'name': '이상희', 'year': 2, 'class': 3, 'student_id': 35}
print('{}, {}학년 {}반 {}번'.format(student['name'], student['year'], student['class'], student['student_id']))


# 2. class를 사용하는 경우,
# -*- coding: utf-8 -*-
class Student(object):
    def __init__(self, name, year, class_num, student_id):  # 파이썬 키워드인 class는 인수 이름으로 사용하지 못 합니다.
        self.name = name
        self.year = year
        self.class_num = class_num
        self.student_id = student_id

    def introduce_myself(self):
        return '{}, {}학년 {}반 {}번'.format(self.name, self.year, self.class_num, self.student_id)


student = Student('이상희', 2, 3, 35)
print(student.introduce_myself())

# 3. 모듈을 사용하는 경우,
# 해당 문구를 student.py에 저장
name = '이상희'
year = 2
class_id = 3
student_id = 35

# 아래 문구 실행'
# import student : 이상하게 에러남
print('{}, {}학년 {}반 {}번'.format(student.name, student.year, student.class_id, student.student_id))

# dir() : 파이썬 표준 내장 함수
# 함수의 인자가 없을 경우에는, 모듈 레벨의 지역변수를, 인자가 있을 경우에는 인자의 모든 속성과 메소드를 보여줌
# 함수는 디버깅할 때 아주 많이 쓰이는 중요한 함수
# 파이썬의 모든 데이터는 인스턴스이다

text = "string"
dir(text)

# text 는 str 타입이 만들어낸 문자열 변수이므로,
# str에 포함된 속성과 메소드를 전부 출력해냄


print(text.__class__) # text의 class 확인
print(isinstance(text, str)) # text의 인스턴스 확인
print(text.upper()) # 메소드 호출

# 함수나 모듈도 오브젝트인지 확인해보자
def my_Function():
    print("my Function에 대한 내용입니다.")
    pass

# ** 속성도 임의로 추가할 수 있음을 알자
print(dir(my_Function)) # my_Functon의 속성 확인
print(my_Function.__doc__) # my_Function의 docstring 출력
my_Function.new_variable = '새로운 변수입니다.' # my function에 새로운 속성 추가
print(dir(my_Function), '\n')
print(my_Function.new_variable)  # 추가한 속성값 출력

# 클래스를 이용하여 새로운 데이터타입을 만들고 그 데이터타입의 인스턴스 만들어보기
class Employee(object):
    pass

emp_1 = Employee()
emp_2 = Employee()

# emp_1 과 emp_2는 다른 메모리 주소 값을 가진 별개의 오브젝트
print(id(emp_1))
print(id(emp_2))

# emp_1 과 emp_2는 같은 클래스의 인스턴스인 것을 확인
class_of_emp_1 = emp_1.__class__
class_of_emp_2 = emp_2.__class__

print(id(class_of_emp_1))
print(id(class_of_emp_2))

# emp_1, emp_2 인스턴스에 변수 추가하여 데이터 저장
emp_1.first = 'Jaehun'
emp_1.last = 'Huh'
emp_1.email = 'koni114@naver.com'
emp_1.pay   = 50000

emp_2.first = 'MinHyung'
emp_2.last  = 'Kim'
emp_2.email = 'minHyung@naver.com'
emp_2.pay   = 50000

print(emp_1.email)
print(emp_2.email)

# 위와 같은 코드는 잘못된 코드.
# 문법상의 오류는 없지만 class는 init 을 통해 변수를 할당받는다.
# ** __init__ : 이니셜라이져라고도 부름
# 인스턴스가 자동 생성될 때 자동 호출하며, 호출되는 순간
# 자동으로 인스턴스 오브젝트를 self 라는 인자로 받음

class Employee(object):
    def __init__(self, first, last, pay):
        self.first = first
        self.last  = last
        self.pay   = pay

    # 이러한 함수를 생성해 쉽게 full Name을 생성 할 수 있음
    # self를 빼먹지 말자. 빼먹었을 때
    # error 문구 : full_name() takes no arguments ( 1 given)
    # -> 아무 인자를 던진 적이 없는데, 1개가 주어졌다고 할까?
    #    이유는 self라는 인자가 자동으로 할당되기 때문이다. 하지만 받질 않았으므로, error가 발생한 것이다
    def full_name(self):
        return '{} {}'.format(self.first, self.last)

emp_1 = Employee('jaehun', 'Huh', 100000)
emp_2 = Employee('heesung', 'Yu', 100000)

print(emp_1.full_name())

# 다음을 보자.
# 클래스를 통해서 메소드를 실행시켰는데, 클래스는 어떤 인스턴스의 메소드를 호춯시켜야 하는지
# 모르기 때문에 대상이 될 인스턴스를 인자로 전달
# 사실 emp_1.full_name()을 실행시키면, -> Employee.full_name(emp_1) 이 호출

print(Employee.full_name(emp_1))

