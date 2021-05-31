## chapter01 - 스칼라 시작하기
### 스칼라란?
* 확장 가능한 언어(Scalable)의 줄임말
* 함수형 프로그래밍과 객체지향 프로그래밍을 동시 지원
*  자바 가상 머신(JVM: Java Virtual Machine) 기반에서 실행되고, 성능이 우수한 환경을 제공하기 위해 언어가 만들어짐

### 스칼라 설치하기
#### 1. JDK 설치
* 스칼라는 JVM 기반에서 실행되므로, Java Runtime을 사용해야함
* 따라서 자바 개발 환경(JDK : Java Development kit) 설치 필요
* JDK 설치 방법은 구글링 참조
* 참고로 eclipse 설치시, Mars 이하 버전에서는 scala IDE가 없음
* command 창에서 다음 명령어를 통해 JDK 설치여부 확인 가능
~~~
java -version
~~~

#### 2. Scala 설치
* Scala 홈페이지에서 scala 설치
* 마찬가지로 설치 방법은 구글 참조
* 스칼라를 자동 설치하려면 OS X의 Homebrew, 윈도우의 Chocolately, 리눅스 apt-get/Yum 패키지 매니저를 통해 설치 가능
~~~
(brew/Choco/apt-get/yum) install scala
scala
~~~

### 스칼라 REPL 사용하기
* Read, Evaluate, Print, Loop의 앞글자를 딴 말
* cmd 창에서 scala를 실행시키는 방식을 말함
* cmd 창에서 scala 명령어를 사용하면 REPL shell 사용 가능
~~~
println("hello world")
~~~
* 화살표 위아래를 이용해서 이전/이후로 사용가능
~~~
3 * 5
~~~
* 해당 수식을 prompt 에 입력하면, res0: Int = 15 라는 결과 출력
* 이는 변수를 입력하지 않아도 자동으로 res0 라는 변수를 생성해 값을 할당시킴
* res0를 이용해서 다른 연산을 수행해보자
~~~
res0 * 10
~~~
* 해당 결과는 res1에 자동 할당됨
* 뒤에 붙은 0,1 숫자는 sequence 처럼 붙여서 사용됨
* 스칼라는 정적타입 시스템을 가진 컴파일 언어이기 때문에 바로 결과 확인 가능

### 용어 정리
##### Runtime
* 프로그래밍 언어가 구동되는 환경을 말함

##### JVM(Java Virtual Machine)
* Java Byte Code를 OS에 맞게 해석 해주는 역할
* 즉 Java를 실행하는 주체  

##### 정적 타입 시스템 vs 동적 타입 시스템
 * 정적 타입 시스템
   * 컴파일시 타입을 결정
   * 프로그래밍 할 때 변수 선언 하는 언어들은 전부 정적 타입 시스템을 따른다고 보면 됨
   * 컴파일시 변수에 대한 타입을 결정하므로 타입 안정성 보장
   * C, C++, Java, Scala..

 * 동적 타입 시스템
   * 런타임시 타입이 결정
   * 프로그래밍시 타입을 명시하지 않음
   * Python, Ruby, R..
   * 타입을 따로 명시하지 않으므로 유연성을 가지지만, 안정성이 떨어짐
