#####################################
## DMwR::knnImputation source 분석 ## 
#####################################

# process 간단 정리
# input data 
# - data    : 거리를 계산하기 위한 dataset
# - k       : 결측치 대체 할 때, 가장 가까운 거리에 위치하는 데이터 몇 개를 가지고 계산할 것이냐? --> k로 설정 
# - scale   : 수치형 데이터에 대한 정규화 여부. --> 일반적으로 거리 기반의 계산은 정규화 해주는 것이 맞음(default = T)
# - meth    : weighAvg, median 이 있음. 
#    - weighAvg : k개데 데이터 중  거리 기반한 가중 평균 이용. 계산식 exp(-x)
#    - median   : k개의 데이터 중 median 값을 계산하여 대체 
# - distData : 이웃을 찾는데 반드시 사용되는 data를 지정할 수 있음. 지정하면 결측 처리 데이터(data), 거리 계산할 데이터(distData)로 구분

#- knnImputation function process
#- 1. 수치형 변수는 scale = T 인 경우, 정규화 수행
#- 2. 범주형 변수는 level로 변경(1, 2, 3..)
#- 3. 결측이 있는 값 --> nas, 결측이 없는 값 --> xcomplete
#- 4. scale function을 통해 유클리디안 거리 계산
#- 5. 거리 계산을 통해 가장 가까운 k 개수 만큼 data select
#    - 이 때 거리 계산은 결측이 있는 데이터 1 row <--> 결측이 없는 나머지 row 의 모든 col 별로 제곱 값을 더한후 제곱근으로 계산.
#- 6. 결측치 대체시, 가중평균(exp(-x)), 또는 median으로 계산

# 특이사항
# - distData와 data는 rbind가 성립해야 함 --> 완벽히 data의 column이 동일해야 한다는 의미

# 해당 library 문제점.
#- 결측치를 complete.cases function을 이용해서 제거 한 후 xcomplete data.frame 을 만들어 냄.
#- 결측치를 제거 한 후 데이터가 없거나, k수 보다 적으면 error 발생

#- k를 입력 받을 수 있는데, 입력 받지 못한 경우 sqrt(nrow(data)) 로 기본 setting 하자.
#- 해당 함수에서 k의 default값은 10

# 사용자가 선택한 컬럼만 결측치를 처리 해야 함
# knnImputation 함수에 data를 통으로 넣을 경우 전부 결측 처리가 돼서 return 됨 
knnImputation <- function (data, k = 10, scale = T, meth = "weighAvg", distData = NULL) 
{
  n <- nrow(data)                  
  
  #- distData가 있으면, distInit을 distData 행 부터 지정
  if (!is.null(distData)){ 
    distInit <- n + 1
    data <- rbind(data, distData)
  }else distInit <- 1
  
  #- 수치형 데이터 --> scale 변환 
  N <- nrow(data)
  ncol <- ncol(data)
  nomAttrs <- rep(F, ncol)
  for (i in seq(ncol)) nomAttrs[i] <- is.factor(data[, i])
  nomAttrs <- which(nomAttrs)
  hasNom <- length(nomAttrs)
  contAttrs <- setdiff(seq(ncol), nomAttrs)
  dm <- data
  if (scale) dm[, contAttrs] <- scale(dm[, contAttrs])
  
  #- 범주형 데이터 --> integer로 변환
  if (hasNom) for (i in nomAttrs) dm[, i] <- as.integer(dm[, i])
  dm <- as.matrix(dm)
  nas <- which(!complete.cases(dm))
  
  
  if (!is.null(distData)) tgt.nas <- nas[nas <= n] else tgt.nas <- nas
  if (length(tgt.nas) == 0) warning("No case has missing values. Stopping as there is nothing to do.")
  xcomplete <- dm[setdiff(distInit:N, nas), ]
  if (nrow(xcomplete) < k) stop("Not sufficient complete cases for computing neighbors.")
  
  #- 4 ~ 6번 process 진행
  for (i in tgt.nas){
    tgtAs <- which(is.na(dm[i, ]))
    dist <- scale(xcomplete, dm[i, ], FALSE)
    xnom <- setdiff(nomAttrs, tgtAs)
    if (length(xnom)) dist[, xnom] <- ifelse(dist[, xnom] > 0, 1, dist[, xnom])
    
    dist <- dist[, -tgtAs]
    dist <- sqrt(drop(dist^2 %*% rep(1, ncol(dist))))
    ks <- order(dist)[seq(k)]
    
    for (j in tgtAs) if (meth == "median") 
      data[i, j] <- centralValue(data[setdiff(distInit:N, nas), j][ks])
      else data[i, j] <- centralValue(data[setdiff(distInit:N,  nas), j][ks], exp(-dist[ks]))
  }
  data[1:n, ]
}

#################
## knn example ##
#################

library(Hmisc)
library(DMwR)
library(dplyr)
library(mlbench)

data(BostonHousing)
anyNA(BostonHousing)

library(DMwR)

#- BostonHousing data 결측치를 자체적으로 생성하고, Y vs YHat 을 비교
data(BostonHousing)
original <- BostonHousing
BostonHousing[sample(1:nrow(BostonHousing), 40), "ptratio"] <- NA
knnOutput <- knnImputation(BostonHousing[, !names(BostonHousing) %in% "medv"]) 

actuals <- original$ptratio[is.na(BostonHousing$ptratio)]
predicteds <- knnOutput[is.na(BostonHousing$ptratio), "ptratio"]

#- iris data 결측치를 자체적으로 생성하고, Y vs YHat을 비교
original <- iris
iris[sample(1:nrow(original), 20), "Species"] <- NA
knnOutput <- knnImputation(iris)
original[is.na(iris$Species),  'Species']
knnOutput[is.na(iris$Species), 'Species']

data     <- iris
k        <- as.integer(sqrt(nrow(data)))
scale    <- T
meth     <- "weighAvg" # weighAvg or median.
distData <- NULL

################
## 생각해보기 ##
################
#- 해당 함수를 사용하면, 따로 계산하고자 하는 컬럼을 지정하는 것이 아니라, 
#- input Data로 들어오는 모든 dataframe을 기반으로 거리 계산을 수행함.
#- 조금 더 detail하게 조정하려면, 계산하고자 하는 컬럼을 지정 받도록 해야 함


