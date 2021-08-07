import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import plot_precision_recall_curve, plot_roc_curve

pd.set_option('display.max_columns', 20)


os.environ['KAGGLE_USERNAME'] = 'jaebig'
os.environ['KAGGLE_KEY'] = '6cf004075ae310d0342dbed981b29aee'

df = pd.read_csv('./heart_failure_clinical_records_dataset.csv')

df.head()
df.info()      #- data count, Not-Null, Dtype
df.describe()
print(df.columns)
num_var = ['creatinine_phosphokinase',
           'ejection_fraction',
           'platelets',
           'serum_creatinine',
           'serum_sodium',
           'time',
           'age']
cat_var = ['anaemia', 'diabetes',
           'high_blood_pressure', 'sex',
           'smoking']
y_var = ['DEATH_EVENT']

# plot을 통한 EDA #
#- histogram, jointplot, pairplot
sns.histplot(x='age', data=df, hue='DEATH_EVENT')
sns.jointplot(x='platelets', y='serum_creatinine', data=df, hue='DEATH_EVENT')
sns.pairplot(df[num_var])
sns.pairplot(df[num_var + y_var], hue='DEATH_EVENT')

#- boxplot(), violinplot(), swarmplot()을 활용한 범주별 통계 확인
sns.boxplot(x='DEATH_EVENT', y='age', data=df)
sns.violinplot(x='DEATH_EVENT', y='age', data=df)
sns.swarmplot(x='DEATH_EVENT', y='age', data=df)

##- Step 3. 모델 학습을 위한 데이터 전처리
#- StandardScaler를 이용하여 데이터 전처리하기
X_num = df[num_var]
X_cat = df[cat_var]
y = df[y_var]

scaler = StandardScaler()
X = pd.DataFrame(scaler.fit_transform(X_num), columns=X_num.columns)
X = pd.concat([X_num, X_cat], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y)
print(f"X_train.shape: {X_train.shape}")
print(f"X_test.shape: {X_test.shape}")
print(f"y_train.shape: {y_train.shape}")
print(f"y_test.shape: {y_test.shape}")

model_lr = LogisticRegression(random_state=0, max_iter=100).fit(X, y)
y_pred = model_lr.predict(X_test)
print(classification_report(y_test, y_pred))

model_xgb = XGBClassifier(random_state=0)
model_xgb.fit(X_train, y_train)
y_pred = model_xgb.predict(X_test)
print(classification_report(y_test, y_pred))

#- feature importance
plt.bar(X.columns, model_xgb.feature_importances_)
plt.xticks(rotation=90)
plt.show()

fig = plt.figure()
ax = fig.gca()
plot_precision_recall_curve(model_lr, X_test, y_test, ax=ax)
plot_precision_recall_curve(model_xgb, X_test, y_test, ax=ax)

fig = plt.figure()
ax = fig.gca()
plot_roc_curve(model_lr, X_test, y_test, ax=ax)
plot_roc_curve(model_xgb, X_test, y_test, ax=ax)