## 2019_06_03
# 비모수 검정
# 
# H0: 정규성
# H1: 정규성을 가지지 않음

# 비모수 검정 사용
# 모집단에 대한 특정 분포를 가정하지 않음
# 표본 크기가 작고, 치우쳐 있거나 표본에 특이치가 여러 개 포함되어 있는 경우 특히 유용

# 일표본 Z검정, 일표본 T검정 -> 1표본 부호 검정, 1표본 Wilcoxon검정
# 2표본 t검정                -> Mann-Whitney 검정
# 분산 분석 검정             -> Kruskal-Wallis 검정, Mood의 중위수 검정, Friedman 검정

# 비모수 검정에서도 데이터는 독립적인 랜덤 표본이여아 함

# ** 비정규 데이터 변환
# 제곱근, 로그, 누승, 역수, 아크사인 등 다양한 함수를 사용하여 데이터 변환 가능

# 1. 우로 치우침 -> 로그 변환
# 2. 좌로 치우침 -> 제곱, 세제곱 변환

# 3. Tukey Ladder of Power 변환
# 단일 변수 정규 변환 : 람다 값을 변환하면서 데이터의 정규성 검정을 실시하여 최적의 람다 값을 찾음
# ANOVA (선형 모형) : 잔차의 정규성 검정 -> 최적의 람다를 찾고 종속변수를 변환하여 다시 분석
# 선형 모형에서는 종속변수만의 변환은 오차 분산의 변동을 초래. -> 모든 설명변수 포함 모든 변수를 개별적 정규변환 필요

# 4. Box-Cox 변환
# x' = (x^람다 - 1) / 람다
# Tukey 변환과 동일하지만, 최적의 람다 값은 MLE 방법에 의해 찾음
# 단일 변수 정규성 변환에서는 Tukey 방법이, ANOVA에서는 Box-Cox 변환이 적절

# **** 정규변환 예제
# 예제 데이터
data(airquality)

# 히스토그램 그리기
install.packages("rcompanion")
library(rcompanion)
.libPaths()

plotNormalHistogram(airquality$Ozone)

library(nortest)

# Anderson-Darling Test
ad.test(airquality$Ozone) # 0.01보다 작으므로, 귀무가설 기각(정규성X)

# shapiro wilk
shapiro.test(airquality$Ozone)

# ** Tip
# rversion 3.5.0 이상이어야 rcompanion 설치 가능
# --> dependency 에서 mvtnorm package가 걸림