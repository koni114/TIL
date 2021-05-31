## Contents
### 폴더 구조
- dataPreprocessing
  - data loading, data extraction, data preprocessing..
- EDA
  - data visualization, correlation, ...
- libraryUsage
  - package나 library 등의 사용 방법 위주 정리
- modeling
  - ML, DL model..
- evaluation
  - model evaluation..
- statistics
  - statistics-based analysis, ..
- module
  - function 단위 module 모음

### History 
- 2020.12.08 최초 생성 
  - 기존 r-programming 자료들을 정리하기 위하여 repo 생성
  - knnImputation.R 추가.  DMwR package 내 knnImputation function source review. process 정리

### Contents summary
```
├── dataPreprocessing
    └── fileToZip.R: R에서 file을 zip으로 만드는 방법
    └── JB_LoadingData.R : 데이터 불러오기 excel, csv, tab, txt
    └── JB_SavingData.R  : 데이터 저장하기
    └── JB_chgColType.R  : 변수타입설정. dplyr을 이용한 변수 타입 변환
                           날짜, 범주, 수치, 문자
    └── JB_itgrtData.R   : 데이터 통합, rbind, cbind
    └── JB_pivotData.R   : 데이터 pivoting
    └── JB_splitData.R   : 데이터 분할
    └── JB_treatNa.R     : 데이터 결측치 처리
                              - 행 제거
                              - 열 제거
                              - 결측치 대체
                                - 평균 값
                                - 이전 값
                                - 임의 값
                                - 중앙 값
    └── JB_treatOutlier.R : 이상치 처리
                            이상치 Rule
                                - IQR
                                - 백분위수
   
                            이상치 대체 값
                                - NA
                                - min/max
                                - 제거
    └── JB_orderByData.R  : 데이터 정렬     
    └── JB_windowData.R   : 데이터 윈도우  
    └── JB_shiftData.R    : 데이터 시프트       
    └── JB_samplingData.R : 데이터 샘플링
    └── JB_stdData.R      : 데이터 표준화 
                                - 01 변환
                                - scale 변환
    └── JB_encodingData.R : 데이터 인코딩 
    └── web_crawling.md : 웹 크롤링의 전반적인 개념 정리

├── EDA 
    └── JB_summary.R : 자료 요약(통계)    
                             - 수치형
                             - 문자형
                             - 날짜형
                             - 범주형
    └── JB_ggpplot2.R : ggplot2 기본 기능 익히기  
    └── JB_ggplot_cheatsheet.R : ggplot2 cheatsheet 정리
    └── JB_ScatterPlot.R : 산점도
    └── JB_timeTrend.R : Time Trend  
    └── JB_pieChart.R  : pieChart  

├── libraryUsage 
    └── dplyr.R : dplyr package 내 함수 사용법 등 정리 
    └── caret.R : caret package 사용법, 예제 등
    └── caret_package.md : caret package documentation 내용 정리
    └── knnImputation.R : DMwR package 내 knnImputation function source review. process 정리
├── modeling
    └── unsupervised
        └── JB_pca.R : 주성분분석
        └── JB_clustering.R : 군집분석
                              - 계층적 군집분석
                              - k-평균 군집분석
    └── supervised
        └── common
            └── JB_correlation.R : 연관성 분석
            └── JB_SelfOrganazingMap : SOM 분석
        └── classification
        └── prediction
            └── JB_LinearRM.R : Linear 회귀 분석 
            └── JB_glmnet.R : 정규화 회귀 분석
                            - Ridge 회귀분석    
                            - Lasso 회귀분석    
                            - elastic 회귀분석  
            └── JB_timeSeries.R : 시계열 예측

        └── ensemble
            └── JB_ensemble.R :   
                             - bagging 
                             - boosting 
                             - random Forest
                             - xgboost
                             
        └── textmining
            └── JB_textMining.R
└── statistics 
    └── JB_normalTest.R : 정규성 검정
    └── JB_corTest.R : 상관분석 
    └── JB_anova.R : 분산분석 
    └── JB_meanDiffer.R : 평균 유의차 분석
    └── JB_varTest.R : 등분산검정 
    └── JB_interaction.R : 교호작용 인자탐지 
    └── JB_confidence_interval : 신뢰 구간 추정 이론 + R code
    └── JB_nonParametricTest : 비모수 검정
    └── JB_normalization : 정규화 변환
    └── 
└── evaluation
    └──  JB_evaluation.R : 모델 평가 방법. 교차 검증
```
