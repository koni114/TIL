# 클래스 변수(Class variable)
# 인스턴스 변수가 각각의 인스턴스마다 가지고 있는 고유한 데이터라고 한다면
# 클래스 변수는 한 단체의 단체명과 같이 클래스로 만들어진 모든 인스턴스가 공유하는 데이터

# 예제를 보면서 이해해보자.
# 어떤 회사가 직원들의 연봉을 매회 1회 인상해 주는데, 특이하게도 전직원 연봉을 동일하게 인상해 준다
# 올해는 회사 매출이 높아 10% 인상률을 가질때, 공통 인상률이 클래스 변수로 만들어질 수 있다.

class Employee(object):

    raise_amount = 1.1

    def __init__(self, first, last, pay):
        self.first = first
        self.last  = last
        self.pay   = pay
        self.email = first.lower() + '.' + last.lower() + '@jaeBig.com'

    def full_name(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        # raise_amount는 클래스 변수의 클래스 네임스페이스에 저장되어 있으니
        # 클래스를 통해서 엑세스 해야함

        # but!! self라는 인스턴스를 이용해서도 호출 가능 -> 클래스 변수인데 어떻게????
        # 하단 참조!
        self.pay = int(self.pay * Employee.raise_amount)


emp_1 = Employee('jaehun', 'Huh', 50000)
emp_2 = Employee('heesung', 'Yu', 50000)

print(emp_1.pay)
emp_1.apply_raise()
print(emp_1.pay)

## ** self.raise_amount 를 통해서도 접근이 가능한 이유,
#  파이썬은 네임스페이스라는 것을 가지고 있음.
#  이 네임스페이스는 오브젝트의 이름들을 나눠서 관리하는데 이름을 찾을때
#  네임스페이스 -> 클래스네임스페이스 -> 수퍼네임스페이스의 순서로 찾아감
#  알아야 할 것은 반대로 찾아가지는 않는 다는 것. 예를 들어 자식 객체에서 부모 객체로는 찾아가지만
#  부모 객체에서 자식 객체로는 찾아가지 않는 개념과 같음
#  즉 self.raise_amount 라고 사용하면 인스턴스 네임스페이스에서 해당 변수를 찾고 없으면
#  클래스 네임스페이스를 찾음

# __dict__ : 클래스와 인스턴스의 네임스페이스안을 살펴볼 수 있음
# dict 메소드를 이용하여 내부를 살펴보면,
# emp_1 이라는 인스턴스의 네임스페이스에는 raise_amount 변수가 없지만
# Employee 클래스의 네임스페이스에는 존재함을 확인할 수 있다

print(emp_1.__dict__)
print(Employee.__dict__)

# 아래 예제를 통해 한번더 확인해 보자
class superClass(object):
    super_var = '수퍼 네임스페이스에 있는 변수 입니다.'

class myClass(superClass):
    class_var = '클래스 네임스페이스에 있는 변수 입니다.'

    def __init__(self):
        self.instance_var = '인스턴스 네임스페이스에 있는 변수입니다.'

my_instance = myClass()

# 엑세스 가능한 경우,
print(my_instance.instance_var)
print(my_instance.class_var)
print(my_instance.super_var)
print(myClass.class_var)
print(myClass.super_var)
print(superClass.super_var)
print('-'*30)

# ** 엑세스 불가능한 경우
# tip : try, except를 이용하면, 오류 발생시 출력 문구를 통해 확인 할 수 있다.
try:
    print(superClass.class_var)
except:
    print("class_var를 찾을수가 없습니다.")


# 그렇다면, 특정 인스턴스에는 20%의 인상률을 올릴 수 있을까?
# -> 일단 해당 클래스의 인스턴스 변수로 raise_amount 변수를 추가하자
# -> 해당 인스턴스의 raise_amount = 1.2 로 변경하면 된다.

class Employee(object):

    raise_amount = 1.1

    def __init__(self, first, last, pay):
        self.first = first
        self.last  = last
        self.pay   = pay
        self.email = first.lower() + '.' + last.lower() + '@jaeBig.com'


    def full_name(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount) # Employee -> self로 변경!


emp_1 = Employee('jaehun', 'Huh', 50000)
emp_2 = Employee('heesung', 'Yu', 50000)

print("emp_1 연봉 20% 인상")
emp_1.raise_amount = 1.2
print(emp_1.pay)
emp_1.apply_raise()
print(emp_1.pay)

print("emp_2 연봉 10% 인상")
print(emp_2.pay)
emp_2.apply_raise()
print(emp_2.pay)

## 다른 예를 들어 한번더 살펴보자.
#  회사의 직원 수를 관리해야 한다고 생각해보자. 이런 경우에는 각각의 직원이
#  이 데이터를 가지고 있을 필요는 없고 한곳에서(클래스 변수) 데이터를 저장하고 참조하는 것이 좋다

class Employee(object):
    raise_amount = 1.1
    num_of_emps = 0  # 1 클래스 변수 정의

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first.lower() + '.' + last.lower() + '@schoolofweb.net'

        Employee.num_of_emps += 1  # 2 인스턴스가 생성될 때마다 1씩 증가

    def __del__(self):
        Employee.num_of_emps -= 1  # 3 인스턴스가 제거될 때마다 1씩 감소

    def full_name(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)  # 1 인스턴스 변수부터 참조를 합니다.


print(Employee.num_of_emps) # 처음 직원 수
emp_1 = Employee('Sanghee', 'Lee', 50000)  # 직원 1명 입사
emp_2 = Employee('Minjung', 'Kim', 60000)  # 직원 1명 입사
print(Employee.num_of_emps) # 직원 수 확인

del emp_1  # 직원 1명 퇴사
del emp_2  # 직원 1명 퇴사
print(Employee.num_of_emps) # 직원 수 확인



