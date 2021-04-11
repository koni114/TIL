print("chapter5 - 파이썬에 날개 달기")
'''
파이썬 프로그래밍의 핵심 - 클래스
** 클래스가 필요한 이유? 
- 똑같은 일을 반복할 때(ex) 계산기를 5개, 10개 만들 때), 인스턴스만 생성하면 되기 떄문에 클래스는 유용

*** 객체와 인스턴스의 차이
navi = Cat() 에서, 일반적으로 navi 는 객체, Cat()은 인스턴스라고 이야기 한다.
즉, navi라는 객체는 Cat의 인스턴스이다! 라고 이야기하는 것이 일반적이다

'''

'''
** 클래스 특징
1. 클래스 함수 첫번째 인자로 반드시 self 를 넣어주어야 한다
  -- self의 특징
  생성자 변수와 같은 역할을 함: 초기에 입력된 변수를 객체에 저장하는 역할.
2. __init__
  인스턴스를 실행될 때마다 항상 실행되는 함수
  생성자 함수와 비슷하다고 생각하면 됨
3. 클래스의 구조
  class 클래스 이름(상속 클래스 명):
  < 클래스 변수 1 >
  < 클래스 변수 2 >
  
  def 클래스 함수(self, 변수1, 변수2..):
  <수행 문장 1>..  

'''

class sum:
    def setData(self, first, second):
        self.first = first
        self.second = second

    def sum(self):
        return (self.first + self.second)

    def mul(self):
        return (self.first * self.second)

    def sub(self):
        return (self.first - self.second)

    def div(self):
        return (self.first / self.second)

import math

a = sum()
a.setData(1,2)
a.sum()
a.sub()
a.div()
a.mul()

a = - 4/11 * math.log((4/11), 2)
b = - 7/11 * math.log((7/11), 2)
a + b


