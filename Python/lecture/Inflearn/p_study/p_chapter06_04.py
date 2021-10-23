"""
Futures(동시성)
- 비동기 작업 처리
- 파이썬 GIL 설명
- 동시성 처리 실습 예제
- Process, Thread 예제
"""
# Future 동시성
# 파이썬 3.2 부터 Future 가 나옴
# 모든 언어에서 동시성은 매우 중요함. 주니어와 시니어를 나누는 Part

# 비동기 작업 실행
# 동기란? A가 끝나기 전까지 B가 실행될 수 없는 경우를 동기 작업이라고 함
# 비동기는 A 작업을 걸어두고 B 작업을 시작하고.. C 작업을 시작하고.. 하는 경우를 비동기 작업이라고 함
# 지연시간(Block) CPU 및 리소스 낭비 방지 -> File 을 쓰거나 Network I/O 를 할 때 동시성 활용을 권장함
# ex) 파일을 쓰는 작업이 1시간 걸리는데, 제어권을 다른 쪽으로 넘겨서 다른 작업 수행 등 ..
# ex) 네이버에서 크롤링 할 시, 느리면 기다리지 말고 다른 작업을 수행 ..
# 비동기 작업과 적합한 프로그램일 경우, 압도적으로 성능이 향상됨

# 2가지 패턴을 실습
# concurrent futures 사용법1
# concurrent futures 사용법2
# 파이썬 3.2 이하에서는 threading, multiprocessing 을 통해 동시성을 코딩함

# futures 패키지에서는 비동기 실행을 위한 API 를 고수준으로 작성 -> 사용하기 쉽도록 개선
# futures 를 사용할 줄 알면, 로우 레벨에 코딩을 하지 않아도 됨

# concurrent.Futures
# 1. 멑티스레딩 / 멀티프로세싱 API 통일 -> 매우 사용하기 쉬움
# 2. 실행 중인 작업 취소, 완료 여부 check, timeout option, callback 함수 추가, 동기화 코드 매우 쉽게 작성
#    -> Promise 개념이라고 함

# GIL(Global Interpreter Lock)
# 파이썬에만 있는 독특한 특징
# 여러 개의 작업을 처리할 때 전체가 Lock 이 걸리는 현상
# 두 개 이상의 thread 가 동시에 실행될 때, 하나의 자원을 엑세스 하는 경우 -> 문제점 방지를 위해 GIL 이 실행됨
# 리소스 전체에 Lock 이 걸림. -> Context Switch(문맥 교환) 비용 발생
# 여러 개의 스레드를 수행하려고 작업하면 하나를 쓰는 것보다 오히려 느린 경우가 많이 발생

# GIL 우회
# 멀티프로세싱을 이용. CPython 이라는 Interpreter 를 사용 등 ..
# ** Interpreter 종류 : PyPy, Jython, CPython ..

# 실습 예제
import os
import time
from concurrent import futures # 내부적으로 threading, multiprocessing 으로 작성되어 있음

# 동시에 4개의 thread 를 활용해서 각 순차적인 합을 계산하는 코드를 작성해보자
WORK_LIST = [100000, 1000000, 10000000, 100000000]

# 동시성 합계 계산 메인 함수
# 누적 합계 함수(제너레이터) -> 동시에 4개가 실행됨
def sum_generator(n):
    return sum(n for n in range(1, n+1))

def main():
    # Worker Count
    worker = min(10, len(WORK_LIST))
    start_tm = time.time() # 시작 시간

    # 결과 건수
    # ProcessPoolExecutor
    with futures.ProcessPoolExecutor() as executor:
        # map -> 작업 순서를 유지, 즉시 실행
        result = executor.map(sum_generator, WORK_LIST)

    end_tm = time.time() - start_tm # 종료 시간
    msg = f'\n Result -> {list(result)} Time : {end_tm:2f}'
    print(msg)

# 실행 -> 시작점
# 해당 코드가 없으면 multi-processing 실행이 안됨
# 실행되는 순간 CPU 사용률이 순간적으로 살짝 늘어남
# 수치 연산을 하는 것들은 Processing 이 더 빠를 것임
# 실제로 실행해보면, multi-process > multi-thread 임을 확인

if __name__ == '__main__':
    main()



