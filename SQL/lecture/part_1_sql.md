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

-- 검색 중간에도 사용가능. 많이 사용하지는 
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
~~~

## chapter15 데이터 삽입하기
- `INSERT`문은 여러 가지 방법으로 사용 가능
  - 완전한 행 삽입하기
  - 부분 행 삽입하기
  - 쿼리 결과 삽입하기
- `INSERT` 문을 사용하려면 특별한 보안 권한이 필요할 수 있음. `INSERT`문을 사용하기 전에 적절한 권한을 갖고 있는지 확인 필요

### 완전한 행 삽입하기
~~~SQL
INSERT INTO Customers
VALUES (1000000006,
        'Toy Land',
        '123 Any Street',
        'New York',
        'NY',
        '11111',
        'USA',
        NULL,
        NULL);
~~~
- 일부 SQL 실행 환경에서는 INSERT 문 뒤에 나오는 INTO를 써도 되고 안써도 됨
- 하지만 무조건 이 키워드를 쓰는 것이 좋은 이유는 SQL 코드를 다른 DBMS에서도 문제없이 실행할 수 있기 때문 
- 위의 코드는 굉장히 위험한데, 그 이유는 컬럼 순서가 언제 바뀔지 모름  
  따라서 다음과 같이 사용하는 것이 더 좋음
~~~SQL
INSERT INTO Customers (cust_id,
                       cust_name,
                       cust_address,
                       cust_city,
                       cust_state,
                       cust_zip,
                       cust_country,
                       cust_contact,
                       cust_email)
VALUES (1000000006,
        'Toy Land',
        '123 Any Street',
        'New York',
        'NY',
        '11111',
        'USA',
        NULL,
        NULL);
~~~
- 작성한 열의 개수와 같게 VALUE에도 있어야 함

### 부분 행 삽입하기
- `INSERT INTO` 다음에 컬럼명을 써주게 되면, 모든 컬럼을 다써주지 않아도 INSERT가 가능  
  당연히 필수적인 값은 값이 누락되서는 안됨
~~~SQL
INSERT INTO Customers (cust_id,
                       cust_name,
                       cust_address,
                       cust_city,
                       cust_state,
                       cust_zip,
                       cust_country)
                       
VALUES (1000000006,
        'Toy Land',
        '123 Any Street',
        'New York',
        'NY',
        '11111',
        'USA');
~~~

### 검색 결과 삽입하기
- 보통 특정한 값을 삽입할 때 INSERT 문을 사용하지만, SELECT 문에서 가져온 결과를 테이블에 넣는 형태도 있음
  `INSERT SELECT` 문인데, 이름에서 유추할 수 있는 것처럼 INSERT문과 SELECT문으로 구성됨
- 다음과 같이 사용 가능
~~~SQL 
INSERT INTO Customers (cust_id,
                       cust_name,
                       cust_address,
                       cust_city,
                       cust_state,
                       cust_zip,
                       cust_country)
SELECT cust_id,
       cust_contact,
       cust_email,
       cust_name,
       cust_address,
       cust_city,
       cust_state,
       cust_zip,
       cust_country
FROM CustNew;
~~~
- 꼭 INSERT문과 SElECT문의 컬럼명이 같을 필요는 없음
- 사실 DBMS는 SELECT문으로 반환되는 열 이름에 신경쓰지 않음. 열의 위치를 사용함
- SELECT문에서 WHERE절을 사용해서 데이터를 가져올 수도 있음
- 위와 같이 `INSERT SELECT`문을 사용하면, 결과로 가져오는 행을 모두 삽입하기 때문에 하나의 문장으로 여러 행을 삽입할 수 있음

### 다른 테이블로 복사하기
- `INSERT`문을 전혀 사용하지 않고도 삽입할 수 있는데, 테이블에 있는 내용을 완전히 새로운 테이블에 복사할 때 `CREATE SELECT` 문을 사용하는 것
~~~SQL
CREATE TABLE CustCopy as SELECT * FROM Customers;
~~~
- `SELECT INTO`는 다음과 같은 특징이 있음
  - `WHERE`나 `GROUP BY` 절과 같은 `SELECT`문의 옵션을 모두 사용 가능
  - 여러 테이블에 있는 데이터를 삽입하기 위해 조인을 사용할 수 있음
  - 데이터를 가져온 테이블 수와는 관계없이, 가져온 데이터는 하나의 테이블에 삽입됨 

### 도전 과제
~~~SQL
--1
INSERT INTO Customers (cust_id,
                      cust_name,
                      cust_address,
                      cust_city,
                      cust_zip,
                      cust_country,
                      cust_contact,
                      cust_email)
VALUES (1000000007,
        'Toy Land',
        '123 Any Street',
        'New York',
        'NY',
        '11111',
        'USA',
        NULL);
--2
~~~

## chapter16 데이터 업데이트와 삭제
- `UPDATE`와 `DELETE`를 사용해 테이블 데이터를 조작하는 방법 학습
- `UPDATE`문 사용시 `WHERE` 절 누락을 매우 조심해야 함
- `UPDATE`문의 기본 형태는 다음과 같이 세 가지 부분으로 이루어져 있음
  - 업데이트할 테이블
  - 열 이름과 새로운 값
  - 어떤 행이 업데이트되어야 하는지를 지정하는 필터 조건
~~~SQL
UPDATE Customers
SET cust_email = 'kim@thetoystore.com'
WHERE cust_id = 1000000005;

-- 여러 열 업데이트
UPDATE Customers
SET cust_email = 'kim@thetoystore.com',
    cust_contact = 'Sam Roberts'
WHERE cust_id = 10000000056
~~~ 
- `UPDATE` 문에서도 SELECT문으로 가져온 데이터로 열을 업데이트하기 위해 서브쿼리를 사용할 수 있음
- 특정 SQL 실행 환경에서는 UPDATE 문에서 FROM 절을 사용하도록 지원하기도 함
- FROM절을 사용하면 다른 테이블에 있는 데이터로 테이블의 열을 업데이트 할 수 있음
- 열값을 삭제하려면 열에 NULL을 설정하면 됨
~~~SQL
UPDATE Customers
SET cust_email = NULL
WHERE cust_id = 1000000005;
~~~

### 데이터 삭제
~~~SQL
DELETE FROM Customers
WHERE cust_id = 1000000006; 
~~~
- `DELETE` 문에서는 열 이름이나 와일드카드 문자를 사용하지 않음
- `DELETE`는 열이 아니라 전체 행을 삭제하므로, 특정 열을 삭제하려면 `UPDATE` 문을 사용해야 함
- 모든 행을 삭제하고 싶을 때, `TRUNCATE`를 사용하면 훨씬 빠르게 삭제가 가능

## chapter17 테이블 생성과 조작
### 테이블 생성
- 테이블을 생성하려면 `CREATE TABLE`이라는 SQL 문을 사용함
- 우리가 DBMS에서 제공하는 대화형 관리 툴을 사용하더라도 실제로는 SQL문을 사용
- `CREATE TABLE`문은 SQL 실행 환경마다 매우 다름
~~~SQL
CREATE TABLE Products
(
    prod_id CHAR(10) NOT NULL,
    vend_id CHAR(10) NOT NULL,
    prod_name CHAR(254) NOT NULL,
    prod_price DECIMAL(8,2) NOT NULL,
    prod_desc VARCHAR(1000) NULL
)
~~~
- NOT NULL과 빈 문자열은 구분하자

### 기본값 지정하기
- 테이블 생성시, 값이 없으면 자동으로 들어가는 기본값을 지정할 수 있음
- 기본값은 CREATE TABLE 문에서 열을 정의할 때 DEFAULT 키워드를 사용해서 지정함
~~~SQL
CREATE TABLE OrderItems
(
    order_num INTEGER NOT NULL,
    order_item INTEGER NOT NULL,
    prod_id CHAR(10) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    item_price DECIMAL(8,2) NOT NULL
); 
~~~
- 기본값은 날짜나 시간 열에도 자주 사용되는데, 예를 들어 시스템 날짜를 가져오는 함수나 변수를 사용하여 행을 삽입하는 시점의 날짜와 시간을 기본값으로 지정할 수 있음
  - Db2 : `CURRENT_DATE`
  - MySQL: `CURRENT DATE`, `Now())`
  - Oracle: `SYSDATE`
  - PostgreSQL: `CURRENT DATE`
  - SQL Server: `GETDATE()`
  - SQLite: `date('now')`

### 테이블 변경하기
- 테이블 정의를 변경할 때 `ALTER TABLE` 문을 사용함
- 모든 DBMS가 `ALTER TABLE`을 지원하지만, 바꿀 수 있는 항목은 DBMS에 따라 다름

#### ALTER TABLE을 사용할 때 고려해야 할 점
- 데이터가 있는 테이블은 변경해서는 안됨
- 모든 DBMS는 존재하는 테이블에 열을 추가하는 것은 허용되지만, 추가하는 열의 데이터형에 몇가지 제약을 둠
- 다수의 DBMS는 테이블에 있는 열을 제거하거나 변경하는 것을 허용하지 않음
- 대부분의 DBMS는 열 이름의 변경은 허용함
- 다수의 DBMS는 데이터가 있는 열을 변경하는 것은 제한하고, 데이터가 없는 열을 변경하는 것에는 제한 사항을 많이 두지 않음

#### ALTER TABLE 사용 방법
- ALTER TABLE 문 뒤에 변경할 테이블 이름을 적음
- 변경할 사항을 나열
~~~SQL
ALTER TABLE Vendors
ADD vend_phone CHAR(20);

-- 컬럼 제거
ALTER TABLE Vendors
DROP COLUMN vend_phone;
~~~

#### 복잡한 데이터 구조 변경 방법
- 새로운 열 구조를 가진 새 테이블을 생성
- `INSERT SELECT` 문을 이용하여 이전의 테이블에 있는 데이터를 새로운 테이블에 복사  
  필요하다면 변환 함수나 계산 필드를 사용
- 새로운 테이블에 원하는 데이터가 있는지 확인
- 이전 테이블의 이름을 변경 또는 삭제
- 새로운 테이블을 이전에 사용한 테이블 이름으로 변경
- 필요하다면 트리거, 저장 프로시저, 인덱스, 왜래 키를 다시 생성

### 테이블 삭제하기
- `DROP TABLE` 구문 이용
- 많은 DBMS가 여타 다른 테이블과 관련된 테이블은 삭제하지 못하게 규칙을 정할 수 있도록 함
- 규칙을 설정하면 그 관계를 삭제하기 전까지 DBMS과 관련된 테이블을 삭제하지 못하게 막음

### 테이블 이름 바꾸기
- `RENAME` 으로 테이블 이름 변경 가능

### 도전과제
~~~SQL
--1
ALTER TABLE Vendors
ADD vend_web VARCHAR(1000);

--2 
UPDATE Vendors
SET VEND_WEB = 'www.github.com/koni114';
~~~

## chapter18 뷰 사용하기
- 뷰가 무엇이고, 어떻게 동작하는지 그리고 뷰를 언제 사용해야 하는지 학습 

### 뷰 이해하기
- 뷰는 가상 테이블. 데이터를 가진 테이블과는 달리, 뷰는 사용될 때 동적으로 데이터를 가져오는 쿼리들을 담고 있을 뿐임
- SQLite는 읽기 전용 뷰만 지원하고 업데이트는 불가
- 뷰는 어떠한 열이나 데이터를 갖고 있지 않음. 대신 테이블을 적절히 조인하기 위해 위에 사용한 것과 같은 쿼리를 가지고 있음
- 뷰 생성 문법은 대부분의 주요 DBMS에서 거의 동일하게 지원함
- 일반적으로 뷰는 생성한 후에 테이블과 같은 방식으로 사용
- 중요한 것은 뷰는 뷰일 뿐이고, 데이터는 딴 곳에 있기 때문에 원 테이블의 데이터가 변경되면 뷰는 변경된 데이터를 가져옴

#### 뷰를 사용하는 이유
- SQL 문을 재사용하기 위해서 사용
- 복잡한 SQL 작업을 단순화하려는 것임. 근본적으로 쿼리 그 자체에 대한 상세 내용을 알지 않고도 작성된 쿼리를 다시 사용할 수 있음 
- 완전한 테이블이 아니라 테이블의 일부만을 노출하기 위해서임
- 데이터를 보호하기 위해서 사용. 사용자는 전체 테이블이 아니라 테이블의 특정 부분에만 접근할 수 있음
- 데이터 형식을 변경하기 위해서 사용. 뷰는 원래의 테이블과 다른 형식으로 데이터를 가져올 수 있음

#### 뷰 규칙과 제한
- DBMS마다 조금씩 종류가 다르기 때문에 우리가 사용하는 DBMS의 메뉴얼을 미리 참고하는 것이 좋음
- 테이블처럼 뷰는 고유한 이름을 가져야 함(다른 테이블 이름이나 뷰 이름을 사용 할 수 없음)
- 생성할 수 있는 뷰의 수에는 제한이 없음
- 뷰를 생성하기 위한 보안 권한을 가져야 함. 이 접근 권한 수준은 DB관리자가 제한함
- 뷰는 뷰를 포함할 수 있음. 즉 뷰는 다른 뷰에서 데이터를 가져오는 쿼리를 사용하여 만들 수 있음  
  몇 겹까지 중첩할 수 있는지는 DBMS마다 다름  
  중첩된 뷰는 쿼리 성능을 현저하게 낮추기 때문에 프로덕션 환경에서 사용하기 전에 철저한 테스트 필요
- 많은 DBMS는 뷰 쿼리에서 ORDER BY 절의 사용을 금지함
- 일부 DBMS는 가져오는 모든 열에 이름을 필히 부여해야 함. 열이 계산 필드라면 별칭을 사용해야 할 것임
- 뷰는 인덱스를 사용할 수 없음. 또한 트리거 또는 그와 연관된 기본값을 사용할 수 없음

### 뷰 생성하기
- `CREATE VIEW`문을 사용해서 생성
- 뷰를 삭제하려면 `DROP`문을 사용. 문법은 `DROP VIEW 뷰이름`  
  뷰를 덮어쓰거나 또는 업데이트하려면, 뷰를 먼저 삭제한 후에 다시 생성해야 함

#### 복잡한 조인을 단순화하기 위한 뷰 생성하기
~~~SQL
CREATE VIEW ProductCustomers AS 
SELECT cust_name, cust_contact, prod_id
FROM Customers, Orders, OrderItems
WHERE Customers.cust_id = Orders.cust_id
AND OrderItems.order_num = Orders.order_num;

-- View를 이용한 데이터 SELECT
SELECT cust_name, cust_contact
FROM ProductCustomers
WHERE prod_id = 'RGAN01';
~~~
- 재사용이 가능한 뷰를 생성하는 것이 중요. 뷰의 범위를 확장하면 재사용이 가능하기 때문에 좀 더 유용함
- 뿐만 아니라, 여러분이 여러 개의 비슷한 뷰를 만들고 관리하지 않도록 함

#### 가져온 데이터의 형식을 변경하기 위해 뷰 사용하기
~~~SQL
CREATE VIEW VendorLocations AS
SELECT TRIM(vend_name) || '(' || TRIM(vend_country) || ')' AS vend_title
FROM Vendors;
~~~

#### 원하지 않는 데이터를 필터링하기 위해 뷰 사용하기
- 뷰는 `WHERE`절과 함께 사용할때도 유용함
~~~SQL
CREATE VIEW CustomerEmailList AS 
SELECT cust_id, cust_name, cust_email
FROM Customers
WHERE cust_email IS NOT NULL;
~~~

#### 계산 필드와 함께 뷰 사용하기
~~~SQL
CREATE VIEW OrderItemsExpanded AS 
SELECT prod_id,
       quantity,
       item_price,
       quantity * item_price AS expended_price
FROM OrderItems
~~~

## chapter19 저장 프로시저 사용하기
- 종종 복잡한 작업을 수행하기 위해 다수의 구문을 사용해야 할 필요가 있음
- 예를 들어 다음 시나리오를 보자
- 시나리오
  - 주문을 처리하려면, 제품의 재고가 있는지 확인
  - 제품이 있다면 다른 고객에게 팔리지 않도록 예약해야 하고, 사용 가능한 수량을 하나 줄여 재고에 정확한 숫자를 반영해야 함
  - 재고가 없다면, 제품을 주문해야 함. 이 작업은 판매처와 연동돼서 작업 해야 함
  - 고객은 어떤 제품이 재고가 있는지, 그리고 어떤 제품은 다시 주문해야 하는지 등의 알림을 받아야 함 
- 위의 시나리오를 처리하려면 여러 테이블과 다양한 SQL 문이 필요함
- 수행해야 할 정확한 SQL 명령문과 순서는 고정된 것이 아님. 제품이 재고가 있는지 없는지에 따라 SQL 문이나 순서는 얼마든지 변경될 수 있음
- 이러한 코드는 SQL문을 각각 따로 작성한 뒤, 결과에 따라 조건에 맞게 명령문을 실행하도록 작성하는 것이 가능함 
- 처리가 필요한 시점마다 우리가 명령문을 수동으로 실행해야 하는데, 다른 방법으로는 저장 프로시저를 사용할 수 있음
- <b>저장 프로시저는 나중에 사용하기 위해 만들어둔 하나 이상의 SQL 명령문 집합을 의미함</b>
- 일종의 배치 파일로 생각해도 됨. 실제로는 배치 파일 이상의 기능을 제공함 

### 저장 프로시저를 사용하는 이유
- 여러 단계로 이루어진 과정을 사용하기 쉬운 하나의 단위로 캡슐화하여 복잡한 작업을 단순화함
- 여러 단계를 반복해서 만들 필요가 없어 데이터 일관성을 보장함  
  모든 개발자가 같은 프로그램을 사용한다면 같은 코드를 사용할 것임
- 오류 방지에도 도움을 줌. 수행해야 할 단계가 많아질수록, 오류는 더욱 발생하기 쉬움
- 변화 관리를 단순화함. 테이블, 열 이름, 비즈니스 로직이 변경되면 저장 프로시저 코드만 바꾸고 다른 것은 수정할 필요가 없음
- 보안성을 높임. 저장 프로시저를 사용하면 기본 데이터에 대한 접근을 제한할 수 있음
- 저장 프로시저는 컴파일된 형태로 저장하기 때문에 명령을 처리하기 위해 DBMS가 해야 하는 일이 줄어들고 그 결과 성능이 향상됨
- 결과적으로 단순성, 보안성, 성능이 향상됨 

### 저장 프로시저의 단점
- 저장 프로시저의 문법은 DBMS마다 매우 달라서 다른 DBMS로의 이식은 거의 불가능함
- 저장 프로시저를 작성하려면 고수준의 기술과 경험이 필요  
  그래서 많은 DB 관리자는 보안 조치 중 하나로 저장 프로시저 생성 권한을 제한함

### 저장 프로시저 실행하기
- 저장 프로시저는 작성하는 횟수보다 훨씬 더 많이 실행됨
- 저장 프로시저를 실행하는 SQL문은 EXECUTE인데, 저장 프로시저의 이름과 전달할 필요가 있는 매개변수를 갖음
~~~SQL
EXECUTE AddNewProduct('JTS01',
                      'Stuffed Eiffel Tower',
                      6.49);
~~~
- `AddNewProduct`라는 이름의 저장 프로시저를 실행하였음.
- 이는 Products 테이블에 새로운 제품을 추가함. 3개의 매개변수를 가지며 새로운 행을 추가하고 적절한 열에 매개변수를 전달함
- 위의 프로시저에서 prod_id를 지정하지 않은 이유는 시스템 내에서 자동으로 입력되게 하기 위해서임


### 저장 프로시저 생성하기
- 저장 프로시저 생성하는 간단한 예제
~~~SQL
CREATE PROCEDURE MailingListCount(
    ListCount OUT INTEGER
)
IS
v_rows INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_rows
    FROM Customers
    WHERE NOT cust_email IS NULL;
    ListCount := v_rows;
END;
~~~
- 위의 저장 프로시저는 ListCount라는 매개변수 하나를 가짐. 결괏값을 가져오는데 사용
- `OUT`키워드는 이런 행동을 명시하기 위해 사용
- `IN`은 저장 프로시저로 값을 전달하기 위해, `OUT`은 저장 프로시저에서 값을 반환하기 위해 사용
- `INOUT`은 두 용도로 모두 사용됨
~~~SQL
var ReturnValue NUMBER
EXEC MailingListCount(:ReturnValue);
SELECT ReturnValue;
~~~

## chapter20 트랜잭션 처리 관리하기
- 트랜잭션의 기본 개념과 트랜잭션을 관리할 때 사용하는 COMMIT 과 ROLLBACK 문의 특징을 알아보자

### 트랙잭션 처리 이해하기
- <b>트랜잭션 처리는 여러 개의 SQL 작업을 일괄적으로 실행하거나 아니면 아예 실행하지 않도록 하여 DB의 무결성을 보장하는 처리 방식</b>
- 트랜잭션 처리는 DB가 부분적으로 작업을 수행하는 것을 막기 위해 여러 SQL 작업을 일괄적으로 처리하는 매커니즘
- 트랜잭션 처리를 이용하면 작업이 중간에 중단되지 않도록 할 수 있음
- 트랜젝션 처리 시 에러가 발생하지 않으면, SQL문 전체가 데이터베이스 테이블에 커밋되고 에러가 발생하면 롤백되어 데이터베이스가 안전한 상태로 복구됨
- 다음의 용어들은 기억하자
  - 트랜잭션(Transaction): 일괄 처리할 SQL 명령어들을 묶은 블록
  - 롤백(Rollback): 변경된 작업 내용들을 모두 취소하는 절차
  - 커밋(Commit): 변경된 작업 내용을 DB에 저장
  - 저장점(SavePoint): 부분적으로 롤백하기 위한 임시 시점
- 트랜잭션 처리는 INSERT, UPDATE, DELETE 문을 관리하기 위해 사용  
  SELECT, CREATE, DROP은 롤백 불가능

### 트랜잭션 통제하기
- 트랜잭션을 관리하는데 있어 가장 중요한 점은 SQL 문을 논리적인 작업 단위로 만들어 데이터가 롤백되어야 하는 시점과 그렇지 않은 시점을 확실하게 명시하는 것임
- 다음은 트랜잭션을 작성하는 방법임
~~~SQL
--Oracle
SET TRANSACTION
...
--PostgreSQL
BEGIN
...
~~~

#### 롤백 사용하기
~~~SQL
DELETE FROM Orders
ROLLBACK;
~~~

#### 커밋 사용하기
- 보통 SQL 문은 실행되면서 데이터베이스 테이블을 바로 변경함
- 이렇게 커밋이 자동으로 일어나는 것을 자동 커밋이라고 하며, 트랜잭션은 자동으로 커밋되지 않음
- 이 또한 DBMS마다 다른데, 일부 DBMS는 트랜잭션의 끝을 자동 커밋으로 다루기도 하고, 일부는 그렇게 다루지 않음 
~~~SQL
--Oracle
SET TRANSACTION
DELETE OrderItems WHERE order_num = 12345;
DELETE Orders WHERE order_num = 12345; 
COMMIT;
~~~

#### 저장점(Save point) 사용하기
- ROLLBACK과 COMMIT 문은 단순히 전체 트랜잭션을 저장하거나 되돌리는 작업만 함
- 간단한 트랜잭션을 사용할 때는 문제가 없지만, 좀 더 복잡한 트랜잭션은 부분적인 커밋이나 롤백이 필요할 수도 있음 
- 트랜잭션에서 전략상 중요한 위치들을 임시 지점으로 정해놓고, 롤백이 필요할 때 임시 지점 중 하나로 되돌리면 됨
- SQL에서는 이 임시 지점을 저장점이라고 부름  
  MariaDB, MySQL, Oracle에서는 저장점을 생성하려면 SAVEPOINT 문을 사용함
~~~SQL
SAVEPOINT delete1;
ROLLBACK TO delete1;
~~~

## chapter21 커서 사용하기
### 커서 이해하기
- SQL 검색 작업은 결과 집합이라고 부르는 여러 행을 반환하고, 이는 한 행도 없을 수도 있고, 여러 행이 될 수도 있음
- 이전까지의 단순한 SELECT 문으로는 첫 번째행, 그다음 행, 이전의 10개 행을 가져올 방법이 없음
- 간혹 행을 앞 뒤로 이동하며 데이터를 가져와야 할 필요가 있는데, 이럴 때 커서를 사용할 수 있음
- <b>커서는 DBMS에 서버에 저장된 쿼리로서 SELECT 문은 아니지만, SELECT 문으로 가져온 결과 집합임</b>
- 커서는 한 번 저장되면, 프로그램에서 필요할 때마다 데이터를 상하로 탐색하면서 검색 결과를 가져올 수 있음
- DBMS마다 커서 옵션과 기능을 다르게 지원함. 다음은 일반적으로 자주 사용하는 커서의 옵션과 기능임

#### 커서의 옵션과 기능
- 커서에 읽기 전용으로 표시하여, 데이터를 읽을 수는 있지만 업데이트나 삭제는 못하게 하는 기능
- 방향과 위치를 제어할 수 있는 기능(전방, 후방, 첫 번째, 마지막, 절대 위치, 상대 위치 등)
- 특정한 열만 수정할 수 있게 표시하고, 그 외의 열은 수정하지 못하게 하는 기능
- 커서를 특정한 요청이나 모든 요청에 접근할 수 있게 하는 범위 지정 기능
- DBMS에서 가져온 데이터를 복사하여(테이블에 있는 실제 데이터를 가리키는 게 아니라 복사본을 가리킬 수 있게), 커서가 연(open) 후 데이터를 사용하는 사이에 데이터가 변경되지 않게 하는 기능
- 커서는 사용자가 화면의 데이터를 위, 아래로 탐색하며 필요에 따라 변경할 수 있는 대화형 프로그램에서 자주 사용됨

### 커서 사용하기
- 커서는 다음과 같음 방식으로 사용됨
- 커서는 반드시 사용하기 전에 선언하여야 함. 이 절차는 실제 어떤 데이터도 가져오진 않고, 단지 사용할 SELECT 문과 커서 옵션을 정의함
- 선언된 커서를 사용하려면 먼저 커서를 열어야 함. 그러면 이전에 정의한 SELECT 문으로 데이터를 가져옴
- 필요할 때마다 데이터를 가진 커서에서 개별 행을 가져옴 
- 커서를 다 사용했으면 커서를 닫고(close), 가능하면 해제시켜야 함(DBMS에 따라 다름)
- 한 번 커서를 선언하면, 필요할 때마다 몇 번이고 다시 열고 닫을 수 있음. 또한 커서를 한 번 열면  
  그 안의 데이터를 몇 번이고 가져올(fetch) 수 있음

#### 커서 만들기
- 커서는 `DECLARE` 문을 사용하여 만들 수 있는데, 이 또한 DBMS마다 다름
- `DECLARE`로 커서 이름을 선언한 다음 SELECT 문을 선언함
- 필요에 따라 `WHERE` 절이나 다른 절을 사용할 수도 있음. 예제는 이메일 주소가 누락된 고객 정보를 알려줄 때 사용하는 코드로, 이메일 주소가 없는 모든 고객 정보를 가져오는 커서를 만듬
~~~SQL
DECLARE 
   CURSOR CustCursor 
   IS 
        SELECT * 
          FROM Customers 
        WHERE cust_email IS NULL; 
~~~

#### 커서 사용하기
~~~SQL
OPEN CURSOR CustCursors
~~~
- OPEN CURSOR문이 처리될 때 쿼리가 수행되며, 나중에 탐색하거나 가져오기 위해 데이터를 저장함
- 이제 `FETCH` 문을 이용하여 데이터에 접근할 수 있음
- `FETCH`는 어떤 행을 가져올지, 어디서부터 가져올지 그리고 어디에 저장할지(예를 들면 변수명 등)를 정의함. 첫 번째 예제는 커서에서 맨 위에 있는 한 행을 가져오기 위한 Oracle 문법임
~~~SQL
-- 아래 예제는 가져온 데이터로 아무런 작업도 하지 않음
DECLARE TYPE CustCursor IS REF CURSOR
    RETURN Customers%ROWTYPE;
DECLARE CustRecord Customers%ROWTYPE
BEGIN
    OPEN CustCursor;
    FETCH CustCursor INTO CustRecord; -- 현재 행을 가져와 CustRecord에 저장
    CLOSE CustCursor;
END;
-- 다음은 커서의 첫 번째 행부터 마지막 행까지 루프를 도는 예제
DECLARE TYPE CustCursor IS REF CURSOR
    RETURN Customers%ROWTYPE;
DECLARE CustRecord Customers%ROWTYPE
BEGIN
    OPEN CustCursor;
    LOOP -- LOOP안에 있어서 현재 행을 가져오는 것을 반복함
    FETCH CustCursor INTO CustRecord;
    EXIT WHEN CustCursor%NOTFOUND;
    ... -- 이 부분에 필요한 코드를 넣어 사용하면 됨
    END LOOP;
    CLOSE CustCursor;
END;
~~~

### 커서 닫기
- 사용이 끝난 커서는 닫아야 함
~~~SQL
CLOSE CustCursor
~~~
- 커서가 닫히면, 다시 열기 전에는 사용할 수 없음
- 한편 다시 사용할 때는 커서를 또다시 선언할 필요가 없고, OPEN 문으로 열기만 하면 됨

## chapter22 고급 데이터 조작 옵션
- 제약 조건, 인덱스, 트리거와 같이 SQL과 함께 발전한 고급 데이터 조작 기능을 살펴보자

### 제약 조건 이해하기
- DBMS는 데이터베이스 테이블에 제약 조건을 정의해 참조 무결성을 보장함
- 대부분의 제약 조건은 테이블 정의에 명시됨

#### 기본 키
- 절대 변하지 않고, 값이 고유함을 보장하기 위해 사용
- 다음 조건을 만족하면, 테이블에 있는 열은 어떤 열이든 기본 키로 설정할 수 있음
  - 두 개 이상의 행이 같은 기본 키 값을 가질 수 없음
  - 모든 행은 기본 키 값을 반드시 지켜야 함
  - 기본 키 값을 가진 열은 변경하거나 업데이트할 수 없음
  - 기본 키 값은 절대 다시 사용되서는 안됨  
    테이블에서 행이 삭제되더라도, 그 값이 다른 행에 다시 할당되어서는 안됨
~~~SQL
CREATE TABLE Vendors (
    vend_id CHAR(10) NOT NULL PRIMARY KEY,
    vend_name CHAR(50) NOT NULL,
    ...
)

-- 다음과 같이 사용 가능
ALTER TABLE vendors ADD CONSTRAINT PRIMARY KEY(vend_id);
~~~

#### 왜래 키(foriegn key)
- 테이블에 있는 열이면서 그 값이 다른 테이블의 기본 키 값 중에 꼭 존재해야 하는 열임
~~~SQL
CREATE TABLE Orders
(
    order_num INTEGER NOT NULL PRIMARY KEY,
    order_date DATETIME NOT NULL,
    cust_id CHAR(10) NOT NULL REFERENCES Customers(cust_id)
)
~~~

#### 고유 키 무결성 제약 조건
- 고유 키 무결성 제약조건(Unique Constraint)은 열에 있는 모든 데이터가 동일한 값을 가질 수 없음을 정의하는 제약 조건 
- 기본 키와 비슷해 보이지만, 몇 가지 차이점이 있음
- 테이블은 여러 Unique Constraint을 가질 수 있지만, 기본 키는 한 테이블에 하나만 정의되어야 함 
- Unique Constraint는 NULL을 가질 수 있음
- Unique Constraint는 변경되거나 업데이트 될 수 있음
- Unique Constraint의 값은 재사용 될 수 있음
- 기본 키와는 달리 Unique Constraint는 왜래 키로 정의되어 사용될 수 없음

#### 체크 무결성 제약 조건
- 열에서 허용 가능한 데이터의 범위나 조건을 지정하기 위한 제약 조건
- 일반적인 용도는 다음과 같음
  - 최솟값이나 최댓값 확인  
    ex) 제품 수량이 0이 될 수 없게 함
  - 범위 지정
  - 특정 값만 허용 
~~~SQL
CREATE TABLE OrderItems
(
    order_num INTEGER NOT NULL,
    order_item INTEGER NOT NULL,
    prod_id CHAR(10) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0)
);

ADD CONSTRAINT CHECK (gender LIKE '[MF]')
~~~

### 인덱스 이해하기
- 인덱스는 데이터를 논리적으로 정렬해 검색과 정렬 작업 시 속도를 높이는 데 사용함
- 인덱스를 이해하기 가장 좋은 방법은, 이 책 뒤에 있는 찾아보기를 갖고 생각해 보는 것
- 사전처럼 내가 찾고자 하는 데이터가 정렬되어 있다면, 쉽게 찾을 수 있는 원리와 동일
- PK는 항상 정렬되어 있어, 기본 키로 특정 데이터를 찾는 것은 항상 빠르면서 효율적인 방법이지만, 다름 컬럼에서 값을 찾는 것은 보통 효율적이지 않음
- 이 때 인덱스를 사용함. 하나 이상의 열을 인덱스로 정의할 수 있는데, 인덱스로 정의한 열은 DBMS가 내용을 정렬해서 저장해 둠
- 인덱스를 정의하면 DBMS는 책에서 찾아보기를 사용할 때와 거의 비슷한 방식으로 찾음

#### 인덱스 생성시 고려사항
- 인덱스는 검색 성능을 개선하지만, 삽입, 수정, 삭제 성능은 저하됨  
  이런 작업을 수행할 때마다 DBMS는 인덱스를 동적으로 업데이트 해야 하기 때문
- 인덱스 데이터는 저장 공간을 많이 차지함
- 모든 데이터가 인덱스에 적합한 것은 아님 . 충분히 고유하지 않은 데이터는 성과 이름 같은 데이터보다 인덱스로 정의하여 얻는 이득이 별로 없음
- 인덱스는 데이터 필터링과 정렬에 사용됨. 특정 순서로 데이터를 자주 정렬한다면, 그 데이터는 인덱싱 후보가 될 수 있음
- 여러 열을 하나의 인덱스로 정의할 수 있음(ex) 도 이름 + 도시명)
- 이러한 인덱스는 도 이름 + 도시명 순서대로 데이터를 정렬할 때만 사용함
- 만약 데이터를 도시명으로만 정렬하길 원한다면 인덱스는 쓸모가 없음
- `CREATE INDEX` 구문으로 생성할 수 잇음
- 다음 문장은 Products 테이블의 제품명으로 인덱스를 생성하는 예제임 
~~~SQL
CREATE INDEX prod_name_ind
ON Products (prod_name);
~~~
- 모든 인덱스는 고유한 이름을 가져야 함
- 인덱스에 포함되는 열은 테이블 이름 다음에 괄호로 묶어서 지정할 수 있음
- 인덱스의 효과는 테이블에 데이터를 추가하거나 변경하면서 변함. 많은 DB 관리자들은 몇 달간 데이터를 조작하고 나면, 한동안 이상적이라고 생각했던 인덱스가 이상적이지 않을 수 있다는 것을 알게됨
- 필요할 때마다 정기적으로 인덱스를 다시 정리하는 것이 좋음

### 트리거 이해하기
- 트리거는 특정한 DB 작업이 발생하면 자동으로 수행되는 특별한 저장 프로시저
- 특정한 테이블에 INSERT, UPDATE, DELETE와 같은 작업이 일어나면 자동으로 실행되는 코드
- 단순히 SQL 문을 저장해놓은 것일 뿐인 저장 프로시저와는 달리, 트리거는 테이블과 묶여서 동작함
- Orders 테이블의 INSERT 작업에 정의한 트리거는 Orders 테이블에 새로운 행을 삽입할 때만 수행되고, Customers 테이블의 INSERT나 UPDATE 작업에 정의한 트리거는 Customers 테이블에서 지정한 작업이 일어날 때만 수행됨
- 트리거는 다음과 같은 데이터에 접근할 수 있음
  - INSERT 작업으로 추가된 데이터
  - UPDATE 작업으로 처리한 이전 데이터와 새로운 데이터
  - DELETE 작업으로 삭제한 데이터 
- 트리거는 지정한 작업이 수행되기 전 또는 후에 수행되는데, 이는 DBMS에 따라 다름
- 트리거의 일반적인 용도는 다음과 같음
  - 데이터 일관성 보장
  - 테이블의 변화를 감지하여 특정한 작업을 수행
  - 추가적인 데이터 유효성 검사나 데이터 롤백 수행
  - 다른 열들의 값을 기초로 어떠한 계산을 하거나 타임스탬프를 갱신
~~~SQL
CREATE TRIGGER customer_state
AFTER INSERT OR UPDATE
FOR EACH NOW
BEGIN
UPDATE Customers
SET cust_state = Upper(cust_state)
WHERE Customers.cust_id = :OLD.cust_id
END;
~~~
- 제약 조건이 트리거보다 빠르기 때문에, 가능하다면 제약 조건을 사용하길 바람

### 데이터베이스 보안
- 보안이 적용되어야 할 작업은 일반적으로 다음과 같음
  - 테이블 생성, 변경, 삭제와 같은 DB 관리 기능에 대한 접근
  - 특정 DB나 테이블에 대한 접근
  - '읽기 전용', '특정 열에만 접근'과 같은 접근 유형
  - 뷰나 저장 프로시저를 통해서만 접근할 수 있는 테이블 지정 
  - 로그인한 계정에 따라 접근과 제어 권한을 다양하게 부여하는 다단계 보안 레벨 생성
  - 사용자 계정 관리 권한
- 보안은 `SQL GRANT`나 `REVOKE` 문으로 관리할 수 있는데, 대부분의 DBMS가 대화형 관리자 유틸리티를 제공함

## 부록 D - SQL 데이터형 사용하기
- 데이터형은 내부적으로 저장 공간을 효율적으로 사용할 수 있게 해줌
- 숫자나 날짜 값은 문자열보다 압축된 형태로 데이터를 저장함
- 데이터형은 정렬 순서를 지정할 수 있게 해주는데, <b>모든 값이 문자열로 처리된다면, 1은 10 이전에 오고, 10은 2 이전에 옴</b>

### 문자열 데이터형
- 문자열 데이터형에는 기본적으로 두 가지(고정 길이 문자열, 가변 길이 문자열)이 있음
- 고정 길이 문자열은 정해진 길이의 문자열만 허용
- 예를 들어 이름 열에는 30개의 문자를, 주민등록번호에는 13개의 문자를 허용할 수 있음
- 이 열은 지정한 길이만큼 공간을 할당함
- 가변 길이 문자열은 다양한 길이의 문자열을 지정함(최댓값은 데이터형과 DBMS에 따라 다름)
- 고정 길이 문자열을 사용하면 훨씬 빨리 정렬하고 조작할 수 있음
- 또한 많은 DBMS가 가변형 열은 인덱스를 만들 수 없게 함
- CHAR: 1~255 길이의 문자열을 저장할 수 있는 고정 길이 문자열
- NCHAR: 멀티바이트나 유니코드 문자를 지원하기 위해 고안된 특별한 형태의 고정 길이 문자열
- TEXT(LONG, MEMO, VARCHAR): 가변 길이 문자열
- CHAR, VARCHAR는 영어는 1바이트, 한글은 2바이트로 계산함

### 수치 데이터형
- 수치 데이텨형은 숫자를 저장하는데, DBMS는 여러 수치 데이터형을 지원하는데, 저장할 수 있는 데이터의 범위가 각각 다름
- BIT: 0,1
- DECIMAL(NUMERIC): 고정 정밀도를 가진 값
- FLOAT(NUMBER): 부동 소수점 값
- INT(INTEGER): 4바이트의 정숫값
- REAL: 4바이트 부동 소수점 값
- SMALLINT: 2바이트 정숫값

### 날짜와 시간 데이터형
- DATE: 날짜
- DATETIME(TIMESTAMP): 날짜와 시간
- SMALLDATETIME: 날짜와 시간
- TIME: 시간