###############
## 연관 분석 ##
###############
#' 연관 규칙이란, 항목들 간의 '조건-결과'식으로 표현되는 유용한 패턴을 말함
#' 이러한 패턴, 규칙을 발견해내는 것을 연관 규칙(association rule)이라고 함
#' 장바구니 하나에 해당하는 정보를 트랜잭션(transaction)이라고 함
#' 우리가 일반적으로 잘 알고있는 연관 규칙은 크게 의미가 없음

## 연관규칙의 측정지표
# 1. 지지도(support)
# 전체 거래 품목 중에서, A, B가 동시에 포함되는 거래의 비율
# 전체 거래 중 품목 A와 B를 동시에 포함하는 거래가 어느 정도인지를 나타내주며, 전체 구매 경향을 파악할 수 있음
# 지지도 = P(A n B) = A와 B가 동시에 포함된 거래수 / 전체 거래 수

# 2. 신뢰도(confidence)
# 품목 A가 포함된 거래 중에서 품목 A, B를 동시에 포함하는 거래일 확률
# 신뢰도 = P(A n B) / P(A) = A와 B가 동시에 포함된 거래 수 / A를 포함하는 거래 수

# 3. 향상도(lift)
# 품목 B를 구매한 고객 대비 품목 A를 구매한 후 품목 B를 구매하는 고객에 대한 확률을 의미
# 향상도가 1보다 크면, 두 품목간의 연관성이 매우 높음을 의미
# 향샹도가 1이면 두 품목이 독립적인 관계를 가짐
# 향상도가 1보다 작으면, 두 품목간의 연관성이 없음
# 향상도 = P(B|A)/P(B) = P(AnB)/P(A)P(B) = 

#' 최소 지지도를 정해 규칙을 도출
#' 지지도를 높은 값에서 낮은 값으로 10%, 5%, 1%, 0.1%와 같이 낮추어가며 실행해야 효율적임

####################
## 연관 분석 절차 ##
####################
# 최소 지지도를 갖는 연관규칙을 찾는 대표적인 방법인 Apriori 알고리즘이 있음
# 최소 지지도보다 큰 집합만을 대상으로 높은 지지도를 갖는 품목 집합을 찾는 것
# 분석 절차는 다음과 같음
#- 최소 지지도를 설정
#- 개별 품목 중에서 최소 지지도를 넘는 모든 품목을 찾음
#- 2에서 찾은 개별 품목만을 이용하여 최소 지지도를 넘는 2가지 품목 집합을 찾음
#- 위 두 절차에서 찾은 품목 집합을 결합하여 최소 지지도를 넘는 3가지 품목 집합을 찾음
#- 반복적으로 수행해 최소 지지도가 넘는 빈발품목 집합을 찾음

##########
## 실습 ##
##########
#- 연관 분석을 위해 실습할 데이터는 arules 패키지 내에 있는 Adult 데이터
#- Adult 데이터는 여러 변수들을 통해서 연소득이 large인지 small인지 예측하기 위한 트랜잭션 형태의 미국 센서스 데이터
install.packages("arules")
library(arules)
data(Adult)

#- apriori function을 통한 연관 규칙 추출
rules <- apriori(Adult)

#- inspect 함수를 사용하면 apriori 함수를 통해 발굴된 규칙을 보여줌
#- 아래는 일부 결과만 확인
#- 아래는 발굴된 규칙 중에 일부만 본 것
#- 결과를 보면 lhs에 해당하는 항목이 없는 경우, rhs(right-hand-side) 결과가 나타나는 무의미한 결과가 나타남
#- 이를 방지하기 위해 지지도, 신뢰도를 조정하여 규칙을 발굴해야 함
inspect(head(rules))

#- 신뢰도, 지지도 값을 지정하여 좀 더 유의미한 결과가 나올 수 있도록 함
#- rhs를 income 변수에 대해서 small인지, large인지 규칙만 나올 수 있도록 하여 income 변수에 대한 연관 규칙만 출력
adult.rules <- apriori(Adult, 
                       parameter  = list(support=0.1, confidence = 0.6),
                       appearance = list(rhs=c('income=small', 'income=large'), default = 'lhs'),
                       control    = list(verbose = F))

adult_ruled_sorted <- sort(adult.rules, by = 'lift')

inspect(head(adult.rules))

#- 연관 규칙 시각화 패키지로, 확인 가능
install.packages("arulesViz")
library(arulesViz)
plot(adult_ruled_sorted, method = "scatterplot")
plot(adult_ruled_sorted, method = "graph", control = list(type='items', alpha = 0.5))







