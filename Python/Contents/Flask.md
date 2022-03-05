# Flask Web Framework
## Flask 란
- Flask는 두개의 외부 라이브러리에 의존 `Jinja2` 탬플릿 엔진과 `Werkzeug WSGI` 툴킷

## Flask 개요
- SQLALchemy나 다른 DB Tool 또는 알맞게 비관계형 데이터 저장소로 고급 패턴을 만들 수 있음
- 파이썬 웹 인터페이스인 WSGI를 위한 프레임웍에 관계없이 사용할 수 있는 툴을 이용할 수 있음
- Flask는 프레임웍의 기능을 변경하기 위한 많은 hook을 포함함

## quick start
### 기본 애플리케이션
- 기본 Flask 애플리케이션은 다음과 같은 모습
~~~python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello world!"

if __name__ == "__main__":
    app.run()
~~~
- 이 내용을 `hello.py`로 저장하고 파이썬 인터프리터로 실행함
- 작성한 애플리케이션을 `flask.py`로 호출하지 않도록 주의해야함. 그 이유는 Flask 자체와 충돌이 나기 때문
~~~shell
$ python hello.py
  * Running on http://127.0.0.1:5000/
~~~
- 웹 브라우저를 열고, http://127.0.0.1:5000/, 로 이동하면 Hello world 나옴
- 위의 코드에 대한 간략한 설명
~~~python
from flask import Flask # -- 1
~~~
- `Flask` class 를 import함. 해당 클래스의 인스턴스가 WSGI 애플리케이션이 됨
~~~python  
app = Flask(__name__)   # -- 2
~~~ 
- 첫 번째 인자는 이 애플리케이션의 이름이 됨. 만약 단일 모듈을 사용해야 한다면 __name__ 을 사용해야 함  
  왜냐하면 애플리케이션으로 시작되는지, 모듈로 임포트되는지에 따라 이름이 달라지기 때문
- Flask class의 인스턴스를 생성. 인자로 모듈이나 패키지의 이름을 넣음  
  이것은 flask에서 탬플릿이나 정적파일을 찾을 때 필요
~~~python
@app.route('/')   # -- 3
def hello_world():
    return "Hello world!"
~~~
- `route` 데코레이터를 사용하여 Flask에게 어떤 URL이 우리가 작성한 함수를 실행시키는지 알려줌
- 작성된 함수의 이름은 그 함수에 대한 URL을 생성하는데 사용되고, 그 함수는 사용자 브라우저에 보여줄 메세지를 리턴함
- 최종적으로 `run()` 함수를 사용해서 우리가 개발한 애플리케이션을 로컬서버로 실행함. 소스파일을 모듈이 아닌 python 인터프리터를 이용해서 직접 실행한다면, `if __name__ == '__main__':` 이 문장은 우리가 실행한 서버가 현재 동작되는 유일한 서버라는 것을 보장함

### 외부에서 접근 가능한 서버 설정
- 위의 서버를 실행했다면, 그 서버는 네트워크 상에 있는 다른 컴퓨터에서 접근이 안되며 로컬서버에서만 접근이 가능함
- 이것이 기본 설정인 이유는 디버그모드상에서 어플리케이션의 사용자가 임의의 파이썬코드를 우리 컴퓨터에서 실행할 수 있기 때문
- debug 모드를 해제하거나 네트워크상에 있는 사용자들을 신뢰한다면, 다음과 같이 `run()` 메소드의 호출을 변경해서 서버의 접근을 오픈할 수 있음
~~~python
app.run(host='0.0.0.0')
~~~
- 위의 변경은 OS에게 모든 public IP를 접근가능하도록 설정함

### debug 모드
- `run()` 메소드는 로컬개발서버를 실행시키기에 좋지만, 코드 변경 후에 수동으로 재시작해야함
- 플라스크는 디버그모드를 지원하면, 서버는 코드변경을 감지하고 자동으로 reload하고, 문제가 발생하면 문제를 찾을 수 있도록 디버거 제공
- 디버깅을 활성화하는 두가지 방식이 있음. 
  - 애플리케이션 객체(`app`)에 플래그로 설정
  - 애플리케이션 실행할 때, 파라미터로 넘겨주는 방식
~~~python
app.debug = True #-- 1
app.run()        

app.run(debug=True)  #-- 2
~~~
- <b>대화식 디버거가 forking 환경에서 동작안됨에도 불구하고(운영서버에서는 거의 사용이 불가능함), 여전히 임의의 코드가 실행될 수 있다. 이런점은 주요 보안 취약점이 될 수 있으므로, 운영 환경에서는 절대 사용하지 말아야한다.</b>

### 라우팅
- 현대의 웹 어플리케이션은 잘 구조화된 URL로 구성되어 있다. 사람들은 URL을 쉽게 기억할 수 있고, 열악한 네트워크 연결 상황하에 기기들에서 동작하는 애플리케이션에서도 사용하기 좋음
- 사용자가 인덱스 페이지를 거치지 않고 바로 원하는 페이지로 접근할 수 있다면 더 좋아할 것임
- `route()` 데코레이터는 함수와 URL을 연결해줌. 아래는 기본적인 예제들임
~~~python
@app.route('/') 
def index():
    return "Index page"

@app.route("/hello")     # --> http://127.0.0.1:5000/hello 
def hello():
    return "Hello world"
~~~
- `app.route`안에 문자열을 입력함으로써, URL을 동적으로 구성할 수 있고, 함수에 여러 rule을 덧붙일 수 있음

### 변수 규칙
- URL의 변수 부분을 추가하기 위해 `<variable_name>` 으로 URL에 특별한 영역으로 표시해야 함  
  해당 부분은 function 의 keyword 인수로서 넘어감
- `<converter:variable_name>` 으로 규칙을 표시하여 converter를 추가할 수 있음
~~~python
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id
~~~
- 다음과 같은 converter 제공
  - `int`: accepts integers
  - `float`: like int but for floating point values
  - `path`: like the default but also accepts slashes 

#### URL 과 redirection 동작
- Flask의 URL 규칙은 Werkzeug 라우팅 모듈에 기반함  
  해당 라우팅 모듈은 unique한 URL을 보장하는 것.
- 아래의 두개를 비교해서 알아두자
~~~python
@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'
~~~
- 두 개의 차이는 URL 정의에 있어서 뒷 슬래시 존재 유무가 다름
- 첫 번째 경우(`@app.route('/projects/')`) 는 project 끝점에 대한 정규 URL은 뒷 슬래시를 포함하는데, 만약 뒷 슬래시 없이 접근하면 Flask가 뒷 슬래시를 가진 정규 URL 로 고쳐줌
- 두 번째 경우(`@app.route('/about')`)는 뒷 슬래시를 포함해서 URL에 접근하면 404 뜸. 
- 이는 URL을 unique 하게 유지하게 도와주며, 검색엔진이 같은 페이지를 중복해서 indexing하지 않도록 도와줌

### URL 생성
- 라우팅이 설정된 함수에 대한 URL을 얻어내려면, `url_for` 이라는 함수를 사용하면 됨
- 첫 번째 인자로 함수의 이름과, URL rule 변수 부분에 대한 다수의 키워드를 인자로 받음  
  알 수 없는 인자는 쿼리 인자로 URL에 덧붙여짐
~~~python
from flask import Flask, url_for
app = Flask(__name__)
@app.route('/')
def index(): pass

@app.route('/login')
def index(): pass

@app.route('/user/<username>')
def profile(username): pass

with app.test_request_context():
    print(url_for("index"))
    print(url_for("login"))
    print(url_for("login", next="/"))
    print(url_for("profile", username="John Doe"))

# /
# /login
# /login?next=/
# /user/John%20Doe
~~~
- 해당 테스트에서는 `test_request_context()` 를 사용. 해당 함수는 flask에게 현재 python shell 에서 테스트를 하고 있음에도 실제 요청을 처리하고 있는 것처럼 상황을 제공함 
- URL을 하드코딩하지 않고 URL을 `url_for`을 얻어내는 이유에는 3가지 적합한 이유가 있음
  - 전체적으로 URL이 어디있는지 기억할 필요없이 한번에 URL을 다 변경할 수 있음
  - URL을 얻어내는 것은 특수 문자 및 유니코드 데이터에 대한 escaping을 명확하게 해주기 때문에 처리할 필요가 없음  
    `John Doe` -> `John%20Doe`  
  - 우리가 작성한 애플리케이션이 URL의 최상위 바깥에 위치한다면(`/` 대신에 `/myapplication`), `url_for()` 가 그 위치를 상대적 위치로 적절하게 처리해줌

### HTTP 메소드
- HTTP(웹 어플리케이션에서 사용하는 프로토콜)는 URL 접근에 대해 몇가지 다른 방식을 제공
- 기본적으로 GET 방식으로 제공되지만, `route()` 데코레이터에 methods 인자를 지정하면 다른 방식으로 변경 가능
~~~python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        do_the_login()
    else:
        show_the_login_form()
~~~
- `GET` 방식이 나타난다면, HEAD가 자동적으로 더해짐. 우리는 이것을 처리할 필요가 없으며  HEAD 요청은 HTTP RFC의 요청으로써 처리된다는 것이 보장됨
- 간단한 HTTP 메소드 설명
  - `GET`: 브라우저가 정보를 단지 얻기위해 서버에 요청
  - `HEAD`: 브라우저가 어떤 페이지의 저장된 내용이 아니라, 헤더라 불리는 정보를 요청
  - `POST`: 브라우저는 서버에게 새로운 정보를 전송하도록 URL에 요청하고, 이 정보가 1번 반드시 저장되는 것을 보장  
            HTML 폼을 통해 서버에 데이터를 전송하는 방식
  - `PUT`: POST와 유사하지만 서버가 오래된 값들을 한번 이상 덮어쓰면서 store procedure를 여러번 실행할 수 있음
  - `DELETE`: 주어진 위치에 있는 정보를 제거
  - `OPTIONS`: 클라이언트에게 요청하는 URL이 어떤 메소드를 지원하는지 알려줌

### 정적 파일
- 동적인 웹 어플리케이션은 정적 파일을 필요로 함. 보통 자바스크립트나 CSS 파일을 의미함  
  이상적으로는 웹서버는 정적 파일들을 서비스하지만, 개발시에는 flask가 그 역할을 대신해줌
- `static` 이라는 폴더를 우리가 생성한 패키지 아래에 만들거나, 모듈 옆에 위치시키면 개발된 애플리케이션에서 `/static` 위치에서 정적 파일을 제공함
- 정적파일에 대한 URL을 얻으려면, `static` end point name을 사용해야함
~~~python
url_for('static'), filename="style.css")
~~~
- 이 파일(style.css)는 파일 시스템에 `static/style.css`로 저장되어야 함

### 요청 데이터 접근하기
- 웹 애플리케이션에 있어 클라이언트에서 서버로 보내는 데이터를 처리하는 것은 중요한 일
- Flask에서 이 정보는 global한 `request` 객체에 의해 제공됨
- 해당 객체가 global 하고 thread safe 하게 처리가 되는데, 그 답은 context local에 있음

#### context local
- Flask에서 특정 객체들은 global 객체인데, 이 객체들은 실제로 특정한 문맥에서 local 객체들에 대한 대리 역할을 수행함
- thread를 다루는 context를 생각해보자. 웹에서 요청이 하나 들어오면, 웹서버는 새로운 thread를 하나 생성함(그렇지 않다면, 다른 방식으로 기반을 이루는 객체가 쓰레드가 아닌 동시성을 제공하는 시스템을 다룰 수도 있음)
- flask가 내부적으로 요청을 처리할 때, flask는 현재 처리되는 thread를 활성화한 context 라고 간주하고, 현재 실행되는 애플리케이션과 WSGI환경을 그 context(thread)에 연결함
- 이렇게 처리하는 것이 context를 지능적으로 처리하는 방식이고, 이렇게 하여 애플리케이션이 끊어짐없이 다른 애플리케이션을 호출할 수 있음 


## 용어 정리
### CGI(Common Gateway Interface)
![img](https://github.com/koni114/TIL/blob/master/Python/img/CGI.jepg)

- 서버와 애플리케이션(클라이언트 아님) 간의 데이터를 주고받는 방식 또는 convention
- CGI도 말 그대로 Interface인데, web server의 요청을 받아 처리해줄 로직을 담고 있는 web application 프로그램 사이의 interface
- CGI를 통해 동적인 contents를 전달하는 방법
  - 서버의 cgi-bin 이라는 폴더를 만들어두고, 그 내부의 script 파일을 만들어둠
  - web-server가 CGI를 통해 cgi-bin에 접속해서 내부의 파일을 실행시키고, 그 결과를 클라이언트에게 전송 

### WSGI(Web Server Gateway Interface)
- Web server가 받은 호출을 python 애플리케이션에 전달하고 응답받기 위한 호출규약
- 파이썬 스크립트가 웹 서버와 통신하도록 도와주며, 웹 서버와 웹 애플리케이션 사이에 위치
![img](https://github.com/koni114/TIL/blob/master/Python/img/WSGI.jepg)

- private physical Server 위의 녹색 선으로 그려진 모든 것들을 합쳐 WAS(Web Application Server)라고 부름
- application을 담을 Web Server라고 생각하면 이해가 쉬움
- <b>WSGI Module + WSGI Process를 합쳐서 WSGI middleware 라고 부름</b>  
  하나로 구성된 것이 아니라, 일부는 Nginx에 내장되어있고 일부는 프로세스로 띄어진 형태
- 결과적으로 WSGI Middleware는 Web 서버와 application 을 연결시켜줌
- WSGI module과 WSGI process는 WSGI protocol로 주고받음
- WSGI는 `Callable Object` 를 통해 Web Server가 요청에 대한 정보를 Application에 전달
- `Callable Object`는 Function이나 Object 의 형태가 될 수 있으며, Web Server는 Callable Object를 통해 2가지 정보를 전해주어야 함
  - HTTP Request에 대한 정보(Method, URL, Data, ...)
  - Callback 함수
- 다음은 함수로 정의된 callable object의 형태의 예
~~~python
# environ --> HTTP request 정보를 가지고 있음
# start_response --> web server 에게 결과를 돌려주기 위한 callback function
def application(environ, start_response):
  body = b'Hello world!\n'
  status = '200 OK'
  headers = [('Content-type', 'text/plain')]
  start_reponse(status, headers)
  return [body]
~~~

#### WSGI Middleware Component 기능
- 호출된 url에 대한 라우팅 기능
- 하나의 프로세스에서 다중 어플리케이션을 동작하도록 처리
- 로드밸런싱
- 컨텐츠 전처리

### Web hook
  - 하나의 앱/웹이 다른 애플리케이션으로 앱관련 이벤트 정보를 실시간으로 제공하기 위한 방법
  - 여기서 말하는 실시간이란, 해당 앱에서 특정 이벤트가 일어나는 즉시, 미리 지정해놓은 URL을 통해 다른 애플리케이션으로 이벤트 관련 정보를 보낸다는 의미 
  - 웹페이지, 웹앱에서 발생하는 특정 행동(event)들을 커스텀 Callback으로 변환해주는 방법

### Routing
- 어떤 네트워크 안에서 데이터의 최적의 경로를 선택하는 과정을 말함  