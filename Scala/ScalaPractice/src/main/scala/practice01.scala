import java.util.Calendar
import java.text.SimpleDateFormat

object practice01 {
  def main(args: Array[String]):Unit = {

    // Calendar.getInstance 로 Date Instance 생성
    val cal = Calendar.getInstance()
    cal.add(Calendar.DATE, -1)
    // println(cal)

    // 다음과 같이 cal.setTime 과 dateFormat.parse 를 통해 설정 가능
    val dateFormat = new SimpleDateFormat("yyyyMMdd")
    cal.setTime(dateFormat.parse("20211108"))

    // foreach 구문
    val x = List(1, 2, 3)
    // x.foreach{ println }

    var sum = 0
    val y = List(1, 2, 3)
    y.foreach(sum += _)
    println(sum)

    val a = List("a", "b", "c", "d")
    a.foreach(c => println(c))

    val v = Vector((1,9), (2,8), (3,7), (4,6), (5,5))
    v.foreach{ case(i,j) => println(i, j) }
    v.foreach(tup => println(tup._1, tup._2))

    // replaceAll
    val test = for {tmp <- a} yield (tmp, tmp.length)
    println(test)

    val tt = 1 :: 2 :: 3 :: Nil
    println(tt)

    // val myList = List("England" -> "London", "Germany" -> "Berlin")
    // val myMap = myList.groupBy(e => e._1).map(e => (e._1, e._2(0)._2))

    // val betterConversion = Map(myList:_*)
    // println(betterConversion)

    // val scala28Map = myList.toMap
    // println(scala28Map)

    val myList = List("England", "London", "Germany", "Berlin")
    val map: Map[String, Int] = myList.map{s => (s, s.length)}.toMap
    println(map)

    // 추가
    val m = mutable.Map[Int,String]()

  }
}
