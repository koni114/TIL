object HelloWorld {
  def main(args: Array[String]): Unit ={

    val x: Int = 5
    println(x * 5) // -- 2
    println(x / 5) // -- 3

    var y: Double = 0.25
    y = 355.0 / 113.0
    println(y)

    // val x = 20
    // val greeting = "hello, world"
    val atSymbol = '@'

    val l: Long = 20
    val i: Int = l.toInt
    println(i)

    val hello = "Hello, there"
    val greeting = "Hello," + "World"
    val matching = (greeting == "Hello, there")
    val theme = "Na " * 16 + "Batman"

    println(hello + " " + greeting)

    // 중괄호를 이용한 문자열 출력 예제
    val item = "apple"
    println(s"How do you like them ${item}s?")

    val input = "Enjoying this apple 3.14159 times today"
    val pattern = """.* apple ([\d.]+) times .*""".r
    val pattern(amountText) = input
    val amount = amountText.toDouble
    println(amount)

    val isFalse = !true
    val isTrue = true
    val unequal = (5 != 6)
    val isLess = (5 < 6)
    val unequalAndLess = unequal & isLess
    val definitelyFalse = false && unequal

    //

  }
}