## Chapter03 - 표현식과 조건문
### 개요
* 표현식, 문장, 조건문에 대해서 설명
* 함수와 표현식은 우리가 입력한 값에 대한 반환값 이외에는 영향을 주지 않음(pure)  
함수형 프로그래밍의 목표이자 이점 중 하나

### 표현식
* 표현식(expression)은 값을 반환하는 코드의 단위
##### 간단한 스칼라 표현식 예제
~~~
"hello" // 리터럴 값
"hel" + "l" + "o" // 계산된 값
~~~
* 두 예제는 서로 다른 방식으로 작성되었지만 동일한 결과 값을 리턴
* 표현식에서 중요한 것은 반환 값 "hello"

#### 표현식으로 값과 변수 정의하기
* 표현식은 값, 변수, 리터럴, 함수 어디든 성립 가능(중요한 특성)

##### 표현식을 이용하여 값과 변수 정의
~~~
val <식별자>[:<타입>] = <표현식>
var <식별자>[:<타입>] = <표현식>   
~~~

#### 표현식 블록
* 중괄호를 이용하여 여러 코드를 묶는 블록을 만들 수 있음
* 블록 내에 국한된 값과 변수를 가짐
* <b/>마지막 표현식의 블록의 반환 값이 됨 </b>

##### 표현식 블록 미사용 vs 표현식 블록 사용 예제
~~~
// 표현식 블록 사용 안한 경우
val x = 5 * 20 ; val amount = x * 10
// 표현식 블록 사용한 경우
val amount = {val x = 5 * 20; x * 10 }
~~~
* 표현식 블록을 사용함으로서 x 값의 의도가 확실함으로 더 클린한 코드
* 표현식 블록은 여러 줄로 확장 가능
##### 표현식 블록 여러 줄 확장 예제
~~~
val amount = {
	val x = 5 * 20
	x * 10
}
~~~
* 표현식 블록의 중괄호는 중첩도 가능  
제어 구조를 사용할 때 중첩 사용
##### 표현식 블록 중첩 사용 예제
~~~
val a = 1; {val b = a * 2; {val c = b + 4; c}}
~~~

### 문장(statement)
* 값을 반환하지 않는 표현식
* 문장의 반환 타입은 Unit
* 보편적으로 사용되는 문장들에는 println() 호출과 값/변수 정의가 있음
~~~
val x = 1
println(1)
~~~
* 문장 블록은 기존 값을 수정, 정의하거나  
어플리케이션 범위 밖(ex) 콘솔, DB 업데이트 등)을 변경하는데 사용

### if-else 블록
* 스칼라는 if와 else만을 지원  
즉 else-if 는 단일 구성체로 인식하지 않고, else + if로 인식됨  

#### if 표현식
* 일반적으로 사용하는 if 표현식과 동일
~~~
if (43 % 3 > 0) println("Not a multiple of 3 ")
~~~
* if 블록 자체가 위의 예제 처럼 문장(statement) 이 아닌 표현식으로 사용되면  
결과가 false면 Any Type이 return될 수 있음

##### 버그를 유발할 수 있는 예제
~~~
val result = {if(false) "what is this return?"}
~~~
#### if-Else 표현식
* 일반적으로 사용하는 if else 표현식과 동일

##### if-Else 예제
~~~
val x = 10; val y = 20
val max = if(x > y) x else y
~~~
* if 표현식에서는 반드시 중괄호를 사용해야 하며,  
if-else는 한 줄에 쓸 경우 중괄호 필요 없음

### 매치 표현식 **
* 스칼라에선 조건부 로직을 좀 더 좋은 방법으로 매치 표현식 사용 가능
* C의 Switch 문과 유사
* 만약 여러개의 case에 걸리면 제일 먼저 걸리는 case 문 실행 후 종료
* 스칼라의 매치 표현식은 0개 또는 단 한개의 Case문만 거칠 수 있으므로 break 사용 안함
* 타입, 정규 표현식, 숫자 범위, 데이터 구조 같은 다양한 항목을 매칭 시킬 수 있을 만큼 유연
* 일반적으로 if-else문 보다 매치 표현식을 더 선호

##### 매치 표현식 구문
~~~
<표현식> match {
	case <패턴 매치> => <표현식>
	[case...]
}
~~~
* case 블록에 다중 표현식이 있는 경우 {} 로 감쌈

##### 매치 표현식 예제
~~~
val x = 10; val y = 20
val max = x > y match {
	case true  => x
	case false => y
}
~~~
* 표현식의 반환값 외 추가적인 동작도 가능

##### case 구문 내 반환값 + println 추가 사용 예제
* 마지막 표현식만 매치 표현식의 반환 값으로 사용
~~~
val message = status match {
	case 200 => "ok"
	case 400 => {
		println(""ERROR - we called the service incorrectly")
		"error"
	}
	case 500 => {
		println("ERROR - the service encountered an error")
		"error"
	}
}
~~~

##### '|'를 사용하여 여러 패턴에 대한 동일 결과 값 리턴 예제
* 해당 case에 없는 값을 매칭시키면 error 발생
* 에러를 피하려면 wildcard-match-all 패턴 사용해야함
~~~
val kind = day match {
	case "MON" | "TUE" | "WED" | "THU" | "FRI" => "weekday"
	case "SAT" | "SUN" => "weekend"
}
~~~

#### wildcard로 매칭하기
* 와일드카드 연산자는 1. 값 바인딩(value binding)과 2. 와일드카드 연산자가 있음
##### 1. 값 바인딩
* 매치 표현식의 입력 패턴은 로컬 값에 바인딩되어 case 블록의 본문에서 사용가능
* 매칭되는 값이 없더라도 바인딩 된 값을 본문에서 사용하므로, error를 발생시키지 않고 예외 처리가 가능
* [case + 바인딩 변수] 형태로 사용하면 값이 반드시 바인딩 됨(뒤에 써야 함)
##### 값 바인딩 예제
* other는 매치 표현식의 변수인 message 값이 할당됨
other라고 쓰지 않아도 상관없음
~~~
val message = "OK"
val status message match {
	case "OK" => 200
	case other => {
		println(s"couldn't parse $other")
	}
}
~~~
##### 2. 와일드카드 연산자
* 와일드카드 연산자는 _ 로 표시  
* 최종값이 들어갈 자리의 이름을 대신하여 placeholder 역할을 함
* _ 는 어떤 입력값이라도 매칭되는 와일드카드 패턴이 됨

##### 구문 : 와일드카드 연산자 패턴
~~~
case _ => <하나 이상의 패턴>
~~~
* <b/>_ 패턴을 사용할 시, 변수 바인딩처럼 바인딩 값에 접근이 불가능</b>
* 접근하려면 입력값(위의 예제에서 message 값)에 접근해야함

##### 와일드카드 연산자 패턴 예제
* OK면 200, 아니면 바인딩 변수 값 return 하는 매치 표현식
~~~
val message = "Unauthorized"
val result = message match  {
	case "OK" => 200
	case _ => println(s"couldn't parse $message")
}
~~~

#### 패턴 가드를 이용한 매칭
* 패턴 내에 if 구문을 사용 -> 패턴 가드를 이용했다고 표현
* if 구문 사용시 중괄호 잘 사용 안 함

##### 패턴 가드를 이용한 매치 표현식 예제
~~~
val response:String = null
response match {
	case s if s != null => println(s"Received '$s'")
	case s => println("Error ! Received a null response")
}
~~~

#### 패턴 변수의 ''타입'' 매칭
* 패턴 변수 -> case 뒤에 오는 변수를 지칭
* 입력 표현식의 타입을 매칭하는 방법도 존재
* 매칭된다면 패턴 변수는 입력값을 다른 타입의 값으로 전환 할 수 있음
* 패턴 변수는 반드시 소문자여야 함
* 매치 표현식을 사용하여 값의 타입을 결정하는 방법 적용 가능  
ex) Any 타입을 가지는 입력 변수가 Int 타입에 매칭될 수 있음
* 이는 스칼라가 객체 지향적 다형성 특징을 가지고 있기 때문
##### 패턴 변수 타입 매칭 예제
* y의 값이 Any 타입을 가지더라도 Int에 매칭되어 해당 값이 출력
* 실제 선언된 타입이 Any더라도 실제 타입으로 매칭되어 반환될 수 있음
* 정수 12810은 Any 타입으로 선언되었어도 그에 맞는(Int) 포멧을 갖게 됨
~~~
val x:Int = 12810
val y:Any = x
y match {
		 case x: String => println(s"'x'")
		 case x: Double => println(f"$x%.2f")
		 case x: Float => println(f"$x%.2f")
		 case x: Long => println(s"${x}l")
		 case x: Int => println(s"${x}i") // 해당 값이 출력
	 }
~~~

### 루프(Loop)
* 스칼라에서 가장 중요한 루프는 for-loop(for-comprehension 이라고도 함)
* 루프 돌 때마다 반환값을 collection 형태로 리턴 가능
* for루프는 중첩, 필터링, 바인딩을 지원하는 등 customizing이 쉬움
* 스칼라에서는 Range라고 불리우는 새로운 데이터 구조가 존재
* to, until 키워드 사용 가능
  * to : 끝을 나타내는 정수를 포함  
  * until: 끝을 나타내는 정수를 포함하지 않음

##### 구문 : 숫자 범위 지정하기
~~~
<시작 정수값> to | until <끝 정수값>
~~~
##### 정의 : for 루프
~~~
for(<식별자> <- <반복자>)[yield][<표현식>]
~~~
* <b/>yield 사용시 컬렉션으로 반환</b>
* for 루프 사용시 (), {} 둘 다 사용 가능
  * () : 한줄에 다중반복자(iteratior)를 사용하는 경우  
	마지막 반복자 전에 ;를 붙여주어야 함
  * {} : 한줄에 단일반복자를 사용하는 경우  
  마지막 반복자 뒤에 ;를 붙이는 것은 선택사항

##### 괄호를 사용한 for 루프 예제
~~~
for (x <- 1 to 7) { println(s"Day $x:") }    // 단순 for-loop
val test = for (x <- 1 to 7) {s"Day $x:"}  // yield를 사용하여 컬렉션을 리턴 받음
println(test)
~~~


* IndexedSeq의 서브타입인 Vector는 IndexedSeq 타입 값에 할당 가능
* 즉 vector 컬렉션은 for 루프에서 반복자로 사용 가능
~~~
for (day <- test) print(day + ", ")
~~~

#### 반복자 가드(조건, 제어)
* for 루프 내 if 표현식 사용 가능

##### 반복자 for 루프 가드 사용 예제
~~~
val threes = for (i <- 1 to 20 if i % 3 == 0) yield i
~~~

##### 반복자 for 루프 가드 사용 예제 2
* if문은 줄 구분을 통해 여러개의 조건을 적용할 수 있음
~~~
val quote = "Faith,Hope,,Charity"
for {
	t <- quote.split(",")
	if t != null
	if t.size > 0
}
{println(t)}
~~~

#### n중 for문
##### n중 for문 사용 예제
~~~
for {
	x <- 1 to 10
	y <- 1 to 3
}{print(s" ($x,  $y) ")  }
~~~

#### 값 바인딩 **
* for 루프 내에서 값 바인딩이 가능
* 스칼라에서 보이는 독특한 방법. 표현식에서 크기가 복잡도를 줄여줌
* 바인딩된 값은 중첩된 반복자, 반복자 가드, 다른 바인딩된 값을 위해 사용 가능

##### 값 바인딩 예제
~~~
val powerOf2 = for (i <- 0 to 8; val pow = 1 << i ) yield pow
~~~

### While, Do/While 루프
* for 루프만큼 보편적이게 사용 안함
* yield 생성이 불가하며, 루프가 표현식이 아님
~~~
var x = 10; while (x > 0) x -= 1
val x = 10
do println(s"$x: ") while(x > 10) x -= 1
~~~

### 요약
* 표현식(ifelse 조건문, 패턴 매칭, 루프..)과 반환값은 모든 애플리케이션의 핵심 구성 요소
* 코드를 작성할 때 표현식을 고려하고 작업하는 것은 굉장히 중요함
* 표현식을 작성할 때 중요한 원칙
  * 코드를 표현식으로 어떻게 구조화할 것인지
  * 어덯게 표현식이 반환값을 유도할 것인지
  * 그 반환값으로 무엇을 할 것인지
