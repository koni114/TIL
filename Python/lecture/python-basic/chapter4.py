print("chapter4 - 프로그램의 입력과 출력은 어떻게 해야할까? ")

'''
- 함수를 사용하는 이유 - 
반복을 줄이기 위해 사용. 프로그램을 일목요연하게 확인 할 수 있음
'''

## 함수의 정의
def sum(a, b):
    return a+b
sum(1,2)

# 입력 값이 몇개가 되는지 모를 때 : *입력 변수
def sum_many(*args):
    sum = 0
    for i in args:
        sum = sum + args
    return sum

'''
* 함수의 결과값은 언제나 하나이다.
'''

# 다음과 같은 경우에는 tuple로 변환해서 return 한다!
def sum_and_mul(a,b):
    return a+b, a*b

sum, mul = sum_and_mul(1,2)

'''
* 입력 변수에 초깃값 설정
- 입력 변수에 초깃값 설정 가능 -> 만약 그 변수에 아무 값도 넘겨주지 않으면 초기값 setting
- 초기화 하고 싶은 변수는 항상 뒤에 배치! (** 중요)

'''

# 초기화 하고 싶다면, 반드시 가장 뒤에 변수를 배치해야한다!
def say_myself(name, old, man = True):
    print("나의 이름은 %s 입니다." %name)
    print("나의 나이는 %d 입니다." %old)
    if man:
        print("남자입니다.")
    else:
        print("여자입니다.")

'''
변수의 효력 범위
- 함수의 매개변수로 선언된 변수는 함수 내에서만 효력
- 전역 변수로 선언하고 싶다면, -> global 변수명 
'''
a = 10
def vartest():
    global a  # 매개 변수 명과 겹치면 곤란하다. global 을 붙이면 전역 변수로 사용 가능
    a = a + 1 # 일반적으로 return 을 통해 전역 변수를 이용함
vartest(a)

'''
** 변수 입력하기: input
'''
number = input("숫자를 입력하세요")
print(number)

'''
* print 자세히 알기
- 큰따옴표(")로 둘러싸인 문자열은 + 연산과 동일
- 문자열 띄어쓰기는 콤마로 한다
- 한 줄에 결과 값 출력하기: end = ''
'''

print("my" "name" "is" "HJH")
print("my"+"name"+"is"+"HJH")
print("my", "name", "is", "HJH")

for j in range(1, 10):
    print(j, end = ' ')
print(' ')  # for문이 끝난 후 뒤에 붙여야만 앞선 for문에 해당하는 값이 출력됨
print("")
print("hello", "my", "name",  "is", end='')

'''
** 파일 읽고 쓰기: open, write
- 파일 열기 모드 
 r 읽기 모드 - 파일을 읽기만 할 때 사용
 w 쓰기 모드 - 파일에 내용을 쓸 때 사용: 기존에 있던 file 이라면 지우고, 기존에 없던 file 이라면 새로 만듬
 a 추가 모드 - 파일의 마지막 내용에 새로운 내용을 추가 할 때 사용
'''

f = open("C:/r/newFiles.txt", 'w')  # write 를 하기위해 불러왔으므로, 쓰거나 추가할 수 없음!
for i in range(1,10):
    data = "%d번째 줄입니다.\n" % i
    f.write(data)
f.close()

'''
** 프로그램 외부에 저장된 텍스트를 읽어 들어오기
- 1. readline()  : 한 줄씩 읽어오기
- 2. readlines() : 텍스트 전체를 리스트로 읽어오기
- 3. read()      : 텍스트 전체를 문자열로 읽어오기
-> 한번 읽어오면, 다시 open function 을 이용해서 문자를 읽어와야한다!!!
'''
f = open("C:/r/newFiles.txt", 'r')

a = f.readlines()
# 한 줄씩 읽어오기 -> 한칸씩 더 띄어쓰기가 되는 문제가 있음..
# 어떻게 해결?
while True:
    line = f.readline()
    if not line:break
    print(line)

# 리스트 형태로 읽어오기

# 한번에 싹다 문자열로 읽어오기
a = f.read()
print(a)

