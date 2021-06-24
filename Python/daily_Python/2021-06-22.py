# Rolling & Shift
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
f_path = 'https://gist.githubusercontent.com/michhar/2dfd2de0d4f8727f873422c5d959fff5/raw/fa71405126017e6a37bea592440b4bee94bf7b9e/titanic.csv'
df = pd.read_csv(f_path, sep=',', skipinitialspace=True)

#- 기준일을 포함하여 과거 3일의 평균을 데이터 프레임에 붙이기
#- 3일이므로, 첫 2일의 평균 값은 NaN
df['Close_lag3_1'] = df['Fare'].rolling(3).mean()

#- shift()안에 숫자를 변경하면서 기능 확인
#- shift 가 1이면, 1개의 row 만큼 데이터를 shifting
df['Close_lag3_2'] = df['Close_lag3_1'].shift(1)

#- 이동평균(Rolling)과 하루 뒤로 미루는(Shift) 작업을 한꺼번에 하려면
df['Fare'].rolling(3).mean().shift(1)

#- 값이 몇 개이면 계산을 할지 지정
#- min_periods = 1 --> 값이 하나라도 있으면 계산!
df['Fare'].rolling(3, min_periods=1).mean()

##############
## NaN값 찾기 ##
##############
df.isnull()
df.isnull().any()  #- 열에 NaN값이 하나라도 있으면 True
df.isnull().sum()  #- 열의 결측치 개수 Return
df.fillna(0)       #- 결측 값이 0으로 대체

#- 딕셔너리를 이용해서 결측치 처리 가능
pd.set_option('display.max_columns', 200)
values = {1: 0.5, 'Cabin': 1.5, 5: 2.5}
df.fillna(value=values)

###############
## 데이터 시각화 ##
###############
#- Matplotlib 라이브러리를 일부 기능을 Pandas 가 내장하고 있음
#- Matplotlib 라이브러리를 불러오지 않아도 사용 가능

df[['Age', 'Fare']].plot()
df.plot(kind='line', x='PassengerId', y=['Fare', 'Age']) #- line plot
df.plot(kind='bar', x='Sex', y=['Fare', 'Age'])          #- bar plot
df.plot(kind='box', y='Wind')                            #- box plot

#- pie chart
tit_survived = df.groupby(['Sex'])[['Survived']].sum()
tit_survived.plot.pie(y='Survived', startangle=90)

########################
## Matplotlib package ##
########################
#- python 에서 데이터를 시각화 할 때 가장 많이 사용하는 패키지
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd

