# part_1
## chapter01- SQL 이해하기
- 데이터베이스 소프트웨어는 DBMS라고 부르고, 데이터베이스는 DBMS를 생성하고 물리적인 저장공간을 말함
- 스키마는 데이터베이스, 테이블의 구조와 속성에 대한 정보를 말함
- 테이블에서 열을 어떻게 나눌 것인지는 굉장히 중요함  
  예들 들어 도로명과 건물명을 하나의 열에 포함시킬 것인지, 아니면 나눌 것인지 고민하는 것은 중요
- 시, 구, 동 / 년, 월, 일 같은 데이터는 나누어 넣는 것이 좋음
- 각각의 DBMS 마다 데이터형은 다름. 따라서 이를 항상 고려하는 것이 좋음

## SQL이란 무엇인가
- Structured Query Language
- 표준 SQL은 ANSI 표준 위원회에서 관리하기 때문에 ANSI SQL이라고 부름

## chapter02- 데이터 가져오기
- 쿼리 수행시, order by를 SQL에 입력하지 않았다면, 데이터는 실행될 때마다 다르게 정렬되어 출력됨
- 왠만하면 세미콜론(;)을 붙이자. 어떤 RDBMS냐에 따라서 반드시 세미콜론을 붙여야 할 수도 있기 때문
- 보통 예약어(SELECT, FROM)등은 대문자, 테이블명, 컬럼명은 소문자로 입력하는 것이 좋음
  (대소문자를 구분하지는 않으며, 특정 RDBMS는 컬럼명의 대소문자를 구분함)
- `DISTINCT` 명령어는 부분적으로 적용할 수는 없음
~~~SQL
-- oracle에서는 먼저 10개를 제한 한 뒤, 그중에 DISTINCT 수행
SELECT DISTINCT vend_id
FROM Products
WHERE ROWNUM <= 10;
~~~
- MySQL, PostgreSQL 등은 `LIMIT`를 사용하는데, 이 때 내가 원하는 행에서 부터 LIMIT를 적용하려면 다음과 같이 `OFFSET` 작성하면 됨
~~~SQL
-- 5행에서부터 5개 추출
SELECT prod_name
FROM Products
LIMIT 5 OFFSET 5;
~~~
- 처음 가져온 행은 0번째 행임. 그래서 만약 LIMIT 1 OFFSET 1은 첫 번째 행이 아닌 두 번째 행을 가져옴
- 여러 줄을 주석처리 하고 싶을 때,  /* */를 사용 함

## chapter03 - 데이터 정렬하기
- `ORDER BY`는 열 이름을 사용하여 정렬할 수도 있고, 열 위치로도 정렬할 수 있음
- 텍스트로 된 데이터를 정렬한다면 A와 a가 같을까? a는 B 다음에 오는 것일까 아니면 Z 다음에 오는 것일까? 
- 대부분의 DBMS 기본값인 사전 정렬 순서에서는, A와 a를 똑같이 구분함. 만약 구분하고 싶다면 설정을 변경해주어야 함

## chapter05 - 고급 데이터 필터링
- `WHERE`절에 `AND`나 `OR` 사용 가능
- `IN` 연산자를 `OR` 연산자보다 더 많이 사용하는 이유는 성능 측면에서 더 빠름
- `IN` 연산자의 가장 큰 장점은 `SELECT` 문을 사용할 수 있다는 점
- `NOT` 연산자를 `WHERE`절 뒤에 사용(보통 NOT은 IN과 많이 사용)
~~~SQL
SELECT prod_name, vend_id
FROM Products
WHERE NOT vend_id = 'DLL01'
ORDER BY prod_name;
~~~

