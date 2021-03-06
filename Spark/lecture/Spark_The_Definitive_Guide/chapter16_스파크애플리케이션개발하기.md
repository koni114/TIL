# chapter16 - 스파크 애플리케이션 개발하기
- 이제 표준 Spark 애플리케이션을 개발하고 클러스터에 배포하는 과정이 얼마나 쉬운지 알아보자
- 설명을 위해 빌드 도구 설정, 단위 테스트 그리고 애플리케이션의 구성 방법을 담은 간단한 탬플릿을 이용
- 이 탬플릿은 이 책의 공식 코드 저장소에서 내려받을 수 있음
- 원한다면 직접 애플리케이션을 만들 수도 있으므로 탬플릿을 꼭 사용하지 않아도 됨
- 이제 첫 번째 Spark 애플리케이션을 만들어보자

## 16.1 Spark 애플리케이션 작성하기
- Spark 애플리케이션은 Spark 클러스터와 사용자 코드 두 가지 조합으로 구성됨
- 이번 예제에서는 클러스터 모드를 로컬 모드로 설정하고 사전 정의된 애플리케이션 사용자 코드로 사용
- Spark가 지원하는 다양한 언어로 Spark 애플리케이션을 개발해보겠음

### 16.1.1 간단한 스칼라 기반 앱
- Scala는 Spark의 기본 언어이기 때문에 애플리케이션을 개발하는 가장 적합한 방법으로 볼 수 있음
- 이는 일반 애플리케이션을 개발하는 방법과 크게 다르지 않음
- Spark 애플리케이션은 두 가지 JVM 기반의 빌드 도구인 sbt나 apache maven을 이용해 빌드할 수 있음
- 이러한 빌드 도구는 각각 장단점을 가지지만 sbt를 사용하는 것이 더 쉬울 것임  
  sbt는 sbt 웹사이트에서 내려받을 수 있으며 설치와 사용법을 배울 수 있음
- 메이븐 역시 메이븐 웹사이트에서 내려받아 설치 가능
- 스칼라 애플리케이션에 sbt 빌드 환경을 구성하려면 패키지 정보를 관리하기 위해 `build.sbt` 파일을 정의해야 함
- `build.sbt` 파일에 포함되어야 할 핵심 항목은 다음과 같음
  - 프로젝트 메타데이터(패키지명, 패키지 버전 정보 등)
  - 라이브러리 의존성을 관리하는 장소
  - 라이브러리에 포함된 의존성 정보
- 이외에도 다양한 정의 방법이 있지만 책의 범위를 벗어나기 때문에 생략
- 필요한 경우 sbt 공식 홈페이지에서 관련 정보를 찾아볼 수 있음
- 다음 코드는 스칼라용 build.sbt 파일 내용 중 일부
- 전체 내용은 탬플릿에서 확인할 수 있음. 이 중 스칼라와 스파크 버전을 정의하는 방법은 반드시 기억해야함
~~~scala
name := "example"
organization := "com.databricks"
version := "0.1-SNAPSHOT"
scalaVersion := "2.11.8"

// Spark 관련 정보
val sparkVersion = "2.2.0"

// Spark 패키지 포함
resolvers += "bintray-spark-packages" at 
"https://dl.bintray.com/spark-packages/maven/"

resolvers += "Typesafe Simple Repository" at 
"http://repo.typesafe.com/typesafe/simple/maven-releases/"

resolvers += "MavenRepository" at
"https://mvnrepository.com/"

libraryDependencies ++= Seq(
    // Spark 코어
    "org.apache.spark" %% "spark-core" % sparkVersion,
    "org.apache.spark" %% "spark-sql" % sparkVersion

    // 나머지 부분 생략
)
~~~
- build.sbt 파일을 정의했으므로 프로젝트에 실제 코드를 작성해볼 차례
- sbt 매뉴얼에서 찾아볼 수 있는 표준 스칼라 프로젝트 구조를 사용  
  (메이븐 프로젝트도 동일한 디렉터리 구조를 가짐)
~~~scala
src/
    main/
        resources/
         <JAR 파일에 포함할 파일들>
        scala/
         <메인 스칼라 소스 파일>
        java/
         <메인 자바 소스 파일>
    test/
        resources
          <테스트 JAR에 포함할 파일들>
        scala
          <테스트용 스칼라 소스 파일>
        java
          <테스트용 자바 소스 파일>
~~~
- 스칼라와 자바 디렉터리에 소스 코드를 작성함
- 이번 예제에서는 다음과 같은 소스 코드를 파일에 작성. 다음은 SparkContext를 초기화하고 애플리케이션을 실행한 다음 종료하는 예제
~~~scala
object DataFrameExample extends Serializable {
    def main(args: Array[Sring]) = {
        
        val pathToDataFolder = args(0)

        // 명시적으로 몇 가지 설정값을 지정한 다음 SparkSession 시작
        val spark = SparkSession.builder().appName("Spark Example")
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse")
        .getOrCreate()

        // UDF를 등록
        spark.udf.register("myUDF", someUDF(_:String):String)

        val df = spark.read.json(pathToDataFolder + "data.json")
        val manipulated = df.groupBy(expr("myUDF(group")).sum().collect()
        .foreach( => println(x))
    }
}
~~~
- `spark-submit` 명령을 사용해 위 예제 코드를 클러스터에 제출
- 실행 명령 중 main 클래스를 지정한 부분을 눈여겨볼 필요가 있음
- 이제 프로젝트를 설정하고 코드를 작성했으니 빌드해야 함. 하나의 JAR 파일 안에 관련 라이브러리를 모두 포함하는 `uber-jar`, `fat-jar`로 빌드하기 위해 `sbt assemble` 명령을 사용할 수 있음
- 이 명령은 몇몇 배포 작업에서는 매우 간단할 수 있지만 때로는 복잡한 상황이 발생할 수도 있음  
(라이브러리 의존성에 충돌이 발생할 수 있는 경우)
- 가장 쉬운 빌드 방법은 `sbt package` 명령 실행. 이 명령을 사용해 관련 라이브러리를 모두 target 폴더로 모을 수는 있지만 관련 라이브러리를 모두 가지고 있는 하나의 거대한 JAR 파일을 만들어내지는 않음

#### 애플리케이션 실행하기
- `target` 폴더에는 `spark-submit`에서 인수로 사용할 jar 파일이 들어있음
- 스칼라 패키지를 빌드하면 다음 예제와 같이 `spark-submit` 명령을 사용해 로컬 머신에서 실행할 수 있음
- 다음 예제에서는 `$SPARK_HOME` 환경변수 사용
- `$SPARK_HOME`은 스파크를 설치한 디렉터리의 경로로 변경할 수도 있음
~~~scala
$SPARK_HOME/bin/spark-submit \
-- class com.databricks.example.DataFrameExample \
-- master local \
target/scala-2.11/example_2.11-0.1_SNAPSHOT.jar "hello"
~~~

### 16.1.2 파이썬 애플리케이션 작성하기
- command line을 사용해 애플리케이션을 작성하는 방식과 매우 유사
- Spakr에는 빌드 개념이 없으며, PySpark 애플리케이션은 파이썬 스크립트에 지나지 않음
- <b>그래서 애플리케이션을 실행하려면 클러스터에서 스크립트를 실행하기만 하면 됨</b>
- 보통 코드 재사용을 위해 여러 파이썬 파일을 하나의 Egg나 ZIP 파일 형태로 압축
- `spark-submit`의 --py-files 인수로 .py, .zip, .egg 파일을 지정하면 애플리케이션과 함께 배포할 수 있음
- 코드를 실행하려면 스칼라나 자바의 메인 클래스 역할을 하는 파이썬 파일을 작성해야 함  
  즉 `SparkSession`을 생성하는 실행 가능한 스크립트 파일을 만들어야 함
- 다음은 `spark-submit`의 `main` 인수로 지정할 클래스의 코드 예제
~~~python
from __future__ import print_function

if __name__ == '__main__':

    from pyspark.sql import SparkSession

    spark = SparkSession.builder\
        .master("local")\
        .appName("World Count")\
        .config("spark.some.config.option", "some-value")\
        .getOrCreate()

    print(spark.range(5000).where("id > 500").selectExpr("sum(id)").collect())
~~~
- 위 코드가 실행되면 애플리케이션에서 활용할 수 있는 SparkSession 객체가 생성됨
- <b>모든 파이썬 클래스에서 SparkSession 객체를 생성하는 것보다 런타임 환경에서 변수를 생성해 파이썬 클래스에 전달하는 방식을 사용하는 것이 더 좋음</b>

#### 애플리케이션 실행하기
- 코드 작성이 끝났다면 실행을 위해 코드를 클러스터에 전달해야 함
- 다음과 같이 `spark-submit` 명령을 호출함  
  spark-submit은 spark 설치 file에 존재함

### 16.1.3 자바 애플리케이션 작성하기

## 16.2 Spark 애플리케이션 테스트
- 지금까지 Spark 애플리케이션을 개발하고 실행하는 방법에 대해서 알아봄
- 이제부터는 약간 지루하지만 아주 중요한 테스트 방법에 대해서 알아보자
- <b>Spark 애플리케이션을 테스트하려면 애플리케이션을 작성할 때 몇 가지 핵심 원칙과 구성 전략을 고려해야 함</b>

### 16.2.1 전략적 원칙
- 데이터 파이프라인과 애플리케이션에 대한 테스트 코드 개발은 실제 애플리케이션 개발만큼이나 중요
- 테스트 코드는 미래에 발생할 수 있는 데이터, 로직 그리고 결과 변화에 유연하게 대처할 수 있도록 해줌
- 이 절에서는 일반적인 Spark 애플리케이션에서 테스트해야 할 내용과 테스트 편리성을 높여주는 코드 구성 방법을 알아보자

#### 입력 데이터에 대한 유연성
- 데이터 파이프라인은 다양한 유형의 입력 데이터에 유연하게 대처할 수 있어야 함
- 비즈니스 요구사항이 변하면 데이터도 변함
- 따라서 Spark 애플리케이션과 파이프라인은 입력 데이터 중 일부가 변하더라도 유연하게 대처할 수 있어야 함  
아니면 오류 상황을 적절하고 유연하게 제어할 수 있어야 함  
따라서 입력 데이터로 인해 발생할 수 있는 다양한 예외 상황을 테스트하는 코드를 작성해야 함
- 그러면 심각한 문제가 발생했을 때만 저녁잠을 깨우는 견고한 애플리케이션을 만들 수 있음

#### 비즈니스 로직 변경에 대한 유연성
- 입력 데이터뿐만 아니라 파이프라인 내부의 비즈니스 로직이 바뀔 수도 있음
- 예상했던 원형 데이터의 형태가 실제 원형 데이터와 같은지 확인하고 싶을 것임
- 이는 원하는 결과를 얻을 수 있도록 실제와 유사한 데이터를 사용해 비즈니스 로직을 꼼꼼하게 테스트해야 함을 의미함
- 이 유형의 테스트에서는 Spark가 가진 기능을 테스트하는 'Spark 단위 테스트'를 작성하지 않도록 조심해야 함
- 대신 비즈니스 로직을 테스트해 복잡한 비즈니스 파이프라인이 의도한 대로 동작하는지 반드시 확인해야 함

#### 결과의 유연성과 원자성
- 입력 데이터 및 비즈니스 로직의 테스트가 완료되었다면 결과를 의도한 대로 반환하는지 확인 해야 함
- 즉 결과 데이터가 스키마에 맞는 적절한 형태로 반환될 수 있도록 제어해야 함
- 단순히 데이터를 특정 경로에 저장해 놓고 전혀 사용하지 않는 경우는 거의 없음
- 즉, 대부분의 Spark 파이프라인은 다른 Spark 파이프라인의 입력으로 사용됨  
따라서 데이터를 소비하는 다음 Spark 데이터의 상태, 즉 데이터가 얼마나 자주 갱신되는지, 데이터가 완벽한지, 마지막 순간에 데이터가 변경되지는 않았는지 등을 이해할 수 있도록 만들고 싶을 것임
- 앞서 언급한 모든 주제들은 데이터 파이프라인을 구성할 때 고려해야 하는 원칙임
- 사실 이 내용은 Spark에만 적용되는 것은 아님. 이런 전략적 사고방식은 구성하려는 시스템의 토대를 마련할 때 중요한 요소

### 16.2.2 테스트 코드 작성 시 고려사항
- 전략적 사고도 중요하지만 애플리케이션 테스트를 쉽게 만들어주는 테스트 구성 전략에 대해 자세히 알아보자
- 적절한 단위 테스트를 작성해 입력 데이터나 구조가 변경되어도 비즈니스 로직이 정상적으로 동작하는지 확인해야 함
- 단위 테스트를 하면 스키마가 변경되는 상황에 쉽게 대응할 수 있음
- 단위 테스트의 구성 방법은 비즈니스 도메인과 도메인 경험에 따라서 다양할 수 있으므로  
  개발자의 역량에 달려있음

#### SparkSession 관리하기
- Spark 로컬 모드 덕분에 JUnit이나 ScalaTest 같은 단위 테스트용 프레임워크로 비교적 쉽게 Spark 코드를 테스트할 수 있음
- 단지 테스트 하네스(test harness)의 일부로 로컬 모드의 SparkSession을 만들어 사용하기만 하면 됨  
- 이런 테스트 방식이 잘 동작하려면 Spark 코드에서 의존성 주입 방식으로 SparkSession을 만들어 사용하기만 하면 됨
- 즉,  SparkSession을 한 번만 초기화하고 런타임 환경에서 함수와 클래스를 전달하는 방식을 사용하면 테스트 중에 SparkSession을 쉽게 교체할 수 있음
- 이 방법을 사용하면 단위 테스트를 수행할 때 테스트용 SparkSession으로 개별 함수를 쉽게 테스트 할 수 있음

#### 테스트 코드용 Spark API 선정
- Spark는 SQL, DataFrame, Dataset등 다양한 API를 제공
- 각 API는 사용자 애플리케이션의 유지 보수성과 테스트 용이성 측면에서 서로 다른 영향을 미칠 수 있음
- 적합한 API는 사용자가 속한 팀과 팀에서 무엇을 필요로 하는지에 따라 달라질 수 있음
- 어떤 팀이나 프로젝트에서는 개발 속도를 올리기 위해 덜 엄격한 SQL과 DataFrame API를 사용할 수 있고 다른 팀에서는 타입 안정성을 얻기 위해 Dataset과 RDD API를 사용할 수 있음
- <b>API 유형에 상관없이 각 함수의 입력과 출력 타입을 문서로 만들고 테스트 해야함</b>
- 타입 안정성 API를 사용하면 함수가 가지고 있는 최소한의 규약을 지켜야 하므로 다른 코드에서 재사용하기 쉬움
- 모든 동적 데이터 타입 언어가 그렇듯 DataFrame이나 SQL을 사용할 때는 혼란을 없애기 위해 각 함수의 입력 타입과 출력 타입을 문서로 만들고 테스트 하는 노력이 필요
- 저수준 RDD API는 정적 데이터 타입을 사용하지만 Dataset API에는 없는 파티셔닝 같은 저수준 API 기능이 필요한 경우에만 사용됨
- Dataset API를 사용하면 성능을 최적화할 수 있으며 앞으로도 더 많은 최적화 방식을 제공할 가능성이 높음
- 애플리케이션에 사용할 언어를 선택할 때도 비슷한 고려사항이 적용됨  
  모든 팀에 적합한 정답은 없지만, 언어별로 서로 다른 이점을 제공하기 때문에 요구사항에 따라 언어를 선택해 사용하면 됨
- 대규모 애플리케이션이나 저수준 API를 사용해 성능을 완전히 제어하려면 스칼라와 자바 같은 정적 데이터 타입의 언어를 사용하는 것을 추천
- Python이나 R은 각 언어가 제공하는 강력한 라이브러리를 활용하려는 경우에 사용하는 것이 좋음
- Spark 코드는 모든 언어의 표준 테스트 프레임워크에서 쉽게 테스트할 수 있어야 함

### 16.2.3 단위 테스트 프레임워크에 연결하기
- 코드를 단위 테스트 하려면 각 언어의 표준 프레임워크(JUnit, ScalaTest 등)를 사용하고 테스트 하네스에서 테스트마다 SparkSession을 생성하고 제거하도록 설정하는 것이 좋음
- 각 프레임워크는 SparkSession 생성과 제거를 수행할 수 있는 메커니즘(ex `before`, `after` 메소드)을 제공
- 이 장의 애플리케이션 탬플릿에는 단위 테스트 샘플 코드가 포함되어 있음

### 16.2.4 데이터 소스 연결하기
- 가능하면 테스트 코드에서는 운영 환경의 데이터소스에 접속하지 말아야 함
- 그래야 데이터소스가 변경되더라도 고립된 환경에서 개발자가 쉽게 테스트 코드를 실행할 수 있음
- 이런 환경을 구성하는 방법의 하나로 <b>비즈니스 로직을 가진 함수가 데이터소스에 직접 접근하지 않고 DataFrame이나 Dataset을 넘겨받게 만들 수 있음</b>
- 이렇게 생성된 함수를 재사용하는 코드는 데이터소스의 종류에 상관없이 같은 방식으로 동작함
- Spark의 구조적 API를 사용하는 경우 이름이 지정된 테이블을 이용해 문제를 해결할 수 있음
- 간단히 몇 개의 더미 데이터셋(ex) 작은 텍스트 파일이나 인메모리 객체로 데이터셋을 만듬)에 이름을 붙여 테이블로 등록하고 사용 가능

## 16.3 개발 프로세스
- Spark 애플리케이션의 개발 프로세스는 기존에 사용하던 개발 흐름과 유사
- 먼저 대화형 노트북이나 그와 유사한 환경에 초기화된 작업 공간을 마련함
- 그리고 핵심 컴포넌트와 알고리즘을 만든 다음 라이브러리나 패키지 같은 영구적인 영역으로 코드를 옮김
- 대화형 노트북(jupyter notebook 같은거 말하는 거 같음)은 단순하게 실험하기 좋은 환경을 제공하므로 많이 추천하는 도구 중 하나
- 또한 데이터브릭스(Databricks) 같이 노트북을 운영용 애플리케이션처럼 실행할 수 있는 도구도 있음
- 로컬 머신에서 실행한다면 `spark-shell`과 스파크가 지원하는 다른 언어용 셸을 이용해 애플리케이션 개발에 활용하는 것이 가장 적합한 방식
- 대부분의 shell은 대화형 애플리케이션을 개발할 때 사용하지만 `spark-submit` 명령은 스파크 클러스터에 운영용 애플리케이션을 실행하기 위해 사용
- 이 책의 서두에서 알아본 것처럼 Spark를 대화형으로 실행하기 위해 셸을 사용할 수 있음
- 이런 모드로 실행할 수 있는 셸에는 PySpark, Spark SQL, SparkR 이 있음
- Spark 설치 경로 하위 bin 디렉터리에는 다양한 shell이 있음  
  각 언어에 맞는 shell을 사용하려면 spark-shell(Scala 지원), spark-sql, pyspark, sparkR 명령 실행
- 애플리케이션을 개발하고 실행할 패키지 또는 스크립트를 만들고 나면 `spark-submit` 명령으로 클러스터에 제출 가능

## 16.4 애플리케이션 시작하기
- 대부분의 Spark 애플리케이션은 `spark-submit` 명령으로 실행함
- 16.1절 '스파크 애플리케이션 작성하기'에서 본 것처럼 `spark-submit` 명령에 옵션, 애플리케이션 JAR 파일 또는 Script와 관련된 인수를 지정해 사용
~~~
./bin/spark-submit \
--class <메인 클래스> \
--master <스파크 마스터 URL> \
--deploy-mode <배포 모드> \
-- conf <키>=<값> \
... # 다른 옵션
<애플리케이션 JAR 또는 Script> \
[애플리케이션의 인수]
~~~
- `spark-submit` 명령으로 spark job을 제출할 때는 클라이언트 모드와 클러스터 모드 중 하나를 선택해야 함
- 하지만 <b>드라이버와 익스큐터 간의 지연 시간을 줄이기 위해 클러스터 모드</b>로 실행할 것을 추천
- 파이썬 애플리케이션을 제출하려면 `.jar` 파일의 위치에 `.py` 파일을 지정하고 파이썬 `.zip`, `.egg`, `.py` 파일을 `--py-files` 에 추가함
- 하단의 표는 특정 클러스터 매니저에서 사용할 수 있는 옵션을 포함해 `spark-submit` 명령에서 사용할 수 있는 모든 옵션 정보를 제공
- `spark-submit --help` 명령을 실행하면 전체 옵션을 직접 확인 가능
  - `--master MASTER_URL` : spark://host:port, mesos://host:port, yarn 또는 local 지정
  - `--deploy-mode DEPLOY_MODE` : 클라이언트 모드, 클러스터 모드 선택. 기본값은 client
  - `--class CLASS_NAME` :  사용자 애플리케이션의 메인 클래스 지정
  - `--name NAME` : 애플리케이션의 이름 지정
  - `--jars JARS` : 드라이버와 익스큐터의 클래스패스에 포함될 로컬 JAR 파일
  - `--packages` : 드라이버와 익스큐터의 클래스패스에 포함된 메이븐 의존성 정보를 콤마로 구분된 목록으로 지정  
  - `exclude-packages` : --packages에 명시된 의존성 라이브러리를 검색할 때 충돌 방지를 위해 제외해야 하는 목록을 콤마로 구분된 목록으로 지정
  - `repositories` : --packages에 지정된 의존성 라이브러리를 검색할 때 사용할 원격 메입ㄴ 저장소를 콤마로 구분된 목록으로 지정
  - `py-files PY_FILES` : 파이썬 애플리케이션 실행 시 PYTHONPATH에 추가할 .zip, .egg, .py 파일을 지정함
  - `files FILES` : 각 익스큐터의 작업 디렉토리에 위치할 파일
  - `conf PROP=VALUE` : 임의의 Spark 환경 설정 속성값 지정
  - `properties-file FILE` : 부가적인 속성 정보를 읽어 들일 파일의 경로 지정
  - `driver-memory MEM` : 드라이버에서 사용할 메모리 지정(ex) 1000M, 2G), 기본값은 1024M
  - `driver-java-options` : 드라이버에 지정할 부가적인 자바 옵션 정보 지정
  - `driver-library-path` : 드라이버에 지정할 부가적인 라이브러리 경로 지정
  - `driver-class-path` : 드라이버에 지정할 부가적인 클래스패스 경로 지정. --jars에 지정한 JAR 파일은 자동으로 클래스패스에 추가됨
  - `executor-memory MEM` : 애플리케이션을 제출할 때 위장용으로 사용할 사용자 이름을 지정함
  - `help, -h` : 도움말 출력
  - `verbose, -v` : 추가적인 디버그 메세지를 출력함
  - `--version` : 사용중인 Spark 버전 출력  

- 특정 배포 환경에서 사용할 수 있는 설정은 다음과 같음

![img](https://github.com/koni114/Spark/blob/main/Spark_The_Definitive_Guide/imgs/clusterManager1.jpg)

![img](https://github.com/koni114/Spark/blob/main/Spark_The_Definitive_Guide/imgs/clusterManager2.jpg)

### 16.4.1 애플리케이션 시작 예제
- 이제 앞서 언급한 옵션을 어떻게 사용하는지 알아보겠음
- 또한 내려받은 Spark의 examples 디렉터리에서 다양한 예제와 데모 애플리케이션을 찾아볼 수도 있음
- 특정 파라미터를 어떻게 사용해야 할지 막막하다면 다음 예제와 같이 로컬 머신에서 SparkPi 클래스를 메인 클래스로 사용해 테스트해볼 수 있음
~~~
./bin/spark-submit \
-- class org.apache.spark.examples.SparkPi \
-- master spark://207.184.161.138:7077 \
-- executor-memory 20G \
-- total--executor-cores 100 \
replace/with/path/to/examples.jar \
1000
~~~
- 파이썬에서는 다음 코드를 이용해 위 예제와 같은 작업을 수행함 
- Spark 디렉터리에서 명령을 실행하면 stand-alone 매니저로 파이썬 애플리케이션(단일 스크립트에 모든 코드가 포함되어 있는 경우)를 제출
- 또한 위 예제와 동일한 수의 익스큐터를 사용하도록 제한할 수 있음
~~~
./bin/spark-submit \
--master spark:://207.184.161.138:7077 \
examples/src/main/python/pi.py \
1000
~~~
- master 옵션의 값을 `local` 이나 `local[*]` 로 변경하면 애플리케이션을 로컬 모드로 실행 가능
- replace/with/path/to/examples.jar 파일을 로컬에서 사용 중인 스칼라와 스파크 버전에 맞게 컴파일한 파일로 바꿔야 할 수도 있음

## 16.5 애플리케이션 환경 설정하기
- Spark는 다양한 환경 설정 제공
- 그 중 일부는 15장에서 알아보았음. 목적에 따라 다양하게 환경을 설정할 수 있으며  
  이 절에서 자세히 알아보겠음
- 이 정보는 참고용이며 특별히 무언가를 찾는 경우가 아니라면 가볍게 살펴보자
- 대부분의 설정은 다음과 같이 분류할 수 있음
  - 애플리케이션 속성
  - 런타임 환경
  - 셔플 동작 방식
  - 스파크 UI
  - 압축과 직렬화
  - 메모리 관리
  - 처리 방식
  - 네트워크 설정
  - 스케줄링
  - 동적 할당
  - 보안
  - 암호화
  - Spark SQL
  - Spark streamming
  - SparkR
- Spark는 다음과 같은 방식으로 시스템을 설정할 수 있음
  - Spark 속성은 대부분의 애플리케이션 파라미터를 제어하며 `SparkConf` 객체를 사용해 스파크 속성 설정 가능
  - 자바 시스템 속성
  - 하드코딩된 환경 파일
- 내려받은 Spark의 `/conf` 디렉터리에서 사용 가능한 여러 종류의 탬플릿 파일을 찾아볼 수 있음
- 애플리케이션을 개발할 때 탬플릿의 설정값을 하드코딩할 수 있으며 탬플릿에 속성값을 지정해 런타임에 사용할 수도 있음
- IP 주소 같은 환경변수는 Spark 클러스터 노드의 `conf/spark-env.sh` 스크립트를 사용해 머신별로 설정할 수 있음
- 마지막으로 `log4j.properties` 파일을 사용해 로그와 관련된 설정을 할 수 있음

### 16.5.1 SparkConf
- `SparkConf`는 애플리케이션의 모든 설정을 관리함
- 다음 예제처럼 `import` 구문을 지정하고 객체를 생성할 수 있음
- Spark 애플리케이션에서 생성된 SparkConf 객체는 불변성임
~~~scala
// 스칼라 코드
import org.apache.spark.SparkConf

val conf = new SparkConf().setMaster("local[2]").setAppName("DefinitiveGuide").set("some.conf", "to.some.value")
~~~
- <b>`SparkConf` 객체는 개별 스파크 애플리케이션에 대한 Spark 속성값을 구성하는 용도로 사용함</b>
- Spark 속성값은 스파크 애플리케이션의 동작 방식과 클러스터 구성 방식을 제어함
- 앞 예제에서는 로컬 클러스터 2개의 스레드를 생성하도록 설정하고 SparkUI에 표시할 애플리케이션 이름을 지정
- 이런 설정값은 이 장의 앞에서처럼 명령행 인수를 통해 런타임에 구성할 수 있음
- 이는 자동으로 기본 Spark 애플리케이션을 포함하는 Spark shell을 시작할 때 도움이 됨
- 예를 들면 다음과 같음
~~~
./bin/spark-submit --name "DefinitiveGuide" --master local[4] ...
~~~
- 시간 주기 형태의 속성값을 정의할 때는 다음 포맷 사용
  - 25ms(밀리세컨드)
  - 5s(초)
  - 10m, 10min(분)
  - 3h(시간)
  - 5d(일)
  - 1y(년)

### 16.5.2 애플리케이션 속성
- 애플리케이션 속성은 `spark-sumbit` 명령이나 Spark 애플리케이션을 개발할 때 설정할 수 있음
- 애플리케이션의 속성은 기본 애플리케이션 메타데이터와 일부 실행 특성을 정의함
- 다음은 애플리케이션 속성 목록

![img](https://github.com/koni114/Spark/blob/main/Spark_The_Definitive_Guide/imgs/appConf1.jpg)

![img](https://github.com/koni114/Spark/blob/main/Spark_The_Definitive_Guide/imgs/appConf2.jpg)

- 드라이버가 실행된 호스트의 4040 포트로 접속한 후 SparkUI의 "Environment" 탭을 확인해 값이 올바르게 설정되었는지 확인할 수 있음
- 사용자가 설정하지 않은 다른 모든 속성은 기본값을 사용

### 16.5.3 런타임 속성
- 드물지만 애플리케이션의 런타임 환경을 설정해야 할 수도 있음
- 관련 속성을 사용해 드라이버와 익스큐터를 위한 추가 클래스패스와 파이썬패스, 파이썬 워커 설정 그리고 다양한 로그 관련 속성을 정의할 수 있음

### 16.5.4 실행 속성
- 실행 속성과 관련된 설정값은 실제 처리를 더욱 세밀하게 제어할 수 있기 때문에 자주 사용하게 됨
- 자주 사용하는 속성으로는 `spark.executor.cores`, `spark.files.maxPartitionBytes`가 있음

### 16.5.5 메모리 관리 설정
- 사용자 애플리케이션을 최적화하기 위해 메모리 옵션을 수동으로 관리해야 할 때가 있음
- 대다수의 메모리 설정은 메모리 자동 관리 기능의 추가로 인해 Spark 2.x 버전에서 제거된 예전 개념이거나 세밀한 제어를 위한 설정이므로 최종 사용자는 신경 쓰지 않아도 됨

### 16.5.6 셔플 동작방식 설정
- 앞서 과도한 네트워크 부하 때문에 Spark Job에서 셔플이 얼마나 큰 병목 구간이 될 수 있는지 설명했음
- 셔플 동작 방식을 제어하기 위한 고급 설정이 존재

### 16.5.7 환경변수
- Spark가 설치된 디렉터리의 `conf/spark-env.sh` 파일(윈도우 환경에서는 `conf/spark-env.cmd` 파일)에서 읽은 환경변수로 특정 Spark 설정을 구성할 수 있음
- 스탠드얼론과 메소스 모드에서는 이 파일로 머신에 특화된 정보를 제공할 수도 있음
- 또한 이 파일은 로컬 애플리케이션이나 제출용 스크립트를 실행할 때 함께 적용
- spark를 설치한다고 해서 conf/spark-env.sh 파일이 기본적으로 존재하는 것은 아님
- 하지만 `conf/spark-env.sh.template` 파일을 복사해서 생성할 수 있음  
  복사된 파일에 반드시 실행 권한을 부여해야 함
- spark-env.sh 스크립트에 다음과 같은 변수를 설정할 수 있음 
  - JAVA_HOME 
  - PYSPARK_PYTHON 
  - PYSPARK_DRIVER_PYTHON
  - SPARKR_DRIVER_R
  - SPARK_LOCAL_IP
  - SPARK_PUBLIC_DNS
- 나열된 목록 외에도 각 머신이 사용할 코어 수나 최대 메모리 크기 같은 Spark 스탠드얼론 클러스터 설정과 관련된 옵션도 있음
- `spark-env.sh` 파일은 shell 스크립트이므로 프로그래밍 방식으로 일부 값을 설정할 수 있음
- 예를 들어 특정 네트워크 인터페이스의 IP를 찾아 `SPARK_LOCAL_IP` 변수의 값 설정 가능

### 16.5.8 애플리케이션에서 Job 스케줄링
- Spark 애플리케이션에서 별도의 스레드를 사용해 여러 잡을 동시에 실행할 수 있음
-  이 절에서의 Job은 해당 액션을 수행하기 위해 실행되어야 할 모든 태스크와 스파크 액션을 의미함
- Spark의 스케줄러는 스레드 안정성을 충분히 보장함
- 그리고 여러 요청(ex) 다수의 사용자가 쿼리를 요청하는 경우)을 동시에 처리할 수 있는 애플리케이션을 만들 수 있음
- 기본적으로 Spark의 스케줄러는 FIFO 방식으로 동작함  
  queue의 head에 있는 잡이 클러스터의 전체 자원을 사용하지 않으면 이후 Job을 바로 실행할 수 있음
- 하지만 queue의 head에 있는 Job이 너무 크면 이후 Job은 아주 늦게 실행될 것임  
- 여러 Spark Job이 자원을 공평하게 나눠 쓰도록 구성할 수도 있음  
  Spark는 모든 Job이 클러스터 자원을 거의 동일하게 사용할 수 있도록 <b>라운드 로빈</b>방식으로 여러 Spark Job의 테스크를 할당
- 즉, 장시간 수행되는 Spark Job이 처리되는 중에 짧게 끝난 Spark Job이 제출된 경우 즉시 장시간 수행되는 Spark Job의 자원을 할당받아 처리
- 따라서 장시간 수행되는 Spark Job의 종료를 기다리지 않고 빠르게 응답할 수 있음
- 이 모드는 사용자가 많은 환경에 적합함
- 페어 스케줄러(Fair scheduler)를 사용하려면 `SparkContext`를 설정할 때 `spark.scheduler.mode` 속성을 FAIR로 지정해야 함
- 페어 스케줄러는 여러 개의 잡을 Pool로 그룹화하는 방식도 지원함
- 그리고 개별 Pool에 다른 스케줄링 옵션이나 가중치를 설정할 수 있음
- 페어 스케줄러를 사용하면 더 중요한 스파크 잡을 할당할 수 있도록 우선순위가 높은 Pool을 만들 수 있음
- 또한 각 Job에 같은 양의 자원을 할당하는 대신 각 사용자의 Spark Job을 그룹화할 수도 있음
- 동시에 실행하는 Job 수를 고려하지 않고 모든 사용자가 같은 양의 자원을 사용하도록 설정하면 됨
- Spark의 페어 스케줄러는 하둡의 페어 스케줄러 모델을 본떠서 만듬
- 사용자가 명시적으로 풀을 지정하지 않으면 Spark는 새로운 Job을 'default' 풀에 할당함
- Job을 제출하는 스레드에서 SparkContext의 로컬 속성인 `spark.scheduler.pool` 속성을 지정해 풀을 지정할 수 있음
- sc가 SparkContext의 변수라고 가정하면 다음과 같이 지정
~~~scala
sc.setLocalProperty("spark.scheduler.pool", "pool1")
~~~
- 이 로컬 속성을 지정하면 이 스레드에서 제출되는 모든 Job은 이 풀을 사용
- 이 설정은 사용자를 대신해 스레드가 여러 잡을 쉽게 실행할 수 있도록 스레드별로 지정할 수 있음
- 스레드에 연결된 풀을 초기화하고 싶다면 spark.scheduler.pool 속성의 값을 null로 지정


## 용어 정리
- 빌드(build)
  - 소스코드 파일을 실행가능한 소프트웨어 산출물로 만드는 일련의 과정
  - 빌드의 단계 중 컴파일이 포함되어 있는데 컴파일은 빌드의 부분집합이라 할 수 있음
- 테스트 하네스(test harness)
  - 시스템과 시스템 컴포넌트를 테스트하는 환경의 일부 
  - 테스트를 지원하기 위해 생성된 코드와 데이터를 의미함
- 페어 스케줄러(Fair Scheduler)
  - 페어 스케줄러는 제출된 작업이 동등하게 리소스를 점유 할 수 있도록 지원
  -  작업 큐에 작업이 제출되면 클러스터는 자원을 조절하여 모든 작업에 균등하게 자원을 할당 하여 줌
  - 메모리와 CPU를 기반으로 자원을 설정 할 수 있음