# FastAPI
## What is FastAPI? 
- 웹 프레임워크: Spring Framework, Django, Flask, Sanic etc
- 마이크로프레임워크: Flask, Sanic
- ASGI 애플리케이션 

## 0. Why FastAPI?
- 배우기 쉽다
- 모던 파이썬 문법
  - 비동기 키워드: `async`, `await`
  - 타입 힌트
- OpenAPI 기반 (+GraphQL)
- 자동 문서 생성
- 마이크로프레임워크
  - API 서버
  - MSA

### FastAPI vs Flask
~~~python
# Flask
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

# FastAPI
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def hello():
    return "Hello, World!"
~~~

## 1. FastAPI 설치 및 Pydantic 소개
### 파이썬 버전 확인하기
- FastAPI는 모던 파이썬(3.6+)만을 지원하므로 3.6 이상의 파이썬이 반드시 설치되어 있어야 함
- 다음의 명령어로 파이썬 버전 확인
~~~shell
$ python3 -V
$ python3 --version
~~~

### 프로젝트 디렉토리 생성
- 프로젝트의 원할한 진행 할 디렉토리를 생성
~~~shell
$ mkdir fastapi_tutorial
$ cd fastapi_tutorial
~~~

### 가상환경 접속
~~~shell
$ source venv/bin/activate
~~~


### 첫 코드 작성하기
- 프로젝트를 열고 `main.py`를 생성한 뒤 다음을 입력
~~~python
# main.py
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def hello():
    return "Hello world!"
~~~
- 가장 간단한 FastAPI 앱을 만듬. FastAPI는 기본적으로 REST API를 쉽게 만들 수 있게 설계됨
- `FastAPI()`를 호출하여 앱을 인스턴스화하고 데코레이터를 이용해 앤드포인트를 만듬
~~~python
@app.get("/")  # GET / 를 호출할 수 있는 앤드포인트
def hello():  # 함수명
    return "Hello, World!"  # 반환
~~~
- FastAPI는 개발 서버를 과감히 빼버림. 즉 FastAPI 앱을 서버를 이용해 실행하려면 `Uvicorn` 또는 `Hypercorn` 등을 설치하여 실행해야함. 
~~~shell
$ pip install uvicorn
$ uvicorn main:app --reload
~~~
- 항상 실행할 때마다 위의 명령어를 실행하기 번거롭다면, `main.py`에 다음과 같이 `Uvicorn` 서버 실행을 추가하고, main.py에 실행
~~~python
import uvicorn

from fastapi import FastAPI


app = FastAPI()



@app.get("/")
def hello():
    return "hello world!"

if  __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
~~~
- 이제 아래와 같이 쉽게 실행이 가능
~~~python
# env 가상환경안에 들어가서 실행해야함! 
$ python main.py
~~~
- 실행결과는 http://localhost:8000 으로 확인할 수 있음
- 놀라운건, http://localhost:8000/docs 로 이동하면 자동 생성된 스웨거 문서도 볼 수 있음

### Pydantic 소개
- FastAPI를 설치하면, 다음의 메인 서브 라이브러리가 자동으로 설치됨
  - `starlette`
  - `pydantic`
- [Starlette](https://www.starlette.io/)은 FastAPI가 사용하는 웹 프레임워크. 사실 FastAPI는 Starlette의 랩퍼 프로젝트
- [pydantic](https://pydantic-docs.helpmanual.io/)는 파이썬 타입 어노테이션 문법에 근거하여 데이터 검증을 해주는 라이브러리.  
비슷한 라이브러리로 [marshmallow](https://marshmallow.readthedocs.io/en/stable/)가 있음
- 다음은 공식 문서에 나와있는 예제
~~~python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name = "John Doe"
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    'id': '123',
    'signup_ts': '2019-06-01 12:22',
    'friends': [1, 2, '3']
}

user = User(** external_data)
print(f"user.id --> {user.id}")
print(f"user.signup_ts --> {user.signup_ts}")
print(f"user.friends   --> {user.friends}")
print(user.dict())

# 결과
# user.id --> 123
# user.signup_ts --> 2019-06-01 12:22:00
# user.friends   --> [1, 2, 3]
# {'id': 123, 
#  'signup_ts': datetime.datetime(2019, 6, 1, 12, 22), 
#  'friends': [1, 2, 3], 
#  'name': 'John # Doe'
#  }
~~~
- <b>코드를 보면, 단순히 타입 검사 뿐만 아니라 적절하게 변형(cast)를 해줌</b>
- 그렇기 때문에 문자열로 통신하는 http 환경에서 제 값을 톡톡히 해냄  
  ex) 웹 애플리케이션에는 정수형인지 문자열인지 알 수 없음. 이 때 pydantic을 사용하여 개발자가 원하는 타입으로 받을 수 있음

## 2. 경로 매개변수
### HTTP HTTPie
- 개발을 편리하게 하는 여러 도구들이 있지만, API 서버를 개발한다면 빠질 수 없는 도구들이 있음
  - `curl`(command line 기반의 웹 요청 도구. Unix, Linux, Windows 등의 주요 OS에서 구동 가능)
  - `wget`(웹에서 파일을 다운로드하기 위한 명령줄 유틸리티)
  - `Postman` 또는 `Insomnia`
  - VS Code extention - REST Client
  - etc ..
- 위 도구들은 전부 HTTP 요청을 생성하는 도구. 각자의 장단점이 있지만, 저는 새로운 도구 소개 --> `HTTPie`
~~~shell
$ brew install httpie
~~~
- 위의 `main.py` 파일을 그대로 사용해서 실행해보기
~~~python
import uvicorn

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
~~~
- FastAPI 앱을 실행하고, 다음을 실행
~~~shell
$ http localhost:8000

# 결과
HTTP/1.1 200 OK
content-length: 14
content-type: application/json
date: Sat, 30 Apr 2022 01:48:40 GMT
server: uvicorn

"hello world!"
~~~
- 호스트가 localhost인 경우 호스트를 생략할 수 있음
~~~shell
$ http :8000

# 결과
HTTP/1.1 200 OK
content-length: 14
content-type: application/json
date: Sat, 30 Apr 2022 01:50:19 GMT
server: uvicorn

"hello world!"
~~~

### 경로 매개변수
- 경로 매개변수(Path Parameters)는 흔히 우리가 말하는 URL 경로에 들어가는 변수를 의미
- 아래의 예제에서 `user_id`가 경로 매개변수임
~~~python
from fastapi import FastAPI
app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id):
    return{"user_id": user_id}
~~~
- 이제 http://localhost:8000/users/123 을 호출하면,
~~~shell
$ http :8000/users/123

HTTP/1.1 200 OK
content-length: 17
content-type: application/json
date: Sat, 30 Apr 2022 02:06:37 GMT
server: uvicorn

{
    "user_id": "123"
}
~~~
- 앞서 `user_id`의 값을 123이라는 정수형을 기대했지만, 문자열로 응답이 옴.
- 이를 해결하려면 변수에 type hint를 지정하면 됨
~~~python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return{"user_id": user_id}
~~~
~~~shell
$ http :8000/users/123
 
HTTP/1.1 200 OK
content-length: 15
content-type: application/json
date: Sat, 30 Apr 2022 02:10:44 GMT
server: uvicorn
{
    "user_id": 123
}
~~~
- 정수형 타입이 아닌 값을 호출하면 에러 발생
~~~shell
$ http :8000/users/12.3

HTTP/1.1 422 Unprocessable Entity
content-length: 104
content-type: application/json
date: Sat, 30 Apr 2022 02:13:00 GMT
server: uvicorn

{
    "detail": [
        {
            "loc": [
                "path",
                "user_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
~~~
- `user_id`의 값으로 부동소수형 12.3을 넣어줬더니 응답코드 422와 함께 위와 같은 오류 메세지가 나타남
- 이렇듯 타입 걱정없이 FastAPI가 알아서 적절한 응답을 보내줌
- 이런 기본적인 오류에 대해서 따로 코딩 할 필요가 없기 때문에 생산성이 올라가게 됨
- 또한 문서에서 바로 확인 및 테스트 할 수 있기 때문에 프론트앤드 개발자가 편해짐  
  http://localhost:8000/docs

### Flask 매개변수 설정 
- Flask의 경우, 다음과 같이 작성했을 것임
~~~python
@app.get("/users/{user_id:int}")
def get_user(user_id):
    return {"user_id" : user_id}
~~~
- 위의 방식을 FastAPI에서 실행하면, 이방식도 잘 동작함을 확인할 수 있음. 경로에서 타입을 명시하면 해당 타입으로 인자를 전달받음
- 하지만 함수 내부는 경로가 아닌 실제 함수 매개변수의 타입을 따르고, pydantic 역시 그렇기 때문에  <b>함수 매개변수에 타입을 설정하는 것이 좋음</b>

### 순서 문제
- fastAPI는 경로 동작이 앤드포인트 선언 순서에 따라 수행됨
- 다음의 두 코드를 비교하여 실행해보면 좋음
~~~python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return{"user_id": user_id}


@app.get("/users/me")
def get_current_user():
    return {"user_id": 123}
~~~
~~~shell
$ http :8000/users/me

HTTP/1.1 422 Unprocessable Entity
content-length: 104
content-type: application/json
date: Sat, 30 Apr 2022 02:31:22 GMT
server: uvicorn

{
    "detail": [
        {
            "loc": [
                "path",
                "user_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
~~~
- 위와 같은 에러 발생. 이는 경로 동작(Path operation)이 엔드포인트 순서에 따라 수행되기 때문
- 제대로 실행하려면 `get_current_user`와 `get_user`의 순서를 바꾸어 주어야 함

## 3. 쿼리 매개변수
### 제일 많이 쓰이는 쿼리 매개변수
- API 뿐만 아니라 우리가 흔히 웹페이지를 들어가면 https://example.com?no=1&page=32 등과 같은 주소 형식을 많이 보게됨
- 호스트 주소 뒤 `?` 뒤에 오는 변수들을 쿼리 매개변수(Query parameters)라 부름
- 각 매개변수는 `&` 기호로 구분되고 `key=value`와 같이 키/값 쌍으로 정의함
~~~python
@app.get("/users")
def get_user(limit: int):
    return{"limit": limit}
~~~
- 위 코드를 실행 후 쉘에서 다음과 같이 입력
~~~shell
$ http ':8000/users?limit=100'
~~~
- 예상한 결과가 응답으로 옴을 확인할 수 있음. 추가로 아래와 같이 기본값을 추가하면 호출 할 때 `limit`값을 받지 않아도 됨
~~~python
@app.get("/users")
def get_user(limit: int = 100): # 추가 기본값.
    return{"limit": limit}
~~~
- `limit`을 선택적(Optional)이게 하려면 `None` 값을 기본값으로 주면 됨.   
  결과는 JSON 형식이므로 `limit` 값은 `null`(typing Optional은 의미가 없음)
- <b>FastAPI는 경로에 매개변수가 없으면 쿼리 매개변수로 함수 매개변수를 받음</b>
- FastAPI는 `True`, `true`, `TRUE`, `1` 전부 `True`로 인식함. 심지어 `on`, `yes`도 `True`로 인식
- 상용 API를 배포할 때는 이렇게 중구난방하게 하지는 않음

### 문자열 열거형의 등장
- 파이썬도 다른 언어처럼 열거체(Enumeration)을 지원함. 다중 상속도 지원
- 열거형(Enumerated Type)이란, 언어의 상수 역할을 하는 식별자. 일부 열거자 자료형은 언어에 기본으로 포함되어 있음
~~~python
from enum import Enum
from fastapi import FastAPI

app = FastAPI()

class UserLevel(str, Enum):
    a = "a"
    b = "b"
    c = "c"


@app.get("/users")
def get_users(grade: UserLevel):
    return {"grade": grade}
~~~
- 위와 같이 작성하면, 반드시 `grade` 매개변수는 a, b, c 중 하나여야함.
- 만약 정의하지 않는 값으로 호출하면 에러 발생.
~~~shell
$ http ':8000/users?grade=d'

# 결과
{
    "detail": [
        {
            "ctx": {
                "enum_values": [
                    "a",
                    "b",
                    "c"
                ]
            },
            "loc": [
                "query",
                "grade"
            ],
            "msg": "value is not a valid enumeration member; permitted: 'a', 'b', 'c'",
            "type": "type_error.enum"
        }
    ]
}
~~~
- 친절하게 허용된 값이 무엇인지 알려줌. 열거형의 기본값을 적을 경우 직접 작성해주는 것이 좋음
~~~python
@app.get("/users")
def get_users(grade: UserLevel= UserLevel.a):
    return {"grade": grade}
~~~

## 4. 요청 본문
- 위의 예제들은 URL에 들어가는 매개변수들을 살펴보았는데, 보통 REST API에서 POST, PUT, PATCH 등의 메소드를 사용하는 경우에 HTTP 본문(body)를 많이 활용함
- 단순 텍스트나 XML로도 보낼 수 있지만, 요즘은 대개 JSON을 사용함

### Pydantic 으로 요청 본문(Request body) 받기
- pydantic 을 이용하면 쉽게 구현 가능
~~~python
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class User(BaseModel):
    name: str
    password: str
    avatar_url: Optional[HttpUrl] = None


@app.post("/user")
def create_user(user: User):
    return user
~~~
- User 클래스는 `pydantic.BaseModel`을 상속하는 데이터 모델
- `name`, `password` 필드는 필수이지만, `avatar_url` 필드는 필수가 아님
- <b>비밀번호는 반드시 암호화해야함!</b> 단순 예제이므로 실무에서는 절대로 위와 같이 코딩해서는 안됨
- 따라서 다음과 같이 httpie를 이용해 테스트 할 수 있음
~~~shell
# 따옴표가 없음을 주의!
$ http :8000/users name=spike password=1234

# 결과
HTTP/1.1 200 OK
content-length: 52
content-type: application/json
date: Sat, 30 Apr 2022 12:17:00 GMT
server: uvicorn

{
    "avatar_url": null,
    "name": "spike",
    "password": "1234"
}
~~~
- 입력과 출력이 같은 에코(echo) API 였기 때문에 입출력이 같음
- 여기서 갑자기 등장한 `HttpUrl`은 pydantic 타입임. 인터넷 환경에는 여러가지 타입들이 존재함.  
  이메일, 파일 경로, 우편 번호 등도 포함해서 다양한 형태의 값들을 받음
- pydnatic은 자주 쓰이는 타입들을 미리 제공하고, 해당하는 타입을 검증함. `HttpUrl`은 그 중 하나이며, 정말 자주 사용하는 타입 중 하나. 
- 위에서 보듯, `avatar_url`은 URL을 입력받아야 하고, 그렇지 않으면 수동으로 데이터 검증을 해줘야 함
- 이런 특수한 문자열의 경우 정규표현식이 아니면 잡아내기 힘듬. 비슷한 예로 이메일 검증 정규표현식이 있음
~~~python
import re

pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
email_regex = re.compile(pattern)
email_regex.match("fastcampus")
email_regex.match("fastcampus@example.com")
~~~
- <b>pydantic에는 `EmailStr`이라는 타입이 있음.</b> 하지만 주제와 벗어나고, 별도의 추가 라이브러리를 설치해야 함

### 복잡한 모델
- JSON은 단순히 키-값만을 가지지 않음. 배열도 있고, 오브젝트가 중첩 될 수도 있음.
- 한가지 예시를 들어보자. 사용자는 인벤토리가 있고, 인벤토리에는 아이템을 담을 수 있음. 다음은 이를 모델링 한 예
~~~python
from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import uvicorn


app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    amount: int = 0


class User(BaseModel):
    name: str
    password: str
    avatar_url: Optional[HttpUrl] = None
    inventory: List[Item] = []


@app.post("/users")
def create_user(user: User):
    return user


@app.get("/users/me")
def get_user():
    fake_user = User(
        name="HuhJaehun",
        password="1234",
        inventory=[
            Item(name="전설 무기", price=1_000_000),
            Item(name="전설 방어구", price=900_000)
        ]
    )
    return fake_user
~~~
~~~shell
$ http :8000/users/me

HTTP/1.1 200 OK
content-length: 180
content-type: application/json
date: Sat, 30 Apr 2022 12:41:11 GMT
server: uvicorn

{
    "avatar_url": null,
    "inventory": [
        {
            "amount": 0,
            "name": "전설 무기",
            "price": 1000000.0
        },
        {
            "amount": 0,
            "name": "전설 방어구",
            "price": 900000.0
        }
    ],
    "name": "HuhJaehun",
    "password": "1234"
}
~~~
- 실제로 위의 예시처럼 사용하는 경우는 없지만, 중첩(Nested) 객체나 리스트(List) 또한 쉽게 표현이 가능하다는 사실을 기억

## 5. 응답(response) 모델
- 이번에는 응답 모델(Response Model)을 만들어보자

### 데코레이터 메소드의 매개변수
- 입력을 어떻게 주어야 하는지도 중요하지만, 실제 API를 호출해보기 전에 응답이 어떻게 오는지 확인하면 더 좋음
~~~python
from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


app = FastAPI()


class User(BaseModel):
    name: str
    password: str
    avatar_url: Optional[HttpUrl] = None


@app.get("/users/me", response_model=User)
def get_user(user: User):
    return user
~~~
- 데코레이터의 매개변수로 `response_model`을 추가하고 `User` 할당
- 이렇게하면 문서(http://localhost:8000/docs)에서 응답이 오는지 확인할 수 있고, 응답 결과에 대해서도 검증을 함

### 응답모델 변형 #1 서로 다른 User 모델
- 앞선 예제들에서는 사용자의 비밀번호를 그대로 보여주는 문제점이 발생
- 가장 단순한 방법은 클래스를 나누는 것
~~~python
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


app = FastAPI()


class CreateUser(BaseModel):
    name: str
    password: str
    avatar_url: HttpUrl = "https://icotar.com/avatar/fastcampus.png?s=200"


class GetUser(BaseModel):
    name: str
    avatar_url: HttpUrl = "https://icotar.com/avatar/fastcampus.png?s=200"


@app.post("/users", response_model=GetUser)  # 응답 모델
def create_user(user: CreateUser):  # 요청 모델
    return user
~~~
- 위의 예제는 비밀번호를 반환하지 않음. 하지만 중복 코드가 있어 불편하기 때문에, 반드시 좋은 방법이라 할 수는 없음
- 때에 따라서는 아래의 방법이 도움이 될 수 있음
~~~python
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


app = FastAPI()


class User(BaseModel):
    name: str
    avatar_url: HttpUrl = "https://icotar.com/avatar/fastcampus.png?s=200"


class CreateUser(User):
    password: str


@app.post("/users", response_model=User)
def create_user(user: CreateUser):
    return user
~~~

### 응답 코드
- HTTP는 다양한 상태 코드를 가짐. 우리는 사용자를 생성하는 API에서 성공했을 경우, 기본값인 200을 반환.  
  이번에는 201 코드를 반환해보자
~~~python
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


app = FastAPI()


class User(BaseModel):
    name: str
    avatar_url: HttpUrl = "https://icotar.com/avatar/fastcampus.png?s=200"


class CreateUser(User):
    password: str


@app.post("/users", response_model=User, status_code=201)  # 추가: status_code
def create_user(user: CreateUser):
    return user
~~~
- 위와 같이 `status_code`에 직접 상태코드를 입력하면 됨. 좀 더 가독성이 좋게 코딩하려면 `fastapi` 에서 `status` 를 import 하면 됨
~~~python
from fastapi import FastAPI, status

status.HTTP_200_OK
status.HTTP_201_CREATED
...
~~~

## 6. 데이터 검증
- FastAPI의 강점 중 하나가 데이터 검증을 위한 방어 코드를 작성하는 대신 알아서 해준다는 것  
  여태까지는 타입 검증이나 필수 값이냐 아니냐만을 봤지만 좀 더 세밀한 제어를 할 수 있음

### Path, Query 함수
- 함수를 정의할 때, 각 매개변수가 경로 매개변수인지 아니면 쿼리 매개변수인지 명시하지 않음
- FastAPI가 알아서 인지했기 때문. 하지만 `Path()`, `Query()` 함수를 이용하면 매개변수를 명시적으로 정의할 수 있고, 다양한 옵션을 추가할 수 있음
- Path, Query 는 `Params` 클래스의 서브 클래스. 하지만 실제로는 클래스를 반환하는 함수.  
  그러므로 Path/Query 클래스가 정확하지만 본 강의에서는 편의상 함수라 부르자
- 아래 코드에서 자세한 설명
~~~python
@app.get("/users/{user_id}/inventory", response_model=List[Item])
def get_item(
        user_id: int = Path(..., gt=0, title="사용자 id", description="DB의 user.id"),
        name: str = Query(None, min_length=1, max_length=2, title="아이템 이름"),
):
    user_items = []
    for item in inventory:
        if item["user_id"] == user_id:
            user_items.append(item)

    response = []
    for item in user_items:
        if name is None:
            response = user_items
            break
        if item["name"] == name:
            response.append(item)

    return response
~~~
- http://localhost:8000/docs 에서 바로 확인 가능
- 영어뿐만 아니라 한글도 글자 갯수를 정확하게 측정함. 다음 두 가지만 주의하면 됨
  - `gt`, `ge`, `lt`, `le`: 숫자
  - `min_length`, `max_length`: `str`
  - `min_items`, `max_items`: 컬렉션(e.g. `List`, `Set`)  
- 뿐만 아니라 `regex` 옵션으로 정규표현식 검증도 가능

### 클래스에서 데이터 정의
- 경로 동작에 사용하는 `Path`, `Query` 매개변수는 위와 같이 동작함. 
- 요청 본문은 pydantic의 클래스로 만들었음. 그럼 JSON을 본문으로 갖는 요청은 어떻게 할까?
~~~python
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, title="이름")
    price: float = Field(None, ge=0)
    amount: int = Field(
        default=1,
        gt=0,
        le=100,
        title="수량",
        description="아이템 갯수. 1~100 개 까지 소지 가능",
    )


@app.post("/users/{user_id}/item")
def create_item(item: Item):
    return item
~~~
- 간단한 모델을 받을 때는 `Body` 클래스를 이용하는 방법도 있음

## 7. 헤더, 쿠키 매개변수
- 헤더/쿠키 매개변수는 앞서 배운 매개변수들과 다른 점이 있음
- 이 매개변수를 다루려면 반드시 `Header`, `Cookie` 클래스를 사용해야 함. 먼저 쿠키를 테스트 해보자

### 쿠키 가져오기
~~~python
from fastapi import FastAPI, Cookie


app = FastAPI()


@app.get("/cookie")
def get_cookies(ga: str = Cookie(None)):
    return {"ga": ga}
~~~
- 쿠키는 사이트에서 정보 수집을 하는 프로그램들이 자주 사용하는 프로그램
- ga 는 구글 애널리틱스가 굽는 쿠키 이름. 
~~~shell
$ http :8000/cookie Cookie:gaGA12.3.4

# 결과
HTTP/1.1 200 OK
content-length: 17
content-type: application/json
date: Sat, 30 Apr 2022 13:57:11 GMT
server: uvicorn

{
    "ga": "GA12.3.4"
}
~~~
-`HTTPie`에서 쿠키는 `Cookie:<key>=<value>;<key>=<value>`와 같이 작성. `;`은 구분자

### 헤더 가져오기
- HTTP 헤더는 종류도 많고 커스텀 헤더도 정말 많이 사용함
~~~python
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/header")
def get_headers(x_token: str = Header(None, title="토큰")):
    return {"X-Token": x_token}
~~~
- 헤더에 X- 접두어는 사용자 정의 헤더라는 것을 의미
- 반드시 이렇게 할 필요는 없지만, 표준 헤더와 구분짓기 위해 사용
- 이 정책은 폐기 되었지만, 여전히 다들 이 관례를 따르고 있음
- 눈 여겨 볼 점은, 파이썬에서 `-`을 변수명으로 허락하지 않기 떄문에, 언더스코어(`_`)를 대신 사용해야 합니다
- 그리고 대소문자 구분을 하지 않음. 실제로 아래와 같이 테스트하면 정상 작동함
~~~shell
$ http :8000/header X-Token:some.secret.token
~~~
- 추가로 `Header`는 다른 클래스와 다르게 `convert_underscores` 옵션을 갖는데 `False`를 줄 경우 하이픈을 언더스코어로 변환하지 않음
- `X-token`이 아니라 `X_token` 이라는 헤더를 위해 존재하는 옵션.  
  하지만 애초에 언더스코어를 사용하는 건 관례를 벗어나므로 왠만해서는 하지 않아야 함


