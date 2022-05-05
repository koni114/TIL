"""
sqlAlchemy 사용법 정리
- python 에서 사용 가능한 ORM(Object-relational mapping)
- 말 그대로, Object 와 relation(테이블) 을 매핑시켜주는 역할을 수행

장점
- 객체 지향적인 코드로 비즈니스 로직에 집중 가능
- 재사용 및 유지보수 편리성이 증가
- DBMS에 대한 종속성이 줄어듬.

단점
- ORM 만으로 서비스를 구현하기 어려움
- 프로시저가 많은 시스템에서는 장점을 가져가기 어려움
"""

# MySQL DB

# database 연결을 위한 스크립트 작성


import sqlalchemy as db
from sqlalchemy.orm import scoped_session, sessionmaker, aliased
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# 1. 데이터베이스 연결
# 코어의 엔진으로 연결 --> 추상화를 통해(Pool) DBAPI 사용가능해짐
# create_engine 함수 안의 parameter 로 원하는 DB의 접속정보 입력.
# 이는 DB 종류에 따라서 달라지므로, sqlAlchemy 문서 참고!
engine = db.create_engine('mysql+pymysql://admin:1234@localhost/study_db')

# 2. session 생성
# --> sessionmaker
# --> 생성한 DB에 데이터 처리를 하기 위하여 생성
# --> session 은 내부적으로 Map 구조이기 때문에 세션의 반환값은 기존에 집어넣은 인스턴스 구조와 동일
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# declarative_base() 는 선언 클래스 정의에 대한 기본 클래스를 작성하는 팩토리 함수
Base = declarative_base()
Base.query = db_session.query_property()

# 3. 테이블 매핑을 위한 클래스 생성
# DB 연결과 SQLAlchemy 의 Base 를 만든 후에 Base 를 상속받는 테이블 클래스를 만들어주면 됨

# __tablename__ --> 정의한 테이블에 매핑하기 위한 테이블 명
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"

# 4. query 날리기
u = User('admin', 'admin@localhost')
db_session.add(u)   # 위의 생성한 인스턴스(u) 를 세션의 함수인 add 로 넘김
db_session.commit()

# 필터로 쿼리문을 날려 결과를 얻어낼 수 있음
out_user = db_session.query(User).filter_by(name='admin').first()
out_user2 = db_session.query(User).order_by(User.id)
out_user3 = db_session.query(User, User.name).all()
for user in db_session.query(User). \
                filter(User.name == "admin") . \
                filter(User.email == "admin@localhost"):
    print(user)

# 잘 입력이 됐는지 확인하고 싶다면, session.query(User).all() 과 같이 불러와 확인
result = db_session.query(User).all()
for row in result:
    print(f"name --> {row.name}, email --> {row.email}")

# 새로 추가한 데이터는 session.new 로 알 수 있음
print(db_session.new)

# 수정은 객체 접근하여 변경해주면 됨
u.name = "admin2"
print(u)

"""
.add 를 했어도 실제로 db에 추가된 것이 아니라, pending 된(계류된) 상태. 실제로 넣을 때는 flush 라는 과정을 통해 입력됨
DB에 쿼리를 하면 pending data 는 flush 되어 접근가능한 상태지만 실제로 저장된 것은 아님
"""

# rollback
# 변경하기 이전의 단계로 돌아감
db_session.rollback()


