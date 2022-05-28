# DB 모델 정의
from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime
from models.database import DMBase


class Customers(DMBase):
    __tablename__ = "Customers"

    cust_id = Column(String(10), primary_key=True, nullable=False)
    cust_name = Column(String(50), nullable=False)
    cust_address = Column(String(50), nullable=True)
    cust_city = Column(String(50), nullable=True)
    cust_state = Column(String(5), nullable=True)
    cust_zip = Column(String(10), nullable=True)
    cust_country = Column(String(50), default=True)
    cust_contact = Column(String(50), default=True)
    cust_email = Column(String(255), default=True)


class OrderItems(DMBase):
    __tablename__ = "OrderItems"

    order_num = Column(Integer, primary_key=True, nullable=False)
    order_item = Column(Integer, primary_key=True, nullable=False)
    prod_id = Column(String(10), nullable=False)
    quantity = Column(Integer, nullable=False)
    item_price = Column(Float, nullable=False)


class Orders(DMBase):
    __tablename__ = "Orders"

    order_num = Column(Integer, primary_key=True, nullable=False)
    order_date = Column(DateTime, nullable=False)
    cust_id = Column(String(10), nullable=False)


class Products(DMBase):
    __tablename__ = "Products"

    prod_id = Column(String(10), primary_key=True, nullable=False)
    vend_id = Column(String(10), nullable=False)
    prod_name = Column(String(255), nullable=False)
    prod_price = Column(Float, nullable=False)
    prod_desc = Column(String(1000), nullable=True)


class Vendors(DMBase):
    __tablename__ = "Vendors"

    vend_id = Column(String(10), primary_key=True, nullable=False)
    vend_name = Column(String(50), nullable=False)
    vend_address = Column(String(50), nullable=True)
    vend_city = Column(String(50), nullable=True)
    vend_state = Column(String(5), nullable=True)
    vend_zip = Column(String(10), nullable=True)
    vend_country = Column(String(50), nullable=True)

