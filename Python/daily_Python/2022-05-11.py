"""
cx_Oracle + sqlAlchemy 를 통한 AlDBSession 객체 생성해보기
- create_engine : connection 엔진 생성
- sessionmaker  : 세션 생성
- AIDBSession   : 함수 내에서 사용하는 db engine session(with 사용을 위하여 __enter__, __exit__)
"""

import os
import cx_Oracle

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

DMBase = declarative_base()


def get_am_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def create_all(base: declarative_base = DMBase, db_engine=engine):
    """
    base 테이블 초기화(생성)
    :param base:
    :param db_engine:
    :return:
    """
    base.metadata.create_all(bind=db_engine)


class AIDBSession:
    """
    함수 내에서 사용하는 db engine session(with 사용)
    """
    def __enter__(self):
        self.db = session_local()
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()



