## mice(multivariate Imputation by Chained Equation)
- 누락된 패턴을 확인하는 방법을 다루고 누락된 자료를 다루는 세 가지 중요한 방법(rational approach, listwise deletion, multiple imputation)을 배워보고자 함

### Missing Data의 종류
- Missing data는 MCAR(Missing completely at random)과 MAR(Missing at Random) 그리고 MNAR(Missing at not random)으로 나누어 볼 수 있음
- MCAR(Missing completely at random))은 변수에 종류와 변수의 값과 상관없이 전체에 걸쳐 무작위적으로 나타나는 것으로, 이러한 missing data는 분석에 영향을 주지 않음. 실제로 MCAR인 경우는 거의 없음
- MAR(Missing at random)은 누락된 자료가 특정 변수와 관련되어 일어나지만 그 변수의 값과는 관계가 없는 경우
- MNAR(Missing at not random)은 누락된 변수의 값과 누락된 이유가 관련이 있는 경우임
- 예를 들어 노인의 우울증에 대한 설문조사를 했는데 실제로 우울증이 심한 경우는 우울한 기분에 대해 자세히 조사하는 항목을 대답하는 것이 괴로워 일부러 회피하여 누락되는 경우 등

### 누락 자료에 대한 rational approach
- 누락된 자료의 경우 수학적인 방법이나 논리적인 방법으로 누락 자료를 회복할 수 있는 경우가 있음
- 예를 들어 나이가 누락된 경우, 생년월일을 알고 있으면 계산 가능
- 성별이 누락된 경우 주민등록번호 뒷자리로 채워 넣는 경우

### Listwise deletion
- 모든 변수들이 정확한 값으로 다 채워져 있는 관측치만을 대상으로 분석을 진행하는 것
- 이 방법은 사실상 한 개라도 누락이 있는 자료들은 모두 제거하는 것으로, 많은 통계 프로그램에서 디폴트 방법으로 되어 있어 회귀나 ANOVA를 시행하면서 누락된 자료가 있다는 문제를 인지하지 못하는 경우도 있음
- Listwise deletion은 자료가 MCAR인 것을 전제로 함. 즉 complete observation이 전체 데이터의 random subsample임을 전제로 함
- Pairwise deletion은 na값이 있는 관측치를 모두 제거하는 것이 아니라 통계에 따라 그때그때 각 쌍의 변수들에 대해 누락된 자료를 제거

### 다중 대입법(multiple imputation, MI)
- 시뮬레이션을 반복하여 누락된 데이터를 채워 넣는 것
- 복잡한 누락된 자료 문제가 있을 때, method of choice임. MI 방법에서는 missing data가 있는 데이터셋이 있을 때 simulation을 통하여 누락된 자료를 채운 complete dataset을 3-10개 만듬
- 누락된 자료는 몬테카를로 방법을 사용해서 채움
- 그런 다음 각각의 dataset에 대해 표준적인 통계방법을 적용하여 그 결과를 바탕으로 통계 결과 및 신뢰구간 제공

### mice imputation process
- 누락된 자료가 있는 데이터 프레임이 있는 경우, mice 함수를 적용하면 누락된 값은 데이터 프레임에 있는 다른 변수를 사용하여 값을 예측하여 채워 넣음
- 누락된 자료가 채워진 완성된 데이터셋을 여러 개 만듬
- 대입 과정에는 무작위 구성 성분이 있기 때문에 각각의 완성된 데이터셋은 조금씩 다름
- 각각의 완성된 데이터셋에 대해 `with()` 함수를 사용하여 통계 모형을 순서대로 적용
- `pool()` 함수를 사용하여 이들 각각의 분석결과를 하나의 결과로 통합