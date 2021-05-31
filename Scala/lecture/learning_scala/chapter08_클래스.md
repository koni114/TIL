## chapter08 - 클래스
* 이제 클래스를 이용해 자신만의 타입을 만들어 보자!
* 클래스(class)는 데이터 구조와 함수(메소드)의 조합으로, 객체지향 언어의 핵심 구성 요소
* 값과 변수로 구성된 클래스는 필요한 만큼 여러번 인스턴스화 될 수 있으며, 각 인스턴스는 자신만의 입력 데이터로 초기화될 수 있음
* 클래스는 상속(inheritance) 으로 다른 클래스로 확장할 수 있어 서브클래스와 슈퍼클래스의 계층구조를 생성할 수 있음
* 다형성(polymorphism)은 서브클래스가 부모 클래스를 대신하여 작업하는 것이 가능하게 함
* 캡술화는 클래스의 외관을 관리하는 프라이버시 제어를 제공

##### 가장 간단한 클래스 구문 만들기
~~~
class User
val u = new User
val isAnyRef = u.isInstanceOf[AnyRef]
~~~
* 값 u를 출력해보면, 클래스 이름과 16진수 문자열을 보게 되는데, 이는 해당 인스턴스에 대한 JVM reference
* 새로운 인스턴스를 생성하면 첫 번째 인스턴스와 메모리 위치가 다르고 따라서 다른 참조를 가지게 됨
* User 클래스 이름 뒤에 출력된 16진수 숫자를 출력하는 메소드는 JVM의 java.lang.Object.toString임
* java.lang.Object 클래스는 스칼라를 포함하여 JVM 내의 모든 인스턴스 루트이며, 기본적으로 스칼라 루트 타입인 Any와 동등
* 인스턴스를 출력함으로써 인스턴스가 루트 타입으로부터 상속한 toString 메소드를 호출
* User 클래스의 실제 부모 타입은 AnyRef

##### User class를 재설계하여 좀 더 유용하게 만들어보기
* 값과 그 값에서 동작하는 메소드 추가
* toString 메소드를 재정의하여 유용한 정보를 제공하는 버전을 제공
~~~
class User {
  val name: String = "Yubaba"
  def greet: String = s"Hello from $name"
  override def toString = s"User($name)"
}

val u = new User
println(u)
println(u.greet)
~~~
* 여기서 추가적으로 name을 매개변수로 값을 받아보자
~~~
class User(n:String) {
  val name: String  = n
  def greet: String = s"Hello from $name"
  override def toString = s"User($name)"
}

val u = new User("Zeniba")
println(u)
println(u.greet)
~~~
* 클래스 매개변수 n은 클래스가 생성되고 나면 그 매개변수를 호출 불가(ex) u.n )

##### name 필드를 클래스 매개변수로 옮겨서 확인해보기
* 초기화를 위해 클래스 매개변수를 사용하는 대신 필드 중 하나를 클래스 매개변수로 선언할 수 있음
* 클래스 매개변수 앞에 val 또는 var 키워드를 추가하면 클래스 매개변수가 클래스의 필드가 됨
~~~
class User(val name: String) {
  def greet: String = s"Hello from $name"
  override def toString = s"User($name)"
}

val users = List(new User("Shoto"), new User("Art3mis")) // 클래스가 List의 타입 매개변수

val sizes = users map (_.name.size)
println(sizes)

val sorted = users sortBy (_.name)
println(sorted)

val third = users find (_.name contains "3")
print(third)

val greet = third map (_.greet) getOrElse "hi" //  
~~~
* 스칼라 개발자라면, 자신만의 클래스를 개발할 때, 컬렉션에서 그 클래스를 사용하게 됨

##### 상속과 다형성의 예제를 작성해보기
* 클래스는 extends 키워드를 이용하여 다른 클래스로 확장 가능
* override 키워드로 상속받은 메소드의 행위를 재정의 할 수 있음
* 클래스에서 필드와 메소드는 this 함수를 이용하여 접근 가능
* 클래스의 부모 클래스의 필드와 메소드는 super 키워드를 이용하여 접근 할 수 있음
~~~
class A {
  def hi = "Hello from A"
  override def toString = getClass.getName
}

class B extends A
class C extends B { override def hi = "hi C -> " + super.hi }

val hiA = new A().hi
val hiB = new B().hi
val hiC = new C().hi
~~~
##### 스칼라의 다형성 실습해보기
* 다형성은 클래스가 호환되는 다른 클래스의 모양새를 띄게 해주는 능력을 말함
* '호환된다'는 의미는 서브클래스의 인스턴스가 그 부모 클래스의 인스턴스를 대신해 사용될 수 있으나, 그 반대로는 가능하지 않음을 말함
~~~
val a: A = new A
val a: A = new B

val b: B = new A(error)
val b: B = new B
~~~
* 만약, A, B, C 인스턴스의 리스트를 생성하고 싶으면, 리스트의 타입은 A로  선언해야함
* 선언하지 않더라도  부모 클래스인 A 타입을 자동으로 추론함
~~~
val misc = List(new A, new B, new C) // List의 타입은 class A로 선언 됨
~~~
### 클래스 정의하기
* 클래스는 <b>타입의 정의로,</b> 핵심 타입이나 다른 클래스의 필드를 포함
* 함수와 마찬가지로, 클래스는 클래스 안에 중첩될 수 있음
* 중첩된 클래스는 자신이 가지고 있는 필드와 메소드 이외에 부모 클래스의 필드와 메소드에도 접근 할 수 있음
* 클래스 내용을 할당하기 위해 메모리에 적재하는 작업을 인스턴스화 또는 인스턴스 생성이라고 함
* 클래스가 좀 더 유용하려면, class parameter 를 사용해야함.
~~~
class Car(val make: String, var reserved: Boolean) {
	def reserve(r: Boolean): Unit = {reserved = r}
}

val t = new Car("Toyota", false)
t.reserve(true)
~~~
*  만약 특정 클래스가 매개변수를 가지는 클래스를 확장한 클래스일 때, 클래스의 정의에 매개변수가 포함되어 있는지 확인해야 함
~~~
class Car(val make: String, var reserved: Boolean) {
	def reserve(r: Boolean): Unit = {reserved = r}
}

class Lotus(val color: String, reserved: Boolean) extends Car("Lotus", reserved)
val l = new Lotus("Silver", false)
println(s"Requested a ${l.color} ${l.make}")
~~~
* 함수와 동일하게, 매개변수를 초기화시켜 선언할 수도 있음(예제는 생략함)
* 함수의 입력 또는 반환 타입을 특징짓는 타입 매개변수 또한 클래스 정의에 사용할 수 있음
ex) List[String]는 String 인스턴스를 포함하며 String을 취하고 반환하는 연산을 지원
##### 우리만의 컬렉션을 만들고, 타입 안전성이 보장되도록 타입 매개변수를 사용해보기
* 새로운 컬렉션은 Iteratble의 부모 클래스인 Traversable[A]를 확장
~~~
class Singular[A](element: A) extends Traversable[A] { // 클래스 정의에서 부모 클래스에 타입 매개변수를 넘기는 좋은 예제
	def foreach[B](f: A => B) = f(element)
}

val p = new Singular("Planes")
p foreach println
val name: String = p.head
~~~
### 그 외에 클래스 유형
#### 추상 클래스
* 추상 클래스(abstract class)는 다른 클래스들에 의해 확장되도록 설계되었으나 , 정작 자신은 인스턴스를 생성하지 않는 클래스
* 추상 클래스를 정의할 때는 class 대신 abstract 키워드 사용
* 추상 클래스는 서브클래스들이 필요로 하는 핵심적인 필드와 메소드를 실제 구현물을 제공하지 않으면서 정의하는데 사용될 수 있음
##### 추상 클래스 예제
~~~
abstract class Car {
	val year: Int
	val automatic: Boolean = true
	def color: String
}

new Car() (error)
class RedMini(val year: Int) extends Car {
	def color = "Red"
}
val m: Car = new RedMini(2005)
~~~
#### 익명 클래스
* 부모 클래스의 메소드를 구현하는 또다른 방식은 익명 클래스를 사용하는 것
* 일회적 익명 클래스를 정의하기 위해 부모 또는 추상 클래스의 인스턴스를 생성하고,  클래스명과 매개변수 다음의 중괄호 안에 구현 내용을 포함하면 됨
##### 자바 어플리케이션에서 일반적으로 사용되는 Listener class 확인해보기
~~~
abstract class Listener {def trigger}
val myListener = new Listener {
	def trigger{ println(s"Trigger at ${new java.util.Date}") }
}
myListener.trigger
~~~
##### 자바 어플리케이션에서 일반적으로 사용되는 Listener class 확인해보기(응용)
* Listener를 등록하고 필요에 따라 나중에 트리거할 수 있는 Listening 클래스가 있음
* 한 줄에 익명 클래스의 인스턴스 생성하고 이를 다른 줄에 있는 등록 함수에 전달
~~~
abstract class Listener { def trigger }
class Listening {
	var listener: Listener = null
	def register (l: Listener){listener = l}
	def sendNotification() {listener.trigger}
}

val notification = new Listening()
notification.register(new Listener {
	def trigger {println(s"Trigger at  ${new java.util.Date}")}
})
notification.sendNotification
~~~
* 서브클래스가 한 번만 필요한 상황이라면, 익명 클래스 구문이 우리 코드를 단순화 시키는데 좋음

### 그 외의 필드와 메소드 유형
####  overloaded method
* 클래스 내에  다른 입력 매개변수를 갖는 복수개의 메소드를 가질 수 있음
~~~
class Printer(msg: String) {
	def print(s: String): Unit = println(s"$msg: $s")
	def print(l: Seq[String]): Unit = print(l.mkString(", "))
}

new Printer("Today's Report").print("Foggy" :: "Rainy" :: "Hot" :: "Nil")
~~~
* 당연하지만, 동일한 이름과 동일한 매개변수를 가지는 메소드는 중복 선언할 수 없음

####  apply method
* apply 메소드는 기본 메소드 또는 인젝터 메소드라고 불림
* 메소드의 이름 없이 호출될 수 있음
* apply 메소드는 근본적으로 메소드 이름 없이 괄호를 사용하여 적용할 수 있는 기능을 제공하는 간단한 방법
##### 미리 정의된 수로 숫자들을 곱하는 클래스 예제
~~~
class Multiplier(factor: Int) = {
	def apply(input: Int) = input * factor
}

val tripleMe = new Multiplier(3)
val tripled = tripleMe.apply(10)
val tripled2 = tripleMe(10) // apply라는 이름 없이도 사용 가능
~~~
* apply 메소드를 사용하면, 코드가 이상하게 보일 수 있음. 따라서 반드시 필요한 곳에 사용

####  Lazy value
* 지금까지 클래스에서 사용했던 필드는 모두 클래스가 처음 인스턴스를 생성할 때 만들어졌음
* lazy value는 자신이 처음 인스턴스화될 때만 생성됨(lazy value 자체에 처음 접근할 때 초기화 됨)
lazy value를 초기화하는 표현식은 그 값이 최초로 호출될 때에만 실행됨
* lazy value는 val 키워드 앞에 lazy 키워드를 추가함으로써  만들 수 있음
##### 일반값이 계산되는 것과 lazy value가 계산되는 것을 비교해주는 예제
~~~
class RandomPoint {
	val x = { println("creating x"); util.Random.nextInt }
	lazy val y = { println("now y"); util.Random.nextInt }
}

val p = new RandomPoint()
println(s"Location is ${p.x}, ${p.y}")
~~~
* 일반 값인 x 필드는 인스턴스 p가 생성될 때 초기화 됨
* lazy value는 우리가 그 값에 처음 접근할 때 초기화 됨
* lazy value는 클래스 수명 내에  실행 시간과 성능에 민감한 연산이 한 번만  
실행될 수 있음을 보장하는 훌륭한 방식
* 파일 기반의 속성, DB Connection, 정말 필요한 경우 한 번만 초기화되어야 하는 불변의 데이터와 같은 정보를 저장하는 데 보편적으로 사용

### 패키징
* 일반적으로 우리가 만든 클래스를 생성한 다음, 어느 시점에 이를 정리해야 함
* 패키지는 스칼라 코드 체계를 위한 시스템
* 패키지는 스칼라 코드를 점으로 구분된 경로를 이용하여 디렉터리별로 정리할 수 있게 해줌
* 소스 맨위에서 package 키워드를 이용하여 그 파일의 모든 클래스가 패키지에 포함됨을 선언하면 됨
* 스칼라의 패키지 명명법은 자바 표준을 따름
ex) Netflix 에서 개발된 utility 메소드를 제공하는 스칼라 클래스라면 'com.netflix.utilities'에 패키징 됨
* 스칼라 소스 파일은 해당 패키지와 일치하는 디렉토리에 저장되어야 함
ex) 'com.netflix.utilities' 패키지의 DateUtilities 클래스는,  
com/netflix/utilities/DateUtilities.scala에 저장 되어야함

#### 패키징된 클래스에 접근하기
* 패키징된 클래스는 점으로 구분된 전체 패키지 경로와 클래스 이름으로 접근할 수 있음
##### java.util 패키지에 있는 JDK의 Date 클래스에 접근해보기
~~~
val d = new java.util.Date
~~~
* 더 편리한 방식으로는 패키지를 현재 namespace에 import 하는 것
* 이 방식으로 클래스는 패키지 접두어가 없어도 접근 가능
##### 클래스를 현재 네임스페이스에 import 하고 새로운 Date 만들기
~~~
import java.util.Date
val d = new Date
~~~
* 자바와 달리,  script 어디에서든 import 명령어를 사용할 수 있음
* 스칼라는 밑줄(_) 연산자를 이용해서 패키지 전체 내용을 한 번에 임포트 할 수 있음
##### import-all을 이용하여 가변적인 컬렉션을 모두 import 하고, ArrayBuffer, Queue collection 시험해보기
~~~
import collection.mutable._
val b = new ArrayBuffer[String]

b += "hello"

val q = new Queue[Int]
q.enqueue(3, 4, 5)

val pop = q.dequeue
println(q)
~~~
* 패키지의 모든 클래스와 하위 패키지를 임포트하는 데는 잠재적인 단점이 있음  
만약 네임스페이스에 동일한 이름의 클래스가 선언되어 있다면, 더이상 접근 할 수 없음  
따라서  반드시 대량 임포트시 패키지의 내용물을 검사해야 함
* 전체 패키지를 임포트하는 대신 import group을 사용할 수 있음
~~~
import collection.mutable.{Queue, ArrayBuffer}
val q = new Queue[Int]
val b = new ArrayBuffer[String]
~~~
* 가변적인 Map 과 불변의 map 컬렉션을 이름 충돌없이 사용하려면 import alias 를 사용해야 함
* 이름이 바뀌는 것은 로컬 네임스페이스에서 클래스에 대한 참조이지 그 클래스 자체는 아님  
따라서 네임스페이스 바깥의 클래스가 실제로 변경되는 것은 아님
##### import alias 사용 예제
~~~
import collection.mutable.{Map => MutMap}
val m1 = Map(1 -> 2)
val m2 = MutMap(2 -> 3)
~~~
* 별칭이 부여된  collection인 MutMap으로 패키지를 기술하지 않아도 이름으로 가변의 맵과 불변의 맵 모두를 사용할 수 있음
#### 패키징 구문
*  패키지를 지정하는 다른 형태(잘 사용 X)로 packaging 구문을 사용
~~~
package com {
	package oreilly {
		class Config(val baseUrl: String = "http://localhost")
	}
}

val url = new.com.oreilly.Config().baseUrl
~~~
### privacy control
* 코드 패키징은 결국 패키지 접근을 관리하기 위해 privacy control를 사용할 수 있다는 점으로 귀결됨
* 코드를 별도의 패키지로 구조화하는 동안 한 패키지의 특정 기능을 다른 패키지에는 숨겨야 할 경우가 있을 수 있음  
ex) 특정 계층이 커뮤니케이션의 중간 계층을 사용하도록 강제하기 위해 낮은 레벨의 persistence code를 사용자 인터페이스 레벨의 코드로부터 은닉할 수 있음  
ex) 서브클래스 확장을 제한하여 부모 클래스의 구현자를 추적할 수 있도록 원할 수도 있음
* 기본적으로 스칼라는 프라이버시 제어를 추가하지 않음. 우리가 작성한 모든 클래스는 인스턴스 생성이 가능하며, 그 필드와 메소드는 어떤 코드에서도 접근할 수 있음
* 클래스 내부에서만 처리되어야 할 가변적인 상태 정보처럼 프라이버시 제어를 해야 할 이유가 있다면, 클래스에서 필드와 메소드 기반으로 프라이버시 제어를 추가할 수 있음
#### protected keyword
* privacy control 중 하나는 필드와 메소드를 protected로 표시하는 것으로 해당 필드와 메소드의 접근을 동일 클래스 또는 그 클래스의 서브 클래스의 코드에서만 가능도록 제한
* val, var, def 키워드 앞에 protected 키워드를 사용
##### protected 사용 예제
~~~
class User { protected val passwd = scala.util.Random.nextString(10) }
class ValidUser extends User { def isVaild = ! passwd.isEmpty }
val isVaild = new ValidUser().isVaild
println(isVaild)

val passwd = new User().passwd ( error )
~~~
* 해당 필드와 메소드의 접근을 이를 정의한 클래스에서만 가능하도록 제한하는 방법은 private으로 표시  
ex) 특정 password를 해당 클래스 내에서 평문으로 저장하였을 때, private으로 접근 제한을 둘 수 있음

#####  User class 내에 password 관리 예제
* 패스워드를 private으로 만들어 'User' class만 접근하도록 함으로써 문제 해결
* 패스워드를 가변적으로 만들고, 경보 시스템을 가지는 퍼블릭 설정 메소드(public setter method)를 추가하여  
패스워드 변경에 대한 로그를 검사
* private 패스워드를 외부의 일고/쓰기에 노출시키지 않고 검증하는 시스템 추가
~~~
class User(private var password: String) = {
	def update(p: String) {
		println("Modifying the password")
		password = p
	}
	def validate(p: String) = p == password
}

val u = new User("1234")
val isValid = u.validate("4567")
println(isVaild)

u.update("4567")
val isValid = u.validate("4567")
println(isVaild)
~~~
### 프라이버시 접근 변경자
* 클래스 자체 뿐만 아니라 클래스 항목들에까지 세밀하게 접근 제어가 필요할 수 있음  
ex) DB 레벨의 메소드 중 일부만 동일 패키지의 다른 클래스에 드러내기를 원할 수 있음
* private, protected 지정에 더하여 access modifier를 기술함으로써 제어 가능
access modifier는 패키지, 클래스, 인스턴스와 같이 주어진 지점까지만  
유효함을 명시하고 그 지점 이내에서는 비활성화 되게 함
* access modifier의 또 다른 이점은 클래스의 접근 제어가 가능하다는 점
* access modifier를 명시하기 위해 private, protected 키워드 다음에 걲쇠괄호 안에 패키지 또는 클래스의 이름을 작성하거나, this를 사용
##### 패키지-레벨, 인스턴스-레벨의 보호를 기술하는 예제
~~~
package com.oreilly {
	// Config class에서의 접근은 com.oreilly 패키지로 제약됨.
	private[oreilly] class Config {
		val url = "http://localhost"
	}

	class Authentication {
	private[this] val password = "jason" // password 필드는 동일 클래스의 동일 인스턴스 내부
										 //  코드 외의 어떤 사람도 접근할 수 없음
	def validate = password.size > 0
	}

	class Test {
		println(s"url = ${new Config().url}")
	}
}

val vaild = new com.oreilly.Authentication().validate // 여기에서 동일 인스턴스로부터 "password"에                              
                                                      // 접근하는 것을 검증
println(vaild)

new com.oreilly.Test // 'Test' 클래스는 성공적으로 'Config' 클래스를 인스턴스화할 수 있지만..
new com.oreilly.Config(error) // 패키지 외부로부터 동일한 작업을 수행할 수 없음
~~~
* 패키지 레벨 보호의 경우, 다른 클래스의 근접성에 기반하여 재정의 할 수 있음
* 인스턴스 레벨의 보호는 클래스의 실제 인스턴스를 기반으로 정책들에 추가적인 제약을 가중시킴

### final class와 sealed class
* final class는 서브 클래스에서 재정의 할 수 없음
* 값, 변수, 메소드를 final 키워드로 표시하면 그 구현은 모든 서브클래스에서 사용할 구현임을 보장
* final class가 너무 제한적이면, sealed class 사용을 고려
* sealed class는 클래스의 서브 클래스가 무모 클래스와 동일한 파일에 위치하도록 제한함
* 클래스 정의 앞에 class 키워드와 함께 sealed 키워드를 붙임으로써 봉인할 수 있음
* sealed class는 특정 서브클래스를 '알고' 참조하는 추상적인 부모클래스를 구현하는데 유용한 방법
* 같은 파일 외부에 서브클래스를 생성하는 것을 제한함으로써 클래스 구조에 대하여 가정할 수 있으며, 그렇지 않으면 심각한 악영향을 미칠 수 있음

### 요약
* 클래스가 값과 메소드의 전용 컨테이너는 아님
* object(객체)가 독자적으로 클래스와 동일하게 사용될 수 있는지를 파악 해야 함
