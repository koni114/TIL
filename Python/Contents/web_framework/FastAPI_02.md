# FastAPI 
## 1. 도커 사용하기
- mysql 설치를 위한 도커 이미지 설치
~~~shell
$ docker run -d -p 80:80 docker/getting-started

# docker 가 잘 설치되었는지 확인
$ docker ps
$ docker container ls

# MySQL 이미지를 받아 호스트에서 설치 없이 사용하기
$ docker run --name fastapi-mysql -e MYSQL_ROOT_PASSWORD=1234 -d mysql:8.0 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

# MySQL 설치가 잘 되었는지 확인
$ docker exec -it fastapi-mysql mysql -uroot -p
~~~

## 2. RDB 연동
- 데이터를 저장할 때 가장 많이 사용하는 시스템이 DBMS임. 특히 전통적으로 RDB를 많이 사용하고 있음
- 요새는 백엔드에서 DB에 쿼리 실행시, ORM(Object Relation Mapper)이란 일종의 중계 프로그램을 많이 사용함
- 말 그대로 object와 relation(table)를 매핑해주는 프로그램
- 파이썬에서 가장 유명한 ORM 중 하나인 `SQLAlchemy`를 이용해 mySQL 연결

### 파일 나누기
- 이번 예시 실행을 위해 파일을 나눠서 진행
  - `main.py`
  - `database.py` : SQLAlchemy 설정
  - `models.py` : SQLchemy Models
  - `schemas.py` : Pydantic Models
~~~
app
├── database.py
├── main.py
├── schemas.py
└── models.py
~~~
### database.py
- 데이터베이스 설정을 위한 파일
~~~python
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
~~~
- 위의 코드를 간략히 설명하자면,
  - `create_engine` 함수를 이용해 DB 연결할 엔진 생성
  - `sessionmaker` 함수를 이용해 세션 생성
  - `declarative_base` 함수는 모델 정의를 위한 부모 클래스 생성
- 파이썬에는 MySQL연결을 위한 드라이버가 여러 존재하는데 그 중 `PyMySQL` 을 사용
~~~shell
$ pip install PyMySQL
~~~

### models.py
- DB 모델은 다음과 같이 정의
~~~python
# DB 모델 정의
from sqlalchemy import Boolean, Column, Integer, String
from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_active = Column(Boolean, default=True)
~~~

### schemas.py
- Pydantic 모델을 정의한 파일
- SQLAlchemy 와 Pydantic 모두  "모델"이라는 용어를 사용
- 그래서 이 둘을 같이 사용할 경우 용어를 정의해야 하는데, FastAPI 공식 문서에는
- pydantic "model" 을 schema 로 표현하여 문제를 해결
~~~python
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
~~~

### main.py
- FastAPI를 실행할 메인 파일
~~~python
import uvicorn
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existed_user = db.query(models.User).filter_by(email=user.email).first()

    if existed_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(email=user.email, password=user.password)
    db.add(user)
    db.commit()

    return user


@app.get("/users", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
~~~
- DB 연동은 여러 방법이 있지만, 의존성 주입을 이용해 연결함. http://localhost:8000 에서 확인해보면 정상 작동하는 것을 확인할 수 있음

## 2. Form 데이터
- Form 은 HTML 태그 중 하나. 대개 어떤 정보를 입력받는 Form에 대한 컴포넌트를 랜더링하기 위해 쓰임
- 그 전에 간단히 정적 파일들을 제공하는 방법을 보자

### 정적 파일
- 보통 웹에서 정적 파일이라고 하면 단순 이미지 뿐만 아니라 html, js, css 를 포함함
- 브라우저는 서버에 요청을 하고, 정적 파일들을 다운로드 함
- FastAPI는 API에 특화되어 있지만, 당연히 정적 파일도 지원을 함
- 먼저 `static`이라는 폴더를 생성한 뒤 `login.html`을 넣어줌.
~~~html
<form method="post" action="http://localhost:8000/login">
  <input type="text" name="username" placeholder="Username" required="required" />
  <input type="password" name="password" placeholder="Password" required="required" />
  <button type="submit" class="btn btn-primary btn-block btn-large">Let me in.</button>
</form>
~~~
- input 태그에서 `name` 의 값이 `form` 매개변수가 됨
~~~python
from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
~~~
- `app.amount()` 함수 다른 WSGI 또는 ASGI 앱을 마운트 가능케 하는 함수임  
  다만, 여기서는 `StaticFiles` 를 이용해 정적 앱을 만들었다고 생각하면 됨

### 주의: 미디어 타입
- 폼의 경우 미디어 타입은 `application/x-www-form-urlencoded` 임  
  하지만, 파일의 경우 폼을 정말 많이 사용하는데, 이 때는 타입을 `multipart/form-data`로 반드시 작성해주어야 함. 

### 주의: Body는 쓰지 못함 
- JSON 형식을 받을 수 없음. 앞에서 말했듯이 미디어 타입이 `application/json`이 아니기 때문. 이건 FastAPI 문제가 아닌 HTTP 스펙임

## 3. 파일 처리
- 파일 업로드는 정말 자주 쓰이는 기능 중 하나. FsatAPI 에서는 쉽게 처리가 가능
- 우선 아래 패키지를 설치
~~~python
$ pip install python-multipart
~~~

### 바이트 스트림으로 받기
~~~python
from fastapi import FastAPI, File

app = FastAPI()


@app.post("/file/size")
def get_filesize(file: bytes = File(...)):
    return {"file_size": len(file)}
~~~
- `File` 클래스만 선언해주면 됨. 대신 `bytes` 라고 바이트열임을 명시 해주면 됨  
  이렇게 할 경우는 다양한 파일 정보를 받을 수가 없음
  
### UploadFile 이용하기
~~~python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/file/info")
def get_file_info(file: UploadFile = File(...)):
    return {
        "content_type": file.content_type,
        "filename": file.filename
    }
~~~
- 위와 같이 `UploadFile` 에는 다양한 정보가 있는데, 재밌는 것은 기존 IO와 같은 메소드를 비동기로 지원
- 그러므로 아래와 같은 메소드를 지원합니다.
  - write
  - read
  - seek
  - close
- 다만, 비동기 메소드들이므로 반드시 `await` 키워드와 함께 써야합니다. 그렇지 않으면 `UploadFile.file` 객체를 이용하면 됩니다. 
- 흔히 말하는 file-like 객체. 다음과 같이 사용할 수 있고 주의할 점은 함수 앞에 `async` 키워드가 붙는다는 걸 명심하셔야 합니다. 
~~~python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/file/info")
async def get_file_info(file: UploadFile = File(...)):
    file_like_obj = file.file
    contents = await file.read()

    return {
        "content_type": file.content_type,
        "filename": file.filename,
    }
~~~
- 비동기를 지원하는 것이 FastAPI의 장점. 현재 Django 역시 지원하고 있고, 조만간 Flask2.0 버전이 출시되는데 그때부터 Flask도 비동기 지원 가능

### 파일 저장
- 예전과는 다르게 클라우드 환경이 발달하면서 정적 파일들은 S3와 같은 스토리지 서비스에 저장을 자주 함
- 하지만, 우리는 전통적인 방식으로 업로드한 파일을 서버에 저장하는 시나리오를 수행해보자
~~~python
from tempfile import NamedTemporaryFile
from typing import IO

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


async def save_file(file: IO):
    # s3 업로드라고 생각해 봅시다. delete=True(기본값)이면
    # 현재 함수가 닫히고 파일도 지워집니다.
    with NamedTemporaryFile("wb", delete=False) as tempfile:
        tempfile.write(file.read())
        return tempfile.name


@app.post("/file/store")
async def store_file(file: UploadFile = File(...)):
    path = await save_file(file.file)
    return {"filepath": path} 
~~~

## 4. 에러 처리
- 어떤 프로그래밍 언어를 사용하던 에러는 발생하는데, `try` 문을 사용하는 것도 하나의 방법이지만 좋은 방법은 아님
- 만약 해당 에러가 발생하는 모든 코드에 대해 `try`문을 작성해야 하고, 이는 다시 중복 코드 사용으로 이어짐

### 일부러 에러 내기
- 에러 처리를 본격적으로 다루기 전에 에러를 일부러 발생시켜 봄
~~~python
from fastapi import FastAPI, HTTPException, status

app = FastAPI()


users = {
    1: {"name": "Fast"},
    2: {"name": "Campus"},
    3: {"name": "API"}
}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id not in users.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"<User: {user_id}> is not exists",
        )
    return users[user_id]
~~~
- 위와 같이 `user_id`인 경우 HTTP 404 Not Found 에러를 내어 해당 사용자가 없음을 나타내고 있음
- 초보 개발자들이 많이 하는 실수 중 하나가 바로 에러가 무조건 발생하지 않도록 하는 것. 이는 좋은 방법이 아님
- 대개 프로그램이 죽지 않게 하는 습관 때문인 경우가 많음
- 위의 경우, 해당 사용자가 없음을 브라우저에게 알려줌으로써 명확한 에러를 보여주고, 프로그램이 죽지는 않음
- 서버는 일종의 데몬으로 시스템의 백그라운드에서 동작하며 에러가 발생해도 죽지 않음
- 물론 치명적인 에러라면 얘기는 다름. 그런 경우 보통 `SIGKILL` 인터럽트가 발생하여 죽음

### 사용자 정의 에러
- 대개의 경우 파이썬 표준 에러나 `HTTPException` 등을 이용하기보다는 사용자 정의 에러를 정의함
~~~python
from fastapi import FastAPI

app = FastAPI()


class SomeError(Exception):
    def __init__(self, name: str, code: int):
        self.name = name
        self.code = code

    def __str__(self):
        return f"<{self.name}> is occured. code: <{self.code}>"


app = FastAPI()


@app.get("/error")
async def get_error():
    raise SomeError("Hello", 500)
~~~
- 이렇게 하면 사용자는 어떤 에러인지 정확히 파악하기가 어려움. 그래서 다음과 같이 `SomeError`를 처리할 핸들러를 만들 수 있음
~~~python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


class SomeError(Exception):
    def __init__(self, name: str, code: int):
        self.name = name
        self.code = code

    def __str__(self):
        return f"<{self.name}> is occured. code: <{self.code}>"


app = FastAPI()


# 추가
@app.exception_handler(SomeError)
async def some_error_handler(request: Request, exc: SomeError):
    return JSONResponse(
        content={"message": f"error is {exc.name}"}, status_code=exc.code
    )


@app.get("/error")
async def get_error():
    raise SomeError("Hello", 500)
~~~
- 실행해 보면 그 차이를 확연히 볼 수 있음. 만약 사용자 정의 에러가 HTTP 에러라면 아래처럼 작성할 수도 있음
~~~python
from typing import Any, Optional, Dict

from fastapi import FastAPI, HTTPException


class SomeFastAPIError(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status_code, detail=detail, headers=headers
        )


app = FastAPI()


@app.get("/error")
async def get_error():
    raise SomeFastAPIError(500, "Hello")
~~~
- FastAPI의 기본 에러를 상속 받으면 자동으로 에러 코드와 내용, 그리고 헤더를 예쁘게 응답해줌
- 물론 이 에러도 따로 핸들러에서 처리해주는 방법 역시 가능함.
- 이는 `starlette`의 미들웨어가 `HTTPException`을 처리하고 있기 때문

## 5. 의존성 주입
- FastAPI의 매력적인 기능인 의존성 주입(Dependency Injection)임. 짧게는 DI라고도 함
- 의존성 주입은 코드의 재사용성을 높여주고, 반환받는 객체의 사용은 쉽게 하되 그 생성 과정에 대한 관심을 버리는 것임

### 함수로 만들기
- 무슨 소리인지 코드를 통해 바로 확인해 보자
~~~python
from typing import Any, Optional, Dict

from fastapi import FastAPI, Depends


app = FastAPI()

items = ({"name": "Foo"}, {"name": "Bar"}, {"name": "Baz"})


async def func_params(
    q: Optional[str] = None, offset: int = 0, limit: int = 100
) -> Dict[str, Any]:
    return {"q": q, "offset": offset, "limit": limit}


@app.get("/items/func")
async def get_items_with_func(params: dict = Depends(func_params)):
    response = {}
    if params["q"]:
        response.update({"q": params["q"]})

    result = items[params["offset"]: params["offset"] + params["limit"]]
    response.update({"items": result})

    return response
~~~
- 아이템을 반환하는 API를 하나 만듬. 이 API는 주로 페이징할 때 많이 사용하는 `q`, `offset`, `limit` 매개변수를 가지고 있음
- 페이징은 굉장히 많이 사용하므로 이렇게 함수로 따로 만들어 두고, `Depends` 를 이용하여 호출 할 수 있음

### 클래스로 만들기
~~~python
from typing import Optional

from fastapi import FastAPI, Depends

app = FastAPI()


items = ({"name": "Foo"}, {"name": "Bar"}, {"name": "Baz"})


class ClassParams:
    def __init__(
        self, q: Optional[str] = None, offset: int = 0, limit: int = 100
    ):
        self.q = q
        self.offset = offset
        self.limit = limit


@app.get("/items/class")
async def get_items_with_class(params: ClassParams = Depends(ClassParams)):
    response = {}
    if params.q:
        response.update({"q": params.q})

    result = items[params.offset: params.offset + params.limit]
    response.update({"items": result})

    return response
~~~

### Pydantic으로 만들기
~~~python
from typing import Optional

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field

app = FastAPI()


items = ({"name": "Foo"}, {"name": "Bar"}, {"name": "Baz"})


class PydanticParams(BaseModel):
    q: Optional[str] = Field(None, min_length=2)
    offset: int = Field(0, ge=0)
    limit: int = Field(100, gt=0)


@app.get("/items/pydantic")
async def get_items_with_pydantic(params: PydanticParams = Depends()):
    response = {}
    if params.q:
        response.update({"q": params.q})

    result = items[params.offset: params.offset + params.limit]
    response.update({"items": result})

    return response
~~~

### DI의 DI
~~~python
from typing import Any, Optional, Dict

from fastapi import FastAPI, Depends

app = FastAPI()


items = ({"name": "Foo"}, {"name": "Bar"}, {"name": "Baz"})


async def get_q(q: Optional[str] = None) -> Optional[str]:
    return q


async def func_params_with_sub(
    q: Optional[str] = Depends(get_q), offset: int = 0, limit: int = 100
) -> Dict[str, Any]:
    return {"q": q, "offset": offset, "limit": limit}


@app.get("/items/func/sub")
async def get_items_with_func_sub(
    params: dict = Depends(func_params_with_sub)
):
    response = {}
    if params["q"]:
        response.update({"q": params["q"]})

    result = items[params["offset"]: params["offset"] + params["limit"]]
    response.update({"items": result})

    return response
~~~

### route 데코레이터의 DI
~~~python
from fastapi import FastAPI, Header, Depends, HTTPException

app = FastAPI()


items = ({"name": "Foo"}, {"name": "Bar"}, {"name": "Baz"})


async def verify_token(x_token: str = Header(...)) -> None:
    if len(x_token) < 10:
        raise HTTPException(401, detail="Not authorized")


@app.get("/items", dependencies=[Depends(verify_token)])
async def get_items():
    return items
~~~

## 6. 인증
- 웹 서비스들의 가장 대표적인 기능 중 하나인 인증. 
- 정말 다양한 웹 인증 방식이 존재하고 이름도 비슷해 보임. 
- OAuth, OAuth2, OpenID, OpenID Connect 등 똑같이 생겼지만 사실 다른 방식

### 웹 인증 방식의 변화
- 인증 방법은 지금도 바뀌고 있음
- 일단, 가장 간단하고 오래된 웹 인증을 먼저 보겠음

### HTTP Basic
~~~python
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials


app = FastAPI()
security = HTTPBasic()


@app.get("/users/me")
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}
~~~
- 위 코드는 HTTP 기본 인증(HTTP Basic)을 구현한 예.  
http://localhost:8000/docs 에서 보면 갑자기 없던 자물쇠 모양과 Authorize 버튼이 추가된 모습을 확인할 수 있음.  
클릭하면 Username 과 Password 를 입력하라는 창이 뜸. 이느  HTTPie로도 실행할 수 있음
~~~shell
$ http -v :8000/users/me Authorization:'Basic c3Bpa2U6MTIzNA=='
~~~
- `Authorization` 헤더를 이용하고, `Basic`이라는 단어로 기본 인증을 하겠다고 전달함
- 뒤에 오는 문자열은 `spike:1234`를 base64 인코딩한 결과
- 기본 인증은 이처럼 `username:password`와 같이 작성
- 또는 다음과 같이 할 수도 있지만, 좋은 방법은 아님
~~~shell
$ http -v 'spike:1234@localhost:8000/users/me'
~~~
- `-v` 옵션으로 요청을 확인할 수 있기 때문에 위 두 코드 모두 동일한 요청을 생성함을 알 수 있음
- 이처럼, FastAPI의 `fastapi.security` 모듈과 의존성 삽입(`Depends`)을 이용해 간단하게 인증 시스템을 구현할 수 있음
- 하지만 실제로는 이 인증은 사용하지 않음

### OAuth2
- OAuth2는 현대적인 웹 인증 방식 중 하나
- 웹 개발자라면 반드시 숙지하고 있어야 함
- 물론 OAuth2를 이용한 OpenID Connect도 있지만, OAuth2보다는 많이 퍼지지 않았음
- 사실 OAuth2도 사이트마다 조금씩 차이가 있습니다. 자세한 정보는 구글링을 하시는게 좋으리라 생각함
- 여기서는 다른 걸 전부 생략하고 저희는 생성된 JWT만 확인하는 방법을 보겠습니다. JWT를 이용하기 위해 다음을 설치
~~~shell
$ pip install python-jose bcrypt
~~~
- 물론 `https://jwt.io/` 에서 사용가능한 다른 라이브러리도 찾을 수 있음.  
  추가로 비밀번호 해시를 위해 `bcrypt` 라이브러리도 설치
~~~python
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordRequestForm,
)
from pydantic import BaseModel
from jose import jwt
from jose.exceptions import ExpiredSignatureError


app = FastAPI()
security = HTTPBearer()

ALGORITHM = "HS256"
SECRET_KEY = "e9f17f1273a60019da967cd0648bdf6fd06f216ce03864ade0b51b29fa273d75"
fake_user_db = {
    "fastcampus": {
        "id": 1,
        "username": "fastcampus",
        "email": "fastcampus@fastcampus.com",
        "password": "$2b$12$kEsp4W6Vrm57c24ez4H1R.rdzYrXipAuSUZR.hxbqtYpjPLWbYtwS",
    }
}


class User(BaseModel):
    id: int
    username: str
    email: str


class UserPayload(User):
    exp: datetime


async def create_access_token(data: dict, exp: Optional[timedelta] = None):
    expire = datetime.utcnow() + (exp or timedelta(minutes=30))
    user_info = UserPayload(**data, exp=expire)

    return jwt.encode(user_info.dict(), SECRET_KEY, algorithm=ALGORITHM)


async def get_user(cred: HTTPAuthorizationCredentials = Depends(security)):
    token = cred.credentials
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, ALGORITHM)
    except ExpiredSignatureError:
        raise HTTPException(401, "Expired")
    user_info = User(**decoded_data)

    return fake_user_db[user_info.username]


@app.post("/login")
async def issue_token(data: OAuth2PasswordRequestForm = Depends()):
    user = fake_user_db[data.username]

    if bcrypt.checkpw(data.password.encode(), user["password"].encode()):
        return await create_access_token(user, exp=timedelta(minutes=30))
    raise HTTPException(401)


@app.get("/users/me", response_model=User)
async def get_current_user(user: dict = Depends(get_user)):
    return user
~~~
- 간단하게 JWT를 발급하고, JWT를 이용하여 인증 시스템을 간단히 구현
- 사실, 이 외에도 구글이나 페이스북과 같이 다른 인증 제공 업체를 이용할 수도 있음
- `SECRET_KEY`는 최소 32바이트 문자열이면 됩니다. 다음과 같은 방법으로 생성할 수 있습니다.
~~~shell
$ openssl rand -hex 32
# 또는 파이썬으로 할 수 있습니다
$ python -c "import secrets;print(secrets.token_hex(32))"
~~~
- 32라는 숫자에 유의하세요. 비밀번호는 다음과 같이 생성할 수 있음
~~~python
import bcrypt
password = "password".encode()
# 또는
password = b"password"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
~~~
- 주의: 위에서 사용된 `SECRET_KEY`나 비밀번호를 절대로 이용하지 마세요!

## 7. 백그라운드 작업
- API에서는 단순히 DB에 대한 CRUD 뿐만 아니라 다양한 작업을 수행할 때가 많음
- 머신 러닝을 시작할 수도 있고, 크롤링, 이메일 등을 보낼때도 있음
- 이런 경우 시간이 오래 걸리기 때문에 응답을 빠르게 줄 수가 없습니다. 이 때 사용가능한 가장 쉬운 방법이 바로 백그라운드 작업임

### 백그라운드 작업
~~~python
import time

from typing import Optional
from fastapi import BackgroundTasks, FastAPI, status

app = FastAPI()


def write_log(message: str):
    time.sleep(2.0)

    with open("log.txt", mode="a") as log:
        log.write(message)


@app.post("/send-notification/{email}", status_code=status.HTTP_202_ACCEPTED)
async def send_notification(email: str, background_tasks: BackgroundTasks):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)

    return {"message": "Message sent"}
~~~
- 위와 같이 `BackgroundTasks`를 임포트 한뒤 함수와 해당 함수의 인자만 넘겨주면 됨
- 여기서는 이메일 보내기라고 했지만, 결과를 바로 확인하기 위해 로그를 쌓고, 대신 시간이 2초 정도 걸리게 했음
- 눈여결 볼 점은 상태코드로 202 Accepted를 반환한 부분임
- 일단 응답을 보내고 결과는 장담할 수 없으나 일단 요청을 처리하겠다는 뜻

### 의존성 주입에서 사용
~~~python
import time

from typing import Optional
from fastapi import BackgroundTasks, Depends, FastAPI, status

app = FastAPI()


def write_log(message: str):
    time.sleep(2.0)

    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: Optional[str] = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}", status_code=status.HTTP_202_ACCEPTED)
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)

    return {"message": "Message sent"}
~~~

### 언제 쓰지 말아야 할까?
- 백그라운드 작업은 정말 강력한 기능 중 하나. 이 기능을 구현하려면 멀티 프로세싱 등을 구현해야 합니다. Flask 프로젝트에서는 간단하게 `subprocess` 표준 라이브러리를 많이 활용했었음
- 정말 강력한 기능이기는 하지만, 백그라운드 작업에 대한 `Fail Over`를 처리하기 힘듬
- 또한, 작업이 클 경우 서버가 사용해야할 리소스를 잡아 먹어 서버가 죽을 수도 있음
- 이런 경우 큐(Queue)를 사용해야 함
- 요즘은 클라우드의 큐 서비스를 많이 활용하는 편
- 아니면 Celery, RabbitMQ 또는 Redis 등을 이용해 큐를 구현