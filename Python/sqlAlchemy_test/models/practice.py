import cx_Oracle
import os
from sqlalchemy import create_engine

cx_Oracle.init_oracle_client("/Volumes/instantclient-basic-macos.x64-19.8.0.0.0dbru")



engine = create_engine(
    cstr,
    convert_unicode=False,
    pool_recycle=10,
    pool_size=50,
    echo=True
)

result = engine.execute('select * from Customers')
