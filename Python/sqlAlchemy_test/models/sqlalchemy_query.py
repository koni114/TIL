import os
import pandas as pd
import numpy as np

from models.table import Customers, Vendors, Products, Orders, OrderItems
from models.database import DBSession, engine
from sqlalchemy import func, desc
from sqlalchemy.sql import label

"""
SELECT DISTINCT vend_id
FROM Products
WHERE ROWNUM <= 10;
"""
result_list = []
with DBSession() as db:
    query = db.query(Products).distinct(Products.vend_id).limit(10)

df = pd.read_sql(query.statement, engine)


"""
SELECT prod_id, prod_price, prod_name, vend_id
FROM products
WHERE vend_id NOT IN ('DLL01', 'BRS01')
ORDER BY prod_name;
"""
pd.set_option("display.max_columns", 100)

with DBSession() as db:
    query = db.query(Products.prod_id,
                     Products.prod_price,
                     func.trim(Products.prod_name),
                     func.trim(Products.vend_id)
                     )\
             .filter(~func.trim(Products.vend_id).in_(['DLL01', 'BRS01'])) \
             .order_by(Products.prod_name)

df = pd.read_sql(query.statement, engine)

"""
SELECT B.PROD_NAME
FROM (SELECT ROWNUM rn, PRODUCTS.*
      FROM PRODUCTS
) B
WHERE rn >= 6 AND rn <= 10;
"""
with DBSession() as db:
    query = db.query(func.trim(Products.prod_name).label("prod_name")
                     ) \
        .limit(5) \
        .offset(5)

df = pd.read_sql(query.statement, engine)
print(df)

"""
SELECT prod_id, prod_name
FROM Products
WHERE prod_name LIKE 'Fish%' 
"""
with DBSession() as db:
    query = db.query(func.trim(Products.prod_id).label("prod_id"),
                     func.trim(Products.prod_name).label("prod_name")
                     ) \
        .filter(Products.prod_name.like("Fish%"))

df = pd.read_sql(query.statement, engine)
print(df)

"""
SELECT prod_id,
       quantity,
       item_price,
       quantity * item_price AS expanded_price
FROM OrderItems
WHERE order_num = 20008;
"""
with DBSession() as db:
    query = db.query(func.trim(OrderItems.prod_id).label("prod_id"),
                     func.trim(OrderItems.quantity).label("quantity"),
                     func.trim(OrderItems.item_price).label("item_price"),
                     label("expanded_price", OrderItems.quantity * OrderItems.item_price)
                     ) \
        .filter(OrderItems.order_num == 20008)
df = pd.read_sql(query.statement, engine)
print(df)

"""
SELECT AVG(prod_price) AS avg_price
FROM Products
WHERE vend_id = 'DLL01';
"""
with DBSession() as db:
    query = db.query(func.avg(Products.prod_price).label("avg_price")
                     ) \
        .filter(func.trim(Products.vend_id) == 'DLL01')
df = pd.read_sql(query.statement, engine)
print(df)

"""
SELECT cust_id, COUNT(*) AS orders
FROM Orders
GROUP BY cust_id
HAVING COUNT(*) >= 2;
"""

with DBSession() as db:
    query = db.query(Orders.cust_id,
                     func.count(Orders.cust_id).label("orders")
                     ) \
        .group_by(Orders.cust_id) \
        .having(func.count(Orders.cust_id) >= 2)
df = pd.read_sql(query.statement, engine)
print(df)

"""
SELECT cust_id, order_date
FROM Orders
WHERE order_num IN (SELECT order_num
                    FROM orderItems
                    WHERE prod_id = 'BR01');
"""
with DBSession() as db:
    subquery = db.query(OrderItems.order_num) \
                 .filter(func.trim(OrderItems.prod_id) == "BR01")

    query = db.query(func.trim(Orders.cust_id).label("cust_id"),
                     func.trim(Orders.order_date).label("order_date")) \
              .filter(Orders.order_num.in_(subquery))

df = pd.read_sql(query.statement, engine)
print(df)

"""
SELECT cust_id, (SELECT COUNT(*)
                 FROM Orders
                 WHERE Customers.cust_id = Orders.cust_id) AS total_ordered
FROM Customers
ORDER BY total_ordered DESC;
"""

with DBSession() as db:
    subquery = db.query(func.count(1).label("count")) \
                 .filter(Customers.cust_id == Orders.cust_id)

    query = db.query(Customers.cust_id,
                     subquery.label("total_ordered")) \
              .order_by(desc("total_ordered"))

df = pd.read_sql(query.statement, engine)
print(df)

"""
SELECT TRIM(vend_name), TRIM(prod_name), prod_price
FROM Vendors, Products
WHERE Vendors.vend_id = Products.vend_id;
"""

with DBSession() as db:
    query = db.query(func.trim(Vendors.vend_name).label("Vendors"),
                     func.trim(Products.prod_name).label("prod_name"),
                     Products.prod_price) \
        .filter(Vendors.vend_id == Products.vend_id)

df = pd.read_sql(query.statement, engine)
print(df)

"""
SELECT cust_name, order_num
FROM Customers LEFT OUTER JOIN Orders
ON Customers.cust_id = Orders.cust_id
ORDER BY cust_name;
"""

with DBSession() as db:
    query = db.query(func.trim(Customers.cust_name).label("cust_name"),
                     func.trim(Orders.order_num).label("order_num")) \
              .outerjoin(Orders, Customers.cust_id == Orders.cust_id) \
              .order_by(Customers.cust_name)

df = pd.read_sql(query.statement, engine)
print(df)

"""
SELECT TRIM(prod_name), COUNT(prod_name) AS orders
FROM Products LEFT OUTER JOIN OrderItems
ON Products.prod_id = OrderItems.prod_id
GROUP BY prod_name
ORDER BY prod_name
"""

with DBSession() as db:
    query = db.query(func.trim(Products.prod_name).label("prod_name"),
                     func.count(Products.prod_name).label("orders")) \
        .outerjoin(OrderItems, Products.prod_id == OrderItems.prod_id) \
        .group_by(Products.prod_name) \
        .order_by(Products.prod_name)

df = pd.read_sql(query.statement, engine)
print(df)

"""
SELECT cust_name, cust_contact, cust_email
FROM Customers
WHERE cust_state IN ('IL', 'IN', 'MI')
UNION
SELECT cust_name, cust_contact, cust_email
FROM Customers
WHERE cust_name = 'Fun4All';
"""

with DBSession() as db:
    subquery_1 = db.query(func.trim(Customers.cust_name).label("cust_name"),
                          func.trim(Customers.cust_contact).label("cust_contact"),
                          func.trim(Customers.cust_email).label("cust_email")) \
                   .filter(func.trim(Customers.cust_state).in_(['IL', 'IN', 'MI']))

    subquery_2 = db.query(func.trim(Customers.cust_name).label("cust_name"),
                          func.trim(Customers.cust_contact).label("cust_contact"),
                          func.trim(Customers.cust_email).label("cust_email")) \
                   .filter(func.trim(Customers.cust_name) == "Fun4All")

    query = subquery_1.union(subquery_2)

df = pd.read_sql(query.statement, engine)
print(df)

"""
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
"""
df = pd.DataFrame([[1000000006, 'Toy Land', '123 Any Street', 'New York','NY',
                   '11111', 'USA']], columns=["cust_id",
                                             "cust_name",
                                             "cust_address",
                                             "cust_city",
                                             "cust_state",
                                             "cust_zip",
                                             "cust_country"])

df.to_sql('customers', engine, schema="testuser", if_exists="append", index=False)

