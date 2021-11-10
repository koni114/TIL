## Scala 타입
### Array
- 스칼라에서 객체로 만들때는 new 를 사용함
~~~scala
val a = new Array[String](2)  

// 배열에 값을 넣는 방법
a(0) = "hello"
a(1) = "world"

// 값 가져오기
// 스칼라에서는 변수 뒤에 하나 이상의 값을 괄호로 돌러싸서 호출
// apply()

print(a(0))
print(a.apply(0))

// 값 넣기
a(0) = "hello"
a.update(0, "hello") 

// 배열을 만드는 더 간편한 방법
// new 도 생략되었고 [String] 도 생략
val a = Array("hello", "world")
~~~

### List
- 스칼라의 배열이 값을 변경 할 수 있는 순서가 정해진 시퀀스라면 스칼라의 List는 기본적으로 값을 변경 할 수 없는 시퀸스임
- 생성은 배열 생성과 비슷
~~~scala
val x = List.fill(3)("foo") // List(foo, foo, foo)
List.tubulabe(5)(n => n * n)
val x = List.fill(3)("foo")

// 원소 가져오기
val a = List(1, 2, 3)
a(2)

// 두개의 리스트 합치기
val a = List(1, 2)
val b = List(3, 4)

val c = a ::: b
val d = a ++ b

// 리스트 앞에 요소 추가
val a = List(1, 2)
val b = 0 :: a

// 리스트 뒤에 추가
val a = List(1,2)
val b = a :+ 2

// 리스트 뒤에 요소 추가 할 때,
// 뒤에 추가하는 연산은 리스트를 뒤집고 원소를 다시 추가 후에 다시 뒤집기
(4 :: List(1,2,3).reverse).reverse
List(1,2,3) ::: List(4)

// List의 다양한 메소드들

// 1. 빈 리스트
List()

// 2. 두 번째 인덱스 원소 얻기
val a = List(1,2,3)
a(2)

// 3. 두번째 원소 '까지' 제거
val a = List(1,2,3)
val b = a.drop(2) // 결과 : List(3)

// 4. 요소 길이 세기
val a = List("hello", "world", "boy")
a.count(s => s.length == 3)


// 5. 리스트의 각 원소를 변경해 새 리스트 반환
val a = List("hello", "world", "boy")
val b = a.map(s => s + "X")

// 다음은 주의하기
val a = 1 :: 2 :: 3 // error 발생

// 리스트 끝에 Nil을 붙여주어야 에러가 발생하지 않는데,
// 리스트 끝에 Nil을 필요로 하는 이유는 :: 메소드가 List 클래스의 맴버이기 때문
// 1 :: 2 :: 3 만 사용했다고 치면, 마지막의 3이 Int 형이여서
// :: 메소드가 없기 때문에 꽝이됨
~~~

## Tuple
- 리스트와 마찬가지로 변경 불가능 
- 리스트와 다른 점은 다른 타입의 값을 넣을 수 있음
- 메소드에서 여러 다양한 객체를 리턴해야 하는 경우 유용

~~~scala
// 생성
val p = (99, "High")      // 타입은 Tuple2[Int, String]
val k = ('u', 'r', 'the') // 타입은 Tuple3[Char, Char, String]

// 원소에 접근
println(p._1) // 튜플의 첫번째 값에 접근

// 주의사항
// 튜플은 각 원소의 접근을 0이 아니라 1부터 시작함
~~~

## Set
- 변경 가능한 것과 변경 불가능한 것 모두를 제공
- Set 을 위한 기반 Trait가 있고, 이를 상속한 변경 가능 집합, 변경 불가능 집합을 위한 2가지 Trait 이 있음
~~~Scala

val s = Set ("Hi", "There") // 리스트나 배열과 비슷하게 생성

import scala.collection.immutable.set
var s = Set ("Hi", "There")
s += "bye"
~~~

## Map
- Map 은 변경 가능한 것  (mutable.Map) 과 변경 불가능한 것
- immutable.Map 모두를 제공
~~~scala
import scala.collection.mutable.Map

// put, remove 메소드는 immutable.Map 에서는 사용 볼가
// 생성

val m = Map[Int, String]()
val m2 = Map(1 -> "one", 2 -> "two")
val m3 = Map((1, "one"), (2, "two"))

// 아래 처럼 List 를 이용해서도 다양하게 가능함
val myList = List("England" -> "London", "Germany" -> "Berlin")
val myMap = myList.groupBy(e => e._1).map(e => (e._1, e._2(0)._2))
val betterConversion = Map(myList:_*)
val scala28Map = myList.toMap 

// map 메소드를 이용
val myList = List("England", "London", "Germany", "Berlin")
val map: Map[String, Int] = myList.map{s => (s, s.length)}.toMap

// 추가 
val m = mutable.Map[Int, String]()
m(0) = "zero"
m += (1 -> "one")
m += (2 -> "two")

// immutable 맵일 경우는 다음과 같이 선언하여 사용
val m2 = m + (3 -> "three") 

// 1은 key, one 은 value
1  -> "one"    
1. -> ("one") // 위의 식의 축약형
~~~
