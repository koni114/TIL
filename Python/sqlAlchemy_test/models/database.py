import os
import cx_Oracle

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from libs.util.config import config
from models.db_utils import get_sqlalchemy_db_url
from libs.util.logger import get_logger, INFO, WARNING, ERROR, MORE, DETAIL

logger = get_logger()

cx_Oracle.init_oracle_client("/Volumes/instantclient-basic-macos.x64-19.8.0.0.0dbru")

SQLALCHEMY_DATABASE_URL = get_sqlalchemy_db_url()

engine = create_engine(name_or_url=SQLALCHEMY_DATABASE_URL,
                       arraysize=1000,
                       echo=False,
                       pool_size=10,
                       max_overflow=3)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

DMBase = declarative_base()


def get_am_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_all(base: declarative_base=DMBase, db_engine=engine):
    """
        base 테이블 초기화(생성)

    :param base:
    :param db_engine:
    :return:
    """
    base.metadata.create_all(bind=db_engine)


class DBSession:
    """
        함수 내에서 사용하는 db engine session(with 사용)
    """
    def __enter__(self):
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
