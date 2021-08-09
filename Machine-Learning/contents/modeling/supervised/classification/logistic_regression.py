#- logistic regression
#- iris data
#- petal : 꽃잎, sepal : 꽃받침
from sklearn import datasets
import numpy as np
import pandas as pd

iris = datasets.load_iris()
print(list(iris.keys()))

X = iris['data'][:, 3:]  #- 꽃잎의 너비
y = (iris['target'] == 2).astype(int)

#- 로지스틱 회귀 모형 훈련
from sklearn.linear_model import LogisticRegression
log_reg = LogisticRegression()
log_reg.fit(X, y)

#- 꽃잎의 너비가 0~3cm인 꽃에 대해 모델의 추정 확률 계산
import matplotlib.pyplot as plt
X_new = np.linspace(0, 3, 1000).reshape(-1, 1)
y_proba = log_reg.predict_proba(X_new)
plt.plot(X_new, y_proba[:, 1], 'g-', label="Iris virginica")
plt.plot(X_new, y_proba[:, 0], 'b--', label="Not Iris virginica")

#- 결과 해석
#- Iris-Verginica 의 꽃잎 너비는 1.4 ~ 2.5cm 사이에 분포
#- 반면 다른 붓꽃은 일반적으로 꽃잎 너비가 더 작아 0.1~1.8cm에 분포. 약간 중첩되는 부분은 존재
#- 양쪽 확률이 50%가 되는 1.6cm 근방에서 결정 경계가 만들어짐

log_reg.predict([[1.7], [1.5]])

# 2. 다항 로지스틱 회귀
# sklearn의 LogisticRegression은 클래스가 둘 이상일 때 기본적으로 OvA 전략을 사용
# 만약 다항 로지스틱 회귀를 사용하려면 multi_class = 'multinomial'로 바꾸면 softmax 회귀 사용 가능
# softmax 회귀를 사용하려면 solver 매개변수에 'lbfgs' 같이 소프트맥스 회귀를 지원하는 알고리즘을 지정해야 함
# ** advanced
# BFGS 알고리즘은 연구자의 이름을 따서 Bfoyden-Fletche -Goldfarb-shanno 알고리즘이라고 부르는 의사 뉴턴 메서드 중 하나
# L-BFGS는 BFGS 알고리즘을 제한된 메모리 공간에서 구현한 것으로 ML 분야에서 널리 사용
# 이 외에 뉴턴 켤레 기울기법(Newton conjugate gradient)인 newton-cg와 확률적 평균 경사 하강법인 sag가 multinomial 매개변수를 지원함
# 이 3개의 알고리즘은 l1 규제를 지원하지 않으며 saga가 l1, l2 규제를 지원하며 대규모 데이터셋에 가장 적합

X = iris['data'][:, (2, 3)]
y = iris['target']
softmax_reg = LogisticRegression(multi_class='multinomial', solver='lbfgs', C=10)
softmax_reg.fit(X, y)

softmax_reg.predict([[5, 2]])
softmax_reg.predict_proba([[5, 2]])
