from functools import wraps

def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}{kwargs!r} -> {result!r}")
        return result
    return wrapper

@trace
def fibonacci(n):
    '''n번째 피보나치 수를 반환함'''
    if n in (0, 1):
        return n
    return fibonacci(n-1) + fibonacci(n-2)

hello = fibonacci(10)
print(fibonacci)
