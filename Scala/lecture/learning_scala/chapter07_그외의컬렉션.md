## chapter07 - 그 외의 컬렉션
* 이번 장에서 어디에나 있지는 않지만, 중요한 스칼라 컬렉션을 알아보자
### 가변적인 컬렉션
* 불변의 컬렉션 List, Map, Set은 불변이지만, 새로운 컬렉션으로 변형 될 수 있음  
ex) 불변의 맵을 생성하고, 하나의 매핑을 제거하고 다른 매핑을 추가하여 변형할 수 있음
~~~
val m = Map("AAPL" -> 597, "MSFT" -> 40)
val n = m - "AAPL" + ("GOOG" -> 521)
println(n)
println(m) // 원래 컬렉션 m은 그대로 남아있음
~~~
* 코드의 안정성은 높이고, 버그를 방지하기 위해 데이터와 데이터 구조는 변경되거나 자신의 상태를 바꿀 수 없음  
ex) 동시성 코드는 어느 시점에나 바뀔 수 있어 손상되기 쉬운 데이터 구조보다 엄격하고 상태가 절대 바뀌지 않는 데이터 구조를 사용하는 것이 더 안전
* 하지만 때에 따라 가변적인 데이터를 생성 할 필요성이 있음  
ex) 루프를 돌 때, 불변의 값을 만들기 전 가변 데이터 등..
* 가변의 컬렉션을 만드는 세 가지  방법에 대해서 알아보자

#### 새로운 가변 컬렉션 생성하기
* 가장 간단하게 컬렉션을 변경하는 방법은 <b/>가변의 컬렉션 타입을 이용하는 것</b>
* 다음의 표는 표준 불변 타입인 List, Map, Set에 대응하는 가변 데이터 타입을 보여줌

> |불변의 타입| 가변적인 대응 타입 |
> |---|:---:|
>  | collection.immutable.List | collection.mutable.Buffer|
>  | collection.immutable.Set |collection.mutable.Set|
>  | collection.immutable.Map |collection.mutable.Map|
* collection.immutable 패키지는 자동 추가되는 한편, mutable 패키지는 아님  
따라서 가변 컬렉션 타입을 호출 할 때 그 타입의 전체 패키지 이름이 포함 되었는지 확인 필요
* collection.mutable.buffer는 범용적인 가변의 시퀀스이며, 시작, 중간, 끝에 요소들을 추가할 수 있음
##### buffer를 이용하여 요소 추가 예제
~~~
val nums = collection.mutable.Buffer(1) // 반드시 초기값을 선언해야 함
for (i <- 2 to 10) nums += i
println(nums)
~~~
* 가변적인 Set이나 Map에서 타입 매개변수를 지정하는 것은 빈 컬렉션을 생성할 때만 필요
* 가변적인 buffer는 언제든지 불변의 리스트로 변경 가능
~~~
val l = nums.toList
~~~
* 마찬가지로, toSet, toMap을 통해 불변의 Set, Map으로 변경 가능

#### 불변의 컬렉션으로부터 가변적인 컬렉션 만들기
* 불변의 컬렉션을 가변적인 컬렉션으로 전환할 수 있음
* 불변의 컬렉션인 List, Map, Set은 모두 toBuffer 메소드를 이용하여 가변적인 타입인 collection.mutable.Buffer 타입으로 전환 가능
* Map 같은 경우 키-값 튜플의 시퀀스로서 버퍼로 전환됨
* Set을 Buffer로 전환할 때 unique 하다는 제약조건이 사라지게 됨  
따라서 다시 Set으로 전환할 때 중복 데이터는 삭제되도록 해야함
##### 불변하는 Map -> 가변 Buffer -> 불변의 Map으로 전환 예제
~~~
val m = Map("AAPL" -> 597, "MSFT" -> 40)
val b = m.toBuffer
b trimStart 1 // trimStart는 시작점에서 부터 n 개수만큼 제거 하는 method
b += ("GOOG" -> 521)
val n = b.toMap
~~~
* 만약 우리가 원하는 것이 단순히 for 루프 내에서 컬렉션을 단순히 추가하는 것이라면  
Buffer 대신 Builder를 사용하는 것이 더 낫다

#### 컬렉션 빌더(builder) 사용하기
* Builder는 Buffer의 단순 형태로, 할당된 컬렉션 타입을 추가하고, 추가(append) 연산만을 지원하도록 되어 있음
* 특정 컬렉션 타입의 빌더를 생성하려면 해당 타입의 newBuilder 메소드를 호출하고 해당 타입의 컬렉션 구성 요소를 포함하면 됨
* builder의 result method를 호출하면 최종적으로 Set으로 전환해줌

##### builder로 Set을 생성하는 예제
~~~
val b = Set.newBuilder[Char]
b += 'h'
b ++= List('e', 'l', 'l',' o')
val helloSet = b.result
println(helloSet)
~~~
* 불변의 컬렉션으로 전환하기 위해 단순히 가변적인 컬렉션을 반복적으로 생성한다면 builder 사용
* 만약 가변적인 컬렉션을 만드는 동안 Iterable 연산이 필요하거나 불변의 컬렉션으로 전환할 계획이 없으면 Buffer나 다른 가변적인 컬렉션 타입중 하나를 사용

### 배열(Array)
* Array는 고정된 크기를 가지며, 내용을 변경할 수 있으며, 인덱스를 가지고 있는 컬렉션
* scala.collections 패키지에 들어있지 않고, 루트 Iterable 타입으로부터 확장된 타입이 아니므로 공식적인 collection은 아님
* Array 타입은 실제로 자바의 배열 타입을 implicit class라 부르는 고급 특징으로 감싼 wrapper임
* implicit class는 배열을 시퀀스처럼 사용할 수 있도록 해줌  
스칼라는 JVM 라이브러리 및 자바 코드와의 호환성을 위해, 그리고 색인된 컬렉션에 대한 보조 기억으로 Array 타입을 제공
~~~
val colors = Array("red", "green", "blue")
colors(0) = "purple"
println(colors)
println(colors.toString())

val files = new java.io.File(".").listFiles
val scala = files map (_.getName) filter(_ endsWith "scala")
~~~
* 결과적으로 Array 내에 배열을 확인 할 수 없다
* 그 이유는 자바 배열은 모든 자바와 스칼라 객체가 상속하는 toString method를 override 하지 않기 때문
* 스칼라 컬렉션은 그렇지 않는데, 그 이유는 모두 자신의 내용물과 구조를 사람이 읽을 수 있도록  toString를 override 함
* 결과적으로 JVM 코드를 위해 필요한 경우가 아니라면 일반적인 용도로 이 타입을 사용하는 것은 권장하지 않음

### Seq와 시퀀스
* Seq는 모든 시퀀스의 루트 타입으로, List 같은 연결 리스트와 Vector 같은 색인 리스트를 포함  (여기서 말하는 색인 리스트는 LinkedList 를 생각하면 됨)
* 루트 타입으로서 Seq는 인스턴스화 될 수 없지만, List를 생성하는 빠른 방법으로 Seq를 호출 할 수 있음
![img](C:/러닝스칼라/seq.png)
출처 : https://alvinalexander.com/scala/understanding-scala-collections-hierarchy-cookbook

#### 시퀀스 타입

> | 이름 | 설명 |
> |---|:---:|
>  | Seq| 모든 시퀀스의 루트, List()의 가장 간단한 방법|
>  | IndexedSeq| 색인 시퀀스의 루트, Vector()의 손쉬운 방법 |
>  | Vector| 색인된 접근을 위해 Array 인스턴스에 의해 지원받는 리스트|
>  | Range| 정수의 범위, 데이터를 즉시 생성함|
>  | LinearSeq| 선형(연결 리스트) 시퀀스의 루트|
>  | List | 구성 요소들의 단방향 연결 리스트 |
>  |Queue | FIFO 리스트 |
>  | Stack| LIFO 리스트 |
>  | Stream| 지연(Lazy) 리스트, 항목들은 그 항목에 접근할 때 추가됨 |
>  |String | 문자(character)의 컬렉션 |
* Vector는 색인 시퀀스로 인덱스로 항목에 직접 접근이 가능
* List는 n번째 항목에 접근하려면 리스트의 헤드로부터 n-1 단계가 필요
* 실제로 Seq, IndexedSeq를 사용할 일은 거의 없을 것임
* 시퀀스에 String 타입이 포함된 것이 좀 다르지만, 스칼라에서는 다른 타입들과 마찬가지로 유효한 컬렉션
* String 타입은 불변의 컬렉션이며, Iterable 연산 뿐만 아니라, split과 trim과 같은 java.lang.String 연산도 함께 지원

##### Iterable의 sub type과 java.lang.String의 wrapper 를 사용하는 예제
~~~
val hi = "Hello, " ++ "worldly" take 12 replaceAll ("w", "W")
~~~

### 스트림(Stream)
*  Stream 타입은 하나 또는 그 이상의 시작 요소들과 재귀 함수로 생성되는 지연(lazy) 컬렉션
* 다른 불변의 컬렉션들은 내용의 100%를 초기화 시점에 받지만, 스트림의 구성 요소들은 최초로 접근될 때 컬렉션에 추가
* 스트림이 생성한 구성 요소들은 나중에 추출될 때를 대비하여 캐시에 저장되어 각 요소가 한 번만 생성됨을 보장함
* 스트림은 무한히 커질 수 있음
* 이론적으로 구성 요소들이 접근 시에만 현실화되는 무한 컬렉션
* List.Nil에 대응하는 항목인 Stream.Empty로 종료될 수 있음
* 리스트와 마찬가지로 헤드(현재 요소)와 테일(컬렉션의 나머지)로 구성된 재귀적인 데이터 구조
* 스트림은 헤드를 포함하는 새로운 스트림을 반환하는 함수와 그 함수를 재귀적으로 호출하여 테일을 구성함으로써 생성할 수 있음
* Stream.cons를 사용하여 헤드와 테일로 새로운 스트림을 구성할 수 있음
##### 새로운 스트림을 구성하고 재귀적으로 생성하는 함수 예제
~~~
def inc(i: Int): Stream[Int] = Stream.cons(i, inc(i+1))
val s = inc(1)
~~~
* 스트림이 생겼는데, 시작값(1)과 ?만 포함하고 있음
* take 메소드를 이용하여 추가적으로 값을 취하고, 리스트로 검색해보자
~~~
val l = s.take(5).toList
println(l)
~~~
* 원래의 스트림 s를 출력해보면, 5개의 구성 요소를 포함하고 있고, 더 많은 요소를 추가 생성할 준비가 되어 있음을 보여줌
* 우리는 계속해서 20, 200, 200개의 구성 요소들을 take를 통해 스트림에 덧붙일 수 있음

#### #:: 연산자
* Stream.cons 연산자 대신 #:: 연산자를 사용할 수 있음  
이를 cons(construct) operator 라고 부름
* 이는 리스트의 생성 연산자 ::를 보완함

##### #:: 사용 예제
~~~
def inc(head: Int): Stream[Int] = head  #:: inc(head + 1)
inc(10).take(10).toList
~~~

##### bounded stream 만들어보는 예제
* Iterable 연산 같은 변형 연산을 지원하지만, 하나 이상의 요소는 포함할 수 없는 모나딕(monadic) 컬렉션
* 먼저, Iterable로 확장되는 모나딕 컬렉션인 Option 타입을 알아보자

~~~




def to(head: Char, end: Char): Stream[Char] = (head > end) match {
  case true => Stream.empty
  case false => to((head+1).toChar, end)
}

val hexChars = to('A', 'F').take(20).toList
println(hexChars)
~~~

### 모나딕 컬렉션
* Iterable 연산 같은 변형 연산을 지원하지만, 하나 이상의 요소는  
포함할 수 없는 모나딕(monadic) 컬렉션
* 먼저, Iterable로 확장되는 모나딕 컬렉션인 Option 타입을 알아보자

#### Option 컬렉션
* 크기가 1이 넘지 않는 컬렉션으로, Option 타입은 단일 값의 존재 또는 부재를 나타냄
* 잠재적으로 누락된 값(ex) 이 값이 초기화되지 않았거나 계산될 수 없는 경우)은 Option 컬렉션으로 감싸고 그 잠재적인 부재를 분명하게 공시함
* 일부 개발자들은 Option을 null 값의 안전한 대체재로 봄  
사용자에게 그 값이 누락될 수 있음을 알리고  NullPointerExeption을 일으킬 가능성을 줄여주기 때문
* 다른 개발자들은 연산 체인을 만드는 더 안전한 방법으로 보는데, 연산 체인 내내 오직 유효한 값만 지속되기 때문
* Option 타입 그 자체는 구현되어 있지 않지만 하나의 요소로 구성된 타입-매개 변수화된 컬렉션인 Some과 빈 컬렉션인 None, 이 두 서브타입에 기반하여 구현할 수 있음
* None 타입은 타입 매개변수가 없음. 그 안에 어떤것도 포함되어 있지 않기 때문
* 두 타입(Some, None)을 직접 사용하거나 Option을 호출하여 Null 값을 감지하고 적절한 서브타입을 선택하도록 할 수 있음

##### nonnull, null 값으로 Option 생성해보기
~~~
var x: String = "Indeed"
var a = Option(x)
println(x)
println(a)

x = null
var b = Option(x)

println(x)
println(b)
~~~
* isDefined와 isEmpty를 사용하여 주어진 Option이 각각 Some인지, None인지 확인할 수 있음
~~~
println(s"a is defined? ${a.isDefined}")
println(s"b is not defined? ${b.isEmpty}")
~~~

##### 나눗셈 연산자 (/)를 0으로 나누는 것을 방지하기 위한 검사 작업 예제
~~~
def divide(amt: Double, divisor:Double): Option[Double] = {
  if (divisor == 0) None
  else Option(amt / divisor)
}

val legit   = divide(5, 2) // 정상이라면 Some에 감싸서 나옴
val illegit = divide(3, 0) // 유효하지 않는 나눔수라면 None return
~~~
* 값을 Option 컬렉션에 감싸서 반환하는 함수는 함수가 입력 값에 적절한 값을 return 하지 못할 수도 있다는 것을 암시
* 즉 Option은 함수 결과를 처리하는 데 타입에 안전한(type-safe) 방식을 제공
* 이 방식이 누락된 값을 의미하는 Null 값을 반환하는 자바 표준보다 안전

##### 빈 컬렉션을 안전하게 처리하도록 headOption 을 호출하는 예제
~~~
val odds = List(1, 3, 5)
val firstodd = odds.headOption
val evens = odds filter (_ % 2  == 0)
val firstEven = evens.headOption
println(firstEven)
~~~

##### filter와 map을 사용하여 'lowercase' 결과를 값을 유지하는 예제
~~~
val words     = List("risible", "scavenger", "gist")
val lowercase = words find (w => w == w.toLowerCase)

println(lowercase)

val filtered  = lowercase filter (_ endsWith "ible") map (_.toUpperCase)
val exactSize = filtered filter (_.size > 15) map (_.size)

println(filtered)
println(exactSize)
~~~
* 연산은 현재 값(Some)에 적용되고 누락된 값(None)에는 적용되지 않지만, 결과 타입은  
마지막 연산의 타입(Option[Int])과 일치할 것임

#### Option으로부터 값 추출하기
* Option 컬렉션은 존재 여부가 확실하지 않은 값을 저장하고  
변환하는 안전한 메커니즘과 연산을 제공함
* <b/>Option 컬렉션은 잠재적인 값을 추출하는 안전한 연산도 제공</b>
* Option.get() 은 None 인스턴스에 적용하면 no such element error를 발생시키므로, 사용을 피하자
* Option 연산의 핵심은, 누락된 값을 안전하게 처리하는데 있음
* Option 값 추출 연산중에 누락된 값 대신 대체하거나 오류 상태를 일으킬 수 있는 함수가 있음

##### nextOption 함수: 매번 유효한 Option 값과 누락된 Option값 중 하나를 반환
~~~
def nextOption = if (util.Random.nextInt > 0) Some(1) else None
~~~

##### 안전한 Option 추출
> | 이름 | 예제 | 설명|
> |---|:---:|:---:|
>  | fold | nextOption.fold(-1)(x => x)| Some인 경우 해당 값 추출. None이면 시작값을 반환|
>  | getOrElse| nextOption getOrElse 5 | Some의 값을 반환하거나 아니면 이름 매개변수의 결과를 반환
>  | orElse | nextOption orElse nextOption | 실제로 값을 추출하지는 않지만 None 인 경우 값을 채우려 함 |
>  | 매치 표현식 | nextOption match {case Some(x) => x; case None => -1}|매치표현식을 이용한 처리|

* 우리만의 함수를 만들 때 입력 매개변수와 반환값에 잠재적 값을 표현해야 하는 경우 유용
* null을 사용해도, 모든 NullPointerExeption을 방지 할 수 없기 때문!

#### Try 컬렉션
* util.Try 컬렉션은 에러 처리를 컬렉션 관리로 바꿔 놓음
* 이 컬렉션은 주어진 함수 매개변수에서 발생한 에러를 잡아내는 메커니즘을 제공하여 함수가  
성공적으로 실행된 경우에는 함수의 결과 값을, 아니면 에러를 반환
* 스랄라는 exception을 발생시킴으로써 에러를 일으킬 수 있음
* 예외를 발생시키기 위해 Exception 인스턴스와 함께 키워드 throw를 사용하면 됨
* Exception에 제공된 텍스트 메세지는 선택사항
~~~
throw new Exception("No DB connection, exiting...")
~~~
##### 예외를 시험해보기 위해 입력 값 기준에 따라 예외를 발생시킬 함수를 생성해보고 예외를 발생시켜 보기
~~~
def loopAndFail(end: Int, failAt: Int):Int = {
  for (i <- 1 to end) {
    println(s"$i) ")
    if (i == failAt) throw new Exception("Too many iterations")
  }
}
~~~
* util.Try 로 감싸서 catch 해보자
* Option 처럼 util.Try 타입은 구현되어 있지 않지만, 두 개의 구현된 서브타입인 Success 와  
Failure를 가지고 있음
* Success 타입은 예외가 발생하지 않으면 반환값을 포함함
* Failure 타입은 발생한 Exception을 포함
~~~
val t1 = util.Try( loopAndFail(2, 3) )
val t2 = util.Try( loopAndFail(4, 2) )
~~~
#### 에러 처리 기법 정리
* 어플리케이션 요건과 맥락에 따라 적절한 에러 처리 방식이 다름
* 경험상 일반적으로 적용되는 에러 처리 기법은 많지 않음

##### 무작위적으로 에러를 발생시키는 함수 생성
~~~
def nextError = util.Try { 1 / util.Random.nextInt(2) }
val x = nextError  // 0이 나와 실패 했다고 가정
val y = nextError // 성공 했다고 가정
~~~

##### Try 를 이용한 에러 처리 메소드

> | 이름 | 예제 | 설명|
> |---|:---:|:---:|
>  | flatMap | nextError flatMap { _ => nextError }| Success인 경우 util.Try를 반환하는 함수를 호출함으로써 현재의 반환값을 새로운 내장된 반환값(또는 예외)에 매핑함. 우리의 'nextError' 데모 함수는 입력값을 취하지 않기 때문에 우리는 현재 Success로부터 사용하지 않는 입력값을 나타내는 언더스코어를 사용함|
>  | foreach| nextError foreach(x => println("success!"+ x)) | Success 인 경우 주어진 함수를 한 번 실행하고, Failure 일 땐 실행하지 않음
>  | getOrElse|  nextError getOrElse 0 | Success에 내장된 값을 반환하거나, Failure인 경우 이름에 의한 매개변수의 결과를 반환 |
>  | orElse| nextError orElse nextError |flatMap의 반대되는 메소드. Failure인 경우 util.Try를 반환하는 함수를 호출. orElse로 Success로 전환할 수 있음|
>  | toOption| nextError.toOption | Success는 Some, Failure는 None으로 전환 |
>  | map | nextError map (_ * 2)| Success 인 경우 새로운 값에 내장된 값을 매핑하는 함수 호출|
>  | 매치 표현식 | nextError match {case util.Success(x) => x; case util.Failure(error) => -1}|매치표현식을 이용한 처리|
>  | 아무 일도 하지 않음| nextError |단순히 호출 값이 어플리케이션을 타도록 내버려 둠|

##### 에러 처리 메소드 예제 : 공백 parsing을 통한 Int 전환
~~~
val input = " 123 "
val result = util.Try(input.toInt) orElse util.Try(input.trim.toInt)
result foreach { r => println(s"Parsed '$input' to $r!") }
val x = result match {
    case util.Success(x) => some(x)
    case util.Failure(ex) => {
      println(s"Couldn't parse input '$input'")
      None
    }
}
~~~
* <b/>예외는 반드시 그 내용이 전달되고 처리되어야 함을 잊지말자</b>

### 퓨처 컬렉션
* 퓨처(future)는 Option과 Try와 같이 잠재적 값을 나타냄
* 다른 점은 thread(스레드)의 최종 반환값의 모나딕 컨테이너 뿐만 아니라 백그라운드 자바 스레드의 monitor 이기도 함
* 퓨처의 호출법은 매우 쉬움. 백그라운드로 실행하고자 하는 함수를 가지고 퓨처를 호출하면 됨
##### 메세지를 출력하는 함수로 퓨처 생성
* 퓨처를 생성하기 전에 현행 세션 또는 어플리케이션에서 함수를 동시 실행하기 위한 context를 지정해야 함
* global context를 사용하여 자바 스레드 라이브러리를 사용 할 것임
~~~
import concurrent.ExecutionContext.Implicits.global
val f = concurrent.Future {println("hi")}
~~~

##### 백그라운드 작업이 여전히 실행되는 동안 퓨처를 받을 수 있도록 Thread.sleep 이용 예제
~~~
import concurrent.ExecutionContext.Implicits.global
val f = concurrent.Future {Thread.sleep(5000);println("hi")}
println("waiting")
~~~
* 백그라운드 작업은 5초 동안 잠든 후에 'hi' 메세지 출력
* 그 사이에 main 스레드에서의 코드는 백그라운드 작업이 완료되기 전에 waiting 메세지 출력
* 퓨처의 작업이 완료될 때 실행할 콜백 함수 또는 추가적인 퓨처를 설정할 수 있음
ex) API 호출은 호출자에게 제어권을 넘겨주는 동안 백그라운드에서 중요하지만 시간이 오래걸리는 작업을 시작 할 수 있음
ex) 네트워크 파일 전송과 같은 비동기적인 이벤트는 퓨처에서 시작할 수 있으며, 작업이 완료될 때까지 또는 시간제한에 도달할 때 까지 main thread가 잠들어 있을 수 있음
* 퓨처는 비동기, 동기 모두 관리 가능
* 비동기식 작업이 더 효율적이기 때문에 백그라운드 스레드와 현행 스레드 모두 계속해서 실행하는 것에 대해 먼저 살펴보도록 하겠음

#### 비동기식으로 퓨처 처리하기
* 퓨처가 완료된 다음 실행될 함수 또는 퓨처에 첫 번째 퓨처의 성공적인 결과값을 전달하여 연결 할 수 있음
* 이 방식으로 처리된 퓨처는 결국 그 함수의 반환값 또는 예외를 포함한 util.Try를 반환
* 성공했다면, 연결된 함수에 전달되거나 반환값으로 전달됨
* 실패했다면, 예외를 발생시키면서 추가적인 함수나 퓨처는 실행되지 않음

* 퓨처의 최종 결과를 받기 위해 콜백 함수를 지정할 수 있음  
콜백 함수는 최종 성공적인 값 또는 예외를 받아 그 퓨처를 생성했던 원래 코드를 해제하여 다른 작업으로 넘어갈 수 있도록 해줌

##### 실제 테스트 케이스르 제공하는 함수 생성 예제
* 잠들어 있다가 값을 반환하거나 예외를 발생시키는 함수
~~~
import concurrent.ExecutionContext.Implicits.global
import concurrent.Future

def nextFtr(i: Int = 0) = Future {
  def rand(x: Int) = util.Random.nextInt(x)

  Thread.sleep(rand(5000)) // 실제로는 효율이 떨어지므로, 사용을 지양하자
  if (rand(3) > 0) (i + 1) else throw new Exception
}
~~~

> | 이름 | 예제 | 설명|
> |---|:---:|:---:|
>  | fallbackTo | nextFtr(1) fallbackTo nextFtr(2) | 두 번째 퓨처를 첫 번째에 연결하고 새로운 종합적인 퓨처를 반환. 첫 번째 퓨처가 성공적이지 않다면, 두 번째 퓨처가 호출 됨|
> |flatMap | nextFtr(1).flatMap(int => nextFtr())|두 번째 퓨처를 첫 번째에 연결하고 새로운 종합적인 퓨처를 반환함. 첫 번째가 성공적이라면 그 반환값이 두 번째를 호출하는 사용됨|
> |map|nextFtr(1) map (_  * 2 )| 주어진 함수를 퓨처에 연결하고 새로운 종합적인 퓨처를 반환함. 퓨처가 성공적이라면 그 반환값이 해당 함수를 호출할 때 사용됨 |
> |onComplete| nextFtr() onComplete { _ getOrElse 0 }| 퓨처의 작업이 완료된 후 주어진 함수가 값 또는 예외를 포함한 util.Try를 이용하여 호출됨 |
> |Future.sequence | concurrent.Future sequence List(nextFtr(1), nextFtr(5))| 주어진 시퀀스에서 퓨처를 병행으로 실행하여 새로운 퓨처를 반환. 시퀀스 내에 모든 퓨처가 성공하면 이들의 반환값으로 리스트가 반환됨. 그렇지 않으면 그 시퀀스 내에서 처음으로 발생한 예외가 반환됨 |

* 지금까지는 퓨처를 어떻게 생성하고 관리하는지를 보는 예제들이였음. 좀 더 퓨처를 유용하게 사용하려면 생성, 관리 외에도 추출이 가능해야 함
* 퓨처의 좀 더 현실적인 예제를 통해 퓨처로 작업하는 방법을 처음부터 끝까지 알아보도록 하자

##### OpenWeatherMap API로부터 일기예보를 읽어와 처리하는 예제
* URL로부터 내용을 읽어오기 위한 스칼라 라이브러리 연산 사용  
io.Source.+fromURL(url: String) 사용
* 일기예보 데이터를 가져올 URL
http://api.openweathermap.org/data/2.5/forecast?mode=xml&lat=55&lon=0&APPID={APIKEY}
* OpenWeatherMap 은 API 접근을 위해 별도 API KEY 필요  
https://home.openweathermap.org/api_keys 에서 확인 가능
* 두 도시의 현재 온도를 확인하고 어느 도시가 더 따뜻한지 확인
* 원격 API를 호출하는 것은 시간-집약적인 작업이 될 수 있으므로 병행식 퓨처로 API 호출하여  
메인(main) 스레드와 동시에 실행할 예정
~~~
import concurrent.Future
def cityTemp(name: String): Double = {
  val url = "http://api.openweathermap.org/data/2.5/weather"
  val cityUrl = s"$url?&APPID=APIID입력&q=$name"
  val json = io.Source.fromURL(cityUrl).mkString.trim
  val pattern = """.*"temp":([\d.]+).*""".r
  val pattern(temp) = json
  temp.toDouble
}

val cityTemps = Future sequence Seq(
  Future(cityTemp("Fresno")), Future(cityTemp("Tempe"))
  )

cityTemps onSuccess {
  case Seq(x,y) if x > y => println(s"Fresno is warmer: $x K")
  case Seq(x,y) if x < y => println(s"Tempe is warmer: $y K")
}
~~~

#### 동기식으로 퓨처 처리하기
* 백그라운드 스레드가 완료되기를 기다리는 동안 스레드를 차단하는 것은 자원이 많이 소모되는 작업
* 트래픽 양이 많거나 높은 성능을 요구하는 어플리케이션이라면 이 방식을 피하고 onComplete나 onSuccess 같은 콜백 함수를 사용하는 것이 좋음
* 하지만 현행 스레드를 차단하고, 백그라운드 스레드가 성공적으로 또는 그렇지 않더라도 완료되기를 기다려야 할 때가 있음

#### 요약
* 스칼라의 가변적인 컬렉션은 두 가지 상이한 장점을 가지고 있음
  * 버퍼, 빌더 또는 다른 방식들을 사용하여 한 번에 하나의 항목씩 컬렉션을 확장하는 증분 버퍼로 사용될 수 있다
  * 불변의 컬렉션이 사용할 수 있는 다양한 종류의 연산을 지원하기도 함
* 스칼라에서의 컬렉션은 애플리케이션 데이터의 단순한 컨테이너 이상임
  * 모나딕 컬렉션은 누락된 데이터, 에러 상황, 동시 처리와 같이 민감하고 복잡한 상황에 대비하여 타입에 안전하며 연결 가능한 연산과 관리 기능을 제공
* 스칼라에서 불변 컬렉션, 가변 컬렉션, 모나딕 컬렉션은 안전하고 표현력 있는 소프트웨어 개발에 있어서 없어서는 안 될 기반 구성 요소
* 
