"""
AsyncIO 멀티 스크래핑 실습
- 타겟 사이트 살펴보기
- 프로그램 설명
- async, await 설명
- 프로그램 테스트
"""
# !pip install asyncio
# !pip install beautifulsoup4

# chapter07-01
# AsyncIO
# 비동기 I/O Coroutine 작업을 쉽게 하도록 만들어 놓은 패키지
# Non-blocking 비동기 처리

# Asyncio 는 라이브러리며, python 3.2 부터 나오는 async/await 을 활용해 병행 처리가 가능한 library
# DB 작업이나 웹 서비스 작업을 동시에 처리할 수 있도록 하는 라이브러리

# Asyncio package
# asyncio is used as a foundation for multiple Python asynchronous frameworks 
# that provide high-performance network and web-servers, database connection libraries, 
# distributed task queues, etc.

# Blocking I/O
#   호출된 함수가 자신의 작업이 완료될 때까지 제어권을 가지고 있음
#   --> 타 함수는 대기해야 함
# non-Blocking I/O
#   호출된 함수(서브루틴)가 return 후 호출한 함수(메인루틴)에 제어권 전달
#   타 함수는 일 지속

# urllib2, request library 는 blocking I/O임
# --> 따라서 두 개의 라이브러리는 asyncio 를 사용하는 것보다 단일 스레드에서 동작하도록 하는 것이 더 좋음 

# 쓰레드 단점: 디버깅의 어려움. 자원 접근 시 race-condition, dead lock 고려 해야 함
# 코루틴 장점: 하나의 루틴(단일 스레드에서)만 실행되며 lock 관리 필요 없음. 제어권으로 실행
# 코루틴 단점: 사용 힘수가 비동기로 구현되어 있어야 하거나 직접 비동기로 구현해야 함
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


import asyncio
import timeit
from urllib.request import urlopen
# urlopen은 block 함수임. 여러 url 을 open 하면 block 됨
# block 이 되는 함수를 사용하면 asyncio 의 효과가 크지 않음.
# 따라서 Coroutine 과 thread 와 process 와 결합하는 패턴을 많이 사용함
# 예를 들어 각각의 작업을 각각의 스레드에서 하는 것이기 때문에 non-block의 효과를 가져올 수 있음
# --> 제대로된 비동기의 효과를 가져올 수 있음

from concurrent.futures import ThreadPoolExecutor
import threading

# 웹 크롤링 예제
# 동시에 여러 웹 사이트를 크롤링하는 프로그램을 만든다면, 더 빠르고 효율적인 어플리케이션이 될 수 있음

# 실행 시작 시간
start = timeit.default_timer()

# 서비스 방향이 비슷한 사이트로 실습 권장(게시판성 커뮤니티)
urls = ['http://daum.net', 'https://naver.com',
        'http://mlbpark.donga.com', 'https://tistory.com', 'https://wemakeprice.com']

async def fetch(url, executor):
    # 쓰레드명 출력
    print("Thread time : ", threading.current_thread().getName(), 'start', url)

    # 실행 : 실행할 때마다 끝나는 순서가 달라짐
    res = await loop.run_in_executor(executor, urlopen, url)
    print("Thread time : ", threading.current_thread().getName(), 'Done', url)

    # 결과 반환
    return res.read()[0:5]



# 함수 내에 yield 예약어를 사용하면 코루틴과 같은 비동기 처리가 가능한데,
# 해당 함수가 클로저인지 등 구분하기가 어려울 수 있으므로
# def 앞에 async 를 붙여 사용

# async -> 비동기 함수임을 선언
async def main():
    # thread pool 생성
    executor = ThreadPoolExecutor(max_workers=10)

    # future 객체 모아서 gather 에서 실행
    # 각 스레드에서 각 하나의 사이트에서 크롤링이 수행됨

    # url 과 thread 를 넣어서 실행. 
    # 즉 url 하나당 하나의 thread를 할당하는 리스트 컴프리핸션 선언
    futures = [
        asyncio.ensure_future(fetch(url, executor)) for url in urls
    ]

    # 결과 취합
    # await --> yield 
    # 모든 결과 값들이 끝나 gathering 될 떄까지 기다린다는 의미
    # futures 는 list 이기 때문에 unpacking 수행
    rst = await asyncio.gather(* futures)

    print()
    print('Result : ', rst)


if __name__ == '__main__':
    # 루프 초기화
    loop = asyncio.get_event_loop()

    # 작업 완료까지 대기
    loop.run_until_complete(main())

    # 수행 시간 계산
    duration = timeit.default_timer() - start

    # 총 실행 시간
    print("Total Running Time :", duration)



