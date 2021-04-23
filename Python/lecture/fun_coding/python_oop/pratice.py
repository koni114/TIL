# quiz: 초간단 연습
# type checker 데코레이터 만들기(인자 유효성 검사)
# digit1, digit2를 곱한 값을 출력하는 함수 만들기
# type_checker 데코레이터로 digit1, digit2가 정수가 아니면 only integer support 출력하고 끝냄
# if(type(digit1) != int) or if(type(digit2) != int)

def checker(func):
    def inner_func(digit1, digit2):
        if (type(digit1) != int) or (type(digit2) != int):
            print("only integer support")
        else:
            func(digit1, digit2)

    return inner_func

@checker
def multiply(digit1, digit2):
    return digit1 * digit2

