# 파라미터에 관계없이 모든 함수에 적용 가능한 Decorator 만들기
def generator_decorator(func):
    def wrapper(*args, **kwargs):
        print("function is decorated")
        return func(*args, **kwargs)

    return wrapper

@generator_decorator
def calc_square(digit):
    return digit ** 2

@generator_decorator
def calc_plus(digit):
    return digit + digit

@generator_decorator
def calc_quad(digit1, digit2, digit3, digit4):
    return digit1 * digit2 * digit3 * digit4

calc_square(10)
calc_plus(10)
calc_quad(10, 20, 30, 40)