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
- 여러 줄을 주석처리 하고 s싶을 때,  /* */를 사용 함

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

SELECT prod_id, prod_price, prod_name
FROM products
WHERE vend_id NOT IN ('DLL01', 'BRS01')
ORDER BY prod_name;
~~~

### 도전과제
~~~SQL
-- 문제1
SELECT vend_name
FROM Vendors
WHERE vend_country = 'USA' and VEND_STATE = 'CA';
-- 문제2
SELECT order_num, prod_id, quantity
FROM OrderItems
WHERE (prod_id = 'BR01' AND quantity >= 100) OR (prod_id = 'BR02' AND quantity >= 100) OR (prod_id = 'BR03' AND quantity >= 100)

-- 문제3
SELECT prod_name, prod_price
FROM Products
WHERE prod_price >= 3 AND prod_price <= 6;

-- 문제4
SELECT vend_name
FROM Vendors
WHERE vend_country = 'USA' AND vend_state = 'CA'
ORDER BY vend_name;
~~~

## chapter06- 와일드카드 문자를 이용한 필터링
- 정확하게 어떤 단어를 가지고 필터링하는 것이 아니라 대략적으로 포함 여부를 가지고 필터링 할 때는  
  와일드카드를 사용
- 검색(WHERE) 절에서 와일드카드 문자를 사용하려면 LIKE 사용
- LIKE는 술어(predicate, 문장 속에서 주어에 대해 진술하는 동사 이하 부분)임
- 와일드카드 검색은 문자열에서만 사용할 수 있으며, 문자열이 아닌 열을 검색할 때에는 와일드카드를 사용할 수 없음
- 다음과 같이 사용 
~~~SQL
SELECT prod_id, prod_name
FROM Products
WHERE prod_name LIKE 'Fish%' 

SELECT prod_id, prod_name
FROM Products
WHERE prod_name LIKE '%bean bag%' 

-- 검색 중간에도 사용가능. 많이 사용하지는 않음
SELECT prod_name
FROM Products
WHERE prod_name LIKE 'F%y' -- F로 시작하고 y로 끝나는 제품
~~~
- 일부 DBMS는 열을 공백으로 채우기 때문에 후행 공백에 주의해야함  
  예를 들어 50개의 문자를 넣을 수 있는 열에 Fish bean bag toy라는 길이가 17인 문자열을 넣으면  
  마지막 33개의 공백이 추가됨
- <b>따라서 F%y라고 하면 나오지 않고, F%y%라고 하면 나옴</b>
- 이런식으로 해결할 수도 있지만, 더 좋은 해결방법은 공백을 제거하는 것
~~~SQL
SELECT prod_name
FROM Products
WHERE prod_name LIKE 'F%y%' -- F로 시작하고 y로 끝나는 제품
~~~
- NULL에 주의하자!  
  % 와일드카드는 모든 것과 매칭되는 것처럼 보일지 모르지만, NULL은 예외임  
  `WHERE prod_name LIKE '%'` 절도 제품명이 NULL인 행은 가져오지 않음

### _ 와일드카드
- 언더라인(_)은 %와 비슷하게 사용되지만, % 와일드카드가 여러 문자열을 대신할 수 있는 것과는 달리 _ 와일드카드는 단 한 개의 문자를 대신함
~~~SQL
SELECT prod_id, prod_name
FROM Products
WHERE prod_name LIKE '__ inch teddy bear%' 
~~~

### 와일드카드 사용 팁
- 와일드카드를 남용해서는 안됨. 다른 검색 연산자를 이용해서 검색이 가능하다면, 그것을 이용해라
- 꼭 필요한 경우가 아니라면 검색 패턴 시작에 와일드카드를 사용하지 말자  
  와일드카드로 시작하는 검색 패턴은 처리가 가장 느림
- 와일드카드 기호의 위치 선정에 주의하자. 만약 와일드카드를 잘못된 곳에 사용한다면, 
  의도된 것과 다른 데이터가 검색될 것임

### 도전과제
~~~SQL
-- 1
SELECT prod_name, prod_desc
FROM Products
WHERE prod_desc LIKE '%toy%'
-- 2
SELECT prod_name, prod_desc
FROM Products
WHERE prod_desc NOT LIKE '%toy%'

-- 3
SELECT prod_name, prod_desc
FROM Products
WHERE prod_desc LIKE '%toy%' AND prod_desc LIKE '%carrots%';

-- 4
SELECT prod_name, prod_desc
FROM Products
WHERE prod_desc LIKE '%toy%carrots%';
~~~

## chapter07 계산 필드 생성하기
~~~SQL
SELECT TRIM(vend_name) || ' (' || TRIM(vend_country) || ')'
FROM Vendors
ORDER BY vend_name;
~~~

### 별칭 사용하기
- 새로운 계산 필드의 이름을 지정하지 않으면 클라이언트 프로그램에서는 이름이 없는 열은 사용할 수가 없음
~~~SQL
SELECT TRIM(vend_name) || ' (' || TRIM(vend_country) || ')'
FROM Vendors
ORDER BY vend_name;
~~~
- 많은 DBMS에서는 `AS`를 생략해도 되지만, 습관적으로 AS를 붙이는 것이 좋음
- 별칭은 다른 용도로도 사용되는데, 한 가지는 실제 테이블 열 이름에 허용되지 않는 문자가 포함되어 있을 때 이름을 바꾸는 데 쓰는 것임
- 아니면 원래 이름이 모호하거나 잘못 읽을 수 있으면 열 이름을 상세히 하는데 사용하기도 함
- 별칭을 여러 단어로 이루어진 문자열로 지정하는 경우, 작은 따옴표로 싸야 함
- 별칭을 파생열(derived column)이라고 부르기도 함

### 수학 계산 수행하기
~~~SQL
SELECT prod_id,
       quantity,
       item_price,
       quantity * item_price AS expanded_price
FROM OrderItems
WHERE order_num = 20008;
~~~
- 계산 결과를 확인하는 방법
~~~SQL
SELECT 2 * 3
FROM dual;

SELECT TRIM('  abc   ')
FROM dual;
~~~

### 도전과제
~~~SQL
-- 1
SELECT vend_id, vend_name AS vname, vend_address AS vaddress, vend_city AS vcity
FROM Vendors
ORDER BY vname;

-- 2
SELECT prod_id, prod_price, prod_price * 0.9 AS sale_price
FROM Products
~~~

## chapter09 데이터 요약
- 기본적으로 SQL은 다섯 개의 그룹 함수 기능을 지원함.  
  AVG, COUNT, MAX, MIN, SUM
- AVG 함수는 하나의 열만 가능하며, NULL값은 무시함
- `COUNT(*)`를 이용해서 행의 수를 셀 수 있으며, NULL 값을 가진 열을 포함하여 행의 수를 셈
- `COUNT(열 이름)`을 사용할 수 있으며, NULL값은 무시하고 count 수행 
- `MAX` 함수를 문자열에서도 사용 가능한데, 정렬 후 마지막에 있는 행을 반환 
- `MIN` 함수도 문자열에서도 사용 가능한데, 정렬 후 가장 처음에 있는 행을 반환
~~~SQL
-- 1
SELECT AVG(prod_price) AS avg_price
FROM Products
WHERE vend_id = 'DLL01';

-- 2
SELECT COUNT(*) AS num_cust
FROM Customers;

-- 3
SELECT count(*) AS num_cust
FROM Customers;
SELECT count(cust_email) AS num_cust
FROM Customers;

-- 4
SELECT MAX(prod_price) AS max_price
FROM Products;

-- 5
SELECT MIN(prod_price) AS min_price
FROM Products;

-- 6
SELECT SUM(item_price * quantity) AS total_price
FROM OrderItems
WHERE order_num = 20005;
~~~

### 중복되는 값에 대한 그룹 함수
- `ALL`을 쓰거나 아무런 키워드도 쓰지 않으면 모든 행에 대해 계산을 수행함
- 중복되는 값을 제거하기 위해 `DISTINCT`라는 키워드 사용
- `COUNT(*)`와 `DISTINCT`는 같이 사용될 수 없음
~~~SQL
SELECT AVG(DISTINCT prod_price) as avg_price
FROM Products
WHERE vend_id = 'DLL01';
~~~

### 그룹 함수 결합하기
- SELECT 문에서는 필요한 만큼의 그룹 함수를 사용할 수 있음
- 그룹 함수의 결과 별칭을 지정할 때, 테이블에 있는 컬럼명을 지정하지 말자. 대부분의 DBMS에서는 지원하지 않음
~~~SQL
SELECT COUNT(*) AS num_items,
       MIN(prod_price) AS price_min,
       MAX(prod_price) AS price_max,
       ROUND(AVG(prod_price),4) AS price_avg
FROM Products;
~~~

### 도전 과제
~~~SQL
--1
SELECT SUM(quantity) as quantity_sum
FROM OrderItems;

--2
SELECT SUM(quantity) as quantity_sum
FROM OrderItems
WHERE prod_id = 'BR01';

--3
SELECT MAX(prod_price) AS max_price
FROM Products
WHERE prod_price <= 10;
~~~

## chapter10 - 데이터 그룹핑
### 그룹 생성하기
- `GROUP BY` 절을 사용하여 생성 가능
- `GROUP BY` 절은 DBMS에게 먼저 데이터를 그룹핑한 후, 각각의 그룹에 대해 계산하라고 지시
- `GROUP BY` 절에는 원하는 만큼의 열을 써서, nested group을 만들 수 있게 해줌
- `GROUP BY` 절에 중첩된 그룹이 있다면, 데이터는 마지막으로 지정된 그룹에서 요약됨
- `GROUP BY` 절에 있는 열은 가져오는 열이거나, 그룹 함수는 아니면서 유효한 수식이어야 함
- `SELECT` 절에서 수식을 사용한다면, `GROUP BY` 절에도 같은 수식을 사용해야 함  
  별칭은 사용할 수 없음
- 대부분의 SQL 실행 환경에서 GROUP BY 절에서 문자나 메모와 같은 가변형 길이의 데이터형은 
  사용할 수 없음
- 그룹 함수 명령문을 제외하고 SELECT 절에 있는 모든 열은 GROUP BY 절에 존재해야 함
- 그룹핑하는 열의 행에 NULL값이 있다면, NULL도 그룹으로 가져옴  
  여러 행이 NULL값을 가진다면, 모두 함께 그룹핑됨
- `GROUP BY` 절은 `WHERE` 절 뒤에 그리고 `ORDER BY` 절 앞에 와야 함
- Microsoft SQL Server같은 일부 SQL 실행 환경은 GROUP BY 절에서 ALL 절을 지원함
- 일부 SQL 환경에서는 SELECT 절에 있는 위치로 GROUP BY에 열을 지정할 수 있음
~~~SQL
--1 
SELECT vend_id, COUNT(*) AS num_prods
FROM Products
GROUP BY vend_id;
~~~

### 그룹 필터링
- `GROUP BY`절을 사용하여 데이터를 그룹핑하는 것뿐만 아니라, SQL은 어떤 그룹을 포함하고 어떤 그룹은 배제할 것인지 필터링도 가능하게 해줌
- 예를 들어 최소 두 번 이상 주문한 고객 리스트를 원한다고 가정해보자  
  `WHERE`절은 그룹에서는 적용할 수 없으므로, `HAVING` 사용
- `WHERE` 절에서 배운 기법과 옵션은 모두 HAVING 절에도 적용 가능. 문법은 동일하지만, 키워드만 다를 뿐임
~~~SQL
SELECT cust_id, COUNT(*) AS orders
FROM Orders
GROUP BY cust_id
HAVING COUNT(*) >= 2;
~~~
- HAVING절과 WHERE절의 가장 큰 차이점은 WHERE절은 데이터가 그룹핑되기 전에 필터링하고, HAVING절은 데이터가 그룹핑된 후에 필터링한다는 점
- WHERE 절에서 필터링 되어 제거된 행은 그룹에 포함되지 않음
- 결과적으로 하나의 문장에 WHERE, HAVING을 모두 사용할 필요가 있다는 것
- 다음 예제에서는 가격이 4달러 이상인 제품을 두 개 이상 가진 판매처를 가져옴
~~~SQL
SELECT vend_id, COUNT(*) as num_prods
FROM Products
WHERE prod_price >= 4
GROUP BY vend_id
HAVING COUNT(*) >= 2;
~~~
- 대부분의 DBMS가 GROUP BY 절이 없는 경우, WHERE와 HAVING을 동일하게 처리하지만 우리 스스로 구분해서 사용하는 것이 좋음

### 그룹핑과 정렬
- ORDER BY와 GROUP BY를 잘 구분해야 함
- GROUP BY 수행시, 결과가 그룹 순서대로 정렬된 것을 볼 수 있지만, 항상 그런 것은 아니며, 필수사항도 아님
- 즉 정렬이 필요하다면 반드시 ORDER BY를 사용해야 함
~~~SQL 
SELECT order_num, COUNT(*) AS items
FROM OrderItems
GROUP BY order_num
HAVING COUNT(*) >= 3
ORDER BY items, order_num;
~~~

### SELECT문 순서
- SELECT
- FROM
- WHERE
- GROUP BY
- HAVING
- ORDER BY

### 도전과제
~~~SQL
--1
SELECT prod_id, COUNT(*) AS order_lines
FROM OrderItems
GROUP BY prod_id
ORDER BY order_lines;
--2
SELECT vend_id, MIN(prod_price) AS cheapest_item
FROM Products
GROUP BY vend_id
ORDER BY cheapest_item;
--3
SELECT order_num
FROM OrderItems
GROUP BY order_num
HAVING SUM(quantity) >= 100;
ORDER BY order_num;
--4
SELECT order_num, SUM(item_price*quantity) AS total_price
FROM OrderItems
GROUP BY order_num
HAVING SUM(item_price*quantity) >= 1000
ORDER BY order_num;
--5
SELECT order_num, COUNT(*) AS items
FROM OrderItems
GROUP BY order_num
HAVING COUNT(*) >= 3
ORDER BY items, order_num;
~~~

## chapter11 서브쿼리 사용하기
- 서브쿼리를 실행할 때, DBMS는 실제 두 번의 작업을 수행함
- 서브쿼리는 하나의 열만 검색할 수 있음. 여러 개의 열을 서브쿼리로 검색하면 에러가 발생함
- 서브쿼리를 사용하는 것이 항상 효율적인 것은 아님
~~~SQL
SELECT cust_name, cust_contact
FROM Customers
WHERE cust_id IN (SELECT cust_id
                  FROM Orders
                  WHERE order_num IN (SELECT order_num
                                      FROM OrderItems
                                      WHERE prod_id = 'RGAN01'))
~~~

### 계산 필드로 서브쿼리 사용하기
- 주문 수량을 Customers 테이블에 있는 고객별로 보고 싶다고 가정해보자
- 다음의 순서대로 진행
  - Customers 테이블에서 고객 목록을 가져옴
  - Orders 테이블에서 각각의 고객이 주문한 수를 셈
- 열 이름이 모호할 때마다 테이블 이름과 열 이름을 마침표(.)로 구분하여 적는 문법을 사용
- 완전한 열 이름(Fully Qualified Column Name)
  - DBMS가 우리의 의도를 제대로 해석하지 못해 잘못된 결과를 가져올 수 있음
  - 가끔은 열 이름이 중복되어 실제로 DBMS가 에러를 내는 경우도 있음
  - SELECT 문에서 두 개 이상의 테이블을 사용한다면 열이름 앞에 테이블명을 붙여주자 
~~~SQL
-- 다음의 서브쿼리는 꼭 기억하자. SELECT문 안에 서브쿼리 존재
SELECT cust_name, 
       cust_state, 
       (SELECT COUNT(*)
        FROM Orders
        WHERE Orders.cust_id = Customers.cust_id) AS orders
FROM Customers
ORDER BY cust_name;
~~~ 

### 도전 과제
- 서브 쿼리를 사용하여 10 또는 그 이상의 가격으로 제품을 구매한 고객 목록 반환
~~~SQL
--1
SELECT cust_id
FROM Customers
WHERE cust_id IN (SELECT cust_id
                  FROM Orders
                  WHERE order_num IN (SELECT order_num
                                      FROM orderItems
                                      WHERE item_price >= 10));

--2
SELECT cust_id, order_date
FROM Orders
WHERE order_num IN (SELECT order_num
                    FROM orderItems
                    WHERE prod_id = 'BR01');

--3
SELECT cust_email
FROM Customers
WHERE cust_id IN (SELECT cust_id
                  FROM Orders
                  WHERE order_num IN (SELECT order_num
                                      FROM orderItems
                                      WHERE prod_id = 'BR01'))

--4
SELECT cust_id, (SELECT COUNT(*)
                 FROM Orders
                 WHERE Customers.cust_id = Orders.cust_id) AS total_ordered
FROM Customers
ORDER BY total_ordered DESC;

--5
SELECT TRIM(prod_name), (SELECT SUM(quantity)
                   FROM OrderItems
                   WHERE Products.prod_id = OrderItems.prod_id) AS quant_sold
FROM Products;
~~~

## chapter12 - 테이블 조인 
- `WHERE` 절을 작성하지 않으면, 카테시안 조인을 수행함  
  카티전 곱을 반환하는 조인 타입을 Cross Join 이라고 부르기도 함
~~~SQL
SELECT TRIM(vend_name), TRIM(prod_name), prod_price
FROM Vendors, Products
WHERE Vendors.vend_id = Products.vend_id;

-- 카테시안 조인 수행
SELECT TRIM(vend_name), TRIM(prod_name), prod_price
FROM Vendors, Products
~~~
- 조인 타입을 표시할 때는 조금 다른 문법을 사용해야 함  
  다음 SELECT 문은 이전의 예제와 같은 결과 반환
~~~SQL
SELECT TRIM(vend_name), TRIM(prod_name), prod_price
FROM Vendors INNER JOIN Products
ON Vendors.vend_id = Products.vend_id;

-- 여러개의 테이블 조인 가능
SELECT TRIM(vend_name), TRIM(prod_name), prod_price, quantity
FROM Vendors INNER JOIN Products
ON Vendors.vend_id = Products.vend_id
INNER JOIN OrderItems 
ON OrderItems.prod_id = Products.prod_id
WHERE order_num = 20007;
~~~
- DBMS에서 조인은 자원을 매우 많이 소비함. 따라서 불필요한 조인을 하지 않도록 각별히 주의해야함
- 각각의 DBMS마다 조인 테이블 개수를 제한하고 있으므로, 확인이 필요

### 도전과제
~~~SQL
--1
SELECT cust_name, order_num
FROM Customers INNER JOIN Orders
ON Customers.cust_id = Orders.cust_id
ORDER BY cust_name, order_num;

--2
SELECT cust_name, order_num, (SELECT SUM(item_price * quantity) 
                              FROM OrderItems
                              WHERE Orders.order_num = OrderItems.order_num) AS OrdersTotal
FROM Customers INNER JOIN Orders
ON Customers.cust_id = Orders.cust_id
ORDER BY cust_name, order_num;

SELECT cust_name,
       Orders.order_num,
       SUM(item_price * quantity) AS OrderTotal
FROM Customers, Orders, OrderItems
WHERE Customers.cust_id = Orders.cust_id
AND Orders.order_num = OrderItems.order_num
GROUP BY cust_name, Orders.order_num
ORDER BY cust_name, order_num;

--3
SELECT order_date
FROM Orders INNER JOIN OrderItems
ON Orders.order_num = OrderItems.order_num
WHERE prod_id = 'BR01';

--5 
SELECT cust_name,
       Orders.order_num, 
       SUM(item_price*quantity) AS total_price
FROM Customers, Orders, OrderItems
WHERE Customers.cust_id = Orders.cust_id
      AND Orders.order_num = OrderItems.order_num
GROUP BY cust_name, Orders.order_num
HAVING SUM(item_price*quantity) >= 1000
ORDER BY cust_name
~~~

## chapter13 - 고급 테이블 조인 생성하기
### 테이블 별칭 사용하기
- 테이블에 별칭을 사용하는 이유는 크게 2가지
  - 사용하는 SQL 명령문의 수를 줄이기 위해
  - 하나의 SELECT문 내에서 같은 테이블을 여러 번 사용하기 위해  
~~~SQL
SELECT cust_name, cust_contact
FROM Customers C, Orders O, OrderItems OI
WHERE C.cust_id = O.cust_id
    AND OI.order_num = O.order_num
    AND prod_id = 'RGAN01';
~~~
- OracleDB 에서는 별칭 AS를 사용하지 않음. 그냥 `Customer C` 라고 씀
- 테이블 별칭은 쿼리가 수행되는 동안에만 사용할 수 있다는 점을 알아두자

### 다른 조인 타입 사용하기
- 셀프조인, 자연조인, 외부조인이라는 세가지 유형 알아보기

#### 셀프조인
- 테이블 별칭을 사용하는 주된 이유중 하나는 SELECT 문에서 같은 테이블을 두 번 이상 참조하기 위해서임
- 예를 들어 Jim Jones라는 사람과 같은 회사에서 일하는 모든 직원에게 메일을 보내려고 함
- 다음과 같이 사용 가능
~~~SQL
--1 sub query
SELECT cust_id, cust_name, cust_contact
FROM Customers
WHERE cust_name = (SELECT cust_name
                   FROM Customers
                   WHERE cust_contact = 'Jim Jones')

--2 self join
SELECT c1.cust_id, c1.cust_name, c1.cust_contact
FROM Customers c1, Customers c2
WHERE c1.cust_name = c2.cust_name AND c2.cust_contact = 'Jim Jones';
~~~
- <b>서브 쿼리보다는 셀프 조인이 성능적으로 훨씬 빠름</b>

### 자연조인(Natual Join)
- 표준조인은 조인하고자 하는 각 테이블에 있는 키가 다 나오는데, 자연조인은 중복 키가 하나만 나옴
- 중복되는 키를 제거하는 방법은 직접 중복되는 열을 제거하는 방법 뿐임
- 일반적으로 한 테이블에서는 와일드카드(SELECT *)를 사용하고, 다른 테이블은 가져올 열을 명시하여 만듬
~~~SQL
SELECT C.*, O.order_num, O.order_date,
       OI.prod_id, OI.quantity, OI.item_price
FROM Customers C, Orders O, OrderItems OIa
WHERE C.cust_id = O.cust_id
    AND OI.order_num = O.order_num
    AND prod_id = 'RGAN01';
~~~

### 외부조인(Outer Join)
- `LEFT OUTER JOIN`, `RIGHT OUTER JOIN`, `FULL OUTER JOIN`

### 그룹 함수와 조인 사용하기
- 그룹 함수는 조인과 함께 사용 가능
- 예를들어 모든 고객 목록과 각각의 고객이 주문한 수량을 가져오길 원한다고 가정
~~~SQL
SELECT Customers.cust_id,
       COUNT(Orders.order_num) AS num_ord
FROM Customers INNER JOIN Orders
ON Customers.cust_id = Orders.cust_id
GROUP BY Customers.cust_id;
~~~

### 도전과제
~~~SQL
--1
SELECT cust_name, order_num
FROM Customers INNER JOIN Orders
ON Customers.cust_id = Orders.cust_id
ORDER BY cust_name;

--2
SELECT cust_name, order_num
FROM Customers LEFT OUTER JOIN Orders
ON Customers.cust_id = Orders.cust_id
ORDER BY cust_name;
--3
SELECT prod_name, order_num
FROM Products LEFT OUTER JOIN OrderItems
ON Products.prod_id = OrderItems.prod_id
ORDER BY prod_name;

--4
SELECT TRIM(prod_name), COUNT(prod_name) AS orders
FROM Products LEFT OUTER JOIN OrderItems
ON Products.prod_id = OrderItems.prod_id
GROUP BY prod_name
ORDER BY prod_name

--5
SELECT Vendors.vend_id, COUNT(Vendors.vend_id)
FROM Vendors LEFT OUTER JOIN Products
ON Vendors.vend_id = Products.vend_id
GROUP BY Vendors.vend_id;
~~~

## chapter14 - 쿼리 결합하기
- `UNION` 연산자를 사용해 여러 개의 SELECT 문을 결합하여 하나의 결과를 얻는 방법을 학습

### 결합 쿼리 이해하기
- 여러 개의 쿼리를 수행해서 하나의 결과로 가져올 수 있음
- 이런 결합 쿼리를 보통 UNION, Compound 쿼리라고 부름
- 기본적으로 결합 쿼리를 사용하는 두 가지 경우의 시나리오가 있음
  - 여러 테이블에 있는 비슷한 구조의 데이터를 하나의 쿼리로 가져오는 경우
  - 한 개의 테이블에서 여러 개의 쿼리를 수행하고 하나의 결과로 가져오는 경우     
- 다음의 두 쿼리는 같은 쿼리
~~~SQL
--1 UNION 
SELECT cust_name, cust_contact, cust_email
FROM Customers
WHERE cust_state IN ('IL', 'IN', 'MI')
UNION
SELECT cust_name, cust_contact, cust_email
FROM Customers
WHERE cust_name = 'Fun4All';

--2 WHERE 조건 이용
SELECT cust_name, cust_contact, cust_email 
FROM Customers
WHERE cust_state IN ('IL', 'IN', 'MI')
    OR cust_name = 'Fun4All'; 
~~~
- 하나의 테이블에서 데이터를 가져와야 할 때, UNION을 사용하면 훨씬 더 간단한 쿼리를 만들 수 있음
- DBMS의 종류에 따라 UNION 제한이 걸려있을 수 있음
- 좋은 DBMS는 SELECT 문을 결합하기 위해 내부적으로 쿼리 최적화기를 사용함
- 이론상으로는 성능 관점에서 여러 개의 WHERE 절 조건이나 UNION을 사용하는 것이 아무런 차이가 없어야 함

### UNION 규칙
- `UNION`은 반드시 두 개 이상의 SELECT 문으로 구성되어야 하며, 각각의 명령문은 `UNION`이라는 키워드로 구분됨
- 각 쿼리는 같은 열이나 수식, 그룹 함수를 가져야 함(일부 DBMS는 열 순서까지 맞추어야 함)
- 열 데이터형은 호환될 수 있음. 정확히 같은 데이터형일 필요는 없지만, DBMS가 내부적으로 변환할 수 있어야 함
- 두 번째 SELECT 문에서 다른 이름을 사용한다고 할지라도 prod_name이 반환됨  
  즉 정렬시, 첫번째 컬럼 명으로 정렬해야함. 아니면 에러 발생

### 중복행 포함하기와 제거하기
- `UNION`은 쿼리 결과에서 자동으로 중복 행을 제거함
- 만약 중복되는 행을 모두 가져오고 싶다면, `UNION ALL`을 쓰면 됨
~~~SQL
SELECT cust_name, cust_contact, cust_email
FROM Customers
WHERE cust_state IN ('IL', 'IN', 'MI')
UNION ALL
SELECT cust_name, cust_contact, cust_email
FROM Customers
WHERE cust_name = 'Fun4All';
~~~ 

### 결합 쿼리 결과 정렬하기
- ORDER BY 절을 사용하여 SELECT 문의 결과를 정렬 할 수 있음
- UNION으로 쿼리를 결합할 때는 딱 하나의 ORDER BY 절을 사용할 수 있는데, 이 ORDER BY 절은 마지막 SELECT 구문 뒤에 와야 함

### 도전과제
~~~SQL
--1
SELECT prod_id, quantity
FROM OrderItems
WHERE prod_id LIKE 'BNBG%'
UNION
SELECT prod_id, quantity
FROM OrderItems
WHERE quantity = 100;

--2
SELECT prod_id, quantity
FROM OrderItems
WHERE prod_id LIKE 'BNBG%' OR quantity = 100;

--3


~~~