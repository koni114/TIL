def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__} --> {args!r}"
              f"--> {kwargs!r}")
        return result
    return wrapper

@trace
def test(x):
    """test 입니다."""
    return x


help(test)