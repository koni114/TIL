# docker-compose 기초 및 문법
## docker-compose 란? 
- 도커 컴포즈는 여러개의 컨테이너를 하나로 묶어주는 역할을 수행
- 도커 컴포즈를 실행하기 위한 설정파일의 문법은 YAML 형식으로 작성할 수 있음

## docker-compose 기본 작성법
- docker-compose 공식 홈페이지에 있는 예제로 설명  
  `https://docs.docker.com/compose/gettingstarted/`

### python flask, redis 예제
~~~python
# app.py
import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
~~~

### `requirements.txt` 작성
~~~txt
flask
redis
~~~

### dockerfile 준비
~~~dockerfile
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
~~~

### docker-compose.yaml 파일 준비
~~~yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/code
    environment:
      FLASK_ENV: development
  redis:
    image: "redis:alpine"
~~~

### docker-compose 문법 설명
- `verison`: 도커 컴포즈 파일의 버전. 
- `services`: 컨테이너를 실행하기 위한 단위라고 보면 됨. 하위에는 서비스 이름 -> 서비스의 옵션 순으로 작성하면 됨
- `build`: build 할 dockerfile 의 경로를 지정해주면 됨
  - `context` : dockerfile 의 경로나 이름이 다른 곳에 있다면, 해당 명령어를 통해 디렉토리 지정
- `ports`: 포트포워딩을 지정하는 옵션. 순서대로 `<호스트 포트>:<컨테이너 포트>`로 작성하면 됨
- `volume`: 바인드 마운트, 볼륨을 지정할 수 있음
- `environment`: 컨테이너에서 사용할 환경변수를 설정할 수 있음
- `depends_on`: 실행순서를 보장받고 싶을 때, 사용