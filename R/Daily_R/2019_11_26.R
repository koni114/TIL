# 2019_11_26.R
# Caret package 완벽 정리
# https://lovetoken.github.io/r/machinelearning/2017/04/23/caret_package.html 블로그를 참조했음을 밝힙니다.
# https://goodtogreate.tistory.com/entry/Caret%EC%9D%98-%EC%9D%B4%ED%95%B4 블로그를 참조했음을 밝힙니다.

# caret : Classification And Regression Training 의 앞글자를 따와 명명
library(caret)
library(dplyr)
library(mlbench)
library(e1071)
library(klaR)
library(pls)
library(ipred)
library(randomForest)

set.seed(1234) 
data(Sonar, package = "mlbench")

Sonar <- Sonar %>% tbl_df

# 1. createDataPartition() function ----
# 일정 비율의 train/test data로 나누어주는 function

# Sonar data를 70 : 30 비율로 나눠보자
# 1.1 sample 함수를 이용한 파티셔닝

indexTrain <- sample(1:nrow(Sonar), round(nrow(Sonar) * .7))

# 1.2 createDataPartition function을 이용한 파티셔닝
# 기본 return 타입이 list 이므로 F로 설정 필요

indexTrain <- createDataPartition(Sonar$Class, p = .7, list = F)
training   <- Sonar[ indexTrain, ]
testing    <- Sonar[-indexTrain, ]

# caret, 머신러닝 알고리즘별 최적의 모수를 찾기 위한 학습방법 설정
# 알고리즘별로 튜닝 파라미터 개수는 달라지는데, p개의 파라미터인 경우 3^p 의 그리드를 탐색하여 후보 모델들을 테스트하게 됨
# ex1) KNN는 K 하나인 단모수이므로 3^1 = 3인 3가지 K 값들을 후보로 두고 모델을 비교하게 됨
# ex2) RRLDA(Robust Regularized Linear Discriminant Analysis)의 경우 모수의 개수가 lambda, hp, penalty 총 3개인데, 3^3 = 27가지 후보군을 비교하게 됨

# 2. trainControl function ----

# cross validation을 할 수 있게끔 도와주는 function
# 예제. 10-fold cross validation을 5번 반복하여 좋은 후보의 파라미터 그리드를 찾게 해주는 일종의 장치를 만드는 코드
fitControl <- trainControl(method = "repeatedcv", number = 10, repeats = 5)

# fitControl 객체는 추후에 학습 과정에서 사용하게 됨

# 3. train function ----
# 학습을 위한 표준화된 인터페이스 함수
# method 인자만 바꿔주면 원하는 학습모델 알고리즘을 구현할 수 있게 됨

# 예제. randomForest 를 통해 훈련데이터셋 학습하기
# 3.1 method 지정 : method parameter에 'rf' 지정

# RF에서 Tuning parameter에 해당되는 'mtry'는 10-fold cross validation을 5번 반복하여 
# 가장 좋게 평가된 것을 선택하는 후보채택방법인 fitControl 객체를 trControl 인자에 입력

# verbose : TRUE 시, mtry 선정 과정이 모두 출력됨

rf_fit <- caret::train(
  
  Class ~ .
  , data      = training
  , method    = "rf"
  , trControl = fitControl
  , verbose   = F
  
)

# 테스트셋에 적용하여 정확도 확인
# confusionMatrix function - Confusion Matrix 및 정확도와 다양한 통계량까지 출력.
# 이때 predict function은 우리가 일반적으로 사용하는 predict function

predict(rf_fit, newdata = testing) %>% confusionMatrix(testing$Class)

# 4. expand.grid function ----
# Tuning parameters 의 그리드 조정
# 최적 파라미터 선정 시 탐색범위와 그리드를 수동으로 조절할 수 있음
# 즉, 더 많은 후보를 설정하기 위해 사용

# 예제. mtry의 후보를 1, 2, 3, 4, 5, 6, 7, 8, 9, 10로 바꾸어 설정하고 이 중에서 채택하는 예제

customGrid <- expand.grid(mtry = 1:10)

rf_fit2 <- train(  Class ~ ., data = training
                   , method = "rf"
                   , trControl = fitControl
                   , tuneGrid = customGrid
                   , verbose = F)


# 5. 랜덤 검색 그리드(random selection of tuning parameter combinations)
# 튜닝 파라미터의 개수가 많으면 많아질수록 탐색 그리드의 개수는 지수적으로 증가하게 되고, 
# 동일한 간격의 그리드 구성으로 인해 탐색과정이 비효율적으로 될 수 있음

# 예제. 튜닝 파라미터가 2개인 RDA(Regularized Discriminant Analysis)로 훈련해보기

rda_fit <- train(  Class ~ .
                   , data      = training
                   , method    = "rda"
                   , trControl = fitControl
                   , verbose   = F)

# 결과를 확인해보면, 9개의 파라미터 조합을 비교하는 것을 볼 수 있음
# 랜덤 검색 그리드를 이용하면 동일간격 조건을 파괴시켜 파라미터 조합을 구성

# trainControl function의 search = 'random'을 통해 검색 타입을 랜덤으로 바꿈

fitControl <- trainControl(  method  = "repeatedcv"
                             , number  = 10
                             , repeats = 5
                             , search  = "random")

# 다시 학습
rda_fit2 <- caret::train(  Class ~ .
                           , data      = training
                           , method    = "rda"
                           , trControl = fitControl
                           , verbose   = F)

# gamma, lamda가 랜덤으로 구성되어 있는 것을 확인할 수 있음
# ** train 함수의 .tuneLength 인자를 사용하면, 튜닝파라미터 조합개수를 늘릴 수 있음
rda_fit2 <- caret::train(    Class ~ .
                             , data       = training
                             , method     = "rda"
                             , trControl  = fitControl
                             , tuneLength = 50
                             , verbose    = F)


# modelLookup function ----
# 특정 모델에서 지원하는 hyper param을 잊었을 경우 사용
# naive bayes model에서 지원하는 parameter 명을 확인

modelLookup("nb")


# 5.VarImp function ----
# 해당 알고리즘의  변수 중요도 계산

# 5.1. binary classification
# 만약 Model에서 제공해주는 importance 측정 방법이 존재하지 않는다면,
# 각 predictor의 importance는 filter를 적용하여 평가 가능

# Roc Curve 분석을 각각의 predictor에 적용하게 됨
# Roc Curve의 면적을 사다리꼴 면적 구하는 식으로 계산하여 이 면적의 값이 variable importance가 됨

# 5.2 multi classification
# 각각의 class를 분리하고 class들의 쌍을 만든다.
# 각 class들에 대해서 최대 curve 면적을 가지는 것을 variable importance로 규정

# 5.3 regression
# 회귀식의 기울기를 이용하거나 R Square를 이용함

# 일반적으로 Kappa 통계량 사용
#  scale = True 주면 0~ 100사이의 값 return
varImp(sms_model1, scale=FALSE)

# filterVarImp function ----
# area under the ROC Curve를 각각의 predictor에 대해서 구하고 싶을 경우, filterVarImp를 사용하게 됨 
RocImp <- filterVarImp(x = training[, -ncol(training)], y = training$Class)
RocImp


## VarImp function을 통해 다변량 인자 탐지 가능한 algorithm list

# 1. Linear Model(lm function)
m.lm    <- lm(V2 ~., data = training)
imp.lm  <- varImp( m.lm ,scale = T)


# 2. Ridge Model(glmnet function) 
# varImp 사용시, lambda value 지정해주어야 함. glmnet function 사용시 alpha = 0
rgm  <- glmnet(
  x      = as.matrix(training[, -1])
  , y      = training[, 1]
  , alpha  = 0
  , family = "gaussian")

imp.ridge <- varImp(  rgm
                      , lambda  = min(rgm$lambda)
                      , scale   = T)


# 3. LASSO Model(glmnet function)
# varImp 사용시, lambda value 지정해주어야 함. glmnet function 사용시 alpha = 1 
lam  <- glmnet(
  x      = as.matrix(training[, -1])
  , y      = training[, 1]
  , alpha  = 1
  , family = "gaussian")

imp.lasso <- varImp(    lam
                        , lambda = min(lam$lambda)
                        , scale  = T)


# 4. ElasticNet Model(glmnet function)
# varImp 사용시, lambda value 지정해주어야 함. glmnet function 사용시 alpha = 0.5 

elsm  <- glmnet(
  x      = as.matrix(training[, -1])
  , y      = training[, 1]
  , alpha  = 0.5
  , family = "gaussian")

imp.lasso <- varImp(    elsm
                        , lambda = min(elsm$lambda)
                        , scale  = T)


# 5. Partial Linear Sqaures(PLS)

mm.pls  <- plsr(  , data = training)


# 6. logistic Model

glm(   f        = 
         , data   = training
       , family = "binomial")

## 7. SVM

train(  f           = 
          , data      = training
        , method    = "svmLinear2",
        tuneGrid  = NULL
        , trControl = trCtl)

## 8. Naive Bayes

trCtl <- trainControl(  method          = "cv"
                        , number        = 2
                        , p             = 0.7
                        , allowParallel = F)


m.nb <- caret::train(     f  = 
                            , data    = training
                          , method  = "naive_bayes",
                          trControl = trCtl)


## 9. Bagging
m.bagg   <- bagging(, training, nbagg = 3)
imp.bagg <- varImp(m.bagg)


## 10. RandomForest 

m.rf     <- randomForest(f = fmla, data = rf_train, importance = TRUE)
