"""
- 계좌번호와 금액만 추출하기

"""
import re

text = '''안녕하세요, 선생님의 계좌번호는 212-08-234562 입니다.
          계좌번호 1234-62-124521로 조회한 결과, 잔액은 200,300원 입니다.
          제 계좌번호는 616132-04-123456이고, 이름은 엘리스입니다. 제 대기번호를 알 수 있을까요?
          회원님의 현재 대기번호는 13번입니다. 감사합니다.
          직거래를 원하시면 계좌번호 1410-12-713088에 30,000원 선입금 바랍니다.'''

#- \\d --> 한자리 이상의 숫자
p1 = "\d+-\d+-\d+"
m1 = re.findall(p1, text)
print(m1)

p2 = "\d+,\d+"
m2 = re.findall(p2, text)
print(m2)


#- ^: 시작문자열
#- ^is는 is 문자열로 시작하지 않기 때문에 아무것도 나오지 않음
p1 = "^Life"         # Life로 시작해야 매치
p2 = "^is"         # is로 시작해야 매치
m1 = re.findall(p1, "Life is short")
m2 = re.findall(p2, "Life is short")
print("m1 결과 : ", m1)
print("m2 결과 : ", m2)

#- $: 끝 문자열
#- $는 제일 뒤에 붙여줘야 함
p1 = "short$"         # short으로 끝나야 매치
p2 = "short$"         # short으로 끝나야 매치
m1 = re.findall(p1, "Life is short")
m2 = re.findall(p2, "Life is short, art is long")
print("m1 결과 : ", m1)
print("m2 결과 : ", m2)

#- OR 연산자 --> | 사용
p3 = "apple|banana"             # apple 또는 banana가 포함되면 매치
m3 = re.findall(p3, "I like apple and banana")

#- ^가 대괄호 안에 쓰이면 not의 의미를 가짐
#- 따라서 aeiou가 아닌 문자열을 추출하고 싶으면 --> [^aeiou] 라고 입력
p4 = "[^aeiou]"
m4 = re.findall(p4, "Life is short, art is long")

#- []와 - 이용하기
#- [0-9]는 숫자, [a-z]는 알파벳 소문자, [A-Za-z]는 알파벳 대소문자와 매칭됨
#- '-'를 사용할 때, 왼쪽에 오는 문자가 오른쪽에 오는 문자보다 유니코드 상 먼저오는 문자여야 함

# 임의의 문자열입니다.
text = "vkvJZZjgsr=B5Al83+#@04?+p%x7DI3k"

p1 = "[0-9]"     # 숫자와 매칭됨
p2 = "[a-z]"     # 알파벳 소문자와 매칭됨
m1 = re.findall(p1, text)
m2 = re.findall(p2, text)
print("m1 결과 : ", m1)
print("m2 결과 : ", m2)

#- \d, \D 사용하기
p1 = '\d'
p2 = '\D'
m1 = re.findall(p1, "el_ice%20$19")
m2 = re.findall(p2, "el_ice%20$19")
print("m1 결과 : ", m1)
print("m2 결과 : ", m2)

#- \w는 [A-Za-z0-9_] 의 의미를 가짐
#- \W는 [^A-Za-z0-9_] 의 의미를 가짐
p1 = "\w"         #
p2 = "\W"         #
m1 = re.findall(p1, "Life is short")
m2 = re.findall(p2, "Life is short")
print("m1 결과 : ", m1)
print("m2 결과 : ", m2)

#- \s는 공백 문자(white space)와 모두 매칭
#- --> \t, \n, \v, \f, \r
#- \S는 그 반대
p1 = "\s"         # 공백 문자와 매칭
p2 = "\S"         # 공백이 아닌 문자와 매칭
m1 = re.findall(p1, "Life is short")
m2 = re.findall(p2, "Life is short")
print("m1 결과 : ", m1)
print("m2 결과 : ", m2)

#- . --> 어떤 문자가 오더라도 매칭되는 메타 문자
#- 예를 들어 c.t 는 , “cat, cbt, cct, c@t, c$t, c t…”등의 문자열과 매칭
text = "cat bat c@t hat cut com cook cant"
p1 = "c.t"        # c로 시작하고 t으로 끝나는, 모든 3글자 단어에 매칭
m1 = re.findall(p1, text)
print("m1 결과 : ", m1)

#- (?i) --> 대소문자 구분 안한다는 메타 문자
#- 해당 문자를 어디에 넣든 대소문자를 구분 안함
text = '''APPLE APPLe APPlE APpLE ApPLE aPPLE APPle APpLe ApPLe aPPLe APplE ApPlE aPPlE AppLE aPpLE apPLE'''
p1 = "APPLE"
p2 = "(?i)APPLE"       # 대소문자를 무시하며 APPLE에 매칭되는 패턴을 작성해보세요.
m1 = re.findall(p1, text)
print("m1 결과 : ", m1)
m2 = re.findall(p2, text)
print("m2 결과 : ", m2)

#- 문자 개수를 지정 --> {n}
#- ex) 숫자 4자리 --> \d{4}
s = '111234a34a12'
p1 = "\d{4}\D\d{2}\D\d{2}$"    # 여기에 정규표현식을 입력하세요.
m1 = re.search(p1, s) is not None
print(m1)

#- * : 0개 이상
text = "ct cat caat caaat caaaaat caaaaaat cbt c1t c@t c_t"
p1 = "ca*t"         # c와 t 사이에 'a'가 0개 이상 있는 경우 매칭
m1 = re.findall(p1, text)
print("m1 결과 : ", m1)

#- + : 1개 이상
#- like[a-z]+ : like 는 매칭 안되고, likelihood, likely ..
#- 다음의 차이를 꼭 기억하자
ext = "apple banana carrot rabbit"
p1 = "[a-z]"        # 영어 소문자 매칭
p2 = "[a-z]+"       # 영단어 단위로 매칭
m1 = re.findall(p1, text)
m2 = re.findall(p2, text)
print("m1 결과 : ", m1)
print("m2 결과 : ", m2)

#- {n}: n개 매칭
text = "1 12 102 8948 754 77 3 222"
p1 = "\d+"       # 숫자 매칭
p2 = "\d{3}"     # 세 자리 수 매칭
m1 = re.findall(p1, text)
m2 = re.findall(p2, text)
print("m1 결과 : ", m1)
print("m2 결과 : ", m2)

#- n개 이상, m개 이하: {n,m}
text = "9 906 7581 28240 840414 3802773 425624"
p1 = "\d{3,5}"         # 자릿수가 3 이상 5 이하인 수
m1 = re.findall(p1, text)
print("m1 결과 : ", m1)

#- n개 이상: {n,}
text = "2 96 4019 884863 56635574 946482 95325201 410505 5802 6661337 2937786 31103"
p1 = "\d{7,}"         # 자릿수가 7 이상인 수
m1 = re.findall(p1, text)
print("m1 결과 : ", m1)

#- ? : 0또는 1개
#- 사용할 때 뒤에 배치시켜야 함
text = "ac abc abbc abbbc abbbbbc"
p1 = "ab?c"         # ac, abc와 매칭
m1 = re.findall(p1, text)
print("m1 결과 : ", m1)

#- 다음을 조심하자.
#- 항상 수량자는 가장 긴 문자열과 매칭하려는 속성이 있음.
#- 만약 방지하려면 제일 마지막에 ?를 붙여야 함
#- 중요한 것은 ?는 0 또는 1의 의미가 아니라는 것
text = "<html><head><Title>제목</head></html>"
p1 = "<.*>"
p2 = "<.*?>"         # ?를 붙이면 제일 처음에 나오는 >를 매칭시킴
m1 = re.findall(p1, text)
m2 = re.findall(p2, text)
print("m1 결과 : ", m1)
print("m2 결과 : ", m2)

#- 작성한 정규식이 매치되어야 하는 s의 조건
# - s는 1개 또는 2개의 숫자로 시작한다.
# - 그 다음, s에 4개 이상의 영어 소문자 알파벳이 온다.
# - 맨 마지막에는, 온점 .이 0개이거나 1개 있다.
# - 이외의 불필요한 문자가 있을 경우 모두 매치되지 않아야 한다.
# 예를 들어 12abcdefg. 는 매칭되어야 하고, 123abc... 는 매칭되면 안 됩니다.
s = input()
p1 = "^\d{1,2}[a-z]{4,}[.]?$"    # 여기에 정규표현식을 입력하세요.
m1 = re.search(p1, s) is not None
print(m1)

### re.compile --> 정규식 객체를 생성하여
### 코드에서 여러번 사용이 가능
text = "abcdefg"
pattern = re.compile("e")
print("정규식 객체의 자료형 : ", type(pattern))
print("정규식 객체 사용하는 경우 : ", pattern.findall(text))
print("객체를 사용하지 않는 경우 : ", re.findall("e", text))

## 그룹 사용해보기
text = "catatatatatat"

#- at를 그룹핑해서 매칭 여부를 확인할 수 있음
p1 = "cat"
p2 = "c(at)+"             # 정규식 패턴 입력!
m1 = re.search(p1, text)
m2 = re.search(p2, text)
print("m1 결과 : ", m1.group())
print("m2 결과 : ", m2.group())

#- 그룹 참조하기
#- 그룹핑한 값을 매번 반복해서 입력해야 하는 것이 아니라,
#- \\1, \\2로 매핑해서 사용 가능
#- g<1>, g<2>
text = "tomato"
p1 = "(to)ma\\1"             # 정규식 패턴 입력!
m1 = re.search(p1, text)
print("m1 결과 : ", m1.group())

#- ** sub() 문자열에서 패턴이 일치하는 부분을 일정 문자열로 교체해 주는 함수
#- 전화 번호 가운데 자리를 *로 교체하는 정규표현식을 만들어보자
text = '''
Elice 123456-1234567 010-1234-5678
Cheshire 345678-678901 01098765432
'''
p1 = "(010)\D?\d{4}\D?(\d{4})"          # 정규식 패턴 입력!
print("m1 결과 : ", re.sub(p1, "\g<1>-****-\g<2>", text))

text = "010 9119 7025"
p1 = "^(010)\D?\d{4}\D?(\d{4})$"
re.search(p1, text)
re.findall(p1, text)

import re
text = "010 9119 7025"
p1 = "(?:010)\D?\d{4}\D?(?:\d{4})"
re.findall(p1, text)
re.search(p1, text)

##- 비캡처링
##- 다음의 그룹 캡처를 사용하면 어떤 결과가 나올까?
c = 'tomato potato'
p1 = '(tom|pot)ato'
m1 = re.findall(p1, text)
print("m1 결과 : ", m1)

#- 결과는 ['tom', 'pot'] 이 나오는데,
#- 그 이유는 파이썬 정규표현식에서 그룹으로 캡처한 부분이 있다면 이외의 부분은 출력하지 않기 때문
#- ato는 그룹에 속해있지 않기 때문에 findall 함수에서 누락된 것

#- 이러한 문제를 해결하기 위해 비캡처링 그룹이 있음
#- 비캡처링 그룹은 패턴 문자들을 묶되, 그룹 단위로 매칭되지는 않게 해줌
#- 그룹으로 묶은 것들을 최종 결과에서 따로 구분하여 사용하지 않는 경우에 적용
#- --> 적용방법은 (?:) 임
text = 'tomato potato'
p1 = "(?:tom|pot)ato"
m1 = re.findall(p1, text)
print("m1 결과 :", m1)

#- 금액을 나타내는 숫자만 추출하고 싶을 때,
#- ex) 1,000, 75,000, 1,000,000 등
text = "마우스의 가격은 7,000원이고, 모니터의 가격은 72,000원이고, 키보드의 가격은 216,000원이고, 그래픽카드는 1,500,000원입니다."
p1 = "[\d{0,3},]*\d{1,3}"
m1 = re.findall(p1, text)
print("m1 결과 :", m1)


##- 전화번호 매칭하기
##- 처음 숫자 3개는 반드시 010으로 시작한다고 가정
import re

s = input()
s = "내 전화번호는 010-9119-7025 입니다."
p1 = "(?:010)(:?\D?\d{4}){2}"      # 여기에 정규표현식을 입력하세요.
p1 = "(010)\D?\d{4}\D?(\d{4})"
m1 = re.search(p1, s) is not None
print(m1)

s = "0101101010101"
test = "^(\d{4})\D?(\d{4})$"
m1 = re.search(test, s) is not None


s = '$'
p1 = "(?=[^aeiouAEIOU])(?=[a-zA-Z])"
m1 = re.search(p1, s) is not None
print(m1)

import re
s = 'elice alice'
p1 = "(?:e|a)lice"
m1 = re.findall(p1, s)
print(m1)
