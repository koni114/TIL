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
        self._grades[name].append(score)

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

>>> 
80.25
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
- 예를들어, defaultdict 클래스에서 default에 해당하는 동작(defaultdict(list)에서 list)을 정의하여 함수로 만든다고 해보자
~~~python
from collections import defaultdict

def log_missing():
    print("키 추가됨")
    return 0

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
- 코드를 처음 보는 사람도 이 클래스의 동작을 알아보기 위한 g시작점이 `__call__` 이라는 사실을 쉽게 알 수 있음
- 이 클래스를 만든 목적이 상태를 저장하는 클로저 역할임을 잘 알 수 있음
- 파이썬은 단순한 함수 인터페이스를 만족시킬 수 있는 여러 가지 방법을 제공함!

#### 기억해야 할 내용
- 파이썬의 여러 컴포넌트 사이에 간단한 인터페이스가 필요할 때는 클래스를 정의하고 인스턴스화하는 대신 간단히 함수를 사용할 수 있음
- 파이썬 함수나 메서드는 first-class. 따라서 함수나 함수 참조를 식에 사용 가능
- `__call__` 특별 메서드를 사용하면 클래스의 인스턴스인 객체를 일반 파이썬 함수처럼 호출할 수 있음
- 상태를 유지하기 위한 함수가 필요한 경우에는 상태가 있는 클로저를 정의하는 대신 `__call__` 메서드가 있는 클래스를 정의할지 고려해보자

### 39-객체를 제너릭하게 구성하려면 @classmethod를 통한 다형성을 활용하라
- 파이썬은 객체뿐 아니라 클래스도 다형성을 지원함
- 클래스가 다형성을 지원하면 좋은 이유는 계층을 이루는 여러 클래스가 자신에게 맞는 유일한 메소드 버전을 구현할 수 있음
- 예를 들어 맵리듀스 구현을 하나 작성하고 있는데, 입력 데이터를 표현할 수 있는 공통 클래스가 필요하다고 하자
- 다음 코드는 하위 클래스에서 다시 정의해야만 하는 read 메서드가 들어 있는 공통 클래스
~~~python
class InputData:
    def read(self):
        raise NotImplementedError #- 아직 구현하지 않았다는 의미
~~~
~~~python
class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        with open(self.path) as f:
            return f.read()
~~~
- `PathInputData`와 같이 InputData의 하위 클래스를 만들 수 있음
- 각 하위 클래스는 처리할 데이터를 돌려주는 공통 read 인터페이스를 구현해야 함
- 비슷한 방법으로, 입력 데이터를 소비하는 공통 방법을 제공하는 맴리듀스 작업자(worker)로 쓸 수 있는 추상 인터페이스를 정의하고 싶음
~~~python
class Worker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None


    def map(self):
        raise NotImplementedError


    def reduce(self, other):
        raise NotImplementedError
~~~
- 다음 코드는 원하는 맵리듀스 기능(단어 개수를 셈)을 구현하는 Worker의 구체적인 하위 클래스
~~~python
class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')


    def reduce(self, other):
        self.result += other.result
~~~
- 위의 클래스를 기반으로 각 객체를 만들고 맵리듀스를 조화롭게 실행하는 책임은 누가 져야 하나?
- 가장 간단한 접근 방법은 도우미 함수를 활용해 객체를 직접 만들고 연결하는 것
- 다음 코드는 디렉터리의 목록을 얻어서 그 안에 들어 있는 파일마다 PathIuputData 인스턴스를 만듬
~~~python
import os

def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))
~~~
- 다음으로 방금 generate_inputs을 통해 만든 InputData 인스턴스들을 사용하는 LineCountWorker 인스턴스를 만듬
~~~python
def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers
~~~
- 이 Worker 인스턴스의 map 단계를 여러 스레드에 공급해서 실행할 수 있음
- 그 후 reduce를 반복적으로 호출해서 결과를 최종 값으로 합칠 수 있음
~~~python
def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    # - first worker를 기준으로 reduce 연산 수행
    first, * rest = workers
    for worker in rest:
        first.reduce(worker)
    return first.result
~~~
- 마지막으로 지금까지 만든 모든 조각을 한 함수 안에서 합쳐서 각 단계를 실행
~~~python
def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)
~~~
- 몇 가지 입력 파일을 대상으로 이 함수를 실행해보면 아주 훌륭하게 작동함
~~~python
def write_test_files(tmpdir):
    os.makedirs(tmpdir)
    for i in range(100):
        with open(os.path.join(tmpdir, str(i)), 'w') as f:
            f.write('\n' * random.randint(0, 100))

tmpdir = 'test_inputs'
write_test_files(tmpdir)

result = mapreduce(tmpdir)
print(f"총 {result} 줄이 있습니다.")
~~~
- 결과적으로 위의 코드는 제너릭하지 못하다는 문제가 있음
- 다른 InputData나 Worker 하위 클래스를 사용하고 싶다면 각 하위 클래스에 맞게 generate_inputs, create_workers, mapreduce를 재작성해야 함
- 이 문제의 핵심은 객체를 구성할 수 있는 제너릭한 방법이 필요하다는 것
- 파이썬에서는 생성자 메서드가 __init__ 밖에 없다는 것이 문제인데, InputData의 모든 하위 클래스가 똑같은 생성자만 제공해야 한다는 것은 불합리함
- 이 문제를 해결하는 가장 좋은 방법은 클래스 메서드(Class method) 다형성을 사용하는 것
- 클래스 메서드라는 아이디어를 맵리듀스에 사용했던 클래스에 적용해보자. 다음 코드는 InputData에 제너릭 @classmethod를 적용한 모습임. @classmethod가 적용된 클래스 메서드는 공통 인터페이스를 통해 새로운 InputData 인스턴스를 생성
~~~python
class GenericInputData:
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError
~~~
- generate_inputs는 GenericInputData의 구체적인 하위 클래스가 객체를 생성하는 방법을 알려주는 설정 정보가 들어 있는 딕셔너리를 파라미터로 받음
- 다음 코드는 입력 파일이 들어있는 디렉터리를 찾기 위해 config를 사용
~~~Python
class PathInputData(GenericInputData):

    def read(self):
        with open(self.path) as f:
            return f.read()


    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):

            yield cls(os.path.join(data_dir, name))
~~~
- 비슷한 방식으로 GenericWorker 클래스 안에 create_workers 도우미 메서드를 추가할 수 있음
- 이 도우미 메서드는 GenericInputData 하위 타입이어야 하는 input_class를 파라미터로 받음
- input_class는 필요한 입력을 생성해줌. GenericWorker의 구체적인 하위 타입의 인스턴스를 만들 때는(클래스 메서드인 create_workers가 첫 번재 파라미터로 받은) cls()를 제너릭 생성자로 사용
~~~python
class GenericWorker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))

        return workers
~~~
- 이 코드에서 input_class.generate_inputs 호출이 바로 여기서 보여주려는 클래스 다형성의 예
- create_workers가 __init__ 메서드를 직접 호출하지 않고 cls()를 호출함으로써 다른 방법으로 GenericWorker객체를 만들 수 있다는 것도 알 수 있음
- 이런 변경이 구체적인 GenericWorker 하위 클래스에 미치는 영향은 부모 클래스를 바꾸는 것뿐
- 마지막으로 mapreduce 함수가 create_workers를 호출하게 변경해서 mapreduce를 완전한 제너릭 함수로 만들 수 있음
~~~python
def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)
~~~
- 똑같은 테스트 파일 집합에 대해 새로운 직업자를 실행하면 이전의 구현과 똑같은 결과를 얻을 수 있음
- 유일한 차이점은 제너릭하게 작동해야 하므로 mapreduce 함수에 더 많은 파라미터를 넘겨야 한다는 것 뿐
~~~python
tmpdir = 'test_dir'
config = {'data_dir': tmpdir}
result = mapreduce(LineCountWorker, PathInputData, config)
print(f"총{result} 줄이 있음")
~~~
- 이제는 각 하위 클래스의 인스턴스 객체를 결합하는 코드를 변경하지 않아도 `GenericInputData`와 `GenericWorker`의 하위 클래스를 내가 원하는 대로 작성할 수 있다

#### 기억해야 할 내용
- 파이썬의 클래스는 생성자가 `__init__` 메서드뿐
- `@classmethod`를 사용하면 클래스에 다른 생성자를 정의할 수 있음
- 클래스 메서드 다형성을 활용하면 여러 구체적인 하위 클래스의 객체를 만들고 연결하는 제너릭한 방법을 제공할 수 있음

### 40-super로 부모 클래스를 초기화해라
- 자식 클래스에서 부모 클래스를 초기화하는 오래된 방법은 바로 자식 인스턴스에서 부모 클래스의 `__init__` 메서드를 직접 호출하는 것 
~~~python
class MyBaseClass:
    def __init__(self, value):
        self.value = value


class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 5)
~~~
- 이 접근 방법은 기본적인 클래스 계층의 경우에는 잘 작동하지만, 다른 경우에는 잘못될 수도 있음 
- 어떤 클래스가 다중 상속에 의해(다중 상속은 왠만하면 피해야 함) 영향을 받은 경우, 상위 클래스의 `__init__`메서드를 직접 호출하면 프로그램이 예측할 수 없는 방식으로 작동할 수 있음
- 다중 상속을 사용하는 경우 생기는 문제 중 하나는 모든 하위 클래스에서 `__init__` 호출의 순서가 정해져 있지 않다는 것임
- 예를 들어 다음 코드는 인스턴스의 value 필드에 대해 작용하는 두 상위 클래스를 정의하고, 부모 클래스를 `TimesTwo`, `PlusFive` 순으로 나열
- `OneWay` 클래스 정의시 부모 클래스 생성자도 동일한 배열로 정의함 --> 결과는 15가 나옴
~~~python
class TimesTwo:
    def __init__(self):
        self.value *= 2


class PlusFive:
    def __init__(self):
        self.value += 5


class OneWay(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)

foo = OneWay(5)
print(f"첫 번째 부모 클래스 순서에 따른 값은 (5 * 2)  + 5 : {foo.value}")

>>> 
15
~~~
- 만약에 부모 클래스를 나열한 순서를 바꾼다고 하더라도 똑같은 15가 나옴
~~~python
class AnatherWay(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)

foo = AnatherWay(5)
print(f"첫 번째 부모 클래스 순서에 따른 값은 (5 * 2)  + 5 : {foo.value}")

>>>
15
~~~
- 즉 클래스 정의에 나열한 부모 클래스의 순서와 부모 생성자를 호출한 순서가 달라서 생기는 문제는 발견하기 쉽지 않고, 코드를 처음 보고 이해하기 어려울 수 있음
- 다이아몬드 상속은 어떤 클래스가 두 가지 서로 다른 클래스를 상속하는데, 두 상위 클래스의 상속 계층을 거슬러 올라가면 공통 클래스가 존재하는 경우를 말함
- 다이아몬드 상속이 이뤄지면, 공통 조상 클래스의 `__init__` 메서드가 여러 번 호출될 수 있기 떄문에 예기치 않은 방식으로 작동할 수 있음
- 다음의 코드는 다이아몬드 상속을 구현한 코드 예제다
~~~python
class TimesSeven(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 7


class PlusNine(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 9

class ThisWay(TimesSeven, PlusNine):
    def __init__(self, value):
        TimesSeven.__init__(self, value)
        PlusNine.__init__(self, value)

foo = ThisWay(5)
print("(5 * 7) + 9 = 44가 나와야 하지만 실제로는.", foo.value)

>>>
(5 * 7) + 9 = 44가 나와야 하지만 실제로는. 14
~~~
- 두 번째 부모 클래스의 생성자 `PlusNine.__init__` 을 호출하면, `MyBaseClass.__init__`이 호출되면서 `self.value`가 다시 5로 돌아감
- 이러한 경우는 디버깅하기가 매우 힘들다!
- 이러한 문제를 해결하기 위하여 파이썬에서는 `super`라는 내장 함수와 표준 메서드 결정 순서(Method Resolution OMRO)가 있음
- super를 사용하면 다이아몬드 계층의 공통 상위 클래스를 단 한번만 호출하도록 보장함
- MRO는 상위 클래스를 초기화하는 순서를 정의함. 이때 C3 선형화 알고리즘을 사용
~~~python
class TimesSeven(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value *= 7


class PlusNine(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value += 9

class ThisWay(TimesSeven, PlusNine):
    def __init__(self, value):
        super().__init__(value)

foo = ThisWay(5)
print("7 * (5 + 9) = 98가 나와야 하고 실제로는.", foo.value)
~~~
~~~python
mro_str = '\n'.join(repr(cls) for cls in ThisWay.mro())
print(mro_str)

>>>
<class '__main__.ThisWay'>
<class '__main__.TimesSeven'>
<class '__main__.PlusNine'>
<class '__main__.MyBaseClass'>
<class 'object'>
~~~
- 중요한 것은 상속 다이아몬드 정점에 도착하면, 각 초기화 메서드는 각 클래스의 `__init__`이 호출된 순서의 역순으로 작업을 수행하게 됨
- `super` 함수에는 두 가지 파라미터를 넘길 수 있는데, 첫 번쨰 파라미터는 우리가 접근하고 싶은 MRO 뷰를 제공할 부모 타입이고, 두 번째 파라미터는 첫 번째 파라미터로 지정한 타입의 MRO 뷰에 접근할 때 사용할 인스턴스
- 다음과 같이 사용가능하지만, object 인스턴스를 초기화 할때는 두 파라미터를 지정할 필요가 없음. 우리가 클래스 정의 안에서 아무 인자도 지정하지 않고 super를 호출하면, 파이썬 컴파일러가 자동으로 올바른 파라미터를 넣어줌
- `super`에 파라미터를 넣는 유일한 경우는 자식 클래스에서 부모 클래스의 특저 기능에 접근해야 하는 경우뿐
~~~python
class ExplicitTrisect(MyBaseClass):
    def __init__(self, value):
        super(ExplicitTrisect, self).__init__(value)
~~~

#### 기억해야 할 내용
- 파이썬은 표준 메서드 결정 순서(MRO)를 활용해 상위 클래스 초기화 순서와 다이아몬드 상속 문제를 해결함
- 부모 클래스를 초기화할 때는 super 내장 함수를 아무 인자 없이 호출해라 

### 41- 기능을 합성할 떄는 믹스인 클래스를 활용해라
- 파이썬은 다중 상속을 지원하는 언어이지만, 다중 상속을 피하는 것이 좋으며 믹스인을 사용할지 고려해보자 
- 믹스인은 자식 클래스가 사용할 메서드 몇 개만 정의하는 클래스
- 믹스인 클래스는 자체 에트리뷰트 정의가 없으므로 믹스인 클래스의 `__init__` 메서드를 호출할 필요도 없음
- 파이썬에서는 타입과 상관없이 객체의 현재 상태를 쉽게 들여다 볼 수 있으므로 믹스인 작성이 쉬움
- 동적인 상태 접근이 가능하다는 말은 제너릭인 기능을 믹스인 안에 한 번만 작성해두면 다른 여러 클래스에 적용할 수 있다는 뜻 
- 믹스인을 합성하거나 계층화해서 반복적인 코드를 최소화하고 재사용성을 최대화 할 수 있음
- 예를 들어 메모리 내에 들어있는 객체를 직렬화에 사용할 수 있도록 딕셔너리로 바꾸고 싶다고 하자. 이런 기능을 제너릭하게 작성해 여러 클래스에 활용하면 어떨까? 
- 다음 코드는 이런 기능을 제공하는 공개 메서드를 사용해 정의한 믹스인 예제임. 이 믹스인을 상속하는 모든 클래스에서 이 함수의 기능을 사용할 수 있음
- 또한 이 `_traverse_dict` 메서드를 `hasattr`를 통한 동적인 애트리뷰트 접근과 isinstance를 사용한 타입 검사, `__dict__`를 통한 인스턴스 딕셔너리 접근을 활용해 간단하게 구현할 수 있음
~~~python
class ToDictMixin:
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    #- 재귀적 기법을 사용
    #- value가 ToDictMixin, dict, list, __dict__ attribute 여부에 따라서
    #- 값을 변환하고 다시 재귀적으로 함수 호출
    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value
~~~
- 다음은 위의 `ToDictMixin`을 사용해 이진 트리를 딕셔너리 표현으로 변경하는 예제 코드임
~~~python
class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


tree = BinaryTree(10, left = BinaryTree(7, right=BinaryTree(9)),
                     right=BinaryTree(13, left=BinaryTree(11)))


print(tree.to_dict())

>>>
{'value': 10, 'left': {'value': 7, 'left': None, 'right': {'value': 9, 'left': None, 'right': None}}, 'right': {'value': 13, 'left': {'value': 11, 'left': None, 'right': None}, 'right': None}}
~~~
- 믹스인의 가장 큰 장점은 제너릭 기능을 쉽게 연결할 수 있고 필요할 때 기존 기능을 다른 기능으로 오버라이드(override)해 변경할 수 있다는 점
- 예를 들어 다음 코드는 BinaryTree에 대한 참조를 저장하는 BinaryTree의 하위 클래스를 정의함
- 이런 순환 참조가 있으면 원래의 `ToDictMixin.to_dict` 구현은 무한 루프를 돈다
~~~python
class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent
~~~
- 해결 방법은 `BinaryTreeWithParent._traverse` 메서드를 오버라이드해 문제가 되는 값만 처리하게 만들어서 믹스인이 무한 루프를 돌지 못하게 하는 것임
- 다음 코드에서 `_traverse`를 오버라이드한 메서드는 부모를 가리키는 참조에 대해서는 부모의 숫자 값을 삽입하고(`value.value` 부분), 부모가 아닌 경우에는 super 내장 함수를 통해 디폴트 믹스인 구현을 호출
~~~python
    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and key == 'parent'):
            return value.value
        else:
            return super()._traverse(key, value)
~~~
- 변환 시 순환 참조를 따라가지 않으므로 `BinaryTreeWithParent.to_dict`가 잘 작동한다
~~~python
root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)
root.to_dict()

>>>
{'value': 10, 
    'left': {'value': 7, 
            'left': None, 
            'right': {'value': 9, 
                        'left': None, 
                        'right': None, 'parent': 7},
             'parent': 10}, 
    'right': None, 
    'parent': None}
~~~
- `BinaryTreeWithParent._traverse`를 오버라이드 함에 따라 BinaryTreeWith Parent를 애트리뷰트로 저장하는 모든 클래스도 자동으로 `ToDictMixin`을 문제없이 사용할 수 있게 됨
~~~Python
class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent


my_tree = NamedSubTree('foobar', root.left.right)

#- 두 개의 결과를 비교해서 확인하기
print(my_tree.__dict__)
print(my_tree.to_dict())

{'name': 'foobar', 
 'tree_with_parent': <__main__.BinaryTreeWithParent object at 0x7ffe3b4268d0>}

{'name': 'foobar',
 'tree_with_parent': {'value': 9, 
                      'left': None, 
                      'right': None, 
                      'parent': 7}}
~~~
- 믹스인을 서로 합성할 수도 있음. 예를 들어 임의의 클래스를 JSON으로 직렬화하는 제너릭 믹스인을 만들고 싶다고 하자.
- 모든 클래스가 `to_dict` 메서드를 제공한다고 가정하면(to_dict를 ToDictMixin 클래스를 통해 제공할 수도 있고 다른 방식으로 제공할 수도 있음), 다음과 같은 제너릭 믹스인을 만들 수 있음
~~~python
import json


class JsonMixin:
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict()) 
~~~
- 여기서 `JsonMixin` 클래스 안에 인스턴스 메서드와 클래스 메서드가 함께 정의됐다는 점에 유의해라
- 믹스인을 사용하면 인스턴스 동작이나 클래스의 동작 중 어느 것이든 하위 클래스에 추가할 수 있음
- 이 예제에서 JsonMixin 하위 클래스의 요구 사항은 `to_dict` 메서드를 제공해야 한다는 점과 `__init__` 메서드가 키워드 인자를 받아야 한다는 것뿐 
- 이런 믹스인이 있으면 JSON과 직렬화를 하거나 역직렬화를 할 유틸리티 클래스의 클래스 계층 구조를 쉽게, 번잡스러운 준비 코드 없이 만들 수 있음
- 예를 들어 데이터센터의 각 요소 간 연결(topology)를 표현하는 클래스 계층이 있다고 하자
~~~python
class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machines = [
            Machine(**kwargs) for kwargs in machines]


class Switch(ToDictMixin, JsonMixin):
    def __init__(self, ports=None, speed=None):
        self.ports = ports
        self.speed = speed


class Machine(ToDictMixin, JsonMixin):
    def __init__(self, cores=None, ram=None, disk=None):
        self.cores = cores
        self.ram = ram
        self.disk = disk
~~~
- 이런 클래스들은 JSON으로 직렬화하거나 JSON으로부터 역직렬화하는 것은 간단함
- 다음은 데이터를 JSON으로 직렬화한 다음에 다시 역직렬화하는 양방향 변환이 가능한지 검사하는 코드임
~~~python
serialized = """{
    "switch": {"ports": 5, "speed": 1e9},
    "machines": [
        {"cores": 8, "ram": 32e9, "disk": 5e12},
        {"cores": 4, "ram": 16e9, "disk": 1e12},
        {"cores": 2, "ram": 4e9, "disk": 500e9}
    ]
}"""

deserialized = DatacenterRack.from_json(serialized)
roundtrip = deserialized.to_json()
assert json.loads(serialized) == json.loads(roundtrip)
~~~
- 이렇게 믹스인을 사용할 때 jsonMixin을 적용하려고 하는 클래스 상속 계층의 상위 클래스에 이미 JsonMixin을 적용한 클래스가 있어도 아무런 문제가 없음
- 이런 경우에도 super가 동작하는 방식으로 인해 믹스인을 적용한 클래스가 제대로 작동함

#### 기억해야 할 내용
- 믹스인을 사용해 구현할 수 있는 기능을 인스턴스 애트리뷰트와 `__init__`을 사용하는 다중 상속을 통해 구현하지 말라
- 믹스인 클래스가 클래스별로 특화된 기능을 필요로 한다면 인스턴스 수준에서 끼워 넣을 수 있는 기능을 활용해라
- 믹스인에는 필요에 따라 인스턴스 메서드는 물론 클래스 메서드도 포함될 수 있음
- 믹스인을 합성하면 단순한 동작으로부터 더 복잡한 기능을 만들어낼 수 있음

## 42-비공개 애트리뷰트보다는 공개 애트리뷰트를 사용해라
- 파이썬에서 클래스의 애트리뷰트에 대한 가시성을 공개(public)와 비공개(private), 두 가지밖에 없음
~~~python
class MyObject:
    def __init__(self):
        self.public_field = 5       #- public
        self.__private_field = 10   #- private

    def get_private_field(self):
        return self.__private_field

foo = MyObject()
assert foo.public_field == 5
~~~
- 객체 뒤에 점 연산자(.)를 붙이면 공개 애트리뷰트에 접근할 수 있음
- 애트리뷰트 이름 앞에 밑줄을 두 개(__) 붙이면 비공개 필드가 됨. 
- 비공개 필드를 포함하는 클래스 안에 있는 메서드에서는 해당 필드에 직접 접근할 수 있음
~~~python
assert foo.get_private_field() == 10
~~~
- 하지만 클래스 외부에서 비공개 필드에 접근하면 예외가 발생함
~~~python
foo.__private_field

>>>
Traceback (most recent call last):
AttributeError: 'MyObject' object has no attribute '__private_field'
~~~
- 클래스 메서드는 자신을 둘러싸고 있는 class 블록 내부에 들어 있기 때문에 해당 클래스의 비공개 필드에 접근할 수 있음
~~~python
class MyOtherObject:
    def __init__(self):
        self.__private_field = 71

    @classmethod
    def get_private_field_of_isntance(cls, instance):
        return instance.__private_field

bar = MyOtherObject()
assert MyOtherObject.get_private_field_of_isntance(bar) == 71
~~~
- 하위 클래스는 부모 클래스의 비공개 필드에 접근할 수 없음
~~~python
class MyParentObject:
    def __init__(self):
        self.__private_field = 71

class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field

baz = MyChildObject()
baz.get_private_field() #- error
~~~
- <b>비공개 애트리뷰트의 동작은 애트리뷰트 이름을 바꾸는 단순한 방식으로 구현됨</b>
- `MyChildObject.get_private_field`처럼 메서드 내부에서 private attribute에 접근하는 코드가 있으면, 파이썬 컴파일러는 `__private_field` 라는 애트리뷰트 접근 코드를 `_MyChildObject__private_field`라는 이름으로 바꿔줌 
- 위 예제에서는 `MyParentObject.__init__` 안에만 `__private_field` 정의가 들어있음
- 이는 이 비공개 필드의 이름이 실제로는 `_MyParentObject__private_field`라는 뜻임
- 부모의 비공개 애트리뷰트를 지식 애트리뷰트에서 접근하면, 변경한 애트리뷰트 이름(`_MyParentObject__private_field`가 아니라 `MyChildObject__private_field`로 이름이 바뀜)이 존재하지 않는다는 이유로 오류가 발생함
- 이 방식을 알고 나면 특별한 권한을 요청할 필요 없이 쉽게, 하위 클래스에서든 클래스 외부에서든 원하는 클래스의 비공개 애트리뷰트에 접근할 수 있음
~~~python
assert baz._MyParentObject__private_field == 71
~~~
- 객체 애트리뷰트 딕셔너리를 살펴보면 실제로 변환된 비공개 애트리뷰트 이름이 들어있는 모습을 볼 수 있음
~~~python
print(baz.__dict__)
>>>
{'_MyParentObject__private_field': 71}
~~~
- 비공개 애트리뷰트에 대한 접근 구문이 실제로 가시성을 엄격하게 제한하지 않는 이유는 무엇일끼?
- 가장 간단한 답을 생각해보면, 파이썬의 모토로 자주 회자되는 '우리는 모두 책임질줄 아는 성인이다'일 것임
- 이 말이 뜻하는 바는 우리가 하고 싶은 일을 언어가 제한해서는 안된다는 것임
- 특정 기능을 확장할지의 여부는 사용자의 책임이다
- 파이썬 프로그래머들은 열어둠으로써 얻을 수 있는 이익이 해악보다 더 크다고 믿음
- 게다가 파이썬은 애트리뷰트에 접근할 수 있는 언어 기능에 대한 훅을 제공하기 때문에 원할 경우에는 객체 내부를 마음대로 주무를 수 있음
- 이러 기능들을 제공하는데, 굳이 다른 방식으로 비공개 애트리뷰트에 접근하는 경우를 막으려고 노력하는 것이 과연 얼마나 큰 가치를 지닐까?
- 내부에 몰래 접근하므로써 생길 수 있는 피해를 줄이고자 파이썬 프로그래머는 스타일 가이드에 정해진 명명규약을 지킴
- 예를 들어 필드 앞에 밑줄이 하나 있으면 protected 필드를 뜻하며, 보호 필드는 클래스 외부에서 이 필드를 사용하는 경우 조심해야 한다는 뜻임
- 파이썬을 처음 사용하는 많은 프로그래머가 하위 클래스나 클래스 외부에서 사용하면 안되는 내부 API를 표현하기 위하여 비공개 필드를 사용하는데, 이 접근 방법은 잘못된 것임
- 괜히 추가적인 코드가 들어가고, 비공개 필드에 접근해야 한다면 여전히 접근이 가능하기 때문이다 
~~~python
    def get__value(self):
        return int(self.__MyStringClass__value)
~~~
- 하지만 우리가 상위 클래스의 정의를 변경하면 더 이상 비공개 애트리뷰트에 대한 참조가 바르지 못하므로 하위 클래스가 깨질 것임
- 일반적으로 상속을 허용하는 클래스 쪽에서 보호 애트리뷰트를 사용하고 오류를 내는 편이 낫다
- 모든 보호 필드에 문서를 추가한 후, API 내부에 있는 필드 중에서 어떤 필드를 하위 클래스에서 변경할 수 있고 어떤 필드를 그대로 나둬야 하는지 명시해라
- 코드를 안전하게 확장할 수 있는 방법을 다른 프로그래머는 물론, 미래의 자신에게도 안내해라
~~~python
class MyStringClass:
    def __init__(self, value):
        # 여기서 객체에게 사용자가 제공한 값을 저장
        # 사용자가 제공하는 값은 문자열로 타입 변환이 가능해야 하며
        # 일단 한번 객체 내부에 설정되고 나면
        # 불변 값으로 취급해야 함
        self.value = value
~~~
- 비공개 애트리뷰트틀 사용할지 진지하게 고민해야 하는 유일한 경우는 하위 클래스의 필드와 이름이 충돌할 수 있는 경우뿐
- 자식 클래스가 실수로 부모 클래스가 이미 정의한 애트리뷰트를 정의하면 충돌이 생길 수 있음
~~~python
class ApiClass:
    def __init__(self):
        self._value = 5
    def get(self):
        return self._value


class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' #- 충돌
~~~
- 주로 공개 API에 속한 클래스의 경우 신경 써야 하는 부분임. 우리가 만든 공개 API를 외부에 제공하는 경우에는 하위 클래스 작성이 우리의 제어 밖에서 일어나므로 이런 문제가 발생해도 리펙터링이 불가능함
- 특히 애트리뷰트 이름이 흔한 이름(예) value)일 때 충돌이 자주 발생할 수 있음
- 이런 문제가 발생할 위험성을 줄이려면 부모 클래스 쪽에서 자식 클래스의 애트리뷰트 이름이 자신의 애트리뷰트 이름과 겹치는 일을 방지하기 위해 비공개 애트리뷰트를 사용할 수 있음
~~~python
class ApiClass:
    def __init__(self):
        self.__value = 5

    def get(self):
        return self.__value

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'

a = Child()
print(f"{a.get()}과 {a._value}는 달라야 함")

>>>
5과 hello는 달라야 함
~~~

#### 기억해야 할 내용
- 파이썬 컴파일러는 비공개 애트리뷰트를 자식 클래스나 클래스 외부에서 사용하지 않도록 엄격하게 금지하지 않음
- 우리의 내부 API에 있는 클래스의 하위 클래스를 정의하는 사람들이 우리가 제공하는 클래스의 애트리뷰트를 사용하지 못하도록 막기보다는 애트리뷰트를 사용해 더 많은 일을 할 수 있도록 하자
- 비공개 애트리뷰트로 접근을 막으려고 시도하기보다는 보호된 필드를 사용하면서 문서에 적절한 가이드를 남겨라
- 여러분이 코드 작성을 제어할 수 없는 하위 클래스에서 <b>이름 충돌이 일어나는 경우</b>를 막고 싶을 때만 비공개 애트리뷰트를 사용할 것을 권함

### 커스텀 컨테이너 타입은 collections.abc를 상속해라
- 파이썬 프로그래밍의 상당 부분은 데이터를 포함하는 클래스를 정의하고 이런 클래스에 속하는 객체들이 서로 상호작용하는 방법을 기술하는 것으로 이뤄짐
- 모든 파이썬 클래스는 함수의 애트리뷰트를 함께 캡슐화하는 일종의 컨테이너라고 할 수 있음
- 파이썬은 데이터를 관리할 때 사용할 수 있도록 리스트, 튜플, 집합, 딕셔너리 등의 내장 컨테이너 타입을 제공함
- 시퀀스처럼 사용법이 간단한 클래스를 정의할 때는 클파이썬 내장 리스트 타입의 하위 클래스를 만들고 싶은 것이 당연함
- 예를 들어 멤버들의 빈도를 계산하는 메서드가 포함된 커스텀 리스트 타입이 필요하다고 가정하자 
~~~python
class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):
        counts = {}
        for item in self:
            counts[item] = counts.get(item, 0) + 1
        return counts
~~~
- `FrequencyList`를 리스트의 하위 클래스로 만듦으로써 리스트가 제공하는 모든 표준 함수를 FrequencyList에서도 사용할 수 있으며, 파이썬 프로그래머들이라면 이런 함수들의 의미가 낯익을 것임
- 게다가 필요한 기능을 제공하는 메서드를 얼마든지 추가 할 수 있음
~~~python
class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):
        counts = {}
        for item in self:
            counts[item] = counts.get(item, 0) + 1
        return counts

foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
print("길이 : ", len(foo))

foo.pop()
print("pop한 다음 :", repr(foo))
print("빈도:", foo.frequency())

>>>
길이 :  7
pop한 다음 : ['a', 'b', 'a', 'c', 'b', 'a']
빈도: {'a': 3, 'b': 2, 'c': 1}
~~~
- 이제 리스트처럼 느껴지면서 인덱싱이 가능한 객체를 제공하고 싶은데, 리스트의 하위 클래스를 만들고 싶지는 않다고 가정해보자 
- 예를 들어, 다음 이진 트리 클래스를 시퀀스(리스트나 튜플)의 의미 구조를 사용해 다룰 수 있는 클래스를 만들고 싶음
~~~python
class BinaryNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
~~~
- 어떻게 이 클래스가 시퀀스 타입처럼 작동하게 할 수 있을까? 파이썬에서는 특별한 이름의 인스턴스 메서드를 사용해 컨테이너의 동작을 구현함
- 인덱스를 사용해 다음과 같이 시퀀스에 접근하는 코드는
~~~python
bar = [1, 2, 3]
bar[0]

#- 다음의 특별 메서드로 해석됨
bar.__getitem__(0)
~~~
- `BinaryNode` 클래스가 시퀀스처럼 작동하게 하려면 트리 노드를 깊이 우선 순회하는 커스텀 `__getitem__` 메서드를 구현하면 됨
~~~python
class IndexableNode(BinaryNode):
    def _traverse(self):
        if self.left is not None:
            yield from self.left._traverse()
        yield self
        if self.right is not None:
            yield from self.right._traverse()

    def __getitem__(self, index):
        for i, item in enumerate(self._traverse()):
            if i == index:
                return item.value
        raise IndexError(f"인덱서 ㅡ범위 초과: {index}")


tree = IndexableNode(
    10,
    left=IndexableNode(
        5,
        left=IndexableNode(2),
        right=IndexableNode(
            6,
            right=IndexableNode(7))),
    right=IndexableNode(
        15,
        left=IndexableNode(11)))
~~~
- 이 트리를 left나 right 애트리뷰트를 사용해 순회할 수 있지만, 추가로 리스트처럼 접근할 수 있음
~~~python
print("LRR:", tree.left.right.right.value)
print("인덱스 0:", tree[0])
print("인덱스 1:", tree[1])
print("11이 트리 안에 있나? ", 11 in tree)
print("17이 트리 안에 있나? ", 17 in tree)
print('트리:', list(tree))

>>>
LRR: 7
인덱스 0: 2
인덱스 1: 5
11이 트리 안에 있나?  True
17이 트리 안에 있나?  False
트리: [2, 5, 6, 7, 10, 11, 15]
~~~
- 문제는 `__getitem__`을 구현하는 것만으로는 리스트 인스턴스에서 기대할 수 있는 모든 시퀀스 의미 구조를 제공할 수 없다는 데 있음
~~~python
len(tree)

>>>
Traceback (most recent call last):
  File "<input>", line 1, in <module>
TypeError: object of type 'IndexableNode' has no len()
~~~
- len 내장 함수는 `__len__` 이라는 특별 메서드를 구현해야 제대로 작동함
- 커스텀 시퀀스 타입은 이 메서드를 꼭 구현해야 함
~~~python
    def __len__(self):
        for count, _ in enumerate(self._traverse(), 1):
            pass
        return count
~~~
- 이것만으로도 완벽하지 않으며, `count`, `index` 메서드도 들어있지 않음
- 결과적으로 자신만의 컨테이너 타입을 직접 정의하는 것은 생각보다 훨씬 어려운 일임을 알 수 있음
- <b>파이썬을 사용할 때 흔히 발생하는 이런 어려움을 덜어주기 위하여 내장 collection.abc 모듈 안에는 컨테이너 타입에 정의해야 하는 전형적인 메서드를 모두 제공하는 추상 기반 클래스 정의가 여러 가지 들어가 있음</b>
- 이런 추상 기반 클래스의 하위 클래스를 만들고 필요한 메서드 구현을 잊어버리면, collections.abc 모듈이 실수한 부분을 알려줌
~~~python
from collections.abc import Sequence

class BadType(Sequence):
    pass

foo = BadType()
>>>
TypeError: Can't instantiate abstract class BadType with abstract methods __getitem__, __len__
~~~
- `SequenceNode`에서 한 것처럼 `collections.abc`에서 가져온 추상 기반 클래스가 요구하는 모든 메서드를 구현하면 index나 count와 같은 추가 메서드 구현을 거져 얻을 수 있음
~~~python
class BetterNode(SequenceNode, Sequence):
    pass

tree = BetterNode(
    10,
    left=BetterNode(
        5,
        left=BetterNode(2),
        right=BetterNode(
            6,
            right=BetterNode(7))))


print("7의 인덱스:", tree.index(7))
print("10의 개수:", tree.count(10))

>>>
7의 인덱스: 3
10의 개수: 1
~~~
- `Set`이나 `MutableMapping`과 같이 파이썬의 관례에 맞춰 구현해야 하는 특별 메서드가 훨씬 많은 더 복잡한 컨테이너 타입을 구현할 때는 이런 추상 기반 클래스가 주는 이점이 더 커짐
- `collection.abc` 모듈 외에도, 파이썬에서는 객체 비교와 정렬을 위해 사용하는 다양한 특별 메서드들이 존재함
- 컨테이너 클래스나 비컨테이너 클래스에서 모두 이런 특별 메서드를 구현할 수 있음

#### 기억해야 할 내용
- 간편하게 사용하는 경우에는 파이썬 컨테이너 타입을 직접 상속해라
- 커스텀 컨테이너를 제대로 구현하려면 수많은 메서드를 구현해야 한다는 점에 주의해라
- 커스텀 컨테이너 타입이 collections.abc에 정의된 인터페이스를 상속하면 커스텀 컨테이너 타입이 정상적으로 작동하기 위해 필요한 인터페이스와 기능을 제대로 구현하도록 보장할 수 있음


## 용어 정리
- refactoring이란?
  - 외부 동작을 바꾸지 않으면서 내부 구조를 개선하는 일
  - 코드가 작성된 후에 디자인을 개선하는 방법
  - 모든 것을 미리 생각하기보다는 개발하면서 지속적으로 좋은 디자인을 찾음 
- 제너릭 함수
  - 어떤 하나의 함수가 여러 타입의 인자를 받고, 인자의 타입에 따라 적절한 동작을 하는 함수  
  - 클래스 내부에서 사용할 데이터 타입을 외부에서 지정하는 기법  
- 직렬화
  - 파이썬 객체를 일련의 바이트들로 전환하는 것을 직렬화, 그 반대로 decode하는 것을 역직렬화라고 함