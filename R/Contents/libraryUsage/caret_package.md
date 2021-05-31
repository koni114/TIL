## caret package 완전 정복
### Customizing the Tuning Process
####  Tuning Grids
* train 함수의 tuneGrid parameter에 data.frame 형태로 할당
* 이 때 data.frame의 column은 tuning parameter의 name 이어야 함
  *  ex) RDA Model 같은 경우, column name이 gamma와 lambda

#### Plotting the Resampling Profile
* plot 함수를 통해서 metric의 performance 와 tuning param 간의 관계를 plotting 해볼 수 있음
~~~
trellis.par.set(caretTheme())
plot(gbmFit2, metric = "Kappa")
~~~

#### trainControl Function
* 모델을 어떻게 만들 것인지에 대한 parameter를 control 하기 위한 function
* Possible parameter values:
  * method : resampling method. ex) boot, cv, LOOCV, LGOCV, repeatedcv, timeslice, none, oob(out-of-bag)  
    * oob:   random forest, bagged trees, bagged earth, bagged flexible discriminant analysis, or conditional tree forest models 에서만 사용 가능
   * number :  fold의 n 값을 의미하거나. bootstrapping, LGOCV의 resampling iteration을 의미
   * repeats  : k-fold cv에서의 repeat 값을 의미
   * verboseIter : training log를 print
   * returnData : trainingData라는 slot에 data를 saving 해줌
   * p : LGOCV에서 training Dataset의 percentag를 말함
   * initialWindow, horizon, fixedWindow : timeslice method 사용시 적용되는 parameter
   * classProbs : 이진 분류 시, ROC 넓이 값 등 계산 필요시 True 지정
   * summaryFunction : 최적의 tuning parameter를 선택하기 위한 지표 함수
   * selectionFunction : 최적의 model을 선택하기 위한 지표를 만드는 함수
   * allowParallel :

#### Choosing the Final Model
* package에 내장되어있는 selectionFunction(best, oneSE, tolerance)를 이용하여 최적의 best 모델을 뽑아냄
  * best : largest/smallest value를 추출
  * oneSE : 최고 성능의 1표준오차 내에 가장 단순한 후보 선택
  * tolerance : 최고의 성능 중 허용된 % tolerance 내에 가장 덜 복잡한 모델 선택
  ex) 2% 손실 내에 가장 덜 복잡한 모델 선택하는 경우,
~~~
whichTwoPct <- tolerance(gbmFit3$results, metric = "ROC",
                         tol = 2, maximize = TRUE)  
cat("best model within 2 pct of best:\n")
gbmFit3$results[whichTwoPct,1:6]
~~~
* 이 때, 어느 하이퍼 파라미터 지표가 적어야 덜 복잡한 모델이라고 할 수 있을까?  
예를 들어 100 interation + 2 depth tree model 과 50 interation + 8 depth 중 어느 모델이 덜 복잡한 모델인가?
* boosted model 같은 경우, interation이 더 중요한 지표로 사용되고 있음..

#### Extracting Predictions and Class Probabilities
* 일반적으로 앞서 train 모델 수행 결과 나온 best Model을 통해 predict을 진행함
* pls나 gbm 모델 처럼  추가적인 parameter가 필요할 수도 있음  
이러한 경우 train object는 parameter optimization 결과들을 새로운 sample 예측에 사용함
* 사용자가 predict.gbm 함수를 직접 사용하는 경우, 트리의 수를 직접 setting 해야하거나,  
binary classification 같은 경우 factor vector로 변경하여 probability 형태로 변경하는 추가 작업이 필요함
* predict.train 함수는 자동으로 이러한 detail 작업을 수행 해 줌
* predict.train 함수의 결과 type은 "class", "prob" 두 개만 사용되도록 함
~~~
predict(gbmFit3, newdata = head(testing))
predict(gbmFit3, newdata = head(testing), type = "prob")
~~~

#### Exploring and Comparing Resampling Distrubutions
##### within-model
* tuning parameter와 resampling  결과 간의 관계를 확인할 수 있는 lattice function이 있음
* xyplot, stripplot, histogram, densityplot은 tuning parameter 간의 연속, 이산분포 결과를 확인 가능
~~~
trellis.par.set(caretTheme())
densityplot(gbmFit3, pch = "|")
~~~
* resamples = 'all' option을 주면 resampling 결과와 across된 plot을 확인 가능

##### between-model
* 여러 모델간의 성능 비교를 할 수 있음
* svm, rda, gbm 모델을 만들어 다양한 plot을 통한 성능 비교가 가능
~~~
set.seed(825)
svmFit <- train(Class ~ ., data = training,
                 method = "svmRadial",
                 trControl = fitControl,
                 preProc = c("center", "scale"),
                 tuneLength = 8,
                 metric = "ROC")

rdaFit <- train(Class ~ ., data = training,
                 method = "rda",
                 trControl = fitControl,
                 tuneLength = 4,
                 metric = "ROC")

resamps <- resamples(list(GBM = gbmFit3,
                          SVM = svmFit,
                          RDA = rdaFit))

# boxplot을 통한 성능(metrics) 지표 비교
theme1 <- trellis.par.get()
theme1$plot.symbol$col = rgb(.2, .2, .2, .4)
theme1$plot.symbol$pch = 16
theme1$plot.line$col = rgb(1, 0, 0, .7)
theme1$plot.line$lwd <- 2
trellis.par.set(theme1)
bwplot(resamps, layout = c(3, 1))

# dotplot
trellis.par.set(caretTheme())
dotplot(resamps, metric = "ROC")

# scatter plot
trellis.par.set(theme1)
xyplot(resamps, what = "BlandAltman")

splom(resamps)
~~~
* 해당 모델은 동일한 training data를 이용하여 모델을 생성하였기 때문에 모델간의 차이를 통계적 분석을 통해 확인할 수 있음
* 이를 통해 내부적인  resample correlation 결과 값을 감소 시킬 수 있음(?)
* 간단한 t-test를 사용하여 평가 가능
~~~
difValues <- diff(resamps)

summary(difValues)
trellis.par.set(theme1)
bwplot(difValues, layout = c(3, 1))

trellis.par.set(caretTheme())
dotplot(difValues)
~~~

#### Fitting Models Without Parameter Tuning
* trainControl 함수를 통해 method = 'none' parameter를 setting하면, resampling과 parameter tuning 없이  
모델 생성
~~~
fitControl <- trainControl(method = "none", classProbs = TRUE)

set.seed(825)
gbmFit4 <- train(Class ~ ., data = training,
                 method = "gbm",
                 trControl = fitControl,
                 verbose = FALSE,
                 ## Only a single model can be passed to the
                 ## function when no resampling is used:
                 tuneGrid = data.frame(interaction.depth = 4,
                                       n.trees = 100,
                                       shrinkage = .1,
                                       n.minobsinnode = 20),
                 metric = "ROC")
gbmFit4
~~~
* `plot.train`, `resamples`, `confusionMatrix.train` 은 사용 X
* `predict.train` 함수는 사용 가능


### 용어 정리
* LOOCV(leave-one-out cross-validation) : 기존 k-fold cv에서 k가 데이터의 개수 만큼 setting되는 CV  
데이터가 적을 경우 효과가 있음
* resample : 복원추출을 의미
* bootstrapping : 현재 있는 표본에서 추가적으로 표본을 복원 추출 하고, 이러한 표본의 통계량을 계산하여 사용하는 방식.

## 15. Variable Importance
* 변수 중요도 평가 함수는 크게 <b>모델정보를 사용하거나, 그렇지 않거나</b> 로 두 그룹으로 나뉨
  * model-based 접근  
  모델의 성능에 변수가 직접적인 영향을 줌  
  모델에 영향을 주는 변수 순서를 계산 방법을 몰라도 알 수 있음
* 분류 모델 같은 경우, 각 class마다 영향을 주는 독립 변수 중요도가 다를 수 있음
* 모든 변수 중요도 값은  varImp.train 함수의 scale = F로 주지 않는 이상 최대 값은 100으로 설정 됨
### 15.1 모델 기반 변수 중요도 측정
 * Linear Models  
   * 각 변수별 t-통계량을 통한 변수 중요도 추정
 * Random Forest
   * out-of-bag 데이터의 예측 정확도가 각 트리마다 기록됨

### 15.2 모델에 독립적인 변수 중요도 측정
* varImp function에 useModel = False 변수를 지정하면 모델 기반의 변수 중요도가 아닌 변수 중요도를 측정해줌
* 'filter' approach 를 통해 각각의 변수를 평가함

#### 분류 분석
* ROC curve 분석을 통해 수행됨
  * 이진 분류인 경우, 통상적으로 사용하는 AUC 값을 이용
  * 다중 분류인 경우, pair-wise 별 AUC 값을 계산

#### 회귀 분석
* nonpara = False가 사용된 경우, 선형 모델이 fit 되고 t-value의 기울기 절대 값이 사용됨
* nonpara = True가 사용된 경우, loess smoother 가 fit 되고, intercept가 null인 경우에  
R^2 통계 값이 사용

#### 코드 예제
~~~
# scale = T 로 주면 0 ~ 100 사이로 자동 정규화
gbmImp <- varImp(gbmFit3, scale = FALSE)
gbmImp
~~~
* filterVarImp function 를 사용하여 ROC Curve 의 면적을 계산할 수 있음
~~~
roc_imp <- filterVarImp(x = training[, -ncol(training)], y = training$Class)
head(roc_imp)
~~~
* built-in importance score가 아닌 model 들은 varImp function을 사용시(ex) SVM) ROC Curve를 계산하여 적용
* plot 함수를 이용하여 importance value를 시각화화여 적용 가능
~~~
plot(gbmImp, top = 20)
~~~

### 용어 정리
* out-of-bag  데이터 : 부트스트랩을 이용한 임의 중복추출 시, 훈련 데이터 집합에 속하지 않는 데이터를 말함
* out-of-bag error : 이 데이터의 실제 값과 각 트리로 부터 나온 예측 결과 사이의 오차로 정의
