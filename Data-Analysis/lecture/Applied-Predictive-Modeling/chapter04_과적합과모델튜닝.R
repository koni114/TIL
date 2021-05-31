##################################
## chatper04. 과적합과 모델튜닝 ##
##################################
#- 신용평가예제에서 사용한 데이터 사용

library(AppliedPredictiveModeling)
data(twoClassData)

#- 예제 데이터
#- 예측 변수는 predictors라는 dataframe에 들어가 있음
#- 예측 변수 두 col와 각 행별 208개의 row sample로 구성
#- 결과 class --> classes 라는 factor형 vector
head(predictors)
str(classes)

#- sample              : 임의 샘플링
#- createDataPartition : 층화 임의 샘플링

set.seed(1)
trainingRows <- caret::createDataPartition(
  classes,
  p = 0.80,
  list = F
)

trainPredictors <- predictors[trainingRows, ]
trainClasses    <- classes[trainingRows]

testPredictors  <- predictors[-trainingRows, ]
testClasses     <- classes[-trainingRows]

# 최대 비유사도 샘플링 방식 사용
# caret::maxdissim function 사용

##############
## 리샘플링 ##
##############
# 반복 훈련/테스트 세트 분할
set.seed(1)
library(caret)
repeatedSplits <- createDataPartition(
  trainClasses, 
  p = 0.80,
  times = 3      #- times : 여러 개로 분할 가능
  )

# bootstrap 
# caret::createResamples
# k-겹 교차 검증 
# caret::createFolds
# 반복 교차 검증
# caret::createMultiFolds

#- k-fold cross validation example
set.seed(1)
cvSplits <- caret::createFolds(
  trainClasses,
  k = 10,
  returnTrain = T
)
str(cvSplits)
fold1 <- cvSplits[[1]]
cvPredictors1 <- trainPredictors[fold1, ]
cvClasses     <- trainClasses[fold1, ]

######################
## 기본적 모델 구축 ##
######################
# train dataset을 통해 5개의 knn model 생성
# test dataset을 통해 성능 평가
# caret::knn3 function : class별 이웃의 비율에 따라 클래스 예측

trainPredictors <- as.matrix(trainPredictors)
knnFit          <- knn3(
  x =  trainPredictors,
  y =  trainClasses,
  k = 5 
)

testPredictors <- predict(
  knnFit, 
  newdata = testPredictors, 
  type = 'class')

head(testPredictors)
str(testPredictors)



