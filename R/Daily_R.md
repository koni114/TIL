## Daily_R

### Daily_R Contents summary
```
├── Daily_R
        └── 2019.05.14.R 
              - getMode function        : 최빈값 구하는 함수
              - beforeNa function       : 이전 값으로 대체하는 로직
              - zoo::na.approx fucntion : NA 기준 앞 뒤의 평균 값을 계산하여 추가
              - type.convert function
              - Hmisc::impute function  : 해당 vector에 특정 값으로 대체 해주는 함수(평균, 최빈, 최소 값 등)
				                          대체된 값의 T, F를 알 수 있어, 결측치 비율을 알 수 있음 
              - zip::zip function       : file -> zip으로 대체
              - fMultivar::rnorm2d      : 특정 수치의 상관을 갖는 관측치를 랜덤으로 추출 할 수 있음
        
        └── 2019.05.15.R
              - ave function            : 그룹별로 사용자 함수를 적용하는 함수. 
              - replace function        : 인덱스를 이용하여 값 변경
        
        └── 2019.05.28.R                
              - 일표본 T-TEST 검정
              - foreach function        : 병렬 처리시 도움이 되는 함수
        
        └── 2019.05.31.R
              - get, assign, parent.frame : R에서의 전역 변수 접근
              - type.convert function     : 문자형 컬럼을 자동으로 인식해서 수치형 컬럼으로 변경
              - plyr::revalue function    : 요인 형태의 데이터 라벨을 변경하는 방법
              - step function 성능 이슈 
        
        └── 2019_06_03.R
              -  T-Test, anova function   : 등분산 일 때, 유의차 검정
              -  Welch, Brown Forsythe    : 이분산 일 때, 유의차 검정
              -  Wilcoxon, kruskal_Walis, mood's test : 비모수 검정, 일표본 
        
        └── 2019_07_04.R
              - parse_date_time function  : lubricate package
                                            아무렇게 막 입력하는 날짜형을 예쁘게 변경 할 수 있는 방법
              - strptime() milesecond 표현 문제
        
        └── 2019_07_26.R
              - 신뢰구간과 백분율의 차이
              - for문 -> apply문으로 변경 방법
              - dplyr mutate를 이용한 이상치 처리 방법
        
        └── 2019_08_21.R
              - __all, _at,  _if, vars, funs function : dplyr package 
              - do function : dplyr package
        
        └── 2019_08_22.R
              - ggplot2 density function
              - optimizer
              - kmeans를 이용한 극소점 찾기
        
        └── 2019_10_15.R 
              - 동적 변수를 가지고 rename을 수행하는 방법
              - match function + colnames function 응용
        
        └── 2019_10_18.R
              - 패키지 설치에 있어 알아야 할 것들 
              - miniCRAN package
              - match fucntion 
        
        └── 2019_10_23.R
              - miniCRAN package 사용법
              - 인터넷이 안될 때 local repo를 이용하여 tar.gz download 받고, 이를 설치하는 방법 guide
        
        └── 2019_10_30.R
              - 수치형으로 변환가능한지 확인하는 방법
              - factor형인 vector에서 level의 값을 1, 0 으로 변환하고 싶을 때
              - combinat package
              - 교호작용이란,
        
        └── 2019_10_31.R
              - 교호작용도(interaction plot)
              - 두 범주형 값 + 한개의 수치형 변수에 대한 교호작용도 그리기
              - 두 연속형 + 한개의 범주형 변수에 대한 교호작용도 그리기 
        
        └── 2019_11_03.R
              - anomaly detection 개념
              - 시계열의 합분해, 곱분해 개념
              - forecast, FBN package를 이용한 이동평균법 응용
        
        └── 2019_11_23.R
              - plotly 를 활용한 box-plot 그리기
              - plotly 를 활용한 scatter-plot 그리기
              - plotly 를 활용한 density-plot 그리기(ggplot 사용 X)
              - plotly 를 활용한 horizontal-bar-plot 그리기(ggplot 사용 X)
              - Tip1. 동적 variable를 이용하여 ggplot 그리기 eval, parse 이용
              - Tip2. 동적 plot을 Json data로 변환하기
        
        └── 2019_11_26.R
              - Caret package
              - createDataPartition, trainControl, train, expand.grid, 
              - 랜덤 검색 그리드(random selection of tuning parameter combinations)
              - modelLookup, VarImp
	 
	└── 2020_12_09.R
	      - list -> data.frame 변환 시, 기존 data.frame 그대로 재정렬 하는 방법. lapply, rbindlist function 이용
```
