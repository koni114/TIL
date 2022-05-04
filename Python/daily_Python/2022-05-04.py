# sqlAlchemy 사용법 정리
# sqlAlchemy -> ORM(Object Relational Mapping) 을 구현해주는 라이브러리

# 예제 수행을 위해 mysql 패키지도 설치

# database 연결을 위한 스크립트 작성

import sqlalchemy as db
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 데이터베이스 연결
# 코어의 엔진으로 연결 --> 추상화를 통해(Pool) DBAPI 사용가능해짐
engine = db.create_engine('mysql+pymysql://admin:1234@localhost/study_db')
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=False, bind=engine))

# Mapping 매핑
# 데이터베이스의 구조와 코드를 연결
# 데이터베이스에 user 라는 테이블이 존재하면 코드 상에도 이 테이블과 정상적으로 연결 될 수 있도록 user table 을 코드로 구현
# 잘못 매핑하거나 매핑이 되어 있지 않은 경우에는 코드 상에서 변경 된 내용을 데이터베이스에 적용할 떄 문제가 발생함.

# ORM에서 매핑하는 법은 2가지가 있음
# - ORM에게 다룰 테이블을 알려주는 방법
# - 데이터베이스의 테이블에 매핑될 테이블 클래스를 코드로 구현하는 방법
# --> SQLAlchemy 는 2가지 방법을 하나로 묶어서 작업할 수 있게 함

Base = declarative_base()
Base.query = db_session.query_property()

# 테이블 생성
# DB 연결과 SQLAlchemy 의 Base 를 만든 후에 테이블 클래스를 만들어주면 됨

from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)


# 스키마 생성
# 테이블 설정을 완료하면 스키마를 생성
# 메타데이터를 보관하고 있는 Base 를 이용해 스키마를 간단하게 생성해줄 수 있음
u = User('admin', 'admin@localhost')
Base.query = db_session.query_property()
Base.metadata.create_all(bind=engine)

db_session.add(u)
