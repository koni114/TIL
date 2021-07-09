#- regular expression

#- 계좌 번호 금액만 추출하기
text = "안녕하세요, 선생님의 계좌번호는 212-08-234562 입니다.
          계좌번호 1234-62-124521로 조회한 결과, 잔액은 200,300원 입니다.
          제 계좌번호는 616132-04-123456이고, 이름은 엘리스입니다. 제 대기번호를 알 수 있을까요?
          회원님의 현재 대기번호는 13번입니다. 감사합니다.
          직거래를 원하시면 계좌번호 1410-12-713088에 30,000원 선입금 바랍니다."

p1 <- "\\d+-\\d+-\\d+"
m1 <- str_extract_all(text, p1)
print(m1)

p2 <- "\\d+,\\d+"
m2 <- str_extract_all(text, p2)
print(m2)

#- ^: 시작문자열
#- ^is는 is 문자열로 시작하지 않기 때문에 아무것도 나오지 않음
p1 <- "^Life"
p2 <- "^is"
m1 <- str_extract_all("Life is short", p1)
m2 <- str_extract_all("Life is short", p2)

print(m1)
print(m2)

#- $: 끝 문자열
#- $는 제일 뒤에 붙여줘야 함
p1 <- "short$"
p2 <- "short$"
m1 <- str_extract_all("Life is short",  p1)
m2 <- str_extract_all("Life is short, art is long",  p2)
print(m1)
print(m2)

#- OR 연산자 --> | 사용
p3 <- "apple|banana" 
m3 <- str_extract_all( "I like apple and banana", p3)
print(m3)

#- ^가 대괄호 안에 쓰이면 not의 의미를 가짐
#- 따라서 aeiou가 아닌 char을 추출하고 싶으면 --> [^aeiou] 라고 입력
p4 = "[^aeiou]"
m4 = str_extract_all("Life is short, art is long", p4)
print(m4)

#- []와 - 이용하기
#- [0-9]는 숫자, [a-z]는 알파벳 소문자, [A-Za-z]는 알파벳 대소문자와 매칭됨
#- '-'를 사용할 때, 왼쪽에 오는 문자가 오른쪽에 오는 문자보다 유니코드 상 먼저오는 문자여야 함

# 임의의 문자열
text = "vkvJZZjgsr=B5Al83+#@04?+p%x7DI3k"
p1 <- "[0-9]"     # 숫자와 매칭됨
p2 <- "[a-z]"     # 알파벳 소문자와 매칭됨
m1 <- str_extract_all(text, p1)
m2 <- str_extract_all(text, p2)
print(m1)
print(m2)

#- \d, \D 사용하기
p1 <- '\d'
p2 <- '\D'
m1 = str_extract_all("el_ice%20$19", p1)
m2 = str_extract_all("el_ice%20$19", p2)
print(m1)
print(m2)

#- \w는 [A-Za-z0-9_] 의 의미를 가짐
#- \W는 [^A-Za-z0-9_] 의 의미를 가짐
p1 <- "\w"         #
p2 <- "\W"         #
m1 = str_extract_all("Life is short", p1)
m2 = str_extract_all("Life is short", p2)
print(m1)
print(m2)

#- \s는 공백 문자(white space)와 모두 매칭
#- --> \t, \n, \v, \f, \r
#- \S는 그 반대
p1 <-"\s"   # 공백 문자와 매칭
p2 <- "\S"  # 공백이 아닌 문자와 매칭
m1 <- str_extract_all( "Life is short", p1)
m2 <- str_extract_all("Life is short",  p2)
print(m1)
print(m2)

#- . --> 어떤 문자가 오더라도 매칭되는 메타 문자
#- 예를 들어 c.t 는 , “cat, cbt, cct, c@t, c$t, c t…”등의 문자열과 매칭
text = "cat bat c@t hat cut com cook cant"
p1 = "c.t"        # c로 시작하고 t으로 끝나는, 모든 3글자 단어에 매칭
m1 = str_extract_all(text, p1)
print(m1)

#- (?i) --> 대소문자 구분 안한다는 메타 문자
#- 해당 문자를 어디에 넣든 대소문자를 구분 안함
text <- "APPLE APPLe APPlE APpLE ApPLE aPPLE APPle APpLe ApPLe aPPLe APplE ApPlE aPPlE AppLE aPpLE apPLE"
p1 <- "APPLE"
p2 <- "(?i)APPLE"       # 대소문자를 무시하며 APPLE에 매칭되는 패턴을 작성해보세요.
m1 <- str_extract_all(p1, text)
print("m1 결과 : ", m1)
m2 = str_extract_all(p2, text)
print("m2 결과 : ", m2)

#- 문자 개수를 지정 --> {n}
#- ex) 숫자 4자리 --> \d{4}
s = '111234a34a12'
p1 = "\\d{4}\\D\\d{2}\\D\\d{2}$"    # 여기에 정규표현식을 입력하세요.
m1 = str_extract_all(p1, s) 
print(m1)
