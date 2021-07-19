#' stringr library를 통한 문자열 처리
#' stringr package가 제공되는 함수
#' - str_length(): 문자열 길이 반환 
#' - str_c(): 문자열 연결, str_join()의 개선형
#' - str_sub(): 범위에 해당하는 부분 문자열 생성
#' - str_split(): 구분자를 기준으로 문자열을 분리하여 부분 문자열 생성
#' - str_replace(): 기존 문자열을 특정 문자열로 교쳬
#' - str_extract(): 문자열에서 특정 문자열 패턴의 첫번째 문자열 추출
#' - str_extract_all(): 문자열에서 특정 문자열 패턴의 모든 문자열 추출
#' - str_locate(): 문자열에서 특정 문자열 패턴의 첫 번째 위치
#' - str_locate_all(): 문자열에서 특정 문자열 패턴의 모든 위치 찾기
library(stringr)
myStr <- "Hongkd1051Leess1002YOU25홍길동2005"
stringr::str_length(myStr)
stringr::str_locate(myStr, '홍길동')
stringr::str_sub(myStr, locate[1], locate[2])
stringr::str_to_upper(myStr)
stringr::str_to_lower(myStr)

myStr <- "Hongkd1051,Leess1002,YOU25,홍길동2005"
stringr::str_replace_all(myStr, 'Hong', 'KIM')
stringr::str_c(myStr,",이순신2019")

str1 <- c("홍길동","김길동","이순신","강감찬")
paste(str1,collapse=",")

myStr <- "Hongkd1051,Leess1002,YOU25,홍길동2005"

# 영문소문자 연속 3문자 추출
stringr::str_extract_all(myStr, "[a-z]{3}")

# 영문소문자 연속 3문자 이상 추출
stringr::str_extract_all(myStr, "[a-z]{3,}")

# 영문소문자 연속 3~5문자 추출
stringr::str_extract_all(myStr, "[a-z]{3,5}")

# 해당 문자열 추출
stringr::str_extract_all(myStr, 'Hong')

# 연속된 3개의 한글 문자 추출
stringr::str_extract_all(myStr, "[가-힣]{3}")

# 연속된 4개의 숫자문자 추출
stringr::str_extract_all(myStr, "[0-9]{4}")

# 영문 소문자 제외한 나머지 추출
stringr::str_extract_all(myStr, "[^a-z]")

# 한글을 제외한 나머지 연속된 5개 추출
stringr::str_extract_all(myStr, "[^가-힣]{5}")

# 숫자를 제외한 나머지 연속된 3개 추출
stringr::str_extract_all(myStr, "[^0-9]{3}")

# w는 한글,영문자,숫자문자를 포함하지만 특수문자는 제외
stringr::str_extract_all(myStr, "\\w{6}")

#- 하나의 컬럼에 있는 데이터를 쪼개 두 개의 컬럼으로 생성
test <- c('hello/world', 'my/name', 'is/HJH')
do.call('rbind', strsplit(test, '/')) %>% data.frame %>% rename(first_name = X1, last_name = X2)



