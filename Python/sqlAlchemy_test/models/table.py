# DB 모델 정의
from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime
from models.database import DMBase


class Customers(DMBase):
    __tablename__ = "CUSTOMERS"

    cust_id = Column(String(10), primary_key=True, nullable=False)
    cust_name = Column(String(50), nullable=False)
    cust_address = Column(String(50), nullable=True)
    cust_city = Column(String(50), nullable=True)
    cust_state = Column(String(5), nullable=True)
    cust_zip = Column(String(10), nullable=True)
    cust_country = Column(String(50), default=True)
    cust_contact = Column(String(50), default=True)
    cust_email = Column(String(255), default=True)

    @staticmethod
    def col_names():
        return ["cust_id", "cust_name", "cust_address", "cust_city"
                "cust_state", "cust_zip", "cust_country", "cust_contact", "cust_email"]


class OrderItems(DMBase):
    __tablename__ = "ORDERITEMS"

    order_num = Column(Integer, primary_key=True, nullable=False)
    order_item = Column(Integer, primary_key=True, nullable=False)
    prod_id = Column(String(10), nullable=False)
    quantity = Column(Integer, nullable=False)
    item_price = Column(Float, nullable=False)

    @staticmethod
    def col_names():
        return ["order_num", "order_item", "prod_id", "quantity", "item_price"]


class Orders(DMBase):
    __tablename__ = "ORDERS"

    order_num = Column(Integer, primary_key=True, nullable=False)
    order_date = Column(DateTime, nullable=False)
    cust_id = Column(String(10), nullable=False)

    @staticmethod
    def col_names():
        return ["order_num", "order_date", "cust_id"]


class Products(DMBase):
    __tablename__ = "PRODUCTS"

    prod_id = Column(String(10), primary_key=True, nullable=False)
    vend_id = Column(String(10), nullable=False)
    prod_name = Column(String(255), nullable=False)
    prod_price = Column(Float, nullable=False)
    prod_desc = Column(String(1000), nullable=True)

    @staticmethod
    def col_names():
        return ["prod_id", "vend_id", "prod_name", "prod_price", "prod_desc"]


class Vendors(DMBase):
    __tablename__ = "VENDORS"

    vend_id = Column(String(10), primary_key=True, nullable=False)
    vend_name = Column(String(50), nullable=False)
    vend_address = Column(String(50), nullable=True)
    vend_city = Column(String(50), nullable=True)
    vend_state = Column(String(5), nullable=True)
    vend_zip = Column(String(10), nullable=True)
    vend_country = Column(String(50), nullable=True)

    @staticmethod
    def col_names():
        return ["vend_id", "vend_name", "vend_address", "vend_city", "vend_state",
                "vend_zip", "vend_country"]

