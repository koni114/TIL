## chapter05 클래스와 인터페이스
### 37-내장 타입을 여러 단계로 내포시키기보다는 클래스를 합성해라
- 파이썬의 내장 딕셔너리 타입을 사용하면 객체의 생명 주기 동안 동적인 내부 상태를 잘 유지할 수 있음
- 여기서 동적이라는 말은 어떤 값이 들어올지 미리 알 수 없는 식별자들을 유지해야 한다는 뜻
- 예를 들어 학생들의 점수를 기록하는데, 학생들의 이름은 미리 알 수 없는 상황이라고 하자
- 이를 때는 학생별로 미리 정의된 애트리뷰트를 사용하는 대신 딕셔너리에 이름을 저장하는 클래스를 정의할 수 있음
~~~python
class SimpleGradebook:
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = []

    def report_grade(self, name, score):
        self._grades[name] = score

    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)


book = SimpleGradebook()
book.add_student('아이작 뉴턴')
book.report_grade('아이작 뉴턴', 90)
book.report_grade('아이작 뉴턴', 95)
book.report_grade('아이작 뉴턴', 85)

print(book.average_grade('아이작 뉴턴'))

>>>
90.0 
~~~
- <b>딕셔너리의 관련 내장 타입은 사용하기 너무 쉬우므로 과하게 확장하면서 깨지기 쉬운 코드를 작성할 위험성이 있음</b>
- 위의 코드를 SimpleGradebook 클래스를 확장해서 전체 성적이 아니라 과목별 성적을 리스트로 저장하고 싶다고 하자
- `_grades` 딕셔너리를 변경해서 학생 이름이 다른 딕셔너리로 매핑하게 하고, 이 딕셔너리가 다시 과목을 성적의 리스트에 매핑하게 함으로써 과목별 성적을 구현할 수 있음
~~~python
from collections import defaultdict


class BySubjectGradebook:
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = defaultdict(list)

    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append(grade)

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total +=  sum(grades)
            count += len(grades)
        return total / count


book = BySubjectGradebook()
book.add_student("알버트 아인슈타인")
book.report_grade("알버트 아인슈타인", '수학', 75)
book.report_grade("알버트 아인슈타인", '수학', 65)
book.report_grade("알버트 아인슈타인", '체육', 90)
book.report_grade("알버트 아인슈타인", '체육', 95)
print(book.average_grade('알버트 아인슈타인'))

>>>
81.25
~~~
- 위의 코드까지는 어느정도 가독성은 보장되고 있음
- 위의 코드에서 각 점수의 가중치를 함께 저장해서 중간고사와 기말고사가 다른 쪽지 시험보다 성적에 큰 영향을 미치게 하고 싶음
- 이런 기능을 구현하는 한가지 방법은 가장 안쪽에 있는 딕셔너리가 과목을 성적의 리스트를 매핑하던 것을 튜플의 리스트로 매핑하도록 변경하는 것
- 다음의 코드를 한 번 보자
~~~python
from collections import defaultdict


class BySubjectGradebook:
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = defaultdict(list)

    def report_grade(self, name, subject, score, weight):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append((score, weight)) #- 튜플로 append

    #- average_grade 계산 방법이 크게 변경됨
    def average_grade(self, name):
        by_subject = self._grades[name]

        score_sum, score_count = 0, 0

        for subject, scores in by_subject.items():
            subject_avg, total_weight = 0, 0

            for score, weight in scores:
                subject_avg += score * weight
                total_weight += weight

            score_sum += subject_avg / total_weight
            score_count += 1

        return score_sum / score_count


book = BySubjectGradebook()
book.add_student("알버트 아인슈타인")
book.report_grade("알버트 아인슈타인", '수학', 75, 0.05)
book.report_grade("알버트 아인슈타인", '수학', 65, 0.15)
book.report_grade("알버트 아인슈타인", '수학', 70, 0.80)
book.report_grade("알버트 아인슈타인", '체육', 100, 0.40)
book.report_grade("알버트 아인슈타인", '체육', 85, 0.60)
print(book.average_grade('알버트 아인슈타인'))

>>>
80.25
~~~
- 이와 같은 복잡도가 눈에 들어오면 더 이상 딕셔너리, 튜플, 집합, 리스트 등의 내장 타입을 사용하지 말고 클래스 계층 구조를 사용해야 함
- 파이썬 내장 딕셔너리와 튜플은 내포 단계가 두 단계 이상이 되면 더 이상 딕셔너리, 리스트, 튜플 계층을 추가하지 말아야 함
- <b>딕셔너리 안에 딕셔너리가 들어가면 프로그래머들이 코드를 읽기 어려워지고, 유지 보수의 악몽으로 들어가게됨</b>
- 코드에서 값을 관리하는 부분이 점점 복잡해지고 있음을 깨달은 즉시 해당 기능을 클래스로 분리해야 함
- 이런 접근 방법을 택하면 인터페이스와 구체적인 구현 사이에 잘 정의된 추상화 계층을 만들 수 있음

#### 클래스를 활용해 리펙터링하기
- 리펙토링시 취할 수 있는 접근 방법은 많은데, 먼저 의존 관계 트리의 맨 밑바닥을 점수로 표현하는 클래스로 옮겨갈 수 있음
- 이렇게 되면 단순한 정보를 표현하는 클래스를 따로 만들면 너무 많은 비용이 듬
- 게다가 점수는 불변 값이기 때문에 튜플이 더 적당해 보임
- 다음의 코드를 보자. 다음 코드는 리스트 안에 점수를 저장하기 위해 (점수, 가중치) 튜플을 이용
~~~python
grades = []
grades.append((95, 0.45))
grades.append((85, 0.55))
total = sum(score * weight for score, weight in grades)
total_weight = sum(weight for _, weight in grades)
average_grade = total / total_weight
~~~
- `total_weight`를 계산할 때는 _를 사용해 각 점수 튜플의 첫 번째 원소를 무시함
- 문제는 점점 property가 늘어날 수록 _의 개수도 늘어나고, 위치 기반이기 때문에 알기가 힘들다는 점
- <b>원소가 세 개 이상인 튜플을 사용한다면 collection 내장 모듈의 namedtuple 타입을 고려하자</b>
~~~python
from collections import namedtuple
Grade = namedtuple('Grade', ('score', 'weight'))
~~~
- `namedtuple` 클래스의 인스턴스를 만들 때에는 위치 기반 인자, 키워드 인자를 사용 가능
- 해당 클래스 기반의 객체에 필드 접근 시 이름이 붙은 애트리뷰트 사용 가능(ex) `Grade.score`, `Grade.weight`)
- 애트리뷰트를 사용할 수 있으므로, 가변성을 지원해야 하거나, 데이터 컨테이너 이상의 동작이 필요한 경우 namedtuple 클래스를 쉽게 바꿀 수 있음

#### namedtuple 한계
- namedtuple은 default 인자를 지정할 수 없어, 선택적인 property가 많은 데이터에 namedtuple을 사용하기는 어려움
- property가 4~5개 많아지면 dataclass 내장 모듈을 사용하는 편이 나음
- namedtuple은 숫자 인덱스나 이터레이션도 가능해서, 외부에 제공하는 API의 경우 이런 특성으로 인해 namedtuple을 실제 클래스로 변경하기 어려울 수 있음
~~~python
from collections import namedtuple
from collections import defaultdict

Grade = namedtuple('Grade', ("score", "weight"))

#- 단일 과목을 표현하는 클래스
class Subject:
    def __init__(self):
        self._grades = []

    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


class Student:
    def __init__(self):
        self._subjects = defaultdict(Subject)

    def get_subject(self, name):
        return self._subjects[name]

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count

#- 마지막으로 모든 학생을 저장하는 컨테이너 만들 수 있음
class Gradebook:
    def __init__(self):
        self._students = defaultdict(Student)

    def get_student(self, name):
        return self._students[name]


book = Gradebook()
albert = book.get_student('알버트 아인슈타인')
math = albert.get_subject('수학')
math.report_grade(75, 0.05)
math.report_grade(65, 0.15)
math.report_grade(70, 0.80)
gym = albert.get_subject('체육')
gym.report_grade(100, 0.40)
gym.report_grade(85, 0.60)
print(albert.average_grade())
~~~

#### 기억해야 할 내용
- 딕셔너리, 긴 튜플, 다른 내장 타입이 복잡하게 내포된 데이터 값으로 사용하는 딕셔너리를 만들지 말라
- 완전한 클래스가 제공되는 유연성이 필요하지 않고 가벼운 불변 데이터 컨테이너가 필요하면 namedtuple을 사용해라
- 내부 상태를 표현하는 딕셔너리가 복잡해지면 이 데이터를 관리하는 코드를 여러 클래스로 나눠서 재작성해라

### 38-간단한 인터페이스의 경우 클래스 대신 함수를 받아라
- 파이썬 내장 API 중 상당수는 함수를 전달해서 동작을 원하는 대로 바꿀 수 있도록 해줌
- <b>API가 실행되는 과정에서 우리가 전달한 함수를 실행하는 경우, 해당 함수를 훅(hook)이라고 부름</b>
- ex) sort 메서드는 key인자로 훅을 받을 수 있음
- 훅을 추상 클래스(abstract class)를 통해 정의해야 하는 언어도 있지만, 파이썬은 단순히 인자와 반환 값이 잘 정의된, 상태가 없는 함수를 훅으로 사용하는 경우가 많음
- 함수는 클래스보다 정의하거나 기술하기가 훨씬 편하므로 훅으로 사용하기에는 이상적이며, 파이썬은 함수를 일급 시민 객체로 취급하기 때문에 함수를 훅으로 사용할 수 있음
- 또한 파이썬은 함수를 first-class object로 취급하기 때문에 함수를 훅으로 사용할 수 있음
- 예를들어, defaultdict 클래스의 default 동작을 우리가 정의하여 함수로 만든다고 해보자
~~~python
from collections import defaultdict

current = {'초록': 12, '파랑': 3}
increment = [
    ('빨강', 5),
    ('파랑', 17),
    ('주황', 9)
]

result = defaultdict(log_missing, current)
print('이전 :', dict(result))
for key, amount in increment:
    result[key] += amount
print('이후 :', dict(result))

>>>
이전 : {'초록': 12, '파랑': 3}
키 추가됨
키 추가됨
이후 : {'초록': 12, '파랑': 20, '빨강': 5, '주황': 9}
~~~
- `log_missing`과 같은 함수를 사용할 수 있으면 정해진 동작과 부수 효과(side effect)를 분리할 수 있기 때문에 API를 더 쉽게 만들 수 있음
- 예를 들어 defaultdict에 전달하는 디폴트 값 훅이 존재하지 않는 키에 접근하는 총 횟수를 세고 싶다고 하자
- 이런 기능을 만드는 방법 중 하나는 상태가 있는 클로저를 사용하는 것
~~~python
from collections import defaultdict

def increment_with_report(current, increments):
    added_count = 0

    def missing():
        nonlocal added_count
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count

current = {'초록': 12, '파랑': 3}
increments = [
    ('빨강', 5),
    ('파랑', 17),
    ('주황', 9)
]

result, count = increment_with_report(current, increments)
assert count == 2
~~~
- 위의 클로저는 상태가 없는 함수에 비해 읽고 이해하기가 어려울 수 있음
- 다른 접근 방법은 작은 클래스를 정의하는 것
~~~python
class CountMissing:
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0
~~~
- 여기서 기억해야 할 것은 <b>일급 함수를 사용해 객체에 대한 CountMissing missing 메서드를 직접 defaultdict의 디폴트 값 훅으로 전달 가능</b>
~~~python
from collections import defaultdict


class CountMissing:
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0

current = {'초록': 12, '파랑': 3}
increments = [
    ('빨강', 5),
    ('파랑', 17),
    ('주황', 9)
]

counter = CountMissing()
result = defaultdict(counter.missing, current)
for key, amount in increments:
    result[key] += amount
assert counter.added == 2
~~~
- 위의 클래스(CountingMissing)처럼 도우미 클래스로 상태가 있는 클로저와 같은 동작을 제공하는 것이 increment_with_report 같은 함수를 사용하는 것 보다 더 깔끔함
- <b>하지만 위의 클래스는 목적이 무엇인지 한번에 알기가 어렵다. 따라서 더 명확히 표현하기 위해서는 파이썬에서 `__call__`을 이용하면 객체를 함수처럼 호출 할 수 있음(아래 코드를 통해 확실히 이해하자)</b> 
- 그리고 `__call__`이 정의된 클래스의 인스턴스에 대해 callable 내장 함수를 사용하면, 다른 일반 함수나 메서드와 마찬가지로 True가 반환됨
- 이런 방식으로 정의돼서 호출될 수 있는 모든 객체를 호출 가능(callable) 객체라고 부름
~~~Python

class BetterCountingMissing:
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

counter = BetterCountingMissing()
assert counter() == 0
assert callable(counter)

#- 다음 처럼 존재하지 않는 키에 대한 접근 횟수를 추적할 수 있음
counter = BetterCountingMissing()
result = defaultdict(counter, current)
for key, amount in increments:
    result[key] += amount
assert counter.added == 2
~~~
- <b>__call__ 메서드는 함수가 인자로 쓰일 수 있는 부분에 이 클래스의 인스턴스를 사용할 수 있는 사실을 나타냄</b>
- 코드를 처음 보는 사람도 이 클래스의 동작을 알아보기 위한 시작점이 `__call__` 이라는 사실을 쉽게 알 수 있음
- 이 클래스를 만든 목적이 상태를 저장하는 클로저 역할임을 잘 알 수 있음
- 파이썬은 단순한 함수 인터페이스를 만족시킬 수 있는 여러 가지 방법을 제공함!

#### 기억해야 할 내용
- 파이썬의 여러 컴포넌트 사이에 간단한 인터페이스가 필요할 때는 클래스를 정의하고 인스턴스화하는 대신 간단히 함수를 사용할 수 있음
- 파이썬 함수나 메서드는 first-class. 따라서 함수나 함수 참조를 식에 사용 가능
- `__call__` 특별 메서드를 사용하면 클래스의 인스턴스인 객체를 일반 파이썬 함수처럼 호출할 수 있음
- 상태를 유지하기 위한 함수가 필요한 경우에는 상태가 있는 클로저를 정의하는 대신 `__call__` 메서드가 있는 클래스를 정의할지 고려해보자


## 용어 정리
- refactoring이란?
  - 외부 동작을 바꾸지 않으면서 내부 구조를 개선하는 일
  - 코드가 작성된 후에 디자인을 개선하는 방법
  - 모든 것을 미리 생각하기보다는 개발하면서 지속적으로 좋은 디자인을 찾음 