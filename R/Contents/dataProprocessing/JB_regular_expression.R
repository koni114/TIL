#- reg expression
text = "안녕하세요, 선생님의 계좌번호는 212-08-234562 입니다.
          계좌번호 1234-62-124521로 조회한 결과, 잔액은 200,300원 입니다.
          제 계좌번호는 616132-04-123456이고, 이름은 엘리스입니다. 제 대기번호를 알 수 있을까요?
          회원님의 현재 대기번호는 13번입니다. 감사합니다.
          직거래를 원하시면 계좌번호 1410-12-713088에 30,000원 선입금 바랍니다."

#- 1. 한자리 이상의 숫자 --> +
exp <- "\\d+-\\d+-\\d+"
stringr::str_extract_all(text, exp)[[1]]

exp <- "\\d+,\\d+"
stringr::str_extract_all(text, exp)[[1]]

#- 2. 시작문자열 : ^
exp  <- "^Life"
exp2 <- "^is"

stringr::str_extract_all('Life is short', exp)[[1]]
tt <- stringr::str_extract_all('Life is short', exp2)[[1]]

#- 3. OR 연산자 사용. --> |
exp <- "banana|apple"
stringr::str_extract_all('I like banana and apple', exp)[[1]]

#- 4. []안의 ^ 연산자 --> not의 의미로 사용
#-    aeiou가 아닌 문자를 추출하고 싶다면, "[^aeiou]" 사용
exp <- "[^aeiou]"
stringr::str_extract_all('Life is short', exp)[[1]]

#- aeiou와 공백을 뺀 나머지 문자열 추출
exp <- "[^aeiou\\s]"
stringr::str_extract_all('Life is short', exp)[[1]]

#- 5. 어떤 문자가 오더라도 매칭 -> .
text <-  "cat bat c@t hat cut com cook cant"
exp  <- "c.t"
stringr::str_extract_all(text, exp)

#- 6. 대소문자 구분 안한다는 문자 -> (?i)
text <- "APPLE APPLe APPlE APpLE ApPLE aPPLE APPle APpLe ApPLe aPPLe APplE ApPlE aPPlE AppLE aPpLE apPLE"
exp  <- "(?i)apple" 
stringr::str_extract_all(text, exp)[[1]]

#- 7. 문자 개수를 지정 --> {n}
#- ex) 숫자 4자리      --> {4}
s = '111234a34a12'
exp = "\\d{4}\\D\\d{2}\\D\\d{2}$"
stringr::str_extract_all(s, exp)[[1]]

#- 8. 0개 이상 --> *
text <- "ct cat caat caaat caaaaat caaaaaat cbt c1t c@t c_t"
exp <- "ca*t"
stringr::str_extract_all(text, exp)[[1]]

#- 9. 1개 이상 --> +
#- ex) like[a-z]+ : like는 매칭 안되고, likehood, likely...
text <- "apple banana carrot rabbit"
exp1 <- "[a-z]"  #- 영어 알파벳 소문자 매칭
exp2 <- "[a-z]+" #- 영어 소문자 단어 매칭
stringr::str_extract_all(text, exp1)[[1]]
stringr::str_extract_all(text, exp2)[[1]]

# 10. n개 매칭 --> {n}
#     ** n개 이상          --> {n,} , 
#        n개 이상 m개 이하 --> {n,m} ,
#- ex) 7자리 이상인 수 : {7, }

text <- "2 96 4019 884863 56635574 946482 95325201 410505 5802 6661337 2937786 31103"
exp  <- "[0-9]{7,}"
stringr::str_extract_all(text, exp)[[1]]


# 11. ** 0또는 1개 --> ?
#     사용할 때 뒤에 배치시켜야 함
text <- "ac abc abbc abbbc abbbbbc"  
exp  <- "ab?c"
stringr::str_extract_all(text, exp)[[1]]

# 12. ** 조심해야 할 Tip
#- 수량자는 항상 가장 긴 부분과 매칭하려는 속성이 있음
#- 만약 방지하려면 제일 마지막에 ?를 붙여야 함
text <- "<html><head><Title>제목</head></html>"
exp1 <- "<.*>"
exp2 <- "<.*?>"

stringr::str_extract_all(text, exp1)[[1]]
stringr::str_extract_all(text, exp2)[[1]]

#- 13. 그룹 사용하기
#- at를 그룹핑해서 매칭 여부 확인
text  <- "catatatatatat"
exp   <- "c(at)+"
stringr::str_extract_all(text, exp)[[1]]

###############################
## 정규 표현식 예제 풀어보기 ##
###############################

#- 1. s는 1개 또는 2개의 숫자로 시작한다.
#-    그 다음, s에 4개 이상의 영어 소문자 알파벳이 온다.
#-    맨 마지막에는, 온점 .이 0개이거나 1개 있다.
#-    이외의 불필요한 문자가 있을 경우 모두 매치되지 않아야 한다.
test <- "12abcdefg."
exp = "^\\d{2}[a-z]{4,}[\\.]?$" 
stringr::str_extract_all(test, exp)[[1]]

#- 2. 전화번호를 찾아 010-****-1234 로 바꿔보기
stringr::str_replace("010-9119-7025", "^(010)\\D?\\d{4}\\D?(\\d{4})", "010-****-\\g<2>")





