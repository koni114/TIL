# 신뢰 구간 추정
# 신뢰구간(confidence interval) : 주어진 확률 1-a에 대하여 표본분포의 통계량이 모집단 모수에 포함되는 구간
# 신뢰계수(confidence coefficient) : n개의 확률표본을 추출하여 신뢰구간을 구하는 잡업을 N번 반복하여 얻은 N개의 신뢰구간 중 (1-a)% 미지의 모수 뮤가
#                              포함되어 있을 확률
#                              -> n개 확률 표본을 N번 반복하여 추출하고, 신뢰구간을 구했을때 모수 평균(뮤)가 포함되어 있을 확률
# 유의 수준(significance level) : n개의 확률표본을 추출하여 신뢰구간을 구하는 잡업을 N번 반복하여 얻은 N개의 신뢰구간 중 미지의 모수 M가 포함되어 있지 않을 확률
# 신뢰 한계(confidence limits) : 신뢰구간의 상하한 값

#' 위의 이론에 대한 simulation을 해보자
#' ex) X ~ N(mean=10, sd=3)인 정규분포에서 20개(n)의 확률표본을 추출하여 100번(N) 수행 했을 때 얻은 100개(N)의 신뢰구간
#'     중에서 95%의 신뢰계수(confidence coefficient, 1-a)만큼은 미지의 모수 M 가 포함되어 있고
#'     5%의 유의수준(significance level, a) 만큼은 미지의 모수 M가 포함되지 않는 경우를, R을 이용해서 simultation 수행


# confidence interval simulation, parameter setting
alpha <- 0.05
N     <- 100
n     <- 20
mu    <- 10
sigma <- 3


layout(matrix(1:2), heights = c(1,2))
x <- seq(0, 20, length = 100)
plot(x, dnorm(x, mean=10, sd=3), type='l', main="Normal distribution, X~N(10,3^2)")
abline(v=mu, col='red', lty=2)
abline(v=mu-1.96*3, col="red", lty=2)
abline(v=mu+1.96*3, col="red", lty=2)


# 확률표본(random sample) : 영어가 더 쉽다
# 확률표본이란 특정한 확률분포로부터 독립적으로 반복하여 표본을. 추출하는 것

# 단일 모집단의 모평균에 대한 신뢰구간 추정
#' 표본이 크고 정규성 충족 시,
#' t.test()      : 모평균
#' chisq.test()  : 모분산
#' prop.test()   : 모비율

#' 정규성 미충족 시,
#' wilcox.test() : 비모수 검정

#' 정규성 여부 검정
#' shapiro.test(), qqnorm(), qqline()

# 귀무가설 vs 대립가설
# 단측검정 vs 양측검정
# 검정통계량(test statistics) 과 p-value

#' ** P-value 해석 : 0.03라고 하는 것은 표본 개수를 임의 추출해서 100번 반복 조사를 해보면
#'                   약 3~4번 정도 귀무가설에 해당하는 값이 나온다는 의미


# Review 2019-05-21

#' is.na()를 이용할 때 내부적으로 df가 들어가는 경우,
#' 조심해야함. 
#' 어떤 데이터 형태가 들어올 것인가?
#' vector, dataframe 등, 어떤 형식이 들어올지를 모른다.
#' 그렇다면, 옳바른 DataFrame이 들어오는지를 정확하게 파악하려면 어떻게 해야하는가?
#' -> 왠만한건, is.data.frame 으로 확인!

all(is.na(iris))
all(is.na(df))
any(is.na(c(1,2,3,4,NA)))