# function.wrap 을 이용해서 함수 데코레이터를 정의해라


def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}({args!r})"
              f"-> {result!r}")
        return result
    return wrapper


@trace
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


