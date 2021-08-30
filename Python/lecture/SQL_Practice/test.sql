-- 1. distinct는 부분적으로 적용할 수 없음
SELECT DISTINCT vend_id
FROM Products
WHERE ROWNUM <= 10

-- 2. postgreSQL, MySQL은 LIMIT을 사용.
--    이 때 내가 원하는 행에서부터 LIMIT을 적용하려면 OFFSET 작성
-- 5행에서 부터 5개 추출
SELECT prod_name
FROM Products
LIMIT 5 OFFSET 5;

-- 데이터 정렬 : ORDER BY
-- DBMS 의 기본값인 사전 정렬 순서에서는 A, a를 구분하지 않음
SELECT prod_name
FROM Products
ORDER BY prod_name;

-- 고급 데이터 필터링
-- WHERE 절에 and, or 사용 가능
-- IN 연산자 보다는 or 가 더 빠름
-- IN 연산자의 가장 큰 장점은 뒤에 SELECT 문 사용 가능
-- NOT 연산자를 WHERE 절 뒤에 사용

SELECT prod_name, vend_id
FROM Products
WHERE NOT vend_id = 'DLL01'
ORDER BY prod_name;

SELECT prod_id, prod_price, prod_name
FROM products
WHERE vend_id NOT IN ('DLL01', 'BRS01')
ORDER BY prod_name;

SELECT TRIM(vend_name) || '(' || TRIM(vend_country) || ')'
FROM vendors
ORDER BY vend_name;

SELECT prod_id,
       quantity,
       item_price,
       quantity * item_price AS expended_price
FROM OrderItems
WHERE order_num = 20008;

SELECT 2 * 3
FROM dual;

SELECT TRIM ('  abc  ')
FROM dual;

SELECT cust_name, cust_contact
FROM Customers C, Orders O, OrdersItems OI
WHERE C.cust_id = O.cust_id
    AND OI.order_num = O.order_num
    AND prod_id = 'RGAN01';


CREATE PROCEDURE MailingListCount(
    ListCount OUT INTEGER
)
IS
v_rows INTEGER;

DELETE FROM Orders
ROLLBACK;

SET TRANSACTION
DELETE OrderItems WHERE order_num = 12345;
DELETE Orders WHERE order_num = 12345
COMMIT;



