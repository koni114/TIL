## chapter05 - 일급(first-class) 함수
* 함수형 프로그래밍의 핵심은 일급(frist-class)함수여야 한다는 점
여기서 말하는 first-class란, 함수가 선언, 호출 이외에 다른 데이터 타입처럼 모든 부분에 사용될 수 있음을 의미
* first-class function은 식별자(identifier)에 할당되지 않고 리터럴 형태로 생성 가능
* 값, 변수 또는 데이터 구조처럼 컨테이너에 저장될 수 있음
* 다른 함수에 매개변수로 사용되거나, 다른 함수의 반환 값으로 사용될 수 있음
* 다른 함수를 매개변수로 받아드리거나,  
반환값으로 함수를 사용하는 함수를 <b/>고차 함수(higher-order function)</b>이라고 함
* 대표적인 고차함수는 map, reduce function이 있음
*  스칼라는 일급 함수, 고차 함수, 선언형 프로그래밍 모두 지원

##### 선언형 프로그래밍 vs 명령형 프로그래밍 간단한 개념만 이해하기
* 선언형 프로그래밍(declarative programming)
  * 무엇을 할 것인지만 정의
  * 어떻게 할 것인지는 정의하지 않음
* 명령형 프로그래밍(imperative programming)
  * 어떻게 할 것인지 정의

### 함수 타입과 값
* 함수의 타입은 함수의 입력 타입과 반환 타입의 그룹으로,  
입력 타입으로부터 출력 타입으로의 방향을 나타내는 화살표로 배열
##### 구문: 함수 타입
~~~
// 참고로, 입력과 출력 타입이 동일한 경우, 입력 타입에 ()를 뺄 수 있음
([<타입>, ...]) => <타입>
~~~

* 다소 어색해보일 수 있지만 결국 함수는  
이름, 입력, 출력이므로 함수의 타입은 입력과 출력 그룹이어야 함
##### 예제 이해해보기!
~~~
def double(x: Int): Int = x * 2
double(5)
~~~
* 여기까지는 익숙하다
* 앞선 chapter에서 선언했던 함수와 동일하다
~~~
val myDouble = Double (error)
val myDouble: (Int) => Int = Double
myDouble(5)
~~~
* 먼저 첫번째 구문이 error가 발생하는 것을 인지하자
* 다시 상기해보면, val <식별자>는 값(value)이다. 당연히 함수명 자체를 value에다가 넣는 것은 불가능하다는 것을 직관적으로 이해할 수 있다
* 함수값을 저장하려면 함수 입력타입, 출력타입을 명시적으로 선언해 주어야 한다((Int) -> Int)
~~~
val myDoubleCopy = myDouble
myDoubleCopy(5)
~~~
* myDouble은 함숫값이므로,  함숫값을 새로운 값에 할당하는 것은  
다른 값들과 마찬가지로 가능하다 !
##### 구문: 와일드카드 연산자로 함수 할당하기
* 함숫값을 정의하는 다른 방법은 기존 함수명 뒤에 _를 붙여줌으로써 정의 가능
~~~
val <식별자> = <함수명>  _
~~~
~~~
def double(x: Int): Int = x * 2
val myDouble = double _
val amount = myDouble(20)
~~~
* 다중 매개변수를 사용하는 명시적 함수 타입으로 정의된 함숫값의 예는 다음과 같음\
* 와일드카드 연산자로도 사용 가능
~~~
def max(a: Int, b: Int) = if(a >  b) a else b
val maximize = (Int, Int) => Int = max
maximize(50, 30)

// 와일드카드 연산자 사용 가능
val maximize = max _
print(maximize(30, 50))
~~~
* 위의 내용들은 함수를 값에 저장하고, 그 값이 정적 타입에 할당함으로써  함수가 어떻게 데이터로 다뤄지는지에 대해 간단히 보여줌

### 고차 함수(higher-order function)
* 고차 함수는 입력 매개변수나 반환값으로 함수 타입의 값을 가지는 함수
* 다음은 고차 함수의 좋은 예로, String에서 동작하지만, 입력 String이 null이 아닌 경우에만 동작하는 다른 함수를 호출
~~~
def safeStringOp(s: String, f: String => String) = {
  if (s != null) f(s) else s
}

def reverser(s: String) = s.reverse

safeStringOp(null, reverser)

safeStringOp("Ready", reverser)
~~~

### 함수 리터럴
* 함수 리터럴(function literal) : 실제 동작하지만 이름이 없는 함수
~~~
 val doubler = (x: Int) => x * 2
 val doubled = doubler(22)
~~~
* 함수 리터럴이 이름을 가지지 않는 함수이지만,  
화살표 구분을 포함한 이 개념은 다양한 이름으로 불리우고 있음
  * 익명 함수(Anonymous function)
  스칼라 언어에서의 공식적인 이름
  * 람다 표현식(Lambda expression)
  C# 이나 Java, python 에서 사용
  * 람다(Lambda)
  람다 표현식의 축약형..
  * function0, function1, function2 ...
  함수 리터럴에 대한 스칼라 컴파일러의 용어로, 입력 인수의 개수를 기반으로 함
  앞선 예제에서는 <function1>이 부여됐음을 볼 수 있음

##### 구문: 함수 리터럴 작성하기
~~~
([<식별자>: <타입>, ...]) => <표현식>
~~~
* 함숫값을 정의하고 새로운 함수 리터럴에 할당해보자
~~~
val greeter = (name: String) => s"Hello, $name"
val hi = greeter("World")
~~~
* 함수 리터럴이 꼭 입력 변수가 필요한 것은 아님
* 어떤 인수도 필요로 하지 않는 함수 리터럴을 작성해보자
~~~
// 1. 입력 값이 없는 함수 선언
def logStart() = "=" * 50 + "\nStarting NOW\n" + "=" * 50
// 함수 리터럴을 함수값으로 할당
val start = () => =" * 50 + "\nStarting NOW\n" + "=" * 50
println(start())
~~~

* 위에서도 설명했지만, 함수 리터럴은 고차 함수 매개변수에서도 정의될 수 있음
~~~
def safeStringOp(s: String, f: String => String) = {
  if (s != null) f(s) else s
}
safeStringOp(null, (s: String) => s.reverse)
safeStringOp("Ready", (s: String) => s.reverse)
~~~
* 예제에서 f: String => String 을 명시해주었는데, 타입 추론때문에 생략 가능
* 명시적 타입을 제거한다는 것은 함수 리터럴에서 괄호를 제거할 수 있다는 것을 의미
~~~
def safeStringOp(s: String, f: String => String) = {
  if (s != null) f(s) else s
}
safeStringOp(null, s => s.reverse)
safeStringOp("Ready", s => s.reverse)
~~~
* 함수 리터럴은 매우 간단한 함수의 표현식이지만,  
스칼라는 자리표시자 구문(placeholder syntax)로 더 간단한 표현식을 지원

### 자리표시자 구문
* placeholder syntax는 함수 리터럴의 축약형
* 지정된 매개변수를 와일드카드 연산자(_)로 대체한 형태를 가짐
* 함수의 명시적 타입이 value에 지정되어 있어야 하며(ex) val doubler: Int),  
매개변수가 한 번 이상 사용되지 않는 경우에 사용( -> _로 표현해야 하므로)
~~~
val doubler: Int => Int = _ * 2  
~~~
* placeholder syntax로 safeStringOp 예제를 호출해보자
~~~
def safeStringOp(s: String, f: String => String) = {
  if (s != null) f(s) else s
}

safeStringOp(null, _.reserve)
safeStringOp("Ready", _.reserve)
~~~
* 두 개의 자리표시자를 가진 예제로 자리표시자가 어떤 순서로 동작하는지 확인해보자
~~~
def combination(x: Int, y: Int, f: (Int, Int) => Int) = f(x, y)
print(combination(23, 12, _ * _))
~~~
* 마지막으로 함수 타입을 매개변수로 선언하여 예제를 작성해보자
~~~  
def tripleOp[A, B](a: A, b: A, c: A, f: (A, A, A) => B) = f(a, b, c)
tripleOp[Int, Boolean](93, 92, 14, _ > _ + _ )
~~~
* 자리표시자 구문은 데이터 구조와 컬렉션으로 작업할 때 유용
* 많은 정렬, 필터링, 다른 데이터 구조 메소드는 일급 함수(first-class)를 사용하는 경향이 있음

### 부분 적용 함수와 커링
* 일반적으로 함수(일반, 고차함수 모두)를 호출하려면 기본 매개변수 값이 있는 함수를 제외하고 매개변수를 모두 지정해서 할당해야함
* 만약 함수 호출을 다시 사용할 때   
일부 매개변수를 그대로 유지하여 이를 다시 타이핑하려면?  
* 먼저 일반적인 함수 하나를 선언해보자
~~~
def factorOf(x: Int, y: Int) = y % x == 0
~~~
* 모든 매개변수를 다시 setting 하고 싶으면 위의 예제처럼 _ 연산자를 이용해서  
함수값을 받으면 된다
~~~
val f = factorOf _
val x = f(7, 20)
~~~
* 매개변수 중 몇개를 그대로 사용하기를 원한다면 다음과 같이  
매개변수 안에 _ 연산자를 사용하면 됨
~~~
val multipleOf3 = factorOf(3, _: Int)
val y = multipleOf3(78)
~~~
* 부분 적용 함수를 정확히 설명하려면,  
다중 매개변수 목록을 가진 함수를 사용하는 것
* 하나의 매개변수 목록을 적용 매개변수와 비적용 매개변수로 나누고,  
한 목록의 매개변수를 적용하고 다른 하나의 매개변수 목록은 적용하지 않는 것.
-> 이를 <b/>커링(currying)</b> 한다고 말함
~~~
def factorOf(x: Int)(y: Int) = y % x == 0
val isEven = factorOf(2) _
val z = isEven(32)
~~~
* 함수 타입 관점에서 다중 매개변수 목록을 가지는 함수는 다중 함수의 체인(chain)으로 간주
* 각각의 매개변수 목록은 별도의 함수 호출로 간주
* 함수 리터럴에서 재사용 가능한 매개변수는 유지하고,  
기존의 매개변수와 새로운 매개변수를 이용하여 새료운 함수를 호출할 수 있음

### 이름에 의한 호출 매개변수
* 함수 타입 매개변수의 다른 형태로 값이나,  
값을 반환하는 함수를 취할 수 있는 <b/>이름에 의한 호출 매개변수</b>임
##### 구문: 이름에 의한 호출 매개변수 지정하기
~~~
def doubles(x: => Int)
~~~
* 이름에 의한 매개변수 사용시, 유연성이 높아짐   
이름에 의한 매개변수를 취하는 함수는 값을 사용할 수 있을 때, 값 대신 함수를 사용해야 할 때 이용될 수 있음
* 이름에 의한 매개변수에 전달된 함수는 그 매개변수에 접근하지 않으면 호출되지 않으므로,
이에 따른 비용 감소 효과가 있음
* 이름에 의한 매개변수를 가지는 함수를 호출해보자
~~~
def doubles(x: => Int)  {
  // 이름에 의한 매개변수 x는 일반적인 값에 의한 매개변수(by-value parameter)와 같이 접근
  println("Now doubling " + x)
  x * 2
}
// doubles 메소드를 일반값으로 호출하며, 정상적으로 동작함
def doubles(5)
def f(i: Int) = {println(s"Hello from f($i)"); i}
// 함숫값으로 호출하면 함숫값이 doubles 메소드 내부에서 호출 됨
// doubles 메소드가 x 매개 변수를 두 번 참조하므로 Hello 메세지가 두 번 호출 됨
doubles(f(8))
~~~
### 부분 함수
* 지금까지 공부한 함수는 완전함수임.  
완전함수는 입력 매개변수를 완전히 처리하는 함수를 말함
* 입력 매개변수를 완전히 처리하지 못하는 함수를 <b/>부분 함수(partial function)</b>이라고 함  
ex) 주어진 수로 나누는 함수인 경우, 0은 처리하지 못함
ex) 제곱근을 구하는 함수인 경우, 음수는 처리하지 못함
* 스칼라의 부분 함수는 case 패턴을 자신의 입력값에 적용하는 함수 리터럴로,
입력 값이 주어진 패턴 중 최소 하나는 일치할 것을 요구
~~~
// 함수 리터럴 생성
val statusHandler: Int => String  = {
  case 200 => "okay"
  case 400 => "Your Error"
  cas 500 => "Our error"
}
statusHandler(200)
statusHandler(400)
statusHandler(1000) (error 발생)
~~~

### 함수 리터럴 블록으로 고차 함수 호출하기
* 우리는 앞서 함수 호출에서 괄호나 공백 대신
표현식 블록으로 함수를 호출하는 방법에 대해서 다룸
* 간단한 예시 하나 보고 가자
~~~
def formatEuro(amt: Double) = f"$amt%.2f"
formatEuro{val rate = 1.32'; 0.235  + 0.7123 + rate * 5.32 }
~~~
* 이 표기법을 고차 함수와 함께 재사용하여 고차 함수를 호출할 수 있음
* 이 구문의 용도는 표현식 블록으로 유틸리티 함수를 호출하는 것
* 예시를 한 번 보자
~~~
def safeStringOp(s: String, f: String => String) = {
  if (s != null) f(s) else s
}
// 스칼라에서 접근할 수 있는 자바의 java.util 패키지의 UUID 유틸리티
val uuid = java.util.UUID.randomUUID.toString
val timedUUID = safeStringOp(uuid, { s =>
  // System.currentTimeMillis 는 1/1000초(1ms) 단위로 에포크 시간을 제공
  val now = System.currentTimeMillis
  //  메소드는 String으로부터 처음 x개의 항목을 반환하며, 이 경우 UUID의 처음 네 부분을 반환
  val timed = s.take(24) + now
  timed.toUpperCase
  })
~~~
* 이 예제에서 여러 줄의 함수 리터럴이 값 매개변수와 함께 함수에 전달
* 이렇게 작성하면 알아보기 힘든 단점이 있으므로, 매개변수를 별도의 그룹으로 구분해보자
~~~
def safeStringOp(s: String)(f: String => String) = {
  if (s != null) f(s) else s
}

val timedUUID = safeString(uuid) { s =>
  val now = System.currentTimeMillis
  val timed = s.take(24) + now
  timed.toUpperCase
}
~~~
* safeStringOp 호출이 쪼금 더 깔끔해졌음(..)

* 다른 예제로, 이름에 의한 매개변수 하나를 취하는 함수를 예로 들어보자
* 함수를 이름에 의한 매개변수 반환 타입과, 메인 함수의 반환 타입을 위해 사용될 타입 매개변수를 이용하여 더 일반적으로 만들어보자
~~~
def timer[A](f: => A): A = {
  def now = System.currentTimeMillis
  val start = now; val a = f; val end = now
  println(s"Executed in ${end - start} ms")
  a
}

val veryRandomAmount = timer {
  util.Random.setSeed(System.currentTimeMillis)
  for (i <- 1 to 100000) util.Random.nextDouble
  util.Random.nextDouble
}
~~~
