"""
sqlAlchemy 와 cx_Oracle 성능 비교하기
"""

import os
import time
import pandas as pd

from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "oracle+cx_oracle://scott:tiger@hostname:port/?service_name=myservice&encoding=UTF-8&nencoding=UTF-8"

engine = create_engine(url=SQLALCHEMY_DATABASE_URI,
                       arraysize=1000,
                       echo=False,
                       pool_size=2,
                       max_overflow=3
                       )


session_local = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


class AlDBSession:
    """
    함수 내에서 사용하는 db engine session(with 사용)
    """
    def __enter__(self):
        self.db = session_local()
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


# sqlAlchemy


# sqlAlchemy 를 통한 쿼리 생성
start_time = time.time()
with AlDBSession() as db:
    result = db.query().where().all()
print(f"oracle --> {round(time.time() - start_time, 4)}s")

# cx_Oracle 를 통한 쿼리 생성
start_time = time.time()
query = """
    SELECT *
    FROM table
    WHERE var_id = 'C4109'
"""

connector = 'oracle'
conn = ""
df = pd.read_sql(query, conn)





