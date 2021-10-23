"""
Futures(동시성)
- Futures wait 예제
- Futures_as_completed
- 동시 실행 결과 출력
- 동시성 처리 응용 예제 설명
"""

# concurrent.futures map
# concurrent.futures wait, as_completed

# 만약 thread 로 작업하는 경우,
# 각각 같은 시간이 걸린다는 보장이 없음
# 결과적으로 세세한 제어가 필요. 위의 두 메서드로 제어 가능
# 또한 작업이 실패할 수도 있음

import time
from concurrent.futures import ProcessPoolExecutor, wait, as_completed # 내부적으로 threading, multiprocessing 으로 작성되어 있음

# 동시에 4개의 thread 를 활용해서 각 순차적인 합을 계산하는 코드를 작성해보자
WORK_LIST = [1000000, 10000000, 100000000, 1000000000]

# 동시성 합계 계산 메인 함수
# 누적 합계 함수(제너레이터) -> 동시에 4개가 실행됨
def sum_generator(n):
    return sum(n for n in range(1, n+1))

def main():
    # Worker Count
    worker = min(10, len(WORK_LIST))
    start_tm = time.time() # 시작 시간

    future_list = []

    # 결과 건수
    # ProcessPoolExecutor
    with ProcessPoolExecutor() as executor:
        # map -> 작업 순서를 유지, 즉시 실행
        #     -> map 은 모든 실행 결과가 끝나기만을 기다렸다가 끝난 후 return 해옴

        for work in WORK_LIST:
            # future 만 반환
            future = executor.submit(sum_generator, work)
            # 스케줄링
            future_list.append(future)
            # 스케줄링 확인
            print(f'Scheduled for {work} : {future}')
            print()

        # 7초 안에 안 끝나는 작업은 강제로 종료
        # 1. wait 사용
        # wait : timeout 지정 가능
        result = wait(future_list, timeout=7)

        # 2. as_completed 결과 출력
        # as_completed -> 작업이 끝나는 대로 바로 return 받아 결과 출력
        # for future in as_completed(future_list):
        #     result = future.result()
        #     done = future.done()
        #     cancelled = future.cancelled()

        # 성공
        print('Completed Tasks : ' + str(result.done))
        # 실패
        print('Pending ones after waiting for 7 Seconds : ' + str(result.not_done))
        # 결과 값 출력
        print([future.result() for future in result.done])

    end_tm = time.time() - start_tm # 종료 시간
    msg = f'\n Time : {end_tm:2f}'
    print(msg)

# 실행 -> 시작점
# 해당 코드가 없으면 multi-processing 실행이 안됨
# 실행되는 순간 CPU 사용률이 순간적으로 살짝 늘어남
# 수치 연산을 하는 것들은 Processing 이 더 빠를 것임
# 실제로 실행해보면, multi-process > multi-thread 임을 확인

if __name__ == '__main__':
    main()