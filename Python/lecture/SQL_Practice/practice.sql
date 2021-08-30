-- chapter 02
-- 1.
SELECT cust_id
FROM Customers

-- 2.
SELECT DISTINCT prod_id
FROM OrderItems

-- 3.
SELECT *
FROM Customers;


SELECT cust_id
FROM Customers;

-- chapter 06
-- 1.
SELECT vend_name
FROM Vendors
WHERE vend_country = 'USA' AND vend_state = 'CA'

-- 2.
SELECT order_num, prod_id, quantity
FROM OrderItems
WHERE (prod_id = 'BR01' AND quantity >= 100) OR (prod_id = 'BR02' AND quantity >= 100) OR (prod_id = 'BR03' AND quantity >= 100)

-- 3.
SELECT prod_name, prod_price
FROM Products
WHERE prod_price >= 3 AND prod_price <= 6;

-- 4.
SELECT vend_name
FROM Vendors
WHERE vend

-- chapter 07
-- 1.
SELECT prod_name, prod_desc
FROM Products
WHERE prod_desc LIKE '%toy%'

-- 2.
SELECT prod_name, prod_desc
FROM Products
WHERE prod_desc NOT LIKE '%toy%'
ORDER BY prod_name

-- 3.
SELECT prod_name, prod_desc
FROM Products
WHERE prod_desc LIKE '%toy%' AND prod_desc LIKE '%carrots%'

-- 4.
SELECT prod_name, prod_desc
FROM Products
WHERE prod_desc LIKE '%toy%carrots%'

-- chapter08
-- 1
SELECT vend_id, vend_name AS vname, vend_address AS vaddress, vend_city AS vcity
FROM Vendors
ORDER BY vname;

SELECT prod_id, prod_price, sale_price * 0.9 AS sale_price
FROM Products

-- chapter09
-- 1
SUM(quantity) as sum_quantity
FROM OrdersItems

-- 2
SUM(quantity) as sum_quantity
FROM OrdersItems
prod_id = 'BR01'

-- chapter10
SELECT prod_id, COUNT(*) AS order_lines
FROM OrderItems
GROUP BY prod_id
ORDER BY order_lines

SELECT vend_id, MIN(prod_price) AS cheapest_item
FROM Products
GROUP BY vend_id
ORDER BY prod_price

SELECT order_num
FROM OrdersItems
GROUP BY order_num
HAVING SUM(quantity) >= 100
ORDER BY order_num


SELECT order_num, SUM(item_price * quantity) AS total_price
FROM OrderItems
GROUP BY order_num
HAVING SUM(item_price * quantity) >= 1000
ORDER BY order_num;

-- chapter11
-- 1.
SELECT order_num
FROM OrderItems

SELECT cust_id, (SELECT COUNT(*)
                 FROM Orders
                 WHERE Customers.cust_id = Orders.cust_id) AS total_ordered
FROM Customers
ORDER BY total_ordered DESC;



