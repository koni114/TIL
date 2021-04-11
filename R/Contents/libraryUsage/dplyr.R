# dplyr package 정복하기
# 기본적으로 dplyr에서 열을 선택할때, 따옴표 사용하지 않는다
# but, 함수 내에 함수를 사용하여 조건을 거는 경우, 따옴표 사용(예외도 있음)
library(dplyr)

# 0. chain operator : %>%
# chain operator 를 사용하면 연속적으로 함수가 적용된 data를 계속 사용할 수 있음
# ** 단축키: ctrl + shift + M

# 1. filter(): 조건 별로 filtering : 결과 값은 조건이 적용된 filtering 된 dataFrame으로 편성 ----
iris %>% filter(Sepal.Length < 5.0 & Petal.Length > 3.0)

# 2. slice() : index를 이용하여 행을 slicing 할 때 사용 ----
iris %>% slice(1:10) 

# 3. select() : 열을 선별 할 때 사용 ----
iris %>% select(Sepal.Length, Petal.Length)

# 3.1. starts_with("문자") : 해당 문자열로 시작하는 열 선택
iris %>% select(starts_with("Sepal"))

# 3.2. ends_with("문자") : 해당 문자열로 끝나는 열 선택
iris %>% select(ends_with("Length"))

# 3.3 contains("") : 해당 문자열이 포함되는 열 선택
iris %>% select(contains("Sep"))

# 3.4 matchs() : 정규 표현식에 해당하는 컬럼 선택

# 3.5 one_of() : 변수 이름 글부에 포함된 모든 열 선택
# ** 그냥 select만을 사용하는 것과의 차이점 : one_of()를 사용하면 해당 조건의 열이 하나도 없더라도 error를 발생시키지 않음
vars <- c("test1", "test2", "test3")
iris %>% select(one_of(vars))  # warning만 발생시키고, row 0 retrun
iris %>% select(vars)  # error 발생

# 3.6 num_range() : (특정 접두사 + 숫자 범위)를 이용하여 열을 찾을 때
iris %>% select(num_range("V", 2:3))

# 4. rename() : 컬럼 명을 변경 ----
# ** 주의 reshape::rename 과 겹치지 않게 주의!! 
# reshape::rename 은 컬럼명에 따옴표 포함 O
# dplyr::rename 은 컬럼명에 따옴표 포함 X

iris %>% rename(V10 = Sepal.Length, V20 = Sepal.Width)

# 5. distinct() : 중복없는 유일한 값을 추출 ----

# dplyr::distinct() VS base::unique()

# 5.1. 성능 
#           dplyr::distinct() -> 빠름 
#           base::unique()    -> 느림

# 5.2. return type - 변수(열) 한개 선택할 때  
#            dplyr::distinct() -> data.frame
#            base::unique()    -> vector

iris %>% distinct(Sepal.Length)
unique(iris[,c("Sepal.Length", "Petal.Length")])
unique(iris[,"Sepal.Length"])

# 6. 샘플링 ----
# 6.1. sample_n() : 무작위로 n 개수 만큼 추출
#                   replace = T : 복원 추출                     
iris %>% sample_n(20, replace = T)  # 무작위로 20개, 복원 추출  

# 6.2. sample_frac() : 무작위(비율로 계산) 비율 만큼 추출
iris %>% sample_frac(0.2, replace = F)  #  무작위로 20%, 비복원 추출

# 6.3. 집단별 층화 추출 : group_by() 이용
iris %>% group_by(Species) %>% sample_n(10)  # Species 별로, 10개씩 층화 추출

# 7. mutate(), transmute() : 파생 변수 생성
# 7.1. mutate()     : 기존변수 + 신규변수까지 저장
# 7.2. transmute()  : 신규변수 저장

iris %>% mutate(sum = Sepal.Length + Sepal.Width + Petal.Length + Petal.Width)     # 기존변수 + 파생변수 저장
iris %>% transmute(sum = Sepal.Length + Sepal.Width + Petal.Length + Petal.Width)  # 파생변수만 저장

# 8. 요약 통계 계산 : summarise ----
iris %>% summarize(
                    mean.Sepal.Length = mean(Sepal.Length),
                    mean.Petal.Length = mean(Petal.Length)
                   )

# 9. bind_rows(): 행 기준으로 dataFrame 병합 ----
# rbind() 와 유사한 기능 수행, 두 개의 함수를 비교하면서 예시 진행

df.1 <- data.frame(x = 1:3, y = 1:3) 
df.2 <- data.frame(x = 4:6, y = 4:6)
df.3 <- data.frame(x = 7:9, z = 3:1)

bind_rows(df.1, df.2)
rbind(df.1, df.2)

# bind_rows() vs rbind()

# 9.1. 열 매칭 여부  
#              bind_rows()  : 두 개의 dataFrame이 완벽히 매칭 되지 않아도 병합 됨. 열이 일치하지 않는 경우, NA 처리
#                             Outer Join과 비슷한 개념
#              rbind()      : 열이 완벽히 일치하지 않으면, error 발생

bind_rows(df.1, df.3)  # y와 z 컬럼이 일치하지 않는 경우에도 error를 발생시키지 않고 NA 처리 후 병합
rbind(df.1, df.3)      # error 발생

# 9.2. 합치기 전 원천 dataFrame 의 여부 파악
#              bind_rows()  : id parameter 를 이용해 합치기 전 dataFrame 알 수 있음. 약간의 트릭 필요
#              rbind()      : 알 수 없음

bind_rows(list(grp_1 = df.1, grp_2 = df.2), .id = "group_id")  # .id 임을 조심하자
rbind()  # 불가능

# 9.3. 처리 속도
#              bind_rows()  : 속도가 훨씬 빠름(약 261배)
#              rbind()      : 느림

one <- data.frame(c(x = c(1:1000000), y = c(1:1000000)))
two <- data.frame(c(x = c(1:1000000), y = c(1:1000000)))

system.time(rbind(one, two))      # 21초
system.time(bind_rows(one, two))  # 0.17초

# 10. bind_cols()  : 열 기준으로 dataFrame을 합칠 때 ----
# bind_rows() 와 대부분 유사.
# ** 다른점 -> bind_rows와 다르게 행의 개수가 같아야만 병합 가능

# 11. all_equal() : 두 개의 dataFrame 을 비교 할 때 ----
# 해당 function 사용 시, dataFrame 의 row, column 순서도 확인하면서 같은지 check 가능
#  -> ignore_row_order, ignore_col_order 를 param으로 이용하여 확인 가능

all_equal(target, current, # two data frame to compare
          ignore_col_order = TRUE, # TRUE : 열 순서 무시 -> 순서가 달라도 같으면 TRUE return
          ignore_row_order = TRUE, # TRUE : 행 순서 무시 -> 순서가 달라도 같으면 TRUE return
          convert = FALSE # Should similar classes be converted? 
                          # Currently this will convert factor to character and integer to double.?)
          )

# 12. cumall(), cumany() : 그룹 별로 조건 확인 후, slicing 하고 싶을 때 ----
# 12.1. cumall() : 그룹 별 해당 조건이 하나라도 일치하지 않으면 전부 제외 -> filter 함수 내부적으로 사용
iris %>% group_by(Species) %>% filter(cumall(Sepal.Length > 3.0)) # 모든 종에 대해서, 3.0 보다 크므로 전부 출력 
                                                                  

# 12.2. cumany() : 그룹 별 해당 조건이 한개라도 맞는 것이 있으면 전부 출력 -> filter 함수 내부적으로 사용
iris %>% group_by(Species) %>% filter(cumany(Sepal.Length > 5.0)) # 모든 종에 대해서, Sepal.Length 값이 한 개라도 5.0 보다 큰 것이
                                                                  # 있으므로, 전부 출력
# 13. cummean() : 특정 값을 누적해 가면서 mean 반환 ----
iris %>% mutate(cummean.iris = cummean(Sepal.Length))

# 14. recycled aggregates : 요약한 통계량을 다시 조건으로 사용하고 싶은 경우 ----
iris %>%  group_by(Species) %>% filter(Sepal.Length > mean(Sepal.Length))  # Species 별로 Sepal.Length 의 평균 값보다 큰 row를 출력

# 15. window function : n개의 행을 input으로 받아 변환된 n 개의 행 output으로 만들어주는 함수 ----

# 15.1. lead() : <- 으로 땡기고 싶을 때,  lead 한다! 1번이 10번을 땡긴다! 라고 외워보자
x <- c(1:10)  # 1~10까지의 vector 제작
lead(x, 2)    # 2만큼 <- 으로 땡겨서 return

# 15.2. lag() : -> 으로 땡기고 싶을 때,
x <- c(1:10)  # 1~10까지의 vector 제작
lag(x, 2)     # 2만큼 -> 으로 땡겨서 return