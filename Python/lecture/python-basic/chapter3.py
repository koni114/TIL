print("chapter3 - 프로그램의 구조를 쌓는다! 제어문")

'''
** if문
- 다른 언어와 차이점 : 들여쓰기를 통해 제어문 구성.
--> tab vs space : 둘 중에 어느 것을 사용하던지 상관 없지만, 혼용하면 안된다는 점!

- **자료형에 따른 참 거짓 
숫자   :  거짓 -> 0,       참 -> 0이 아닌 숫자
문자열 :  거짓 -> ""(공백), 참 -> 공백이 아닌 문자열 
리스트 :  거짓 -> [],      
튜플   :  거짓 -> ()
딕셔너리 : 거짓 -> {}
--> 파이썬에서는 공백 및 빈 객체인 경우 거짓을 return 
'''
i = 3
if i in [1,2,3]:
    print("helloWorld")


'''
x in s
x not in s
-> 파이썬에서만 제공해주는 명령어
'''
if 1 in [1, 2, 3]:
    print("1이 있습니다.")

if 1 not in [2,3,4]:
    print("1이 없습니다.")

# elif : elseif 를 elif로 사용
pocket = ['paper', 'cellphone']
card = 1

if 'money' in pocket:
    print("돈 있음")
elif card:
    print("카드 있음")
else:
    print("걸어가라")


# 해당 제어문에서 아무것도 출력 또는 하고 싶지 않다면 !? : pass
if 'money' in pocket:
    pass
else:
    print("check")


## 이렇게 줄여 쓸 수도 있다는 점!
if 'money' in pocket: pass
else: print("카드를 꺼내라")

'''
** while 문
- 다른 언어와 동일!
- 무한 루프를 빠져나오고 싶다면, ctrl + c 
'''

'''
** for 문
'''


# 1. 다양한 for문의 사용
a = [(1,2), (2,3), (3,4)]
for (first, second) in a:
    print(first + second)


# 2. for문과 자주 사용되는 range 함수
a = range(10)
for i in a:
    print(i)

# 3. 리스트 안에 for문 포함하기
a = [1, 2, 3, 4]
result = [num * 3 for num in a]
result = [num * 3 for num in a if num % 2 == 0]
result = [x*y for x in range(1, 10)
                for y in range(1, 5)]


result = [num * 3 for num in a]
result = [num * 3 for num in a if num % 2 == 0]
