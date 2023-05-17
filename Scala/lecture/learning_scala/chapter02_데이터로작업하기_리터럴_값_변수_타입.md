## Chapter02 - 데이터로 작업하기: 리터럴, 값, 변수, 타입

### 간단 맛보기
* 리터럴  
  * 소스코드 상에 바로 등장하는 데이터. ex) 'A', 'Hello world', 10 ..
* 값  
  * 불변의 타입을 갖는 저장 단위
  * 값은 정의 될 때만 할당 되고, 재할당은 불가
  * 리터럴과의 차이점을 반드시 숙지
* 변수
  * 가변의 타입을 갖는저장 단위
  * 변수 정의시 데이터를 할당할 수 있고, 언제든지 재할당이 가능  
* 타입
  * 우리가 앞으로 작업할 데이터들의 종류를 말함
  * 스칼라의 모든 데이터는 타입을 가짐
  * 모든 스칼라 타입은 데이터를 처리하는 메소드를 갖는 클래스로 정의
  * 스칼라 값(리터럴 아님)은 다음과 같이 정의
~~~
val <이름> : <타입> = <리터럴>
~~~
##### int 타입인 값 x에 5를 할당해보는 예제
~~~
val x : Int = 5
x * 5 // -- 2
x / 5 // -- 1
~~~
* 예제 설명
  * -- 1: 기존 x 변수에 사칙연산을 수행하면 정숫값을 반환
  * -- 2: REPL 내에서 수행시 자동으로 res0 값 생성
* res0, res1 값을 가지고 추가 작업도 가능(REPL)
~~~
var a: Double = 0.25
a = 355.0 / 113.0
~~~

### 값(Value)
* val 키워드 사용하여 정의
* 가장 보편적인 데이터 저장 기본 단위
* 불변(immutable) 타입을 갖는 스토리지 단위
* 명시적 타입이 없으면 타입 추론(Type Inference) 기반으로 타입을 추론함
##### 값 정의
~~~
val <식별자>[: <타입>] = <데이터>
~~~
* 우변이 <데이터> 라는 점 생각하자(리터럴이 아님)
##### 값 할당 예제
~~~
val x = 20
val greeting = "hello, world"
val atSymbol = '@'
~~~
* 초깃값과 호환되지 않는 타입으로 값 정의시 컴파일 에러 발생
##### 호환되지 않는 타입으로 값 정의시 에러
~~~
val x: Int = "Hello" // error 발생
~~~

### 변수(Variable)
* 일반적으로 값을 저장하고 값을 가져올 수 있도록 할당됨
* 또는 예약된 메모리 공간에 대응하는 유일한 식별자를 의미
* 메모리 공간은 동적이며 가변적임
* var 키워드 사용
* 스칼라에서는 변수(var)보단 값(val)을 선호
  * val이 불변의 값이기 때문에 좀 더 안정적이기 때문
* 변수 사용 예제 : 임시 데이터 저장, 루프 내 가변적인 변수 등..
##### 변수 정의
~~~
var <식별자>[: <타입>] = <데이터>
~~~
* 변수도 타입 생략 가능
* 재할당시 다른 타입 데이터는 재할당 불가능
##### 변수 사용 간단 예제
~~~
var x = 5
x = x * 5
x = "what's up" // error
~~~
* 형변환이 가능하면 재할당 가능(ex) Double -> Int )

### 값, 변수 명명하기
* 스칼라에서 유효한 식별자를 만들기 위해 문자, 숫자, 기호를 조합하는 규칙
  * 하나의 문자 다음에는 아무것도 없거나, 하나 이상의 문자 OR 숫자
  * 하나의 문자 다음에는 하나 이상의 문자 또는 숫자가 올 시, 사이에 '_' 사용
  * 하나 OR 그 이상의 연산자 기호 사용
  * ' ' 사용
  ##### 명명 예제
~~~
val π = 3.14159
val $ = "USD currency symbol"
val o_O = 'Hmm'
val 50cent = "%0.50" (error, 숫자로 시작 안됨)
val a.b = 25(error, 마침표는 연산자 기호가 아님)
val 'a.b' = 25(잘안씀)
~~~
* 스칼라에선 camel Case가 일반적인 표기법'

### 타입(Type)
* 스칼라에서 값, 변수 정의시 숫자 타입과 비숫자 타입이 있음
* 객체나 컬렉션을 포함하여 아래 표에 해당하는 핵심 타입이 모든 타입의 기본 요소
* 실제 핵심 타입 자체도 자신의 데이터에 동작하는 메소드와 연산자를 갖는 객체
* 스칼라는 원시 데이터 타입이 없음 -> Int 만 지원

> |이름| 설명 | 크기 | 최솟값 | 최댓값
> |---|:---:|:---:|:---:|:---:|
>  | Byte |부호 있는 정수| 1바이트| -128 | 127
>  | Short |부호 있는 정수| 2바이트| -32768 | 32767
>  | Int |부호 있는 정수| 4바이트| -2^31| 2^31 - 1
>  | Long |부호 있는 정수| 8바이트| -2^63 | 2^63 - 1
>  | Float |부호 있는 부동 소수점| 4바이트| n/a| n/a
>  | Double |부호 있는 부동 소수점| 8바이트| n/a | n/a
* 스칼라는 타입 순위에 기반하여 타입 변환이 이루어짐. 위의 표는 타입 순위를 높은순으로 나열
##### 타입 순위 파악을 위한 예제
~~~
val b: Byte = 10
val s: Short = b
val d: Double = s
~~~
* 스칼라는 높은 순위의 데이터 타입이 낮은 순위의 데이터 타입으로 자동 변환하지 않음
* (to + 타입) 메소드를 이용하여 수동으로 타입 전환 가능
##### to + 타입 메소드를 이용한 수동 타입 변환 예제
~~~
val l: Long = 20
val i: Int  = l.toInt
~~~

#### 리터럴 타입을 위한 스칼라 표기법
* 스칼라 리터럴 타입의 대소문자는 구별되지 않음

> |리터럴| 타입 | 설명 |
> |---|:---:|:---:|
>  | 5 |Int| 접두사/접미사 없는 정수 리터은 기본적으로 Int|
>  | 0x0f |Int| 접두사 0x는 16진수 표기법을 의미|
>  | 5l |Long| 접미사 'l'은 Long 타입을 의미|
>  | 5.0 |Double| 접두사/접미사 없는 소수 리터럴은 기본 Double형|
>  | 5f |Float| 'f'접미사는 Float 타입을 나타낸다|
> | 5d |Double| 'd'접미사는 Double 타입을 나타냄|

### 문자열(String)
* 기본적인 java, Python 등의 언어들의 문자열과 동일
* Python 처럼 문자열에 연산기호 사용이 가능
##### 문자열 연산기호 예제
~~~
val hello = "Hello, there"
val greeting = "Hello," + "World"
val matched = (greeting == "Hello, World")
val theme = "Na " * 16 + "Batman"
~~~
* 여러줄의 문자열은 큰따옴표 3개(""") 를 이용하여 생성  
이 때 역슬래시는 인지하지 못함

##### 값을 바인딩하여 문자열 출력 예제: interpolation
~~~
val approx = 335/113f
println("Pi, using 355/113, is about" + approx + '.')
~~~
##### 중괄호를 이용한 문자열 출력 예제
~~~
val item = "apple"
println(s"How do you like them ${item}s?")
println(s"Fish n chips n vinegar, ${"pepper "*3}salt")
~~~

##### 정규표현식
* String 타입은 정규 표현식을 지원하는 다양한 내장(bulit-in) 연산을 제공
> |이름| 예시 | 설명 |
> |---|:---:|:---:|
>  | matches |"Froggy went a' courting" matches ".*courting"| 정규 표현식이 전체 문자열과 맞으면 참(True)을 반환|
>  | replaceAll |"milk, tea, muck" replaceAll ("m[^ ]+k", "coffee")| 일치하는 문자열을 모두 치환 텍스트로 치환함|
>  | replaceFirst |"milk, tea, muck" replaceFirst ("m[^ ]+k", "coffee")| 첫 번째로 일치하는 텍스트를 치환|

##### 정규 표현식 사용 정의
~~~
val <정규 표현식 값>(<식별자>) = <입력 문자열>
~~~
##### 정규 표현식 사용 예제: 문자열 숫자형 값 캡처
~~~
val input = "Enjoying this apple 3.14159 times today"
val pattern = """.* apple ([\d.]+) times .*""".r
val pattern(amountText) = input
val amount = amountText.toDouble
~~~

### 스칼라 타입 개요
* 모든 스칼라 타입(ex) AnyVal, AnyRef) 은 타입 계층 구조의 일부로 존재함
* 아래 그림은 스칼라 핵심 타입의 계층 구조를 나타냄
![img](https://github.com/koni114/learning_scala/blob/master/ScalaTypeHierarchy.png)
* Any, AnyVal, AnyRef 타입은 스칼라 타입 계층 구조의 루트
* AnyVal
  * AnyVal을 확장한 타입은 데이터를 표현하는데 사용하는 핵심 값들이기 때문에 값 타입(value type) 이라고 함
  *  객체 힙 메모리에 할당되거나, JVM 기본값으로 스택에 지역적으로 할당
* AnyRef
  * 오직 객체로 힙 메모리에 할당  

#### Char 타입
* 작은 따옴표를 사용하여 char 타입 표현
##### char 타입 간단 예제
~~~
val c = 'A'
val i: Int = c
~~~

#### Boolean 타입
* &와 &&의 차이
  * & :  첫 번째 인수가 False 여도 두 번째 인수까지 검사함
  * && : 첫 번째 인수가 True면 두 번째 인수를 검사하지 않음  

##### Boolean 타입 간단 예제
~~~
val isTrue = !true
val isFalse  = !true
val unequal = (5 != 6)
val isLess = (5 < 6)
val unequalAndLess = unequal & isLess
val definitelyFalse = false && unequal
~~~
* 스칼라는 다른 타입을 boolean 타입으로 자동 전환해주지 않음
  * ex) null 아닌 문자열을 true로 평가하지 않음
  * ex) 숫자 0은 false와 다름
  * ex) 해당 값의 상태를 boolean으로 평가해야한다면 명시적으로 비교해야함

#### Unit 타입
* 자바에서 Void와 유사
* 데이터가 없음을 나타냄
* Unit 타입은 어떤 것도 반환하지 않는 함수나 표현식의 반환 타입으로 쓰임
~~~
val nada = ()
~~~

#### tuple 타입
* 둘 이상의 값을 가지는 순서가 있는 컨테이너
* 포함된 값들은 다른 타입이여도 됨
* 리스트나 배열과는 달리 튜플의 요소들을 반복할 수 없음

##### 튜플 생성 구문 정의
~~~
( <값 1>, <값 2>[,<값 3> ...])
~~~

##### 튜플 예시
~~~
val info = (5, "Korben", true)
~~~
* 튜플의 항목은 1부터 시작하는 인덱스를 사용하여 접근 가능
~~~
val name = info._2
~~~
* 두 개 항목의 튜플 생성의 다른 형식 : -> 사용
* 튜플에서 key-value 쌍을 표현하는 가장 보편적 방법
~~~
val red = "red" -> "0xff0000"
val reserved = red._2 -> red._1
~~~
