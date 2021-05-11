## chapter06 메타클래스와 애트리뷰트
- 파이썬의 특성을 열거할 때, 메타클래스를 자주 언급하는데, 실제로 메타클래스가 어떤 목적으로 쓰이는지 이해하는 프로그래머는 거의 없음
- 메타클래스(meta-class)라는 이름은 어렴풋이 이 개념이 클래스를 넘어서는 것임을 암시
- 간단히 말해, 메타클래스를 사용하면 파이썬의 class문을 가로채서 클래스가 정의될 때마다 특별한 동작을 제공할 수 있음
- 메타클래스처럼 신비롭고 강력한 파이썬 기능으로는 동적으로 애트리뷰트 접근을 커스텀화해주는 내장 기능을 들 수 있음
- 파이썬의 객체지향적인 요소와 방금 말한 두 기능이 함께 어우러지면 간단한 클래스를 복잡한 클래스로 쉽게 변환할 수 있음
- 하지만 이런 강력함에는 많은 함점이 뒤따름. 동적인 애트리뷰트로 객체를 오버라이드하면 예기치 못한 부작용이 생길 수 있음
- 메타클래스로 만든 멋진 기능을 초보 파이썬 개발자는 쉽게 이해할 수 없을 것임
- 최소 놀람의 법칙(rule of least surprise)을 잘 따르고 정해진 관용어로만 이런 기능을 사용하는 것이 중요

### 44-세터와 게터 메서드 대신 평범한 애트리뷰트를 사용해라
- 다른 언어를 사용하다가 파이썬을 접한 프로그래머들은 클래스에 게터(getter)나 세터(setter) 메서드를 명시적으로 정의하곤 함. 이런 코드는 파이썬답지 않음
- 특히 필드 값을 증가시키는 연산 등의 경우에는 이런 메서드를 사용하면 코드가 지저분해짐
- 세터와 게터를 사용하기는 쉽지만, 이런 코드는 파이썬답지 않음
~~~Python
class OldResister:
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms

r0 = OldResister(50e3)
print("이전 : ", r0.get_ohms())
r0.set_ohms(10e3)
print("이후 :", r0.get_ohms())

#- 특히 필드 값을 증가시키는 연산 등의 경우에는 코드가 지저분해짐
r0.set_ohms(r0.get_ohms() - 4e3)
assert r0.get_ohms() == 6e3
~~~
- 하지만 이런 유틸리티 메서드를 사용하면 클래스 인터페이스를 설계할 때 도움이 되기도 함. 즉 게터와 세터 같은 유틸리티 메서드를 쓰면 기능을 캡슐화하고, 필드 사용을 검증하고, 경계를 설정하기 쉬워짐
- 클래스가 시간이 지남에 따라 진화하기 때문에 클래스를 설계할 때는 클래스를 호출하는 쪽에 영향을 미치지 않음을 보장하는 것이 중요
- <b>하지만 파이썬에서는 명시적인 세터나 게터 메서드를 구현할 필요가 전혀 없음</b> 대신 다음 코드와 같이 항상 단순한 공개 애트리뷰트로부터 구현을 시작해라
~~~python
class Resister:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


r1 = Resister(50e3)
r1.ohms = 10e3
r1.ohms += 5e3
~~~
- <b>나중에 애트리뷰트가 설정될 때 특별한 기능을 수행해야 한다면, 애트리뷰트를 @property 데코레이터와 대응하는 setter 애트리뷰트로 옮겨갈 수 있음</b>
- 다음 코드는 Register라는 새 하위 클래스를 만듬. Register에서 volltage 프로퍼티에 값을 대입하면 current 값이 바뀜
- 코드가 제대로 작동하려면 세터와 게터의 이름이 우리가 의도한 프로퍼티 이름과 일치해야 함
~~~python
class VoltageResistance(Resister):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms
~~~
- 이제 voltage 프로퍼티에 대입하면 voltage 세터 메서드가 호출되고, 이 메서드는 객체의 current 애트리뷰트를 변경된 전압 값에 맞춰 갱신함
~~~python

class VoltageResistance(Resister):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms

r2 = VoltageResistance(1e3)
print(f"이전 : {r2.current: .2f} 암페어")
r2.voltage = 10
print(f"이후 : {r2.current: .2f} 암페어")

>>>
이전 :  0.00 암페어
이후 :  0.01 암페어
~~~
- 프로퍼티에 대해 setter를 지정하면 타입을 검사하거나 클래스 프로퍼티에 전달된 값에 대한 검증을 수행할 수 있음
- 다음 코드에서는 모든 저항값이 0옴보다 큰지 확인하는 클래스를 정의함
~~~Python
class BoundedResistance(Resister):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError(f"저항 > 0이어야 합니다. 실제 값: {ohms}")
        self._ohms = ohms

r3 = BoundedResistance(1e3)
r3.ohms = 0

>>>
ValueError: 저항 > 0이어야 합니다. 실제 값: 0
~~~
- 생성자에 잘못된 값을 넘겨도 예외가 발생
~~~python
r3 = BoundedResistance(0)

>>>
ValueError: 저항 > 0이어야 합니다. 실제 값: 0
~~~
- 예외가 발생하는 이유는 `BoundedResistance.__init__` 이 `Resister.__init__`을 호출하고 이 초기화 메서드는 다시 self.ohms =  -5라는 대입문을 실행하기 때문
- 이 대입으로 인해 `BoundedResistance`에 있는 `@ohms.setter` 메서드가 호출되고, 이 세터 메서드는 객체 생성이 끝나기 전에 즉시 저항을 검증하는 코드를 실행
- `@property`를 사용해 부모 클래스에 정의된 애트리뷰트를 불변으로 만들 수도 있음
~~~python

class FixedResistance(Resister):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Ohms는 불변 객체입니다.")
        self._ohms = ohms


r4 = FixedResistance(1e3)
r4.ohms = 2e3

>>>
AttributeError: Ohms는 불변 객체입니다.
~~~
- `@property` 메서드를 사용해 세터와 게터를 구현할 때는 게터나 세터 구현이 예기치 않은 동작을 수행하지 않도록 만들어야 함
- 예를 들어 getter 프로퍼티 안에 다른 애트리뷰트를 설정하면 안됨
~~~Python
class MysteriousResistor(Resister):
    @property
    def ohms(self):
        self.voltage = self._ohms * self.current #- getter 프로퍼티 안에 voltage 프로퍼티 설정
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        self._ohms = ohms

r7 = MysteriousResistor(10)
r7.current = 0.01
print(f"이전: {r7.voltage: .2f}")
r7.ohms
print(f"이후: {r7.voltage: .2f}")

>>>
이전:  0.00
이후:  0.10
~~~
- 게터나 세터를 정의할 때 가장 좋은 정책은 관련이 있는 객체 상태를 `@property.setter` 메서드 안에서만 변경하는 것
- 동적으로 모듈을 임포트하거나, 아주 시간이 오래 걸리는 도우미 함수를 호출하거나, I/O를 수행하거나, 비용이 매우 많이 드는 데이터베이스 질의를 수행하는 등 호출하는 쪽에서 예상할 수 없는 부작용을 만들어내면 안됨
- 클래스를 사용하는 쪽에서는 애트리뷰트가 다른 일반적인 파이썬 객체와 마찬가지로 빠르고 사용하기 쉬울 것으로 예상함
- 더 복잡하거나 느린 연산의 경우에는 일반적인 메서드를 사용해라
- `@property`의 가장 큰 단점은 애트리뷰트를 처리하는 메서드가 하위 클래스 사이에서만 공유될 수 있다는 것
- 서로 관련이 없는 클래스 사이에 같은 구현을 공유할 수 없음. 하지만 파이썬은 재사용 가능한 프로퍼티 로직을 구현할 때는 물론 다른 여러 용도에도 사용할 수 있는 디스크립터(descriptor)를 제공함

#### 기억해야 할 내용
- 새로운 클래스 인터페이스를 정의할 때는 간단한 공개 애트리뷰트에서 시작하고, 세터나 게터 메서드를 가급적 사용하지 말라
- 객체에 있는 애트리뷰트에 접근할 때 특별한 동작이 필요하면 `@property`로 구현 가능 
- `@property` 메서드를 만들 때는 이상한 부작용을 만들면 안됨
- `@property` 메서드가 빠르게 실행되도록 유지해라. 느리거나 복잡한 작업의 경우에는 프로퍼티 대신 일반적인 메서드를 사용

### 45-에트리뷰트를 리펙터링하는 대신 @property를 사용해라 
- 내장 @property 데코레이터를 사용하면, 겉으로는 단순한 애트리뷰트처럼 보이지만 실제로는 지능적인 로직을 수행하는 애트리뷰트를 수행할 수 있음
- `@property`의 고급 활용법이자 흔히 사용하는 기법으로는 간단한 수치 애트리뷰트를 그때그때 요청에따라 계산해 제공하도록 바꾸는 것을 들 수 있음
- 이 기법은 기존 클래스를 호출하는 코드를 전혀 바꾸지 않아도 클래스 애트리뷰트의 기존 동작을 변경할 수 있기 때문에 유용함(특히 이 방법은 이 클래스를 호출하는 코드 중에 우리가 제어할 수 없는 부분이 많은 경우 유용)
- @property는 인터페이스를 점차 개선해나가는 과정에서 중간중간 필요한 기능을 제공하는 수단으로 유용
- 예를 들어 일반 파이썬 객체를 사용해 리키 버킷(leaky bucket) 흐름 제어 알고리즘을 구현한다고 하자. 다음 코드의 `Bucket` 클래스는 남은 가용 용량(quota)과 이 가용 용량의 잔존 시간을 표현함
~~~python
from datetime import datetime, timedelta

class Bucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()   #
        self.quota = 0                     #- 가용 용량

    def __repr__(self):
        return f"Bucket(quota= {self.quota})"
~~~
- 리키 버킷 알고리즘은 시간을 일정한 간격으로 구분하고(주기라고 함), 가용 용량을 소비했을 때, 기간(period)가 지났을 경우, 남아있는 가용 용량은 reset됨
~~~python
def fill(bucket, amount):
    #- bucket : bucket class
    #- amount : 가용 용량
    now = datetime.now()
    #- 지나간 시간이 period보다 길면, 가용용량과 시간 reset 시킴
    if now - bucket.reset_time > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount
~~~
- 가용 용량을 소비하는 쪽(ex) 데이터 전송 클래스 등)에서는 어떤 작업을 하고 싶을 때마다 먼저 리키 버킷으로부터 자신의 작업에 필요한 용량을 할당받아야 함
~~~python
#- 필요한 용량 할당 가능 여부 확인
def deduct(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    else:
        bucket.quota -= amount
        return True #- bucket의 가용 용량이 충분하므로, 필요한 분량을 사용함 
~~~
- 이 클래스를 사용하려면 먼저 bucket의 가용 용량을 미리 정해진 할당량만큼 먼저 채워야 함
~~~python
bucket = Bucket(60) #- 60초 period
fill(bucket, 100)
print(bucket)

>>>
Bucket(quota= 100)
~~~
- 그 후 사용할 때마다 필요한 용령을 버킷에서 빼야함
~~~python
bucket = Bucket(60) #- 60초 period
fill(bucket, 100)
print(bucket)

if deduct(bucket, 99):
    print("99 용량 사용")
else:
    print("가용 용량이 작아서 99 용량을 처리할 수 없음")
print(bucket)

>>>
99 용량 사용
Bucket(quota= 1)
~~~
- 어느 순간이 되면, 버킷에 들어있는 가용 용량이 데이터 처리에 필요한 용량보다 작아지면서 더 이상 작업을 진행하지 못하게 됨
- 이런 경우 버킷의 가용 용량 수준은 변하지 않음
~~~python
if deduct(bucket,3):
    print('3 용량 사용')
else:
    print("가용 용량이 작아 3 용량을 사용할 수 없음")
print(bucket)

>>>
가용 용량이 작아 3 용량을 사용할 수 없음
Bucket(quota= 1)
~~~
- 이 구현의 문제점은 버킷이 시작될 떄 가용 용량이 얼마인지 알 수 없다는 점
- 물론 한 주기 안에서는 버킷에 있는 가용 용량이 0이 될 떄까지 계속 감소하지만, 가용 용량이 0이 되면, 버킷에 새로운 가용 용량을 할당하기 전까지 default는 항상 False를 반환
- 이런 일이 발생할 때 `deduct`를 호출하는 쪽에서 자신이 차단된 이유가 Bucket에 할당된 가용 용량을 다 소진했기 때문인지, 이번 주기에 아직 버킷에 매 주기마다 재설정하도록 미리 정해진 가용 용량을 추가받지 못했기 때문인지 알 수 있으면 좋음
- 이러한 문제를 해결하기 위하여 이번 주기에 재설정된 가용 용량인 `max_quota` 와 이번 주기 버킷에서 소비한 용량의 합계인 `quota_consumed`를 추적하도록 클래스를 변경할 수 있음
~~~python
class NewBucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return (f'NewBucket(max_quota={self.max_quota},'
                f'quota_consumed={self.quota_consumed}')   
~~~
- 원래의 Bucket class와 인터페이스를 동일하게 제공하기 위해 `@property` 데코레이터가 붙은 메서드를 사용해 클래스의 두 애트리뷰트(`max_quota`와 `quota_consumed`)에서 현재 가용 용량 수준을 그때그때 계산하게 함 (재설정된 값인 `max_quota`에서 지금까지 사용한 양인 quota_consumed를 빼면 현재 할당 가능한 가용 용량을 알 수 있음)
~~~python
class NewBucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0        #- 주기 갱신에 따른 가용 용량
        self.quota_consumed = 0   #- 이번 주기에 소비된 용량의 합계

    def __repr__(self):
        return (f'NewBucket(max_quota={self.max_quota},'
                f'quota_consumed={self.quota_consumed}')

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # 새로운 주기가 되고 가용 용량을 재설정하는 경우
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            # 새로운 주기가 되고 가용 용량을 추가하는 경우
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            # 어떤 주기 안에서 가용 용량을 소비하는 경우
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta
~~~
- 위의 클래스를 토대로 다음과 같이 실행 가능
~~~python
bucket = NewBucket(60)
print("최초 :", bucket)
fill(bucket, 100)
print("보충 후 :", bucket)

if deduct(bucket, 99):
    print("99 용량 사용")
else:
    print("가용 용량이 작아서 99 용량을 처리할 수 없음")
print("사용 후,", bucket)

if deduct(bucket, 3):
    print("3 용량 사용")
else:
    print("가용 용량이 작아서 3 용량을 처리할 수 없음")

print('여전히', bucket)
~~~
- 가장 좋은 점은 `Bucket.quota`를 사용하는 코드를 변경할 필요가 없고 이 클래스의 구현이 변경됐음을 알 필요도 없다는 것
- Bucket을 사용하는 새로운 방법은 제대로 작동하고, 추가로 `max_quota`와 `quota_consumed`에도 직접 접근 가능
- 객체가 처음부터 제대로 인터페이스를 제공하지 않거나 아무 기능도 없는 데이터 컨테이너 역할만 하는 경우가 실전에서는 자주 발생함
- 시간이 지나면서 코드가 커지거나, 프로그램이 다루는 영역이 넓어지거나, 장기적으로 코드를 깔끔하게 유지할 생각이 없는 프로그래머들이 코드에 기여하는 등의 경우 이런 일이 발생함
- `@property`는 실제 세계에서 마주치는 문제를 해결할 때 도움이 됨. 하지만 @property를 과용하지는 말고 너무 많아지면 클래스를 리펙토링하자

#### 기억해야 할 내용
- @property를 사용해 기존 인스턴스 애트리뷰트에 새로운 기능을 제공할 수 있음
- @property를 사용해 데이터 모델을 점진적으로 개선해라
- @property 메서드를 너무 과하게 쓰고 있다면, 클래스와 클래스를 사용하는 모든 코드를 리펙터링하는 것을 고려해라

### 46-재사용 가능한 @property 메서드를 만들려면 디스크립터를 사용해라
- @property의 가장 큰 문제점은 재사용성
- @property가 데코레이션하는 메서드를 같은 클래스에 속하는 여러 애트리뷰트로 사용할 수는 없음. 그리고 서로 무관한 클래스 사이에서 @property 데코레이터를 적용한 메서드를 재사용할 수도 없음
- 예를 들어 학생의 숙제 점수가 백분율 값인지 검증하고 싶다고 하자
~~~python
class Homework:
    def __init__(self):
        self._grade = 0

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        if not (0 <= value <= 100):
            raise ValueError("점수는 0과 100사이 입니다.")
        self._grade = value
~~~
- @property를 사용하면 이 클래스를 쉽게 사용할 수 있음
~~~python
galileo = Homework()
galileo.grade = 95
~~~
- 이제 이 학생에게 시험 점수를 부여하고 싶다고 하자. 시험 과목은 여러 개고, 각 과목마다 별도의 점수가 부여됨
~~~python
class Exam:
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError('점수는 0과 100사이입니다.')

    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value
~~~
- 이런 식으로 계속 확장하려면, 시험 과목을 이루는 각 부분마다 새로운 @property를 지정하고 관련 검증 메서드를 작성해야 하므로 금방 지겨워짐
- 게다가 이런 접근 방법은 일반적이지도 않음. 숙제나 시험 성적 이외의 부분에 백분율 검증을 활용하고 싶다면 똑같은 @property와 검증 대상 _grade 세터 메서드를 번거롭게 다시 작성해야 함
- <b>이런 경우 파이썬에서 적용할 수 있는 나은 방법은 디스크립터를 사용하는 것</b>
- 디스크립터 프로토콜은 파이썬 언어에서 애트리뷰트 접근을 해석하는 방법을 정의함
- 디스크립터 클래스는 `__get__`과 `__set__`메서드를 제공하고, 이 두 메서드를 사용하면 별다른 준비 코드 없이도 원하는 점수 검증 동작을 재사용할 수 있음
- 이런 경우 같은 로직을 한 클래스 안에 속한 여러 다른 애트리뷰트에 적용할 수 있으므로 디스크립터가 믹스인보다 낫다
- 다음 코드는 Grade의 인스턴스인 클래스 애트리뷰트가 들어 있는 Exam 클래스를 정의함. Grade 클래스는 다음과 같은 디스크립터 프로토콜을 구현함
~~~python
class Grade:
    def __get__(self, instance, instance_type):
        ...

    def __set__(self, instance, value):
        ...

class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()
~~~
- `Grade` 클래스가 작동하는 방식을 설명하기 전에, `Exam` 인스턴스에 있는 이런 디스크립터 애트리뷰트에 대한 접근을 파이썬이 어떻게 처리하는지 이해하는 것이 중요
- 다음과 같은 프로퍼티 대입의 해석을 확인하자
~~~python
exam = Exam()
exam.writing_grade = 40

#- 다음과 같이 해석됨
Exam.__dict__['writing_grade'].__set__(exam, 40)

exam.writing_grade

#- 다음과 같이 해석됨
Exam.__dict__['writing_grade'].__get__(exam, Exam)
~~~
- 이런 동작을 이끌어내는 것은 object의 `__getattribute__` 메서드임
- <b>간단히 말해, Exam 인스턴스에 writing_grade라는 이름의 애트리뷰트가 없으면 파이썬은 Exam 클래스의 애트리뷰트를 대신 사용함. 이 클래스의 애트리뷰트가 `__get__`, `__set__` 메서드가 정의된 객체라면 파이썬은 디스크립터 프로토콜을 따라야 한다고 결정함</b>
- 이 동작과 Homework 클래스에서 property를 점수 검증에 사용한 방식을 이해했다면, 다음과 같이 Grade 디스크립터를 구현하려고 시도하는 것이 타당해 보임
~~~python
#- __get__, __set__ 메서드를 grade set, get처럼 구현

class Grade:
    def __init__(self):
        self._value = 0

    def __get__(self, instance, instance_type):
        return self._value

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError("점수는 0과 100사이 입니다.")
        self._value = value
~~~
- 위의 코드는 잘못됐는데, 한 Exam 인스턴스에서는 정상적이게 작동하지만 여러개의 Exam 인스턴스를 사용하면 한 Grade 인스턴스를 공유하기 때문에 예기치 못한 동작이 일어남
~~~python
first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 99
print("쓰기 : ", first_exam.writing_grade)
print("과학 : ", first_exam.science_grade)

#- 문제는 여기서 발생
second_exam = Exam()
second_exam.writing_grade = 75
print(f"두 번쨰 쓰기 점수 : {second_exam.writing_grade} 맞음")
print(f"첫 번쨰 쓰기 점수 : {first_exam.writing_grade} 틀림: 82점이어야 함")

>>>
쓰기 :  82
과학 :  99
두 번쨰 쓰기 점수 : 75 맞음
첫 번쨰 쓰기 점수 : 75 틀림: 82점이어야 함
~~~
- 프로그램이 실행되는 동안 Exam 클래스가 처음 정의될 때, 이 애트리뷰트에 대한 Grade 인스턴스가 단 한번만 생성됨
- Exam 인스턴스가 생성될 때마다 Grade 인스턴스가 생성되지는 않음
- 이를 해결하려면 Grade 클래스가 각각의 유일한 Exam 인스턴스에 대해 따로 값을 추적하게 해야함 
- 인스턴스별 상태를 딕셔너리에 저장하면 이런 구현이 가능
~~~python
class Grade:
    def __init__(self):
        self._values = {}

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError("점수는 0과 100 사이에 존재해야함")
        else:
            self._values[instance] = value
~~~
- 이 구현은 간단하고 잘 작동하지만, 여전히 한 가지 함정이 존재함. 바로 메모리를 누수시킨다는 점
- values 딕셔너리는 프로그램이 실행되는 동안 `__set__` 호출에 전달된 모든 Exam 인스턴스에 대한 참조를 저장하고 있음
- 이로 인해 인스턴스에 대한 참조 카운터가 절대로 0이 될 수 없고, 따라서 garbage collection이 인스턴스 메모리를 재활용하지 못함 
- <b>이 문제를 해결하기 위해 파이썬 weakref 내장 모듈을 사용할 수 있음</b>
- 이 모듈은 `WeakKeyDictionary`라는 특별한 클래스를 제공하며, _values에 사용한 단순한 딕셔너리 대신 이 클래스를 쓸 수 있음
- `WeakKeyDictionary`의 독특한 부분은 딕셔너리에 객체를 저장할 때 일반적인 강한 참조대신에 약한 참조를 사용한다는 점
- 파이썬 쓰레기 수집기는 약한 참조로만 참조되는 객체가 사용 중인 메모리를 언제든지 재활용 할 수 있음
- 따라서 `WeakkeyDictionary`를 사용해 _values를 저장된 Exam 인스턴스가 더 이상 쓰이지 않는다면(해당 객체를 가리키는 모든 강한 참조가 사라졌다면) 쓰레기 수집기가 해당 메모리를 재활용할 수 있으므로 더 이상 메모리 누수는 없음
~~~python
from weakref import WeakKeyDictionary

class Grade:
    def __init__(self):
        self._values = WeakKeyDictionary()   #- dict -> WeakKeyDictionary

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError("점수는 0과 100 사이에 존재해야함")
        else:
            self._values[instance] = value
~~~

#### 기억해야 할 내용
- @property 메서드의 동작과 검증 기능을 '재사용'하고 싶다면 디스크립터 클래스를 만들어라
- 디스크립터 클래스를 만들 때는 메모리 누수를 방지하기 위해 WeakKeyDictionary를 사용해라
- `__getattribute__` 가 디스크립터 프로토콜을 사용해 애트리뷰트 값을 읽거나 설정하는 방식을 정확히 이해해라

### 47- 지연 계산 애트리뷰트가 필요하면 __getattr__, getattribute__, setattr__을 사용해라
- 파이썬 object 훅은 사용하면 시스템을 서로 접합하는 제너릭 코드를 쉽게 작성할 수 있음
- 예를 들어 데이터베이스 레코드를 파이썬 객체로 표현하고 싶다고 하자. 데이터베이스에는 이미 스키마 집합이 있음
- 우리가 만들 레코드에 대응하는 코드도 데이터베이스 스키마가 어떤 모습인지 알아야 함
- 하지만 파이썬에서 데이터베이스와 파이썬 객체를 연결해주는 코드가 특정 스키마만 표현할 필요는 없음
- 스키마를 표현하는 클래스는 더 일반적으로 만들 수 있음
- 평범한 인스턴스 애트리뷰트나 @property 메서드, 디스크립터 등은 미리 정의해야 하므로 이런 용도에는 사용할 수 없는데, `__getattr__`이라는 특별 메서드를 사용하면 동적 기능을 활용할 수 있음
- 어떤 클래스 안에 `__getattr__` 메서드 정의가 있으면, 이 객체의 인스턴스 딕셔너리에 찾을 수 없는 애트리뷰트에 접근할 때마다 `__getattr__`이 호출됨
~~~python
class LazyRecord:
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = f"{name}를 위한 값"
        setattr(self, name, value)
        return value
~~~
- 다음 코드에서는 foo라는 존재하지 않는 애트리뷰트를 사용하는데, 파이썬은 방금 정의한 `__getattr__` 메서드를 호출하고, 이 메서드는 `__dict__` 인스턴스 딕셔너리를 변경함
~~~python
class LazyRecord:
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = f"{name}를 위한 값"
        setattr(self, name, value)
        return value

data = LazyRecord()
print("이전 :", data.__dict__)
print("foo :", data.foo)
print("이후 :", data.__dict__)

>>>
이전 : {'exists': 5}
foo : foo를 위한 값
이후 : {'exists': 5, 'foo': 'foo를 위한 값'}
~~~
- 다음 코드와 같이 LazyRecord에 로그를 추가해서 `__getattr__`이 실제로 언제 호출되는지 살펴보자
- 여기서는 무한 재귀를 피하고 실제 프러퍼티 값을 가져오기 위해 `super().__getattr__()`를 통해 상위 클래스의 `__getattr__` 구현을 사용했다는 점에 유의해라
~~~python
class LoggingLazyRecord(LazyRecord):

    def __getattr__(self, name):
        print(f"*호출: __getattr__({name!r})"
                f"인스턴스 딕셔너리 채워 넣음")
        result = super().__getattr__(name)
        print(f"*반환: {result!r}")
        return result


data = LoggingLazyRecord()
print("exists:", data.exists)
print("첫 번쨰 foo: ", data.foo)
print("두 번쨰 foo: ", data.foo)

>>>
exists: 5
*호출: __getattr__('foo')인스턴스 딕셔너리 채워 넣음
*반환: 'foo를 위한 값'
첫 번쨰 foo:  foo를 위한 값
두 번쨰 foo:  foo를 위한 값
~~~
- exists 애트리뷰트가 인스턴스 딕셔너리에 있으므로, `__getattr__`이 호출되지 않음
- 반면 foo 애트리뷰트는 처음에 인스턴스 딕셔너리에 없으므로 맨 처음 foo에 접근하면 `__getattr__`이 호출됨
- 하지만 foo에 접근하면 `__getattr__` 이 호출돠고, 안에서 setattr을 수행해 인스턴스 딕셔너리 안에 foo라는 애트리뷰트를 추가함. 따라서 두 번째로 foo에 접근하면 _getattr_이 호출되지 않는다는 사실을 로그에서 확인 가능
- 이러한 기능은 스키마가 없는 데이터에 지연 계산으로 접근하는 등의 활용이 필요할 때 아주 유용
- 스키마가 없는 데이터에 접근하면 `__getattr__` 이 한 번 실행되면서 프로퍼티를 적재하는 힘든 작업을 모두 처리함
- 이후 모든 데이터 접근은 기존 결과를 읽게 됨

#### __getattribute__
- 이 데이터베이스 시스템 안에서 트랜젝션이 필요하다고 하자
- 이제는 사용자가 프로퍼티에 접근할 때 상응하는 데이터베이스에 있는 레코드가 유효한지, 그리고 트랜잭션이 여전히 열려 있는지 판단해야함 
- 기존 애트리뷰트를 확인하는 빠른경로로 객체의 인스턴스 딕셔너리를 사용하기 때문에 `__getattr__` 훅으로는 이런 기능을 안정적으로 만들 수는 없음
- 이와 같은 고급 사용법을 제공하기 위해 파이썬은 `__getattribute__` 라는 다른 object 훅을 제공
- <b>이 특별 메서드는 객체의 애트리뷰트에 접근 할때마다 수행됨</b>
- 심지어 애트리뷰트 디렉터리에 존재하는 애트리뷰트에 접근할 때도 수행됨. 이를 사용하면 프로퍼티에 접근할 때마다 항상 전역 트랜젝션 상태를 검사하는 등의 작업을 수행할 수 있음
- 이런 연산은 부가 비용이 많이 들고 성능에 부정적인 영향을 미칠 수 있지만, 때로는 이런 비용을 감수할 만한 가치를 지닌 경우도 있다는 점을 명심하자
- 다음 코드는 `__getattribute__`가 호출될 때마다 로그를 남기는 `ValidatingRecord`를 정의함
~~~python

~~~
