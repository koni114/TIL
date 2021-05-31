## chapter04 - 함수
* 함수형 프로그래밍 언어에서 함수는 굉장히 중요
* 함수형 프로그래머는 단일 - 목적으로 작성된 함수를 갖고 일련의 연산 수행
* 순수 함수의 특징
  * 하나 또는 그 이상의 입력 매개변수를 가짐
  * 입력 매개변수만을 가지고 계산 수행
  * 값을 반환
  *  <b> 동일 입력에 대해 항상 같은 값을 반환 </b>  
  *  함수 외부의 어떤 데이터도 사용하거나 영향을 주지 않음
  *  함수 외부 데이터에 영향을 받지 않음
* 스칼라 어플리케이션을 조직화 및 모듈화한다는 것은  
pure-function과 non-pure-function을 분명하게 명명하고 구분해 내는 것

##### 구문: 반환값이 없는 함수의 가장 기본적인 형태
~~~
def <식별자> = <표현식>
~~~
* 반환 값이 없는 함수를 만드는 경우
  * 현행 데이터의 포멧을 만들 때
  * 새로운 데이터를 위한 원격 서비스를 확인할 때
  * 단지 고정값을 반환하는 함수가 필요할 때
~~~
def hi = "hi"
~~~
#####  반환 타입을 지정한 함수 정의 예제
* 마지막 줄은 함수 반환 값
* 중간에 종료하려면 return 사용
~~~
def hi: String = "hi"
def multiplier(x:Int, y:Int):Int = {x * y}
~~~
##### 함수 조기 종료(return 사용) 예제
* 함수 조기 종료는 입력값이 유효하지 않거나, 비정상적인 경우 사용
~~~
def safeTrim(s: String):String = {
	if(s == null) return null
	s.trim()
}
~~~

### 프로시저(procedure)
* 프로시저는 반환값을 가지지 않는 함수
* println과 같이 statement를 사용하는 함수도 프로시저
* 타입을 Unit으로 사용시 명시적으로 사용자에게 전달 가능
##### 프로시저 사용 예제
~~~
def log(d: Double) = println(f"Got value $d%.2f")
dfe log(d: Double): Unit = println(f"Got value $d%.2f")
~~~

#### 빈 괄호를 가지는 함수
* 괄호가 있는 것이 없는 것보다 더 좋은 함수 표기법

##### 빈 괄호 함수 예제
~~~
def hi(): String = "hi"
~~~

### 표현식 블록을 이용한 함수 호출
* 함수에 계산된 결과 값을 바로 전달하는 경우 사용
~~~
def formatEuro(amt: Double) = "f$amt%.2f"
formatEuro(3.4645)
formatEuro {val rate = 1.32; 0.235 + 0.7123 + rate * 5.32}
~~~

### 재귀 함수
* 기본 예제
~~~
def power(x:Int, n:Int):Int = {
	if (x >= 1) return x * power(x, n-1)
	else 1
}
~~~
* stack oveflow 에러에 빠지지 않게 조심해야 함  
stack overflow :  프로그램이 호출 스택에서  이용 가능한 공간 이상을 사용하려고 할 때 나는 현상
* tail-recursion(꼬리재귀)를 사용하면 최적화 시킬 수 있음  
* tail-recursion을 위해 최적화된 함수를 표시하는 annotation 존재
##### tail-recursion  : 재귀 함수 호출 시, 스택을 재사용하면서 메모리를 과도하게 사용하지 않도록 최적화 하는 방법
*  마지막 문장이 재귀적 호출인 함수만이 고리-재귀를 최적화 시킬 수 있음
* 함수가 꼬리 재귀로 최적화될 수 없으면 error 발생 : <b> @annotation.tailrec </b> 추가
* <b>꼬리 재귀는 가변 데이터를 사용하지 않고 반복할 수 있는 유용한 방법</b>
##### error가 발생하는 경우 예제1 : 마지막 호출이 재귀 함수가 아님
~~~
@annotation.tailrec
def power(x:Int, n:Int): Long = {
	if (n >= 1) x * power(x, n-1)
	else 1
}
~~~

##### error가 발생하는 경우 예제2  : 마지막 호출이 재귀가 아니라 곱셈
~~~
@annotation.tailrec
def power(x:Int, y:Int, value:Int): Long = {
	if(n <= 1) value
	else power(x, n-1, x * value)
}
~~~

### 중첩 함수
* 메소드 내에 반복해서 사용해야 할 필요가 있는 로직이 있는데  
외부 메소드로서는 사용되지 않는 경우 중첩 함수로 사용
##### 세 수 최댓값 찾는 예제
* max의 매개변수가 다르므로 명이 같아도 상관없음
* 스칼라 함수는 함수 이름과 매개변수 타입 목록으로 구분됨
* 위 경우 매개변수가 같더라도 결과적으로 내부함수부터 호출되기 때문에 충돌나지 않음
~~~
def max(a: Int, b:Int, c:Int): Int = {
	def max(a:Int, b:Int): Int = {
	if (a > b) a else b
	}

	max(max(a, b), c)
}
~~~

### 매개변수 이름으로 호출하는 함수
* 스칼라 함수는 매개변수의 이름으로 호출 가능. 이름이 있으면 순서를 맞추지 않아도 됨

##### 예제: 매개변수의 이름으로 호출하는 경우
~~~
def greet(prefix:String, name:String) = s"$prefix $name"
greet(name = "Brown", prefix = "Mr")
~~~

### 기본값을 가지는 매개변수를 호출하는 함수
* 매개변수의 기본값을 지정하도록 하고, 선택적 호출 가능
~~~
def greet(prefix: String = "", name: String) = s"$prefix$name"
val greeting1 = greet(name = "Paul")
~~~

### 가변 매개변수를 가지는 함수
* 가변 인수(vararg) 0개 이상의 여러 인수가 일치할 수 있는 함수 매개변수
* 가변 매개변수: 정해지지 않는 개수의 입력 값
* 가변 매개변수는 반드시 불변 매개변수 뒤에 위치해야 함
* 함수 정의에서 *를 추가하면 가변 매개변수와 해당
##### 총합을 계산해주는 함수 예제
~~~
def sum(items: Int *):Int = {
	var total = 0
	for (i <- items) total += i
	total
}
~~~

### 그룹별 매개변수를 사용하는 함수
* 일반적으로 매개변수 리스트를 하나의 괄호로 만들어 냄
* 여러개의 괄호를 사용해 여러 그룹의 매개변수로 나누는 방식 제공
~~~
def max(x: Int)(y: Int):Int = {
	if (x > y) x else y
}
~~~

### 매개변수에 동적 타입 추가한 함수 **
* 매개변수에 동적 타입 추가 가능
* 매개변수 타입, 반환 타입에 동적 반환 가능
* 타입 시스템은 스칼라의 유연성, 기능성, 재사용성의 핵심 특징

##### 정의: 타입 매개변수 지정 함수
~~~
def <함수명>[타입명](<매개변수이름>:<타임명>): <타입명> ...
~~~

##### 타입 매개변수 예시
* 입력값을 그대로 반환하는 항등 함수(identity function)을 만들어보자
~~~
def identity(s: String): String = s
~~~
* 위의 식으로는 String만 호출 가능. 다른 함수를 정의하지 않는 한 다른 타입(ex) Int)을 호출할 수 없음
* 그렇다면 Any Type은 어떻게 만드는 것일까?
* 다음 생성된 예제를 보자!
~~~
def identity(a: Any):Any = a
val s: String = identity("Hello") // (error)
~~~
* 함수의 반환값이 Any Type 이기 때문에  String Type을 담지 못함
* 타입 매개변수를 사용하면 어떤 타입이던지 반환값으로 만들어 사용 가능
~~~
def identity[A](a: A):A = a
val s = identity[String]("Hello")
val d = Double = identity[Double](2.717)
~~~
 * 타입 추론으로 생략 가능  
 타입 매개변수에 타입을 넣지 않아도 추론되어 전환됨
##### 타입 매개변수 생략 예제
~~~
// 타입 추론으로 타입  매개변수 생략
val a: String = identity("hello")
val d: Double = identity(0.333)

// 값 변수 매개변수까지 생략
val c = identity("hello")
val d = identity(0.333)
~~~

### 메소드와 연산자
* 함수는 객체(object) 안에 존재하며, 객체의 데이터에 동작하므로 클래스 내 함수를 칭하는
더 적절한 용어는 메소드(method)
* <b>메소드는 클래스 내에서 정의한 함수</b>
* 메소드를 호출하는 방식은 자바에서와 동일(.를 이용)

##### String 타입 적용 메소드
* String 타입에 적용하는 많은 유용한 메소드 중 하나를 호출
##### String 타입에 기본 메소드 호출 예제
~~~
val s = "vacation.jpg"
val isJEPG = s.endsWith(".jpg")
~~~

##### Double 타입 유용 메소드 예제
~~~
val d = 65.642
d.round
d.floor
d.compare(18.0)
d.+(2.721)
~~~
* 연산자는 실제로 메소드. 함수 이름처럼 연산자 기호를 사용하여 쓰임
* 연산자 표기법(operation notation)인 객체 메소드 호출의 다른형태로 현재의 연산자 표기법 사용 가능  
(ex) a + b)
* 이러한 연산자 표기법을 infix operation notation 이라고 함

##### 연산자 표기법의 예제
~~~
d compare 18.0
d + 2.721
~~~
* 여러개의 매개변수가 있는 경우, 연산자 표기법을 사용하려면 list로 묶어 단일 연산자로 취급해야함

### 가독성 있는 함수 작성하기
* 함수를 어떻게 작성할 것인가?
* 함수를 쓰는 것은 이를 재사용 한다는 것
* 함수를 읽기 쉽게 만들기  
  * 함수 이름을 잘 요약해서 만들자!
  * 사용자가 전체 함수를 보기 위해 위아래 스크롤을 움직이지 않아도 되게 하기
* 주석 추가하기(매우 중요)
  * 한줄 주석: //
  * 범위 주석: / **/
  *  scaladoc 해더 추가: /** 시작하여 */ 로 종료
  * 매개변수는 @param 키워드 다음에 매개변수 이름과 설명 붙이기
##### 주석 예제
~~~
/**
  * 선행 혹은 후행 공백 없이 입력 문자열을 반환
  * 입력 문자열이 Null인 경우, null을 반환
  * 매개변수 s는 입력 문자열
  */
def safeTrim(s: String): String = {
  if(s == null) return null
  s.trim()
}
~~~ 
