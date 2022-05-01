# Pydantic 모델을 정의한 파일
# SQLAlchemy 와 Pydantic 모두  "모델"이라는 용어를 사용
# 그래서 이 둘을 같이 사용할 경우 용어를 정의해야 하는데, FastAPI 공식 문서에는
# pydantic "model" 을 schema 로 표현하여 문제를 해결

from pydantic import BaseModel


class UserCase(BaseModel):
    email: str


class UserCreate(UserCase):
    password: str


class User(UserCase):
    id: int
    email: str
    is_active: bool

    class Config:
        orm_mode = True

