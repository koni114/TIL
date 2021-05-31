## chapter06 보편적인 컬렉션
* 컬렉션(collection) 프레임워크는 배열, 리스트, 맵, 집합 트리와 같이  
주어진 타입을 가지는 하나 또는 그 이상의 값을 수집하는 데이터 구조를 의미
### 리스트, 집합, 그리고 맵
* 먼저 불변의 단방향 연결 리스트인 List 타입에 대해서 알아보자
* 리스트는 이를 함수로 호출해서 생성할 수 있음
~~~
val numbers = List(32, 95, 24, 21, 17)
val colors = List("red", "green", "blue")
println(s"I have ${colors.size} colors: $colors")
~~~
* 스칼라는 시작 인덱스는 0
* head()와 tail() 메소드를 사용하여 list에 접근 할 수 있음
~~~
val colors = List("red", "green", "blue")
println(colors.head)
println(colors.tail)
colors(1)
~~~
* for 루프를 통해 list 반복하기
~~~
val numbers = List(10, 32, 41, 22, 18)
var total; for (i <- numbers) total += i
println(total)
~~~
* 스칼라의 컬렉션은 반복(iterate), 매핑(map), 축소(reduce) 하며
광범위한 다른 유용한 연산을 수행하기 위해 고차 함수를 확장하여 사용
* 리스트와 다른 컬렉션에서 사용할 수 있는 고차함수인 foreach(), map(), reduce()를 알아보자
* 각 메소드에는 함수 리터럴이 전달됨
* 함수 리터럴에는 괄호로 묶인 입력 매개변수와 함수 본문이 포함되어 있음
~~~
val colors = List("red", "green", "blue")
colors.foreach((c: String) => println(c))

val sizes = colors.map((c: String) => c.size)
println(sizes)

val numbers = List(32, 95, 24, 21, 18)
val total = numbers.reduce((a: Int, b: Int) => a + b)
println(total)
~~~
* Set은 유일한 요소들로 이루어진 불변의 컬렉션
* List와 유사하게 동작함
~~~
val unique = Set(10, 20, 30, 20, 20, 10)
val sum = unique.reduce((a: Int, b:Int) => a + b )
println(sum)
~~~
* Map은 불변의 키-값 저장소로, 다른 언어에서는 해쉬맵(hashMap), 딕셔너리(dictionary) 또는 연관 배열로 알려져 있음
* Map을 생성할 때, 키-값 쌍으  튜플로 기술하면 됨
* 키와 값 튜플을 기술하기 위해 -> 사용
~~~
val colorMap = Map("red" -> 0xFF0000, "green" -> 0xFF00, "blue" -> 0xFF)

val redRGB = colorMap("red")
val cyanRGB = colorMap("green") | colorMap("blue")
val hasWhite = colorMap.contains("White")
for (pairs <- colorMap) { println(pairs) }
~~~
### 리스트에는 무엇이 있는가?
* 컬렉션에는 문자열이나 숫자 대신 다른 타입의 값도 저장할 수 있음
~~~
val oddsAndEvents = List(List(1, 3, 5), List(2, 4, 6))
~~~
* Map과 유사하게 생긴 collections도 생성 가능
~~~
keyValues = List(('A', 65), ('B', 66), ('C', 67))
~~~
* 리스트를 리스트의 첫 번째 항목인 헤드(head)와
이를 제외한 나머지 항목들인 tail로 분해할 수 있음
~~~
val first = primes.head
val remaining = primes.tail
~~~
* List의 순회는 while문에서 isEmpty를 이용해서 마지막까지 순회가 가능함
~~~
val primes = List(2, 3, 5, 7, 11, 13)
var i = primes
while(!i.isEmpty) {print(i.head + ", "); i = i.tail}
~~~
* 가변적인 변수를 사용하지 않고, 재귀적 형태로 리스트를 순회하는 함수를 만들수도 있음
~~~
val primes = List(2, 3, 5, 7, 11)
def visit(i :List[Int]){
  if (i.size > 0) {
        print(i.head + ", ")
        visit(i.tail)
    }  
}
visit(primes)
~~~
* 스칼라에서는 List의 종점 값이 반드시 Nil 인스턴스로 끝나기 때문에
이를 비교하여 루프를 돌 수 있음
~~~
val primes = List(2, 3, 5, 7, 11, 13)
var i = primes
while(i != Nil){print(i.head + ", ") i = i.tail}
~~~
* 새 빈 리스트를 생성하면 실제로는 새로 생긴 인스턴스 대신 Nil를 반환할 것임
* Nil은 불변하는 데이터 구조이기 때문에 근본적으로  
새로 생긴 빈 리스트 인스턴스와 차이가 없음
* 단일 항목을 가지는 새로운 리스트를 생성하면, 자신의 tail로 Nil을 가리키는
단일 리스트 항목을 생성한다
~~~
val l: List[Int] = List()
println(l == Nil)

val m: List[String] = List("a")
println(m.head)
println(m.tail == Nil)
~~~
* 리스트를 생성하는 다른 방법으로, Nil과의 관계를 이용하는 것
* Lisp를 인정하는 또다른 의미로, 스칼라는 리스트를 만들기 위해
생성(cons) 연산자의 사용을 지원
* Nil을 기반으로 항목들을 결합하기 위해
오른쪽 결합형(right-associative) 생성 연산자 ::를 사용하여
전형적인 List(...) 형식을 사용하지 않고도 리스트를 만들 수 있음
~~~
val numbers = 1 :: 2 :: 3 :: Nil
~~~
* :: 연산자를 이용해서 기존 리스트 앞에 값을 추가하여 새로운 리스트를 만들 수 있음
~~~
val first = List(1)
val second = 2 :: first
second.tail = first
~~~
### 리스트 산술 연산
* 풍부한 List 메소드를 알아보자
* List 컬렉션은 불변의 데이터이기 때문에 변경한다의 의미는 새로운 리스트를 반환하는 것과 같다
> |이름| 예제 | 설명 |
> |---|:---:|:---:|
>  | :: |1 :: 2 :: Nil | 리스트에 개별 요소를 덧붙임, 오른쪽-결합형 연산자|
>  | ::: |List(1, 2) ::: List(3, 4)| 리스트 와 리스트를 결합함|
>  | ++ |List(1, 2) ++ List(2, 3)| 리스트에 다른 컬렉션을 덧붙임|
>  | == |List(1, 2) == List(2, 3)| 두 컬렉션의 타입과 내용이 똑같으면 참을 반환|
>  | distinct|List(3, 5, 4, 3,  4).distinct | 중복 요소가 없는 리스트 버전을 반환|
> | drop | List('a', 'b', 'c', ' d') drop 2| '리스트의 첫 번째 n개 요소를 뺌|
> | filter | List(23, 8, 14, 21) filter (_ > 18) | 참/거짓 함수를 통과한(만족한) 리스트의 요소들을 반환|
> | flatten |List(List(1,2), List(3, 4)).flatten| 리스트의 리스트 구조를 그 요소들을 모두 포함하는 단일 리스트로 반환|

> |이름| 예제 | 설명 |
> |---|:---:|:---:|
>  | partition | List(1, 2, 3, 4, 5) partition (_ < 3) | 리스트의 요소들을 참/거짓 함수의 결과에 따라 분류하여, 두 개의 리스트를 포함하는 튜플을 만듬|
>  | reverse |List(1, 2,  3).reverse | 리스트 요소들의 순서를 거꾸로 함|
>  | slice | List(2, 3, 5, 7) slice (1, 3) | 리스트 중 첫 번째 인덱스부터 두 번째 인덱스 -1까지 해당하는 부분을 반환|
> | sortedBy | List("apple", "to") sortBy(_.size) | 주어진 함수로부터 반환된 값으로 리스트 순서를 정렬|
>  |sorted |List("apple", "to").sorted| 핵심 스칼라 타입의 리스트를 자연값 기준으로 정렬|
>  | splitAt|List(3, 5, 4, 3,  4) splitAt 2 | List 요소들을 주어진 인덱스의 앞에 위치하는지 뒤에 위치하는지에 따라 두 리스트의 튜플로 분류함|
> | take | List(2, 3, 5, 7, 11, 13) take 3 | 리스트에서 첫 번째 n개의 요소들을 추출함 |
> | zip |  List(1, 2) zip List("a", "b")| 파이썬에서의 zip과 동일한 역할 수행|
* 여기서 고차함수는 sortBy, filter, partition이 있다
~~~
val f = List(23, 8, 14, 21) filter (_ > 18)
print(f)

val p = List(1, 2, 3, 4, 5) partition (_ <  3)
print(p)

val s = List("apple", "to") sortBy (_.size)
print(s)

~~~
* 기본적으로 List는 연결 리스트이기 때문에 그 앞에 항목들을 추가하거나,
그 앞의 항목들을 제거하는 것은 리스트 전체를 순회 할 필요가 없음
*  리스트의 시작부에서 연산을 수행하는 것이 리스트 끝에서 작업하는 것보다 더 낫다

### 리스트 매핑
* Map 메소드는 함수를 취하여 그 함수를 리스트의 모든 요소에 적용하고,
그 결과를 새로운 리스트에 수집함
* 스칼라 리스트에서 사용할 수 있는 map 메소드 중 몇개만 보여줌

> |이름| 예제 | 설명 |
> |---|:---:|:---:|
>  | collect | List(0, 1, 0) collect {case 1 => "ok"} | 각 요소를 부분 함수를 사용하여 변환하고, 해당 함수를 적용할 수 있는 요소를 유지함|
>  | flatMap |List("milk, tea") flatMap (_.split(','))| 주어진 함수를 이용하여 각 요소를 변환하고, 그 결과 리스트를 이 리스트에 평면화함|
>  | map |List("milk", "tea") map (_.toUpperCase)| 주어진 함수를 이용하여 각 요소를 반환|

~~~
List(0, 1, 0) collect {case 1 => "ok"}
List("milk,tea") flatMap (_.split(","))
List("milk", "tea") map (_.toUpperCase)
~~~

 ### 리스트 축소하기
 * 리스트의 수학적 축소 연산을 살펴보자
 > |이름| 예제 | 설명 |
 > |---|:---:|:---:|
 >  | max | List(41, 59, 26).max | 리스트의 최댓값 구하기|
 >  | min |List(10.9, 32.5, 4.23, 5.67).min| 리스트의 최대값 구하기|
 >  | product |List(5, 6, 7).product | 리스트의 숫자들을 곱하기 |
 >  | sum | List(11.3, 23.5, 7.2).sum|리스트의 숫자들을 합산하기 |

 > |이름| 예제 | 설명 |
 > |---|:---:|:---:|
 >  | contains| List(41, 59, 26) contains 29 | 리스트가 이 요소를 포함하고 있는지 확인|
 >  | endsWith |List(10.9, 32.5, 4.23, 5.67) endsWith List(4, 3)| 리스트가 주어진 리스트로 끝나는지를 검사|
 >  |exists  |List(5, 6, 7) exists (_ < 18 ) | 리스트에서 최소 하나의 요소에 대해 조건자가 성립하는지를 검사 |
 > |forall  |List(5, 6, 7) foirall (_ < 18 ) | 리스트에서 모든 요소에 대해 조건자가 성립하는지를 검사 |
 >  | startsWith | List(11.3, 23.5, 7.2) startsWith List(0) | 리스트가 주어진 리스트로 시작하는지를 테스트함 |
~~~
def contains(x: Int, l: List[Int]): Boolean = {
    var a: Boolean = false
    for (i <- l) { if (!a) a = (i == x)}
   a
}

val included = contains(19, List(46, 19, 92))
~~~
* 해당 함수 로직은 개선될 여지가 있음
* contains 로직을 함수 매개변수로 옮김으로서 우리는  
추가적인 리스트 축소 연산을 지원하는 재사용 가능한 함수를 생성할 수 있음
~~~
def boolReduce(l: List[Int], start: Boolean)(f: (Boolean, Int) => Boolean): Boolean = {
  var a = start
  for (i <- l) a = f(a, i)
  a
}
val included = boolReduce(List(45, 11, 13), false) {
  (a, i) => if (a) a else (i == 19)
}
~~~
* 위의 식을 임의의 타입의 리스트와 축소 연산에 적용할 수 있도록  
'일반화' 할 수 있음
* 이를 통해 sum, max 등 다른 수학적 연산을 구할 수 있음
~~~
def reduceOp[A, B](l: List[A], start: B)(f: (B, A) => B): B = {
  var a = start
  for (i <- l ) a = f(a, i)
  a
}

val included = boolReduce(List(45, 11, 13), false) {
  (a, i) => if (a) a else (i == 19)
}

val answer = reduceOp(List(11.3, 23.5, 7.2), 0.0)(_ + _)
~~~
* 스칼라의 컬렉션은 reduceOp와 유사한 내장 연산을 제공하고 있음

![img](https://github.com/koni114/learning_scala/blob/master/learning_scala.jpg)
* fold, reduce, scan은 모두 리스트 요소와 동일한 타입의 값을 반환해야 하는 한편,  
각 연산의 오른쪽/왼쪽 변형 함수들은 고유의 반환 타입을 지원함
* 다른 주요 차이점은 순서에 있음  
foldLeft나 foldRight는 리스트를 반복하는 방향을 지정하는 한편, 방향성이 없는 연산은 반복의 순서를 지정하지 않음
* 앞서 구현한 contains 와 sum 연산을 fold 연산을 통해 다시 구현해보자
~~~
val included = List(46, 19,92).foldLeft(false) { (a, i) =>
  if (a) a else (i == 19)
}
val answer = List(11.3, 23.5, 7.2).reduceLeft(_ + _)
~~~

### 컬렉션 전환하기
* 스칼라는 리스트에서 다른 컬렉션 타입으로의 변환이 굉장히 쉽다!

> |이름| 예제 | 설명 |
> |---|:---:|:---:|
>  | mkString | List(24, 99, 104).mkString(", ") | 주어진 구분자를 사용하여 컬렉션을 String으로 만듦|
>  | toBuffer| List('f', 't').toBuffer | 불변의 컬렉션을 가변적인 컬렉션으로 전환|
>  |toList  | Map("a" -> 1, "b" -> 2).toList | 컬렉션을 List로 전환 |
> |toMap |Set(1 -> true, 3 -> true).toMap | 두 요소(길이)로 구성된 튜플의 컬렉션을 Map으로 전환 |
> |toSet  | List(2, 5, 5, 3, 2).toSet| 컬렉션을 Set으로 전환 |
>  | toString | List(11.3, 23.5, 7.2).toString | String으로 컬렉션의 타입을 포함하여 만듬 |
* 불변의 컬렉션인 List, Map, Set은 빈 컬렉션으로 만들 수 없으며, 기존 컬렉션으로부터 매핑되는 것이 더 적절
*

#### 자바와 스칼라 컬렉션 호환성
* 스칼라는 JVM으로 컴파일하고 그 위에서 동작하므로 JDK와 상호작용 뿐만 아니라, 어떤 자바 라이브러리도 추가 할 수 있어야 한다는 것이 보편적인 요구사항
* 자바와 스칼라 컬렉션은 기본적으로 호환되지 않음
* 자바와 스칼라 컬렉션 사이를 직접 전환할 수 있도록 다음 명령어를 추가할 수 있음
~~~
import collection.JavaConverters._
~~~
* import 명령어는 JavaConverters와 그 메소드를 현재의 네임스페이스에 추가함
* 소스 파일에서는 import 명령어가 추가된 파일 또는 로컬 범위의 나머지를 의미

### 컬렉션으로 패턴 매칭하기
* 이전에 우리는 단일 값 패턴을 매칭하는 매치 표현식을 사용했음
~~~
val statuses = List(500, 404)
val msg = statuses.head match {
  case x if x < 500 => "okay"
  case _ => "whoah, an error"
}
~~~
* 전체 컬렉션을 매칭하기 위해 패턴으로 새로운 컬렉션을 사용해보자
~~~
val msg = statuses match {
  case x if x contains(500) => "has error"
  case _ => "okay"
}
~~~
* 값 바인딩으로 패턴 가드에서 컬랙션의 일부 또는 모든 요소에 값을 바인딩 할 수 있음
~~~
val msg = statuses match {
  case List(500, x) => s"Error followed by $x"
  case List(e, x) => s"$e was followed by $x"
}
~~~
* 리스트는 헤드 요소와 테일로 분해할 수 있음. 동일하게 패턴으로써 리스트는 헤드와 테일 요소에  
  매칭될 수 있음
~~~
 val head = List('r', 'g', 'b') match {
   case x :: xs => x
   case Nil => ' '
 }
~~~
