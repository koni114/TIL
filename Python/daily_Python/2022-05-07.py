# function.wrap 을 이용해서 함수 데코레이터를 정의해라
# 시간을 측정할 수 있는 데코레이터 작성

import time
from functools import wraps

def time_check(func):
    @wraps(func)
    def wrapper(* args, ** kwargs):
        start_s = time.time()
        result = func(* args, ** kwargs)
        end_s = time.time()
        print(f"{func.__name__} --> {round(end_s - start_s, 4)}s")
        return result
    return wrapper

@time_check
def ten_second_check():
    time.sleep(10)

# ten_second_check()

ten_second_check = time_check(ten_second_check)
print(ten_second_check)
