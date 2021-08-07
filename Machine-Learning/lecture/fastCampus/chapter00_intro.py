###################################
## 간단하게 python library 사용해보기  ##
###################################

# 1. numpy package
import numpy as np
matrix_a = np.asarray([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
matrix_b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
matrix_c = matrix_a + matrix_b
print(matrix_c)

#- 2. pandas package
import pandas as pd
col_ids = pd.Series(data=[1,2,3,4])
col_teams = pd.Series(data=['A', 'A', 'B', 'B'])
col_names = pd.Series(data=['김태웅', '허재훈', '이승규', '권구민'])
col_score = pd.Series(data=[100, 95, 20, 30])

df = pd.DataFrame(data={'id': col_ids,
                        'teams': col_teams,
                        'names': col_names,
                        'score': col_score})

#- 3. matplotlib package

import matplotlib.pyplot as plt

x = np.linspace(0, 1, 100)
y = x
yy = x ** 2

fig = plt.figure()
ax = fig.gca()             #- Axes 구현
ax.plot(x, y, 'r-')
ax.plot(x, yy, 'g-')
ax.set_title('y = x and y = x^2')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend(['y = x', 'y = x^2'])
ax.grid()
fig.show()

#- 4. Seaborn package
#- 기본적인 통계량을 확인할 수 있는 plot을 만들 수 있게 제공해주는 pakcage

import seaborn as sns
sns.histplot(x='score', data=df, bins=2)
sns.histplot(x='score', data=df, hue='teams')
sns.boxplot(y='score', x='teams', data=df)

#- 5. Plotly package
#- Plotly 회사에서 만든 패키지 -> Cloud에서 서비스를 함
#- Plotly Python Open Source Graphing Library

import plotly.express as px
fig = px.line(x=['a', 'b', 'c'], y=[1, 3, 2], title='sample figure')
fig.show()

import plotly.express as px
fig = px.line(x=['a', 'b', 'c'], y=[1, 3, 2], title='sample figure')
fig.show()

############################
## kaggle datasets download by API
import os
os.environ['KAGGLE_USERNAME'] = 'jaebig'
os.environ['KAGGLE_KEY'] = '6cf004075ae310d0342dbed981b29aee'

# !kaggle -h
# !kaggle datasets download -d adityakadiwal/water-potability

