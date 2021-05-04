from functools import wraps


def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}({kwargs!r})"
              f"-> {result!r}")
        return result
    return wrapper
from functools import wraps


def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}({kwargs!r})"
              f"-> {result!r}")
        return result
    return wrapper

@trace
def fibonacci(n):
    """n번쨰 피보나치 수를 반환한다."""
    if n in (0, 1):
        return n
    return (fibonacci(n-2) + fibonacci(n-1))

fibonacci = trace(fibonacci)
print(fibonacci)




@trace
def fibonacci(n):
    """n번쨰 피보나치 수를 반환한다."""
    if n in (0, 1):
        return n
    return (fibonacci(n-2) + fibonacci(n-1))

fibonacci = trace(fibonacci)
print(fibonacci)



