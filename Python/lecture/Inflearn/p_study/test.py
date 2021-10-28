"""
이번 복습에서는 병행성과 병렬성에 대해서 간단하게 알고 넘어가자.

# 병행성(concurrency)
  - 하나의 서버에 여러 개의 작업을 수행하는 것을 의미함
  - 제너레이터 yield 명령어를 통해 병행성을 구현할 수 있음

# 제너레이터란?
  - Iterator 를 리턴하는 함수?
  - 현재 return 할 값만 메모리 상에 Loading 시켜두고,

# Macro 도 tag meta 가 조업 해석에 존재.
- Micro Hadoop 은 계정 권한 별로 분리해서 하는 것은 잘 안됨.
  이번에 tera one 들어오면서 biz_mart 에 접근하게끔.

# 사용자 계정
  - UI 상에서는 계정별로 접근을 하지만, 서버는 ruser01 하나의 계정을 공용계정을 사용하고 있음
    자원이나 정보들을 공유하고, 일관성 관리를 하기 위해서 그렇게 했다.

# 모델 실행
  - 450개 정도 된다.
  - flask, plumber
  - TCP 는 모델을 다 그때 그때마다 메모리 올려서 하는게 맞고,
  - memory-onLoad 상에서 하는 것은 Flask/Plumber

# 코멘트 기술
  - tag meta
  - 쿼리를 직접 할 수 있게 해달라.

# jupyter-Notebook 은 지금도 띄우는 것은 가능함.
- 수동이 아니라 자동화 해서 하는 것은 가능
- workflow 를 실행할 때 queue 는 없음. queue 를 쓰면 각 컴포넌트마다 서비스 처럼 띄어야 함.
  UI 버전이 spring framework

# 시스템 엔지니어
# UI 개발자
# Python engine 개발자
"""

def coroutine1():
    print(f">>> coroutine started.")
    i = yield
    print(f">>> coroutine received {i}")

cr1 = coroutine1()
print(cr1, type(cr1))
next(cr1)
cr1.send(1000)

def coroutine2(x):
    print(f">>> coroutine started : {x}")
    y = yield x
    print(f">>> coroutine received : {y}")
    z = yield x + y
    print(f">>> coroutine received : {z}")

cr3 = coroutine2(10)
print(next(cr3))
cr3.send(1000)

def generator1():
    yield from 'AB'
    yield from range(1, 4)

t1 = generator1()
print(next(t1))