# ** 클로저(closure)
# 클로저란 무엇일까? 위키백과의 번역을 그대로 들고 와 보자
'''
프로그래밍 언어에서의 클로저란 first-class 함수를 지원하는 언어의 네임 바인딩 기술이다.
클로저는 어떤 함수를 함수 자신이 가지고 있는 환경과 함께 저장한 레코드이다.
또한 함수가 가진 프리변수(free variable)를 클로저가 만들어지는 당시의 값과
레퍼런스에 맵핑하여 주는 역할을 한다. 클로저는 일반 함수와는 다르게, 자신의 영역 밖에서 호출된 함수의 변수값과
레퍼런스를 복사하고 저장한 뒤, 이 캡처한 값들에 엑세스할 수 있게 도와준다.
'''

# 프리변수(free variable)란?
'''
파이썬에서 프리변수는 코드블럭안에서 사용은 되었지만, 그 코드블럭안에서 정의되지 않은 변수를 뜻함.
나중에 더 심도있게 다루도록 하자
'''

# 클로저의 개념을 예제를 통하여 쉽게 이해해 보도록 하자
def outer_func():   #1
    message = 'Hi'  #3

    def inner_func():   #4
        print(message)  #6

    return inner_func() #5

outer_func() #2

# 프로그램을 실행하니, "Hi"라는 문자가 출력됨
# 간단한 구문이지만, 차근차근 뜯어가면서 확인해 보자

# 1. #1에서 정의된 함수 outer_func를 #2에서 호출한다.
# 2. outer_func가 실행된 후, 가장 먼저 하는 것은 message라는 변수에 Hi라는 문자 할당(#3)
# 3. #4 에서 inner_func를 정의하고 #5번에서 inner_func를 호출하며 동시 리턴
# 4. #6에서 message 변수를 참조하여 출력. 여기서 message 는 inner_func안에서는 정의되지 않았지만
#    inner_func 안에서 사용되기 때문에 프리 변수라고 부름

# 여기까지 이해하는데는 전혀 문제가 되질 않는다.
# 다음단계로 넘어가보자

def outer_func():   #1
    message = 'Hi'  #3

    def inner_func():   #4
        print(message)  #6

    return inner_func   #5 <--- ()를 지웠다!

outer_func() #2

# 아무것도 출력되지 않았다.
# outer_func이 리턴할 때 inner_func을 실행(--> 실행한다는 의미는 inner_func())하지 않고
# 오브젝트를 리턴했기 때문이다.

# 이번에는 outer_func이 리턴하는 inner_func 오브젝트를 변수에 할당하여 보자
# 그리고 my_func에 inner_func 함수가 할당되어 있는지 확인해 보자

my_func = outer_func() #2
print(my_func)

# 할당 되어 있음을 확인할 수 있다.
# 그렇다면, my_func 변수를 이용해 inner_func 함수를 호출하여 보자

my_func() #7
my_func() #8
my_func() #9

# 신기한 것은, outer_func()은 #2에서 호출 된 후, 종료되었다.
# 하지만 #7, #8, #9 에서 호출 된 my_func()은 함수가 outer_func 함수의 로컬변수인 message를 참조했다는 것이다.
# 어떻게 가능했을까? -> 해답은 closure 이다!

# 다음 코드를 실행시켜 보면서 차근차근 파악해보자.

def outer_func():
    message = 'Hi'

    def inner_func():
        print(message)

    return inner_func

my_func = outer_func()

print(my_func)          #7
print(dir(my_func))     #8
print(type(my_func.__closure__)) #9
print(my_func.__closure__)       #10
print(dir(my_func.__closure__[0])) #11
print(my_func.__closure__[0].cell_contents) #12

#7 결과 : my_func 변수에 inner_func 함수 오브젝트 할당되어 있음
#8 결과 : 클로저가 데이터를 어떻게 숨키는지 확인해보았더니, __closure__ 안에 들어가 있음
#9 결과 : __closure__ type -> tuple
#10 결과 : 튜플안에 item이 하나 들어있음
#11 결과 : 튜플안에 첫 번째 아이템 -> cell_contents 라는 속성이 들어있음
#12 결과 : cell 오브젝트는 어떤 속성들을 가지고 있을까요? -> 이중에 cell_contents라는 속성이 있음
# 13 결과 : 내부적으로 Hi가 들어있음을 확인! 클로저 함수의 데이터가 어디 들어가 있는지 알아냈다



