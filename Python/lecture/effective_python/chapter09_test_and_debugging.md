## chapter09 테스트와 디버깅
- 파이썬은 컴파일 시점에 정적 타입 검사(static type checking)를 수행하지 않음
- 또한, 파이썬 인터프리터가 컴파일 시점에 프로그램이 제대로 작동할 것이라고 확인 할 수 있는 요소가 전혀 없음
- 파이썬은 선택적인 타입 애너테이션(optional type annotation)을 지원하며, 이를 활용해  정적 분석을 수행함으로써 여러 가지 오류를 감지할 수 있음 
- 하지만 여전히 파이썬은 근본적으로 동적인 언어이며, 프로그램을 실행하는 도중에 어떤일이든 벌어질 수 있음
- 파이썬에서는 소스 코드에서 어떤 함수가 존재한다는 사실이 분명해 보여도 실행 시점에 해당 함수를 호출할 때 함수가 정의돼 있는지 궁극적으로 확신할 수는 없음
- 따라서 이런 동적인 동작은 축복인 동시에 저주이기도 함
- 현재 파이썬 개발자 중 상당수는 정적 타입 검사를 생략함으로써 단순성과 간결성을 얻을 수 있고 결과적으로 생산성이 높아지므로 타입 검사를 생략할 만한 가치가 있다고 말함
- 하지만 파이썬을 사용하는 사람 대부분은 프로그램을 작성하다가 너무나 어처구니없는 실수를 저질러 오류를 발생시킨 무서운 경험이 한두번 씩은 있음 
- 내가 들었던 최악의 오류 사례는 동적 임포트로 인해 발생한 부작용으로, 프로덕션 코드에서 SystaxError가 발생해 서버 프로세스가 중단된 사건
- 하지만 우리는 의문을 품어야 한다. 프로덕션에 배포하기 전에 프로그램을 더 잘 테스트하지 않은 이유는 무엇인가? 컴파일 시점의 정적 타입 안정성이 모든 오류를 방지해주지는 못함
- 코드를 작성할 때 쓴 언어와 관계없이 우리는 항ㅅ아 자신이 작성한 코드를 테스트해야 함
- <b>다른 언어보다도 파이썬에서 테스트를 통해 코드의 올바름을 검증하는 것이 중요한 것은 사실</b>
- 다행히 파이썬 프로그램을 실행할 때 큰 위험이 될 수 있는 동적인 기능들이 우리의 코드에 대한 테스트를 작성하거나 잘못 작동하는 프로그램을 디버깅하는 작업을 아주 쉽게 할 수 있도록 해줌
- 우리는 파이썬의 동적 기능을 사용해 프로그램의 동작을 다른 동작으로 오버라이드함으로써 테스트를 구현하고 프로그램이 예상대로 작동하는지 확인할 수 있음
- 테스트를 코드에 대한 보험으로 생각하자. 테스트를 잘 작성하면 코드가 올바르다고 더 확신할 수 있음
- 코드를 확장하거나 리펙터링하면, 코드의 동작을 검증하는 테스트를 활용해 변경된 부분을 쉽게 식별할 수 있음
- 잘 작성한 테스트가 많이 있다면 파이썬 코드를 변경하기가 더 쉬워질 뿐이지 결코 더 어려워지지는 않음

### 75- 디버깅 출력에는 repr 문자열을 사용해라
- 파이썬 프로그램을 디버깅할 때 print 함수와 형식화 문자열을 사용하거나 logging 내장 모듈을 사용해 출력을 만들면 아주 긴 출력이 생김
- 파이썬의 내부 정보도 일반 애트리뷰트만큼 접근하기 쉬움
- 우리에게 필요한 작업은 프로그램이 실행되는 동안 print를 호출해 상태가 어떻게 바뀌었는지 알아내고 무엇이 잘못됐는지 이해하는 것임
- `print` 함수는 인자로 받은 대상을 사람이 읽을 수 있는 문자열로 표시함. 예를 들어 기본 문자열을 출력하면 주변에 따옴표를 표시하지 않고 내용을 출력함
~~~python
print('foo 뭐시기')

>>>
foo 뭐시기
~~~
- 여러 가지 다른 방법을 사용해도 똑같은 결과를 얻을 수 있음
  - 값을 print에 전달하기 전에 str 함수를 호출함 
  - % 연산자에 '%s' 형식화 문자열 사용
  - f-문자열에서 값을 표시하는 기본 형식화 방식을 사용
  - format 내장 함수를 호출
  - __format__ 특별 메서드를 명시적으로 호출함
  - __str__ 특별 메서드를 명시적으로 호출함 
~~~python
my_value = 'foo 뭐시기'
print(str(my_value))
print('% s' % my_value)
print(f"{my_value}")
print(format(my_value))
print(my_value.__format__('s'))
print(my_value.__str__()) 
>>>
foo 뭐시기
foo 뭐시기
foo 뭐시기
foo 뭐시기
foo 뭐시기
foo 뭐시기
~~~
- 문제는 어떤 값을 사람이 읽을 수 있는 형식의 문자열로 바꿔도 이 값의 실제 타입과 구체적인 구성을 명확히 알기 어렵다는 점임. 예를 들어, print의 기본 출력을 사용하면 5라는 수와 '5'라는 문자열의 타입을 구분할 수 없음
~~~python
print(5)
print('5')

int_value = 5
str_value = '5'
print(f"{int_value} == {str_value} ?")
~~~
- 디버깅 과정에서 print를 사용한다면 이런 타입의 차이가 문제가 됨
- 디버깅을 할 때 원하는 문자열은 거의 대부분 객체를 `repr` 로 나타낸 버전임. `repr` 내장 함수는 객체의 출력 가능한 표현(printable representation)을 반환하는데, 출력 가능한 표현은 반드시 객체를 가장 명확하게 이해할 수 있는 문자열 표현이어야 함 
- 내장 타입에서 `repr` 이 반환하는 문자열은 올바른 파이썬 식임
~~~python
a = '\x07'
print(repr(a))

>>>
'\x07'
~~~
- repr이 돌려준 값을 eval 내장 함수에 넘기면 repr에 넘겼던 객체와 같은 객체가 생겨야 함  
  (물론 실전에서 eval을 호출할 때는 아주 조심해야 함)
~~~python
b = eval(repr(a))
assert a == b
~~~
- <b>print를 사용해 디버깅 할 때도 값을 출력하기 전에 repr를 호출해서 타입이 다른 경우에도 명확히 차이를 볼 수 있게 만들어야 함</b>
~~~python
print(repr(5))
print(repr('5'))

>>>
5
'5'
~~~
- repr을 호출하는 것은 % 연산자에 %r 형식화 문자열을 사용하는 것이나 f-문자열에 !r 타입 변환을 사용하는 것과 같음
~~~python
print('%r' % 5)
print('%r' % '5')

int_value = 5
str_value = '5'
print(f"{int_value!r} !- {str_value!r}")

>>>
5
'5'
5 !- '5'
~~~
- 예를 들어 파이썬 클래스의 경우 사람이 읽을 수 있는 문자열 값은 repr 값과 같음
- 이는 인스턴스를 print에 넘기면 원하는 출력이 나오므로 굳이 인스턴스에 대해 repr을 호출할 필요가 없다는 뜻
- 안타깝지만 object를 상속한 하위 클래스의 repr 기본 구현은 그다지 쓸모가 없음. 예를 들어 다음 코드는 간단한 클래스를 정의하고 그 클래스의 인스턴스를 출력함
~~~Python
class OpaqueClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

obj = OpaqueClass(1, 'foo')
print(obj)

>>>
<__main__.OpaqueClass object at 0x7fd58914ce90>
~~~
- 이 출력은 eval 함수에 넘길 수도 없고, 객체의 인스턴스 필드에 대한 정보도 전혀 들어 있지 않음
- 이 문제를 해결하는 방법은 두 가지가 있는데, 첫 번째는 객체를 다시 만들어내는 파이썬 식을 포함하는 문자열을 돌려주는 `__repr__` 특별 메서드를 직접 정의할 수 있음
~~~python
class BetterClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'BetterClass{self.x!r}, {self.y!r})'
~~~
- 이제 repr이 훨씬 더 유용한 값을 돌려줌
~~~python
class BetterClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'BetterClass({self.x!r}, {self.y!r})'

obj = BetterClass(2, '뭐시기')
print(obj)

>>>
BetterClass(2, '뭐시기')
~~~
- 클래스 정의를 마음대로 바꿀 수 없는 경우에는 `__dict__` 애트리뷰트를 통해 객체의 인스턴스 딕셔너리에 접근할 수 있음
- 다음 코드는 OpaqueClass 인스턴스의 내용을 출력함
~~~python
obj = OpaqueClass(4, 'baz')
print(obj.__dict__)

>>>
{'x': 4, 'y': 'baz'}
~~~

#### 기억해야 할 내용
- 내장 파이썬 타입 값에 대해 print를 호출하면 해당 값을 사람이 읽을 수 있게 표현한 문자열을 얻음
- <b>얻은 문자열에서는 타입 정보가 감쳐줘 있음</b>
- repr을 내장 파이썬 타입 값에 대해 호출하면 해당 값을 표현하는 출력 가능한 문자열을 얻음
- repr로 얻은 문자열을 eval 내장 함수에 전달하면 원래 값을 돌려받을 수 있음
- 형식화 문자열의 %s는 str과 마찬가지로 사람이 읽을 수 있는 문자열을 만들어냄. str, %r은 repr과 마찬가지로 출력 가능한 문자열을 만들어냄. f-문자열에서 !r 접미사를 붙이지 않고 텍스트 치환식을 사용하면 사람이 읽을 수 있는 형태의 문자열이 만들어짐
- 직접 클래스의 `__repr__` 특별 메서드를 정의해서 인스턴스의 출력 가능한 표현을 원하는 대로 만들 수 있고, 이를 통해 디버깅할 때 더 자세한 정보를 표시할 수 있음

### 76-TestCase 하위 클래스를 사용해 프로그램에서 행동 방식을 검증해라
- 파이썬에서 테스트를 작성하는 표준적인 방법은 `unittest` 내장 모듈을 쓰는 것. 예를 들어 utils.py에 다음 코드처럼 유틸리티 함수가 정의돼 있고, 다양한 입력에 대해 제대로 작동하는지 검증하고 싶다고 하자
~~~python
# utils.py
def to_str(data):
    if isinstance(data, str):
        return data
    elif isinstance(data, bytes):
        return data.decode('utf-8')
    else:
        raise TypeError('str이나 bytes를 전달해야 함'
                        f'찾은 값: {data!r}')
~~~
- 테스트를 정의하려면 `test_utils.py`,  `utils_test.py` 둘 중 하나의 이름의 파일을 만들어야 함
- 두 방식 중 어느쪽이든 우리가 좋아하는 쪽을 택하면 됨. 이 파일 안에 원하는 동작이 들어 있는 테스트를 추가함
~~~python
from unittest import TestCase, main
from utils import to_str


class UtilsTestCase(TestCase):
    def test_to_str_bytes(self):
        self.assertEqual('hello', to_str(b'hello'))

    def test_to_str_str(self):
        self.assertEqual('hello', to_str('hello'))

    def test_failing(self):
        self.assertEqual('incorrect', to_str('hello'))


if __name__ == '__main__':
    main()
~~~
- 그 후 명령줄에서 파이썬을 사용해 테스트 파일을 실행함
- 이 예제의 테스트 메서드 중에서 둘은 성공하고 하나는 실패함
~~~python
F..
======================================================================
FAIL: test_failing (__main__.UtilsTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "utils_test.py", line 13, in test_failing
    self.assertEqual('incorrect', to_str('hello'))
AssertionError: 'incorrect' != 'hello'
- incorrect
+ hello


----------------------------------------------------------------------
Ran 3 tests in 0.001s

FAILED (failures=1)
~~~
- 테스트는 TestCase의 하위 클래스로 구성됨. <b>각각의 테스트 케이스는 이름이 test라는 단어로 시작하는 메서드들임</b>
- 어떤 테스트 메서드가 아무런 Exception도 발생 시키지 않고 실행이 끝나면(assert 문에서 발생하는 AssertionError도 Exception으로 침) 테스트가 성공한 것으로 간주함
- <b>테스트 중 일부가 실패하더라도 TestCase 하위 클래스는 최초로 문제가 발생한 지점에서 실행을 중단하지 않고, 나머지 테스트 메서드를 실행해서 우리가 테스트 전체에 대해 전반적인 그림을 그릴 수 있게 해줌</b>
- 어느 한 테스트를 개선하거나 빠르게 수정한 경우, 명령줄에서 테스트를 실행할 때 테스트 모듈 내에서 해당 메서드의 경로를 지정해 원하는 테스트 메서드만 실행할 수도 있음
~~~python
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
~~~
- 원한다면 테스트 메서드 내부에 있는 구체적인 중단점(breakpoint)에서 직접 디버거를 호출해 테스트가 실패한 원인을 더 깊이 파고들 수도 있음
- TestCase 클래스는 테스트에 단언문(assertion)을 만들 때 도움이 되는 여러 도우미 메서드를 제공함
- 예를 들어 `assertEqual`은 두 값이 같은지 비교하고, `assertTrue`는 주어진 주어진 불 식이 참인지 검증하는 등 이외에도 많은 메서드가 있음(help(TestCase)를 하면 전체 목록 확인 가능)
- 이런 메서드들은 테스트가 왜 실패했는지 알 수도 있도록 모든 입력과 출력을 표시해주므로 파이썬 내장 assert 문보다 더 나음
- 예를 들어, 다음은 똑같은 테스트 케이스를 작성하면서 도우미 단언문 메서드를 사용한 경우와 단순히 단언문만 사용한 경우를 보여주는 코드임
~~~python
from unittest import TestCase, main
from utils import to_str


class AssertTestCase(TestCase):
    def test_assert_helper(self):
        expected = 12
        found = 2 * 5
        self.assertEqual(expected, found)

    def test_assert_statement(self):
        expected = 12
        found =  2 * 5
        assert expected == found

if __name__ == '__main__':
    main()
~~~
- 다음 두가지 케이스의 실패 메세지를 확인해보자
~~~python
FF
======================================================================
FAIL: test_assert_helper (__main__.AssertTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "assert_test.py", line 9, in test_assert_helper
    self.assertEqual(expected, found)
AssertionError: 12 != 10

======================================================================
FAIL: test_assert_statement (__main__.AssertTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "assert_test.py", line 14, in test_assert_statement
    assert expected == found
AssertionError

----------------------------------------------------------------------
Ran 2 tests in 0.001s

FAILED (failures=2)
~~~
- 예외가 발생하는지 검증하기 위해 with 문 안에서 컨텍스트 메니저로 사용할 수 있는 `assertRaises ` 도우미 메서드도 있음
- 이 메서드를 사용한 코드는 try/except 문과 비슷하므로, 테스트 케이스의 해당 부분에서 예외가 발생할 것으로 예상한다는 점을 아주 명확히 들어냄
~~~python
# assert_test.py
from unittest import TestCase, main
from utils import to_str


class UtilErrorTestCase(TestCase):
    def test_to_str_bad(self):
        with self.assertRaises(TypeError):
            to_str(object())

    def test_to_str_bad_encoding(self):
        with self.assertRaises(UnicodeDecodeError):
            to_str(b'\xfa\xfa')


if __name__ == '__main__':
    main()

#- 결과적으로 에러가 발생하지 않음
#- why? with 구문으로 exception 처리를 했기 때문    
~~~
- 테스트 가독성을 더 높이기 위해 TestCase 하위 클래스 안에 복잡한 로직이 들어가는 도우미 메서드를 직접 작성할 수도 있음
- 다만 <b>도우미 메서드 이름이 test로 시작하지 않아야 함</b>
- test로 시작하면 도움 메서드가 아니라 테스트 케이스로 취급하기 때문
- 도우미 메서드는 TestCase가 제공하는 단언문 메서드를 호출하지 않고 fail 메서드를 호출해서 어떤 어떤 가정이나 불변 조건을 만족하지 않았음을 확실히 표현할 수도 있음
- 예를 들어 다음 코드는 제너레이터의 동작을 검증하기 위해 만든 도우미 메서드임
~~~python 
from unittest import TestCase, main


def sum_sqaures(values):
    cumulative = 0
    for value in values:
        cumulative += value ** 2
        yield cumulative


class HelperTestCase(TestCase):
    def verify_complex_case(self, values, expected):
        expect_it = iter(expected)
        found_it = iter(sum_sqaures(values))
        test_it = zip(expect_it, found_it)

        for i, (expect, found) in enumerate(test_it):
            self.assertEqual(
                expect,
                found,
                f'잘못된 인덱스: {i}')

        #- 두 제너레이터를 모두 소진했는지 확인
        try:
            next(expect_it)
        except StopIteration:
            pass
        else:
            self.fail('실제보다 예상한 제너레이터가 더 김')

        try:
            next(found_it)
        except StopIteration:
            pass
        else:
            self.fail('예상한 제너레이터보다 실제가 더 김')



    def test_wrong_lengths(self):
        values = [1.1, 2.2, 3.3]
        expected = [
            1.1 ** 2,
        ]
        self.verify_complex_case(values, expected)


    def test_wrong_results(self):
        values = [1.1, 2.2, 3.3]
        expected = [
            1.1 ** 2,
            1.1 ** 2 + 2.2 ** 2,
            1.1 ** 2 + 2.2 ** 2 + 3.3 ** 2 + 4.4 ** 2,
                    ]
        self.verify_complex_case(values, expected)


if __name__ == '__main__':
    main()
~~~
- 도우미 메서드를 사용하면 테스트 케이스를 더 짧고 읽기 좋게 만들 수 있음
- 게다가 오류 메세지도 더 이해하기 쉬워짐
~~~python
======================================================================
FAIL: test_wrong_lengths (__main__.HelperTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "helper_test.py", line 45, in test_wrong_lengths
    self.verify_complex_case(values, expected)
  File "helper_test.py", line 21, in verify_complex_case
    f'잘못된 인덱스: {i}')
AssertionError: 1.2100000000000002 != 1 : 잘못된 인덱스: 0

======================================================================
FAIL: test_wrong_results (__main__.HelperTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "helper_test.py", line 55, in test_wrong_results
    self.verify_complex_case(values, expected)
  File "helper_test.py", line 21, in verify_complex_case
    f'잘못된 인덱스: {i}')
AssertionError: 36.3 != 16.939999999999998 : 잘못된 인덱스: 2

----------------------------------------------------------------------
Ran 2 tests in 0.001s
~~~
- 일반적으로는 한 TestCase 하위 클래스 안에 관련된 일련의 테스트를 함께 정의함
- 미묘한 경우(edge case)가 많다면 각 함수를 서로 다른 TestCase 하위 클래스에 정의할 때도 있음
- <b>그렇지 않다면 한 모듈 안에 포함된 모든 테스트 함수를 한 TestCase 하위 클래스에 정의한다</b>
- 각 기본 클래스에 대응하는 TestCase 하위 클래스를 별도로 만들고, 각 TestCase 하위 클래스 안에 대응하는 기본 클래스의 모든 메서드에 대한 테스트 메서드를 정의하는 경우도 있음
- `TestCase` 클래스가 제공하는 `subTest` 도우미 메서드를 사용하면 한 테스트 메서드 안에 여러 테스트를 정의할 수 있음
- 이 `subTest`를 사용하면 준비 코드를 작성하지 않아도 됨. 특히 데이터 기반 테스트를 작성할 때 `subTest`가 도움이 되며, subTest를 사용하면 하위 테스트 케이스 중 하나가 실패해도 다른 테스트 케이스를 계속 진행할 수 있음
- 다음 코드는 이런 특성을 보여주고자 정의한 데이터 기반 테스트 정의임
~~~Python
# data_driven_test.py
from unittest import TestCase, main
from utils import to_str

class DataDrivenTestCase(TestCase):
    def test_good(self):
        good_cases = [
            (b'my bytes', 'my bytes'),
            ('no error', b'no error'),
            ('other str', 'other str'),
        ]
        for value, expected in good_cases:
            with self.subTest(value):
                self.assertEqual(expected, to_str(value))

    def test_bad(self):
        bad_cases = [
            (object(), TypeError),
            (b'\xfa\xfa', UnicodeDecodeError),
        ]
        for value, exception in bad_cases:
            with self.subTest(value):
                with self.assertRaises(exception):
                    to_str(value)


if __name__ == '__main__':
    main()
~~~
- no error 테스트 케이스는 실패하면서 어디가 잘못됐는지 알려주는 오류 메세지를 표시해주지만, 다른 테스트 케이스는 계속 실행되고 통과함
~~~python
.
======================================================================
FAIL: test_good (__main__.DataDrivenTestCase) [no error]
----------------------------------------------------------------------
Traceback (most recent call last):
  File "data_driven_test.py", line 14, in test_good
    self.assertEqual(expected, to_str(value))
AssertionError: b'no error' != 'no error'

----------------------------------------------------------------------
Ran 2 tests in 0.001s

FAILED (failures=1)
~~~

#### 기억해야 할 내용
- unittest 내장 모듈 안에 있는 TestCase 클래스의 하위 클래스를 정의하고 테스트하려는 동작마다 메서드를 정의함으로써 테스트를 정의할 수 있음. TestCase 하위 클래스 안에서 테스트 메서드의 이름은 test로 시작해야 함
- 테스트 안에서는 파이썬 내장 `aseert` 문을 사용하지 말고, `assertEqual`과 같이 TestCase 클래스에 정의된 여러 가지 도우미 메서드를 사용해 원하는 동작을 확인해라
- 준비 코드를 줄이려면 `subTest` 도우미 메서드를 사용해 데이터 기반 테스트를 정의해라

### 77- setUp, tearDown, setUpModule, tearDownModule을 사용해 각각의 테스트를 격리해라
- TestCase 클래스에서는 테스트 메서드를 실행하기 전에 테스트 환경을 구축해야 하는 경우가 자주 있음
- <b>이런 테스트 과정을 테스트 하네스라고 부르기도 함</b>
- 그렇게 하려면 TestCase 하위 클래스 안에서 setUp과 tearDown 메서드를 오버라이드 해야함
- setUp은 테스트 메서드를 실행하기 전에 호출되고, tearDown 메서드는 테스트 메서드를 실행한 다음에 호출됨
- 두 메서드를 활용하면 각 테스트를 서로 격리된 상태에서 실행할 수 있음
- 테스트 간의 격리는 테스트를 제대로 진행하기 위해 가장 중요한 실무 지침임
- 예를 들어, 다음은 각각의 테스트를 진행하기 전에 임시 디렉터리를 만들고 테스트가 끝난 후 디렉터리 내용을 지우는 TestCase 클래스를 정의한 코드임
~~~python
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main


class EnvironmentTest(TestCase):
    def setUp(self):
        self.test_dir = TemporaryDirectory()
        self.test_path = Path(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_modify_name(self):
        with open(self.test_path / 'data_bin', 'w') as f:
            ...


if __name__ == '__main__':
    main()
~~~
- 프로그램이 복잡해지면 코드를 독립적으로 실행(목(mock) 등)하는 대신에 여러 모듈 사이의 end-to-end 상호작용을 검증하는 테스트가 필요할 수도 있음
- 이 부분이 단위 테스트와 통합 테스트 간의 서로 다른 점임
- 파이썬에서는 두 테스트가 필요한 이유는 서로 동일함. 바로 모듈이 제대로 작동하는지 검증하기 전에는 모듈이 실제로 제대로 작동하는지 알 수 없기 때문임. 따라서 파이썬에서는 두 유형의 테스트가 모두 중요함
- 흔히 발생하는 문제로 통합 테스트에 필요한 테스트 환경을 구축할 때 계산 비용이 너무 비싸거나, 너무 오랜 시간 소요될 경우가 있음. 예를 들어, 통합 테스트를 진행하기 위해 DB 프로세스를 시작하고 데이터베이스가 모든 인덱스를 메모리에 읽어올 때까지 기다려야 할 수도 있음
- 이런 지연 시간이 있으면 TestCase 클래스의 setUp과 tearDown 메서드에서 테스트를 준비하고 정리하는 과정이 비실용적임 
- 이런 상황을 해결하기 위해 <b>unittest 모듈은 모듈 단위의 테스트 하네스 초기화를 지원함</b> 
- 이 기능을 활용하면 비싼 자원을 단 한번만 초기화 하고, 초기화를 반복하지 않고도 testCase 클래스와 테스트 메서드를 실행할 수 있음
- 나중에 모듈 안에 모든 테스트가 끝나면 테스트 하네스를 한 번만 정리하면 됨
- 다음 코드는 TestCase 클래스가 들어 있는 모듈 안에 `setUpModule`과 `tearDownModule` 메서드를 정의해 위 동작을 사용함
~~~python
from unittest import TestCase, main

def setUpModule():
    print("* 모듈 설정")

def tearDownModule():
    print("* 모듈 정리")

class IntegrationTest(TestCase):
    def setUp(self):
        print("* 테스트 설정")

    def tearDown(self):
        print("* 테스트 정리")

    def test_end_to_end1(self):
        print("* 테스트1")

    def test_end_to_end2(self):
        print("* 테스트2")

if __name__ == '__main__':
    main()

$ python3 integration_test.py
* 모듈 설정
* 테스트 설정
* 테스트1
* 테스트 정리
.* 테스트 설정
* 테스트2
* 테스트 정리
.* 모듈 정리
~~~

#### 기억해야 할 내용
- 단위 테스트(함수, 클래스 등의 기본 단위를 격리시켜 검증하는 테스트)와 통합 테스트를 모두 작성하는 것이 중요
- setUp과 tearDown 메서드를 사용하면 테스트 사이를 격리할 수 있으므로 더 깨끗한 테스트 환경을 제공할 수 있음
- 통합 테스트의 경우 모듈 수준의 함수인 `setUpModule`과 `tearDownModule`을 사용하면 테스트 모듈과 모듈 안에 포함된 모든 TestCase 클래스의 전체 생명 주기 동안 필요한 테스트 하네스를 관리할 수 있음

### 78- 목(mock)을 사용해 의존 관계가 복잡한 코드를 테스트해라
- 테스트를 작성할 때 필요한 공통 기능으로, 사용하기에 너무 느리거나 어려운 함수와 클래스의 mock을 만들어 사용하는 기능이 있음
- 예를 들어 동물원에서 먹이 주는 시간을 관리하는 프로그램이 필요하다고 하자. 다음 코드는 특정 종에 속하는 모든 동물과 그 동물들에게 최근에 먹이를 준 시간을 데이터베이스에 질의해서 반환하는 함수
~~~python
class DatabaseConnection:
    ...

def get_animals(database, species):
    # 데이터베이스에 질의함
    ...
    # (이름, 급양 시간) 튜플 리스트를 반환함
~~~
- 이 함수를 테스트 할 때 사용할 DatabaseConnection 인스턴스를 어떻게 얻을 수 있을까?
- 다음은 DatabaseConnection 인스턴스를 만들어 테스트 대상 함수에 전달하는 코드임
~~~python
database = DatabaseConnection('localhost', '4444')
get_animals(database, '미어캣')

>>>
Not connected
~~~
- 물론 실행 중인 데이터베이스가 없으므로 테스트는 실패함. 한 가지 해결책은 테스트할 때 정말로 데이터베이스 서버를 기동하고 그 서버에 연결하는 것
- 하지만 데이터베이스를 완전히 자동으로 실행하려면, 단순한 단위 테스트를 진행하는 경우에도 스키마를 설정하고 데이터를 채워넣는 등 너무 많은 작업 필요
- 더 나아가 DB 서버를 기동하려면 실제로 많은 시간이 소요되기 때문에 단위 테스트 진행이 오래 걸리고 테스트 관리가 어려워질 수 있음
- 더 나은 방법은 데이터베이스를 mocking 하는 것. mock은 자신이 흉내 내려는 대상에 의존하는 다른 함수들이 어떤 요청을 보내면 어떤 응답을 보내야 할 지 알고, 요청에 따라 적절한 응답을 돌려줌
- mock과 fake는 구분하는 것이 중요함. fake는 DatabaseConnection의 기능을 대부분 제공하지만 더 단순한 단일 스레드 인메모리 데이터베이스를 사용함
- 파이썬 `unittest.mock` 내장 모듈을 사용하면 mock을 만들고 테스트에 사용할 수 있음
- 다음 코드는 DB에 실제 접속하지 않고 `get_animals` 함수를 시뮬레이션 하는 Mock 인스턴스를 보여줌
~~~python
from datetime import datetime
from unittest.mock import Mock

mock = Mock(spec=get_animals)
expected = [
    ('점박이', datetime(2020, 6, 5, 11, 15)),
    ('털보', datetime(2020, 6, 5, 12, 30)),
    ('조조', datetime(2020, 6, 5, 12, 45))
]
mock.return_value = expected
~~~
- Mock 클래스는 목 함수를 만듬. 목의 return_value 애트리뷰트는 목이 호출됐을 때 돌려줄 값
- spec 인자는 목이 작동을 흉내 내야 하는 대상이며, 목은 대상에 대한 잘못된 요청이 들어오면 오류를 발생시킴. 여기서는 대상이 함수임
- 예를 들어, 다음은 목 함수를 애트리뷰트가 들어 있는 객체처럼 다룰 때 발생하는 오류를 보여줌
~~~python
#- does_not_exists 객체를 호출 --> error attribute가 없음
mock.does_not_exists

Traceback...
AttributeError: Mock object has no attribute 'does_not_exists'
~~~
- 일단 목이 생기면 목을 호출하고, 목이 반환하는 값을 받고 , 반환받은 값이 예상하는 값인지 검증할 수 있음
- 여기서 목이 database를 실제로 사용하지는 않기 때문에 고유한 object 값을 목의 database인자로 넘김
- 우리가 관심있는 것은 `DatabaseConnection` 인스턴스를 필요로 하는 객체들이 제대로 작동하기 위해 공급받은 database 파라미터를 제대로 연결해 사용하는지 여부뿐임
~~~python
database = object()
result = mock(database, '미어캣')
assert result == expected
~~~
- 이렇게 하면 목이 제대로 응답했는지를 검증할 수 있음. 하지만 목을 호출한 코드가 제대로 인자를 목에게 전달했는지 어떻게 알 수 있을까? 이를 위해 Mock 클래스는 `assert_called_once_with`라는 메서드를 제공함
- 이 메서드는 어떤 파라미터가 목 객체에게 정확히 한 번만 전달됐는지 검증함
~~~python
mock.assert_called_once_with(database, '미어캣')
~~~
- 잘못된 파라미터를 전달하면 예외가 발생하고 `assert_called_once_with` 단언문을 사용한 TestCase는 실패함
~~~python
mock.assert_called_once_with(database, '기린')

>>>
Actual call: mock(<object object at 0x7f828b87b550>, '미어캣')
~~~
- 여기서 database의 경우처럼 목에 전달되는 개별 파라미터에 관심이 없다면 `unittest.mock.ANY` 상수를 사용해 어떤 인자를 전달해도 관계없다고 표현할 수 있음
- 또 Mock의 `assert_called_with` 메서드를 사용하면, 가장 최근에 목을 호출할 때 어떤 인자가 전달됐는지 확인할 수도 있음
~~~python
from unittest.mock import ANY

mock = Mock(spec=get_animals)
mock('database 1', '토끼')
mock('database 2', '들소')
mock('database 3', '미어캣')

mock.assert_called_with(ANY, '미어캣')
~~~
- 테스트 대상 객체의 동작에서 어떤 파라미터가 중요하지 않을 때는 ANY가 유용함. 때로는 여러 파라미터에 대한 기댓값을 하나하나 지정해 테스트를 과도하게 구체적으로 만들기보다는 ANY를 좀 더 자유롭게 사용해서 테스트를 느슨하게 하면 좋을 때가 있음
- Mock 클래스는 예외 발생을 쉽게 모킹할 수 있는 도구도 제공함
~~~python
class MyError(Exception):
    pass

mock = Mock(spec=get_animals)
mock.side_effect = MyError('에구머니나! 큰 문제 발생')
result = mock(database, '미어캣')

>>>
MyError: 에구머니나! 큰 문제 발생
~~~
- Mock 클래스에는 더 많은 기능이 들어 있으니 help(unittest.mock.Mock)에서 모든 기능을 꼭 살펴보자
- Mock이 작동하는 매커니즘을 설명했으므로, 이제 실제 테스트 상황에서 단위 테스트를 작성하기 위해 목을 효율적으로 사용하는 방법을 살펴보자
- 다음 코드는 데이터베이스와 상호작용하기 위한 몇 가지 함수를 사용해 동물원의 여러 동물에게 먹이를 여러 차례 급양하는 함수를 정의함
~~~python
def get_food_period(database, species):
    return 10

def feed_animal(database, name, when):
    return 10

def do_rounds(database, species):
    now = datetime.utcnow()
    feeding_timedelta = get_food_period(database, species)
    animals = get_animals(database, species)
    fed = 0

    for name, last_mealtime  in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_animal(database, name, now)
            fed += 1

    return fed
~~~
- 우리가 만들 테스트의 목적은 `do_rounds`가 실행될 때 원하는 동물에게 먹이가 주어졌는지, 데이터베이스에 최종 급양 시간이 기록되는지, 함수가 반환한 전체 급양 횟수가 제대로인지 검증하는 것
- 이를 위해 `datetime_utcnow`를 모킹해서 테스트를 실행하는 시간이 서머타임이나 다른 일시적인 변화에 영향을 받지 않게 만듬
- 데이터베이스에서 값을 가져와야 하는 `get_food_period`와 `get_animals`도 모킹해야 함
- 그리고 `feed_animal`을 모킹해서 데이터베이스에 다시 써야 하는 데이터를 받을 수 있게 만들어야 함
- 문제는 다음과 같음. 목 함수를 만드는 방법을 알고 원하는 값을 설정하는 방법도 아는데, 테스트 대상인 `do_rounds` 함수가 실제 함수가 아닌 목 함수를 쓰게 바꾸는 방법은 무엇일까?  
 --> 모든 목 함수 요소를 키워드 인자로 받도록 함
~~~python
def do_rounds(database, species, *,
              now_func=datetime.utcnow,
              food_func=get_food_period,
              animals_func=get_animals,
              feed_func=feed_animal):

    now = now_func()
    feeding_timedelta = food_func(database, species)
    animals = animals_func(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_func(database, name, now)
            fed += 1

    return fed
~~~
- 이 함수를 테스트하려면 모든 Mock 인스턴스를 미리 만들고 각각의 예상 반환 값을 설정해야 함
~~~python
now_func = Mock(spec=datetime.utcnow)
now_func.return_value = datetime(2020, 6, 5, 15, 45)

food_func = Mock(spec=get_food_period)
food_func.return_value = timedelta(hours=3)

animals_func = Mock(spec=get_animals)
animals_func.return_value = [
    ('점박이', datetime(2020, 6, 5, 11, 15)),
    ('털보', datetime(2020, 6, 5, 12, 30)),
    ('조조', datetime(2020, 6, 5, 12, 45)),
]

feed_func = Mock(spec=feed_animal)
~~~
- 그 다음에 목을 `do_rounds` 함수에 넘겨서 디폴트 동작을 오버라이드하면 `do_rounds` 함수를 테스트 할 수 있음
~~~Python
database = object()

#-  털보와 조조가 3시간이 지났으므로 결과는 fed = 2가 나옴.
result = do_rounds(
    database,
    '미어캣',
    now_func=now_func,
    food_func=food_func,
    animals_func=animals_func,
    feed_func=feed_func)

assert result == 2
~~~
- 마지막으로 `do_rounds`가 의존하는 함수가 모두 우리가 예상하는 값을 전달받았는지 검증할 수 있음
~~~python
food_func.assert_called_once_with(database, '미어캣')
animals_func.assert_called_once_with(database, '미어캣')

feed_func.assert_has_calls(
    [
        call(database, '점박이', now_func.return_value),
        call(database, '털보', now_func.return_value),
    ],
    any_order=True #- 호출순서는 고려하지 않음
)
~~~
- `datetime.utcnow` 목의 경우 함수 반환 값을 통해 값을 검증할 수 있기 때문에 파라미터 값이나 호출됫 횟수는 검증하지 않음
- `get_food_period`나 `get_animals`에 대해서는 `assert_called_once_with`를 사용해 단 한번만 호출됐는지, 우리가 원하는 인자를 받았는지 검증함
- `feed_animals` 함수는 `unittest.mock.call` 도우미 함수와 `assert_has_calls` 메서드를 사용해 데이터베이스에 기록하는 함수가 두 번 호출됐는지를 검증함
- 이런 식으로 키워드 방식으로만 호출할 수 있는 인자를 사용해 목을 주입하는 방식은 잘 작동하지만, 코드가 장황해지고 테스트 대상 함수를 모두 변경해야 한다는 단점이 있음
- `unittest.mock.patch` 관련 함수들은 목 주입을 더 쉽게 만들어줌
- `path` 함수는 임시로 모듈이나 클래스의 애트리뷰트에 다른 값을 대입해줌. `patch`를 사용하면 앞에서 본 데이터베이스에 접근하는 함수하는 임시로 다른 함수로 대치할 수 있음
- 다음 코드는 `patch`를 사용해 `get_animals`를 목으로 대치함
~~~python
from unittest.mock import patch
print("패치 외부:", get_animals)

with patch('__main__.get_animals'):
    print("패치 내부:", get_animals)

print('다시 외부:', get_animals)
~~~
- 다양한 모듈이나 클래스, 애트리뷰트에 대해 patch를 사용할 수 있음
- patch를 with 문 내에서 사용할 수도 있고, 함수 데코레이터로 사용할 수도 있으며, TestCase 클래스 안의 setUp이나 tearDown 메서드에서 사용할 수도 있음
- 모든 옵션을 보려면 `help(unittest.mock.patch)`를 살펴보라 
- 하지만 patch를 모든 경우에 사용할 수 있는 것은 아님. 예를 들어 `do_rounds`를 테스트하려면 현재 시간을 돌려주는 `datetime.utcnow` 클래스 메서드를 모킹해야 함. 하지만 `datetime` 클래스가 C 확장 모듈이므로 파이썬에서 다음과 같이 변경할 수는 없음
~~~python
with patch('datetime.datetime.utcnow'):
    datetime.utcnow.return_value = fake_now

>>>
TypeError: can't set attributes of built-in/extension type 'datetime.datetime'
~~~
- 이를 우회하려면 patch를 적용할 수 있는 다른 도우미 함수를 만들어서 시간을 얻어야 함
~~~Python
def get_do_rounds_time():
    return datetime.utcnow()

def do_rounds(database, species):
    now = get_do_rounds_time()

with patch('__main__.get_do_rounds_time'):
    ...
~~~
- 다른 방법으로, `datetime.utcnow` 목에 대해서는 키워드로 호출해야만 하는 인자를 사용하고 다른 모든 목에 대해서는 `patch`를 사용할 수도 있음
~~~python
def do_rounds(database, species, *, utcnow=datetime.utcnow):
    now = utcnow()
    feeding_timedelta = get_food_period(database, species)
    animals = get_animals(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_func(database, name, now)
            fed += 1

    return fed

#
from unittest.mock import DEFAULT

with patch.multiple('__main__',
                    autospec=True,
                    get_food_period=DEFAULT,
                    get_animals=DEFAULT,
                    feed_animal=DEFAULT):
    now_func = Mock(spec=datetime.utcnow)
    now_func.return_value = datetime(2020, 6, 5, 15, 45)
    get_food_period.return_value = timedelta(hours=3)
    get_animals.return_value = [
        ('점박이', datetime(2020, 6, 5, 11, 15)),
        ('털보', datetime(2020, 6, 5, 12, 30)),
        ('조조', datetime(2020, 6, 5, 12, 45))
    ]

    result = do_rounds(database, '미어캣', utcnow=now_func)
    assert result == 2
~~~
- 설정이 끝나면 테스트를 실행하고 `patch.multiple` 을 사용한 with문 안에서 제대로 목 호출이 이뤄졌는지 검증할 수 있음
~~~python
food_func.assert_called_once_with(database, '미어캣')
animals_func.assert_called_once_with(database, '미어캣')

feed_func.assert_has_calls(
    [
        call(database, '점박이', now_func.return_value),
        call(database, '털보', now_func.return_value)
    ],
    any_order=True)
~~~
- `patch.multiple` 키워드 인자들은 `__main__` 모듈에 있는 이름 중에서 테스트하는 동안에만 변경하고 싶은 이름에 해당됨
- `DEFAULT` 값은 각 이름에 대해 표준 Mock 인스턴스를 만들고 싶다는 뜻
- `autospec=True` 를 지정했기 때문에 만들어진 목은 각각이 시뮬레이션하기로 돼 있는 객체(__main__ 모듈에 있는 이름이 같은 원객체)의 명세를 따름
- 이런 식으로 목을 사용해도 제대로 작동하지만, 우리가 만든 코드를 테스트하기 좋게 리펙터링하면 테스트의 가독성이 더 좋아지고 테스트 준비 코드도 줄어들 수 있음 

#### 기억해야 할 내용
- `unittest.mock` 모듈은 Mock 클래스를 사용해 인터페이스의 동작을 흉내낼 수 있음
- 테스트를 할 때 테스트 대상 코드가 호출해야 하는 의존관계 함수를 설정하기 힘들 경우에는 목을 사용하면 유용함
- 목을 사용할 때는 테스트 대상 코드의 동작을 검증하는 것과 테스트 대상 코드가 호출하는 의존 관계들이 호출되는 방식을 검증하는 것이 모두 중요. `Mock.assert_called_once_with`나 이와 비슷한 메서드를을 사용해 이런 검증을 사용
- 목을 테스트 대상 코드에 주입할 때는 키워드를 사용해 호출해야 하는 인자를 쓰거나 `unittest.mock.patch` 또는 이와 비슷한 메서드들을 사용함

### 79- 의존 관계를 캡슐화해 모킹과 테스트를 쉽게 만들라
- 앞서 `unittest.mock` 내장 모듈의 기능을 활용해 데이터베이스 등에 복잡하게 의존하는 테스트를 작성하는 방법을 설명함
- 하지만 이런 방식으로 만든 테스트 케이스에는 준비 코드가 많이 들어가므로 테스트 코드를 처음 보고 테스트가 무엇을 검증하려는 것인지 이해하기 어려울 수 있음
- 이러한 테스트를 개선하는 한 가지 방법은 `DatabaseConnection` 객체를 인자로 직접 전달하는 대신 래퍼 객체를 사용해 데이터페이스 인터페이스를 캡슐화 하는 것
- 더 나은 추상화를 사용하면 목이나 테스트를 더 쉽게 만들 수 있으므로 때로는 더 나은 추상화를 사용하도록 코드를 리펙터링할 만한 가치가 있음
- 다음 코드는 이전 Better way에서 다룬 여러 가지 데이터베이스 도우미 함수를 개별 함수가 아니라 한 클래스 안에 들어 있는 메서드가 되도록 다시 정의함
~~~python
lass ZooDatabase:
    ...

    def get_animals(self, species):
        ...

    def get_food_period(self, species):
        ...

    def feed_animal(self, name, when):
        ...
~~~
- 이제 `do_rounds` 함수가 ZooDatabase 객체의 메서드를 호출하도록 변경할 수 있음
~~~python
def do_rounds(database, species, *, utcnow=datetime.utcnow):
    now = utcnow()
    feeding_timedelta = database.get_food_period(species)
    animals = database.get_animals(species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) >= feeding_timedelta:
            database.feed_animal(name, now)
            fed += 1
    return fed
~~~
- 이제는 `unittest.mock.patch`를 사용해 목을 테스트 대상 코드에 주입할 필요가 없으므로 `do_rounds`에 대한 테스트를 작성하기가 더 쉬움
- path를 사용하는 대신, 이제는 ZooDatabase를 표현하는 Mock 인스턴스를 만들어 do_rounds의 database로 넘길 수 있음 . Mock 클래스는 자신의 애트리뷰트에 대해 이뤄지는 모든 접근에 대해 목 객체를 반환함
- 이런 애트리뷰트들을 메서드처럼 호출할 수 있고, 이 애트리뷰트들을 사용해 호출 시 반환될 예상 값을 설정하고 호출 여부를 검증할 수 있음
- 이런 기능을 통해 클래스 안에 있는 모든 메서드에 대한 목을 쉽게 제공할 수 있음
~~~python 
database = Mock(spec=ZooDatabase)
print(database.feed_animal)
database.feed_animal()
database.feed_animal.assert_any_call()

>>>
<Mock name='mock.feed_animal' id='140550663150288'>
~~~
- ZooDatabase 캡슐화를 사용하도록 Mock 설정 코드를 다시 작성할 수 있음
~~~python
from datetime import timedelta
from unittest.mock import call

now_func = Mock(spec=datetime.utcnow)
now_func.return_value = datetime(2019, 6, 5, 15, 45)

database = Mock(spec=ZooDatabase)
database.get_food_period.return_value = timedelta(hours=3)
database.get_animals.return_value = [
    ('점박이', datetime(2019, 6, 5, 11, 15)),
    ('털보', datetime(2019, 6, 5, 12, 30)),
    ('조조', datetime(2019, 6, 5, 12, 55))
]
~~~
- 이제 테스트 대상 함수를 실행하고, 함수가 의존하는 모든 메서드가 예상대로 호출되었는지 확인 가능
~~~python
result = do_rounds(database, '미어캣', utcnow=now_func)
assert result == 2

database.get_food_period.assert_called_once_with('미어캣')
database.get_animals.assert_called_once_with('미어캣')
database.feed_animal.assert_has_calls(
    [
        call('점박이', now_func.return_value),
        call('털보', now_func.return_value),
    ],
    any_order=True)
~~~
- 클래스를 모킹할 때 spec 파라미터를 Mock에 사용하면, 테스트 대상 코드가 실수로 메서드 이름을 잘못 사용하는 경우를 발견할 수 있으므로 특히 도움이 됨
- 테스트 대상 코드와 단위 테스트 양쪽에서 메서드 이름을 똑같이 잘못 사용하는 오류를 저질러서 프로덕션 가서야 실제 오류를 발견하게 되는 함정을 예방할 수 있음
~~~python
database.bad_method_name()
~~~
- 이 프로그램을 중간 수준의 통합 테스트와 함께 end-to-end로 테스트하고 싶다면 여전히 프로그램에 ZooDatabase를 주입할 방법이 필요
- 의존 관계 주입(dependency injection)의 연결점 역할을 하는 도우미 함수를 만들어 ZooDatabase를 프로그램에 주입할 수 있음
- 다음 코드에서는 global 문을 사용해 모듈 영역에 ZooDatabase를 캐시해주는 도우미 함수를 정의함
~~~python
DATABASE = None

def get_database():
    global DATABASE
    if DATABASE is None:
        DATABASE = ZooDatabase()
    return DATABASE

def main(argv):
    database = get_database()
    species = argv[1]
    count = do_rounds(database, species)
    print(f'급양: {count} {species}')
    return 0
~~~
- 이제 patch를 사용해 ZooDatabase를 주입하고, 테스트를 실행하고, 프로그램 출력을 검증할 수 있음
- 여기서는 목 `datetime.utcnow`를 사용하지 않고 단위 테스트와 비슷한 결과를 낼 수 있도록 목이 반환하는 데이터베이스 레코드의 시간을 현재 시간에 대한 상대적인 값으로 설정
~~~python
import contextlib
import io
from unittest.mock import patch

with patch('__main__.DATABASE', spec=ZooDatabase):
    now = datetime.utcnow()

    DATABASE.get_food_period.return_value = timedelta(hours=3)
    DATABASE.get_animals.return_value = [
        ('점박이', now - timedelta(minutes=4.5)),
        ('털보', now - timedelta(hours=3.25)),
        ('조조', now - timedelta(hours=3)),
    ]

    fake_stdout = io.StringIO()
    with contextlib.redirect_stdout(fake_stdout):
        main(['프로그램 이름', '미어캣'])

    found = fake_stdout.getvalue()
    expected = '급양: 2 미어캣\n'

    assert found == expected
~~~
- 결과가 예상한 값과 맞아 떨어짐. 이런 통합 테스트도 쉽게 만들 수 있었던 이유는 테스트를 쉽게 작성할 수 있도록 프로그램을 재구현했기 때문

#### 기억해야 할 내용
- 단위 테스트를 작성할 때 목을 만들기 위해 반복적인 준비 코드를 많이 사용해야 한다면, 테스트 대상이 의존하는 다른 기능들을 쉽게 모킹할 수 있는 클래스로 캡슐하는 것이 좋음
- unittest.mock 내장 모듈의 Mock 클래스는 클래스를 시뮬레이션할 수 있는 새로운 목을 반환함
- 이 목은 목 메서드처럼 작동할 수 있고 클래스 내 각각의 애트리뷰트에 접근할 수도 있음
- 단대단 테스트를 위해서는 테스트에 사용할 목 의존 관계를 주입하는 데 명시적인 연결점으로 쓰일 수 있는 도우미 함수를 더 많이 포함하도록 코드를 리펙터링하는 것이 좋음

### 80-pdb를 사용해 대화형으로 디버깅해라
- 프로그램을 개발하다 보면 누구나 버그와 마주치기 마련임. print 함수를 사용하면 다양한 문제의 근원을 추적할 수 있음
- 한편 문제가 될 법한 구체적인 경우에 대한 테스트를 작성하는 것도 문제를 격리시키는 좋은 방법임
- 하지만 이런 도구만으로는 버그의 근본적인 이유를 찾기에 충분하지 않음. 더 강력한 도구가 필요하다면 파이썬 내장 대화형 디버거를 사용해보아라
- 디버거를 사용하면 프로그램의 상태를 들여다보고, 지역 변수를 출력하고, 파이썬 프로그램을 한 번에 한 문장씩 실행할 수 있음
- 대부분의 다른 프로그래밍 언어에서 디버거를 사용할 때는 소스 파일에서 프로그램 실행을 일시 중단하고 싶은 줄을 지정하고 프로그램을 실행함
- <b>이와 반대로 파이썬에서 디버거를 사용하는 가장 편한 방법은 문제를 조사하기에 가장 적합한 지점에서 프로그램이 디버거를 초기화할 수 있게 프로그램을 변경하는 것</b>
- 이는 파이썬 프로그램을 일반적인 상태로 시작하는 경우와 디버거로 시작하는 경우에 차이가 없다는 뜻임
- 디버거를 초기화하기 위해 해야 할 일은 `breakpoint` 내장 함수를 호출하는 것뿐
- 이 함수는 pdb 내장 모듈을 임포트하고 `set_trace` 함수를 실행하는 것과 똑같은 일을 함
~~~python
import math


def compute_rmse(observed, ideal):
    total_err_2 = 0
    count = 0
    for got, wanted in zip(observed, ideal):
        err_2 = (got - wanted) ** 2
        breakpoint() #- 여기서 디버거 시작
        total_err_2 += err_2
        count += 1

    mean_err = total_err_2 / count
    rmse = math.sqrt(mean_err)
    return rmse

result = compute_rmse(
    [1.8, 1.7, 3.2, 6],
    [2, 1.5, 3, 5]
)
~~~
- breakpoint가 실행되자마자, breakpoint 바로 다음 줄로 실행이 옮겨가기 전에 프로그램 실행이 일시 중단됨
- 프로그램을 시작한 터미널에서는 대화형 파이썬 셀이 시작됨
~~~python
(venv) heojaehun@jaebigui-MacBookPro effectivePython % python3 main.py 
> /Users/heojaehun/gitRepo/TIL/effectivePython/main.py(10)compute_rmse()
-> total_err_2 += err_2
(Pdb) 
~~~
- (Pdb) 프롬프트에서 p <이름> 으로 지역 변수 이름을 입력하면 변수에 저장된 값을 출력할 수 있음
- `locals` 내장 함수를 호출하면 모든 지역변수 목록을 볼 수 있음
- (Pdb) 프롬포트에서는 모듈을 임포트하거나, 새로운 객체를 만들거나, help 내장 함수를 실행하거나, 심지어는 프로그램의 일부를 변경할 수도 있음
- 추가로 디버거는 프로그램 실행을 제어하고 이해할 수 있게 도와주는 여러 가지 특별한 명령을 제공함
- help를 입력하면 모든 명령어 목록을 볼 수 있음
- 다음 세 가지 명령은 실행 중인 프로그램을 관찰할 때 매우 유용
  - `where`: 현재 실행 중인 프로그램의 호출 스택을 출력. 이 명령을 사용하면 실행 중인 프로그램의 현재 위치를 알 수 있고, `breakpoint` 트리거가 어떻게 발동됐는지 알 수 있음
  - `up`: 실행 호출 스택에서 <b>현재 관찰 중인 함수를 호출한 쪽으로 호출 스택 영역을 한 단계 이동</b>해서 해당 함수의 지역 변수를 관찰할 수 있도록 함, u만 써도 됨
  - `down`: <b>실행 호출 스택에서 한 수준 아래로 호출 스택 영역을 이동</b>함. Down 대신 d만 써도 됨
- 현재 상태를 살펴본 후에는 다음 다섯 가지 디버거 명령을 사용해 프로그램 실행을 다양한 방식으로 제어할 수 있음
  - `step`: 프로그램을 다음 줄까지 실행한 다음 제어를 디버거로 돌려서 디버거 프롬포트를 표시  
  소스 코드 다음 줄에 함수를 호출하는 부분이 있다면 해당 함수의 첫 줄에서 디버거로 제어가 돌아옴
  - `next`: 프로그램을 다음 줄까지 실행한 다음 제어를 디버거로 돌려서 디버거 프롬포트를 표시. 소스 코드의 다음 줄에 함수를 호출하는 부분이 있다면, 해당 함수에서 반환된 다음에 제어가 디버거로 돌아옴
  - `return`: 현재 함수에서 반환될 때까지 프로그램을 실행한 후 제어가 디버거로 돌아옴
  - `contunue`: 다음 중단점에 도달할 때까지 프로그램을 계속 실행함(프로그램 소스 코드에 있는 breakpoint 호출이나 디버거에서 설정한 중단점에서 제어가 디버거에게 돌아옴)  
  실행하는 중에 중단점을 만나지 못하면 프로그램 실행이 끝날 때까지 프로그램을 계속 실행함
  - `quit`: 디버거에서 나가면서 프로그램도 중단시킴. 문제의 원인을 찾았거나, 프로그램을 너무 많이 실행했거나, 프로그램을 수정한 후 다시 시도해봐야 할 때 이 명령 사용
- 프로그램 어디에서든 breakpoint 함수를 호출할 수 있음. 디버깅하려는 문제가 어떤 구체적인 조건에서만 발생한다는 사실을 알고 있다면, 해당 조건을 만족시킨 후 breakpoint를 호출하는 평범한 파이썬 코드를 추가할 수 있음
- 예를 들어 다음 코드에서는 데이터 지점의 오류 제곱이 1보다 클 때만 디버거를 시작함
~~~python
import math


def compute_rmse(observed, ideal):
    total_err_2 = 0
    count = 0
    for got, wanted in zip(observed, ideal):
        err_2 = (got - wanted) ** 2
        if err_2 >= 1:  #- true인 경우만 디버거 시작
            breakpoint()
        total_err_2 += err_2
        count += 1

    mean_err = total_err_2 / count
    rmse = math.sqrt(mean_err)
    return rmse

result = compute_rmse(
    [1.8, 1.7, 3.2, 6],
    [2, 1.5, 3, 5]
)
print(result)
~~~
- 디버거를 시작하는 또 다른 유용한 방법으로 사후 디버깅이 있음. 사후 디버깅을 사용하면 예외가 발생하거나 프로그램에게 문제가 생겨 중단된 뒤에 프로그램을 디버깅 할 수 있음
- 특히 breakpoint 함수 호출을 어디에 추가해야 할지 잘 모르는 경우 도움이 됨
- 다음은 함수 인자로 7j라는 복소수를 넘겨서 프로그램이 중단되는 코드임
~~~python
import math


def compute_rmse(observed, ideal):
    total_err_2 = 0
    count = 0
    for got, wanted in zip(observed, ideal):
        err_2 = (got - wanted) ** 2
        total_err_2 += err_2
        count += 1

    mean_err = total_err_2 / count
    rmse = math.sqrt(mean_err)
    return rmse

result = compute_rmse(
    [1.8, 1.7, 3.2, 7j],
    [2, 1.5, 3, 5]
)
~~~
- 명령줄에서 `python3 -m pdb -c continue main.py` 프로그램 경로를 사용하면 pdb 모듈이 프로그램 실행을 제어하게 할 수 있음
- continue 명령은 pdb에게 프로그램을 즉시 시작하라고 명령함
- 프로그램이 실행된 후 문제가 발생하면 대화형 디버거로 바로 들어가기 떄문에 그 시점부터 코드 상태를 관찰할 수 있음
- 대화형 파이썬 인터프리터에서 프로그램을 실행하는 중에 예외가 발생했는데 처리되지 않은 경우, pdb 모듈의 pm 함수를 호출하면 사후 디버깅을 사용할 수 있음
~~~terminal
$ python3
>>> import my_module
>>> my_modules.compute_stddev([5])
>>> import pdb; pdb.pm()
~~~

#### 기억해야 할 내용
- 프로그램에서 관심이 있는 부분에 `breakpoint` 내장 함수 호출을 추가하면 그 위치에서 파이썬 대화형 디버거를 시작할 수 있음
- 파이썬 디버거 프롬포트는 완전한 파이썬 셀이기 때문에 실행 중인 프로그램의 상태를 원하는 대로 관찰하거나 변경할 수 있음
- pdb 셀 명령어를 사용하면 프로그램 실행을 정밀하게 제어할 수 있고, 프로그램의 상태를 관찰하는 과정과 프로그램을 진행시키는 과정을 번갈아가며 수행할 수 있음
- 독립 실행한 파이썬 프로그램에서 예외가 발생한 경우(command에서 실행한 경우, 한줄씩 실행한 경우), pdb 모듈을 사용하거나 대화형 파이썬 인터프리터(`import pdb; pdb.pm()`)를 사용해 디버깅 할 수 있음

### 81- 프로그램이 메모리를 사용하는 방식과 메모리 누수를 이해하기 위해 tracemalloc을 사용해라
- 파이썬 기본 구현인 CPython은 메모리 관리를 위해 <b>참조 카운팅(reference counting)</b>을 사용
- 이로 인해 어떤 객체를 가리키는 참조가 모두 없어지면 참조된 객체도 메모리에서 삭제되고 메모리 공간을 다른 데이터에 내어줄 수 있음
- CPython에는 순환 탐지기(cycle dectector)가 들어 있으므로 자기 자신을 참조하는(A -> B -> C -> A 처럼 고리 모양으로 서로를 참조하는) 객체의 메모리도 언젠가는 garbage collection 됨
- 이론적으로 대부분의 파이썬 개발자가 프로그램에서 메모리를 할당하거나 해제하는 것을 신경쓰지 않아도 된다는 말
- 파이썬 언어와 CPython 런타임이 알아서 메모리 관리를 해줌. 하지만 실전에서는 더 이상 사용하지 않는 쓸모없는 참조를 유지하기 대문에 언젠가 결국 메모리를 소진하게 되는 경우가 있음 
- 파이썬 프로그램이 사용하거나 누수시키는 메모리를 알아내기란 매우 어려운 일
- 메모리 사용을 디버깅하는 첫 번째 방법은 gc 내장 모듈을 사용해 현재 garbage collector가 알고 있는 모든 객체를 나열시키는 것. 꽤 둔탁한 방법이기는 하지만 프로그램 메모리가 어디에 쓰이고 있는지 빠르게 감을 잡을 수 있음
~~~python
#- waste_memory.py
import os


class MyObject:
    def __init__(self):
        self.data = os.urandom(100)


def get_data():
    values = []
    for _ in range(100):
        obj = MyObject()
        values.append(obj)
    return values


def run():
    deep_value = []
    for _ in range(100):
        deep_value.append(get_data())
    return deep_value
~~~
- 그리고 gc 내장 모듈을 사용해 실행 중 생성한 객체의 개수와 생성한 객체 중 일부를 출력하는 프로그램을 실행함
~~~python
# using_gc.py
import gc

found_objects = gc.get_objects()
print("이전 :", len(found_objects))

import waste_memory
hold_reference = waste_memory.run()

found_objects = gc.get_objects()
print("이후 :", len(found_objects))

for obj in found_objects[:3]:
    print(repr(obj)[:100])

>>>
이전 : 25758
이후 : 35609
~~~
- `gc.get_objects`의 문제점은 객체가 어떻게 할당됐는지 알려주지 않음. 복잡하  프로그램에서는 특정 클래스에 속하는 객체가 여러 다른 방식으로 할당될 수 있음
- 객체 전체 개수를 아는 것은 메모리를 누수시키는 객체를 할당한 코드를 알아내는 것 만큼 중요하지 않음
- 파이썬 3.4부터는 이런 문제를 해결해주는 tracemalloc 이라는 내장 모듈이 새로 도입됨
- tracemalloc은 객체를 자신이 할당된 장소와 연결시켜줌. 이 정보를 사용해 메모리 사용의 이전과 이후 스냅샷(snapshot)을 만들어 서로 비교하면 어떤 부분이 변경됐는지 알 수 있음
- 다음 코드는 이런 접근 방법을 사용해 프로그램에서 메모리를 낭비하는 세 가지 이유를 찾아냄
~~~python
# top_n.py
import tracemalloc

tracemalloc.start(10)
time1 = tracemalloc.take_snapshot()

import waste_memory

x = waste_memory.run()
time2 = tracemalloc.take_snapshot()

stats = time2.compare_to(time1, 'lineno') #- 두 스냅샷을 비교

for stat in stats[:3]:
    print(stat)

>>>
/Users/heojaehun/gitRepo/TIL/effectivePython/waste_memory.py:7: size=2475 KiB (+10.8 KiB), count=30053 (+138), average=84 B
/Users/heojaehun/gitRepo/TIL/effectivePython/waste_memory.py:11: size=12.2 KiB (+5976 B), count=173 (+83), average=72 B
/Applications/PyCharm CE.app/Contents/plugins/python-ce/helpers/third_party/thriftpy/_shaded_thriftpy/_compat.py:97: size=6664 B (-3360 B), count=47 (-42), average=142 B
~~~
- 출력에 있는 크기와 카운트 레이블을 보면 프로그램에서 메모리를 주로 객체와 이런 객체를 할당한 소스 코드를 명확히 바로 알 수 있음
- `tracemalloc` 모듈은 각 할당의 전체 스택 트레이스(stack trace)를 출력  
  (tracemalloc.start 함수에 전달한 프레임 최대 개수만큼만 거슬러 올라가며 출력함)
- 다음 코드는 프로그램에서 메모리를 가장 많이 사용하는 곳의 스택 트레이스를 출력
~~~python
import tracemalloc

tracemalloc.start(10)
time1 = tracemalloc.take_snapshot()

import waste_memory

x = waste_memory.run()
time2 = tracemalloc.take_snapshot()

#- compare_to 메소드의 인자를 traceback으로 입력
stats = time2.compare_to(time1, 'traceback')
top = stats[0] #- 가장 많이 사용하는 부분 출력
print("가장 많이 사용하는 부분은:")
print('\n'.join(top.traceback.format()))

>>>
  File "/Users/heojaehun/gitRepo/TIL/effectivePython/waste_memory.py", line 21
    deep_value.append(get_data())
  File "/Users/heojaehun/gitRepo/TIL/effectivePython/waste_memory.py", line 13
    obj = MyObject()
  File "/Users/heojaehun/gitRepo/TIL/effectivePython/waste_memory.py", line 7
    self.data = os.urandom(100)
~~~
- 이와 같이 스택 트레이스는 프로그램에서 메모리를 소모하는 일반적인 함수나 클래스의 구체적인 용례를 파악할 떄 가장 중요한 도구임

#### 기억해야 할 내용
- 파이썬 프로그램이 메모리를 사용하고 누수하는 양상을 이해하기는 어려움
- gc 모듈은 어떤 객체가 존재하는지 이해할 때는 도움이 되지만, 객체가 어떻게 할당됐는지 파악할 수 있는 정보는 제공하지 않음
- `tracemalloc` 내장 모듈은 프로그램이 메모리를 사용하는 이유를 알고 싶을 때 쓸 수 있는 강력한 도구

