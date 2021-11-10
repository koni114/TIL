## scala가 Java와 다른점
- Scala에서는 순수 함수를 사용하도록 지향해야 함
- 스칼라에서 모든 것은 객체
- 스칼라는 타입 추론이 용이함. 즉 타입을 지정하지 않아도 내부에서 알아서 판단이 가능
~~~scala
val a = 10; a = 11 // error
var b = 10; b = 11 // good
~~~
- 중요한 것은, 참조가 바뀌면 안된다는 것이며 참조하고 있는 대상안의 값은 바뀌어도 무방함
~~~scala
class Test {
    var a = 1
    def set(n:Int) = {a = n}
    def print() = {println(a)}
}

val test = new Test()
test.print()
test.set(10)  // val 로 선언했지만, 값이 바뀜
test.print()
~~~
