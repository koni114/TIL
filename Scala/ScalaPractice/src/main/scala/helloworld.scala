object HelloWorld {
  def main(args: Array[String]): Unit ={

    def combination(x:Int, y:Int, f: (Int, Int) => Int) = f(x , y)
    println(combination(10, 20, _ * _))

    def tripleOp[A, B](a: A, b: A, c: A, f: (A, A, A) => B) = f(a, b, c)
    println(tripleOp[Int, Boolean](93, 92, 14, _ > _ + _))

    def factorOf(x: Int, y: Int) = y % x == 0
    val f = factorOf _
    println(f(10, 20))

    val multiple3 = factorOf(3, _ : Int)
    val y  = multiple3(78)
    println(y)



  }

}