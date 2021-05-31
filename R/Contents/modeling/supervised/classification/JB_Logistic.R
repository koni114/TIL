## 로지스틱 회귀 분석

a         <- iris %>% filter(Species == 'setosa' | Species == 'versicolor')
a$Species <- as.factor(a$Species)
b         <- glm(Species ~ Sepal.Length, data = a, family = binomial)
summary(b)

# 회귀계수 검정에서 p-값이 거의 0 이므로, Sepal.Length가 매우 유의한 변수이며,
# Sepal.Length가 한 단위 증가함에 따라 Versicolor일 오즈가 exp(5.140) := 170배 증가함을 알 수 있음

# Residual deviance는 예측변수 Sepal.Length가 추가된 적합 모형의 이탈도를 나타냄
# Null deviance에 비해 자유도 1 기준에 이탈도의 감소가 74.4 정도의 큰 감소를 보이며, 
# 귀무가설이 기각되지 않으며 적합값이 관측된 자료를 잘 적합하고 있다고 말할 수 있음 

# 로지스틱 회귀 계수
coef(b)

# 오즈의 증가량 exp(B)
exp(coef(b)["Sepal.Length"])

# 회귀계수 beta와 오즈의 증가량 exp(B)에 대한 신뢰구간
confint(b, parm = "Sepal.Length")
exp(confint(b, parm = "Sepal.Length"))

# fitted() 함수를 통해 적합 결과 확인
fitted(b)[c(1:5, 96:100)]
predict(b, newdata = a[c(1, 50, 51, 100), ], type = "response")

# 적합된 로지스틱 회귀 모형의 그래프
plot(a$Sepal.Length, a$Species, xlab = "Sepal.Length")
x = seq(min(a$Sepal.Length), max(a$Sepal.Length), 0.1)
lines(x, 1+(1/(1+(1/exp(-27.831 +5.140*x)))), col = "red")

#############################
## 다중 로지스틱 회귀 분석 ##
#############################
# vs      -> 종속변수
# mpg, am -> 독립변수

str(mtcars)
glm.vs <- glm(vs ~ mpg + am, data = mtcars, family = binomial)
summary(glm.vs)

# 다중 로지스틱 회귀계수에 대한 해석
## mpg
# 다른 모든 변수들이 고정된 상태에서 mpg 값이 한단계 증가함에 따라
# vs가 1일 오즈가 exp(0.6809) ~= 1.98배 증가
## am 
# 다른 모든 변수들이 고정된 상태에서 am 값이 한단계 증가함에 따라
# am가 1일 오즈가 exp(-3.0073) ~= 0.05배, 즉 95% 감소

######################################
## 다중 회귀 분석의 변수선택법 적용 ##
######################################
# 'both', 'backward', 'forward'
step(glm.vs, direction = 'forward')

# anova 함수는 모형의 적합(변수가 추가되는) 단계별로 이탈도의 감소량과 유의성 검정 결과를 제시해 줌
# 결과적으로 mpg와 am을 차례로 추가했을 때 통계적으로 유의함을 알 수 있음 
anova(glm.vs, test = 'Chisq')



