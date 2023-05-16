"""
시계열(Time Series)의 4가지 구성 요인
추세 요인, 순환 요인, 계절 요인, 불규칙 요인

시계열 구성요인 간 결합 방식에 따라 2가지로 나눌 수 있음
- 구성요인 간 독립적이라고 가정하고 각 구성요인을 더하는 가법 모형(addictive model)
- 구성요인 간 독립적이지 않고 상호작용을 한다고 가정하여 구성요인 간 곱해주는 승법 모형(multiplicative model)

시계열 가법 모형(time series addictive model)
- 추세 요인 + 순환 요인 + 계절 요인 + 불규칙 요인
- Yt + Tt + Ct + St + It

시계열 승법 모형(time series multiplicative model)
- 추세 요인 * 순환 요인 * 계절 요인 * 불규칙 요인
"""

#- 가법 모형의 시계열 자료를 가상으로 만들어 보자
import numpy as np
import pandas as pd

dates = pd.date_range('2020-01-01', periods=48, freq="M")
timestamp = np.arange(len(dates))

trend_factor = timestamp * 1.1
cycle_factor = 10 * np.sin(np.linspace(0, 3.14 * 2, 48))
seasonal_factor = 7 * np.sin(np.linspace(0, 3.14 * 8, 48))
np.random.seed(2004)
irregular_factor = 2 * np.random.randn(len(dates))

df = pd.DataFrame({'timeseries':trend_factor + cycle_factor + seasonal_factor + irregular_factor,
                   'trend':trend_factor,
                   'cycle':cycle_factor,
                   'seasonal':seasonal_factor,
                   'irregular':irregular_factor}, index = dates)

#- 시게열 가법 모형 자료 시각화
import matplotlib.pyplot as plt

plt.figure(figsize=[10, 6])
df.timeseries.plot()
plt.title('Time Series (Addictive Model)', fontsize=16)
plt.ylim(-12, 55)
plt.show()

"""
시계열 분해
- 시계열 자료를 추세(Trend), 계절성(Seasonality), 잔차(Residual)로 분해
- time series plot을 보고, 시계열의 주기적 반복/계절성이 있는지, 가법 모형과 승법 모형중 무엇이 더 적합할지 판단함

- 가법 모형을 가정할 시,
- 시계열 자료에서 추세(trend)를 뽑아내기 위해 중심 이동 평균을 이용함
- 원 자료에서 추세 분해값을 빼줌(detrend). 그러면 계절 요인과 불규칙 요인만 남게 됨
- 다음에 계절 주기로 detrend 이후 남은 값의 합을 나누어주면 계절 평균을 구할 수 있음
  ex) 2월 계절 평균 : (2020-02 + 2021-02 + 2022-02 + 2023-02) / 4
- 원래의 값에서 추세와 계절성 분해값을 빼주면 불규칙 요인이 남게 됨

- 시계열 분해 후에 추세와 계절성을 제외한 잔차가 특정 패턴 없이 무작위 분포를 띠고 작은 값이면 추세와 계절성으로 
  모형화가 잘된 것이고, 시계열 자료의 특성을 이해하고 예측하는데 활용 가능
- 시계열 분해 후에 잔차에 특정 패턴이 존재한다면 잔차에 대해서만 다른 모형을 추가로 적합할 수도 있음

"""

#- 다음은 1차 선형 추세 + 4년 주기 순환 + 1년 단위 계절성 + 불규칙 데이터의 가법모형으로 시계열 데이터를 만들어보자
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dates = pd.date_range('2020-01-01', periods=48, freq='M')

timestamp = np.arange(len(dates))
trend_factor = timestamp * 1.1
cycle_factor = 10 * np.sin(np.linspace(0, 3.14 * 2, 48))
seasonal_factor = 7 * np.sin(np.linspace(0, 3.14 * 8, 48))
np.random.seed(2004)
irregular_factor = 2 * np.random.randn(len(dates))

df = pd.DataFrame({'timeseries': trend_factor + cycle_factor + seasonal_factor + irregular_factor,
                   'trend': trend_factor,
                   'cycle': cycle_factor,
                   'trend_cycle': trend_factor + cycle_factor,
                   'seasonal': seasonal_factor,
                   'irregular': irregular_factor},
                  index=dates)

#- python의 statsmodels 라이브러리를 사용해 가법 모형 가정 하에 시계열 분해 수행
from statsmodels.tsa.seasonal import seasonal_decompose

ts = df.timeseries
result = seasonal_decompose(ts, model='addictive')

plt.rcParams['figure.figsize'] = [12, 8]
result.plot()
plt.show()

#- 기존의 시계열 구성 요소와 시계열 분해를 통해 분리한 추세, 계절성, 잔차를 겹쳐서 그려봄
# ground truth & timeseries decompostion all together

# -- observed data
plt.figure(figsize=(12, 12))
plt.subplot(4,1, 1)
result.observed.plot()
plt.grid(True)
plt.ylabel('Observed', fontsize=14)

# -- trend & cycle factor
plt.subplot(4, 1, 2)
result.trend.plot()        # from timeseries decomposition
df.trend_cycle.plot()     # groud truth
plt.grid(True)
plt.ylabel('Trend', fontsize=14)

# -- seasonal factor
plt.subplot(4, 1, 3)
result.seasonal.plot()  # from timeseries decomposition
df.seasonal.plot()        # groud truth
plt.grid(True)
plt.ylabel('Seasonality', fontsize=14)

# -- irregular factor (noise)
plt.subplot(4, 1, 4)
result.resid.plot()    # from timeseries decomposition
df.irregular.plot()    # groud truth
plt.grid(True)
plt.ylabel('Residual', fontsize=14)
plt.show()

#- 원래의 관측치, 추세, 계절성, 잔차 데이터 아래처럼 시계열 분해한 객체에서
#- obsered, trend, seasonal, resid라는 attribute를 통해 조회 가능

print(result.observed)
print(result.trend)
print(result.seasonal)
print(result.resid)

###############################
## 시계열 분해를 통한 시계열 예측 예제 ##
################################
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.seasonal import STL
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.ar_model import AR

import matplotlib.pyplot as plt
import seaborn as sns

#- data
#- Price, Open, High, Low Change
plt.rcParams['figure.figsize'] = [12, 9]
df = pd.read_csv('EURUSD.csv', sep='\t', index_col='Date')
df.index = pd.to_datetime(df.index)
df.sort_index(inplace=True)
df = df.resample('W').last() #- 주 단위로 데이터 resampling.
series = df['Price']

cycle, trend = sm.tsa.filters.hpfilter(series, 50)
fig, ax = plt.subplots(3, 1)
ax[0].plot(series)
ax[0].set_title('Price')
ax[1].plot(trend)
ax[1].set_title('Trend')
ax[2].plot(cycle)
ax[2].set_title('Cycle')
plt.show()

#- SYL decomposition
result = STL(series).fit()
chart = result.plot()
plt.show()

#- 가격 변동을 예측 방법

#- 1. persistence model
#- 마지막으로 관찰 된 값을 다음 값에 대한 예측으로 할당하여 작동하는 가장 간단한 모델
#- 정교한 모델은 아니지만, AR model과의 비교해서 사용할 수 있는 성능 기준을 제시함
#- RMSE (Root Mean Squared Error)를 사용하여 모델 성능을 평가

#- RMSE는 Test Dataset에 대해서만 성능을 판단함
#- 이 경우는 마지막 30%에 해당함

predictions = series.shift(1).dropna() #- 단순히 7일치를 shifting, 주의할 점은 index만 1칸씩 이동
test_score = np.sqrt(mean_squared_error(series[int(len(series) * 0.7) + 1:],
                                        predictions.iloc[(int(len(series) * 0.7)):]))
print(f"Test RMSE: {test_score:.2f}")

plt.plot(series.iloc[-25:], label='Price')
plt.plot(predictions.iloc[-25:], color='red', label='Prediction')
plt.legend()
plt.show()



