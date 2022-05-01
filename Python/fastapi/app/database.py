# 데이터베이스 설정을 위한 파일.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. create_engine 함수를 사용해 DB 연결할 엔진 생성
engine = create_engine("mysql+pymysql://admin:1234@0.0.0.0:3306/dev")

# 2. sessionmaker 함수를 이용해 세션 생성
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# 3. declarative_base 함수는 모델 정의를 위한 부모 클래스 생성
Base = declarative_base()
