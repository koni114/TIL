"""
정규 표현식 자가 TEST
"""
###################
#- 1 접두사와 접미사 ##
###################
#- 단어 리스트 words 에 들어있는 단어 중, 접두사와 접미사를 지정하여 원하는 단어만 출력해보자
#- 조건
#  - p1에 ex로 시작하는 단어들만 출력하도록 패턴을 입력해라
#  - p2에 Ful 로 끝나는 단어들만 출력하도록 패턴을 입력해라
import re
p1 = "^ex[A-Za-z]*"         # ex로 시작해야 매치
p2 = "[A-Za-z]*ful$"         # ful 로 끝나야 매치

words = ["flexible", "carefully", "chocolate",
         "expand", "exclude", "wonderful", "helpful"]

result1 = []
result2 = []

for word in words :
    # 단어들을 검사하여 리스트에 넣는 코드입니다. 수정하지 않아도 됩니다.
    m1 = re.findall(p1, word)
    m2 = re.findall(p2, word)

    result1 += m1
    result2 += m2

print("ex로 시작하는 단어 : ", result1)
print("ful로 끝나는 단어 : ", result2)

###################
## 2. 시작과 끝 찾기 ##
####################
#- s는 다음과 같은 형식을 따릅니다.
#- wnnnn.
#  - w는 알파벳, 숫자, 언더스코어를 나타낸다.
#  - n은 숫자를 나타낸다.
#  - .은 온점을 나타낸다.
#  - s는 ww로 시작해서 .으로 끝나야만 합니다.
import re
s = input()
p1 = "^\w{1}\d{4]\.$"    # 여기에 정규표현식을 입력하세요.
m1 = re.search(p1, s) is not None
print(m1)

###################################
## 3. 공백을 제외한 모든 문자들과 매칭하기 ##
####################################
#- 작성한 정규식이 매치되어야 하는 ss의 조건입니다
# - aa.aa.aa.aa.aa
# - a는 공백 문자를 제외한 모든 문자(개행 문자, 탭 문자 등을 제외한 문자들)를 나타낸다.
# - . 은 온점을 나타낸다.
# - 즉, 12.34.56.ab.cd 같은 문자열과 매칭하고, 12.34.56.78.90.ab.cd.ef
#   같은 문자열이나 12.34.ab 같은 문자열과는 매칭하면 안 됩니다.
import re
s = input()
p1 = "^(\S{2}\.){4}(\S{2})$"    # 여기에 정규표현식을 입력하세요.
m1 = re.search(p1, s) is not None
print(m1)

################################
## 4. ‘s’로 끝나는 단어인지 확인하기 ##
################################
#- 작성한 정규식이 매치되어야 하는 s의 조건입니다.
#  - s는 오직 영어 소문자와 대문자로만 구성되어 있어야 한다.
#  - s는 's'로 끝나야 한다.
import re
s = input()
p1 = "^[A-Za-z]*s$"      # 여기에 정규표현식을 입력하세요.
m1 = re.search(p1, s) is not None
print(m1)

################################
## 5. ‘s’로 끝나는 단어인지 확인하기 ##
################################
#- 작성한 정규식이 매치되어야 하는 s의 조건입니다.
#  - 모든 입력되는 ss는 “한 글자” 문자임이 보장됩니다.
#  - 정규식이 매치되는 s는 알파벳 자음이어야 합니다.
#  - 알파벳 자음은 대소문자를 구분하지 않습니다.
import re
s = "a"
p1 = "(?=[^aeiouAEIOU])(?=[a-zA-Z])"   # 여기에 정규표현식을 입력하세요.
m1 = re.search(p1, s) is not None
print(m1)
