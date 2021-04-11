install.packages("AppliedPredictiveModeling")
library(AppliedPredictiveModeling)

# apropos function
# 관심있는 class나 함수를 찾는데 유용한 함수
apropos("confusion")

# RSiteSearch function
# 모든 패키지 중에서 함수를 찾아야 할 경우
RSiteSearch("confusion", restrict = "functions")

# data 항목
# 각 세포 구분 인자(Cell)과 어떤 세포가 잘 구분됐는지를 나타내는 요인 백터(Class)
# Case 변수는 어떤 세포가 훈련 세트나 테스트 세트에 사용됐는지를 나타냄

data("segmentationOriginal")
segData <- subset(segmentationOriginal, Case == "Train")
cellID  <- segData$Cell
class   <- segData$Class
case    <- segData$Case
segData <- segData[, -c(1:3)]

# 원본 데이터에는 예측 변수의 바이너리 형태인 여러 "상태(status)" 관련 컬럼이 포함돼 있음
# 이 컬럼들을 제거하려면 컬럼 이름에 "Status"가 포함된 컬럼을 찾아야 함. 이들을 제거하자
statusColNum <- grep("Status", colnames(segData))
segData      <- segData[,-statusColNum]

##########
## 변환 ##
##########
# 어떤 항목들은 한쪽으로 많이 치우쳐져 있음.
# 각 예측 변수별 샘플의 왜도를 계산
library(e1071)
skewness(segData$AngleCh1)  # 하나의 컬럼만 변환하는 경우
skewValues <- apply(segData, 2, skewness)
head(skewValues)

# caret package의 BoxCoxTrans function을 통해 적절한 변환법을 찾은 후,
# 이 방법을 적용해 새 데이터를 만들어 줌
library(caret)
Ch1AreaTrans <- BoxCoxTrans(segData$AreaCh1)
predict(Ch1AreaTrans, head(segData$AreaCh1))

# prcomp function을 이용하여 PCA 적용
# 중심화 및 척도화 진행
pcaObject <- prcomp(
  segData,
  center = T,
  scale  = T
       )

# 각 요소별 분산의 누적 비율 계산
percentVariance <- pcaObject$sd^2 / sum(pcaObject$sd^2)*100
percentVariance[1:3]

# 변환된 값은 x라고 불리는 하위 객체 형태로 저장
head(pcaObject$x[, 1:5])

# rotation 행은 예측 변수에 대응. 열을 객체에 대응하는 형태
head(pcaObject$rotation[,1:3])

#############
# 공간 변형 #
#############

s
# caret::spatialSign function : 공간 형태 변환

###############
# 다양한 변환 #
###############
# caret::preProcess 사용
# ex) Box-Cox 변환 -> 중심화 -> 척도화 -> PCA 적용
trans <- preProcess(
  segData,
  method = c("BoxCox", "center", "scale", "pca"))
transformed <- predict(trans, segData)
head(transformed[, c(1:5)])

##########
# 핕터링 #
##########
#  caret::nearZeroVar function
# 3.5장에 나왔던 법칙을 적용하는 0에 가까운 분산을 찾는 함수
nearZeroVar(segData)

# 예측 변수 간 상관관계를 기준으로 변수 filtering
correlations <- cor(segData)
dim(correlations)
correlations[1:4, 1:4]

# corrplot::corrplot function
# 데이터의 상관관계 구조를 시각적으로 확인
corrplot::corrplot(correlations, order = 'hclust')

# findCorrelation function
# 3.5장에 나오는 상관변수 filtering algorithm 적용
# 대상 예측 변수 후보를 고른 후, 해당 열의 번호 반환
highCor <- findCorrelation(correlations, cutoff = 0.7)
length(highCor)
filteredSegData <- segData[,-highCor]
