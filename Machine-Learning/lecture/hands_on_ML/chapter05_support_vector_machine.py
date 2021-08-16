#- Support Vector Machine
import numpy as np
from sklearn import datasets
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC


iris = datasets.load_iris()
X = iris.data[:, (2,3)]
y = (iris['target'] == 2).astype(np.float64)

svm_clf = Pipeline([
    ('scaler', StandardScaler()),
    ("linear_svc", LinearSVC(C=1, loss='hinge'))
])

svm_clf.fit(X, y)
svm_clf.predict([[5.5, 1.7]])

#- moons dataset을 PolynomialFeatures,
#- StandardSscaler, LinearSVC를 연결하여 pipeline을 만듬
from sklearn.datasets import make_moons
from sklearn.preprocessing import PolynomialFeatures
X, y = datasets.make_moons(n_samples=100, noise=0.15)
print(f"moons datasets shape : {X.shape}")
print(f"moons datasets y shape : {y.shape}")
polynomial_svm_clf = Pipeline([
    ("poly_features", PolynomialFeatures(degree=3)),
    ("scaler", StandardScaler()),
    ("svm_clf", LinearSVC(C=10, loss="hinge"))
])
polynomial_svm_clf.fit(X, y)

#- SVC model을 활용한 커널 트릭 사용
from sklearn.svm import SVC
poly_kernel_svm_clf = Pipeline([
    ("scaler", StandardScaler()),
    ("svm_clf", SVC(kernel="poly", degree=3, coef0=1, C=5))
])
poly_kernel_svm_clf.fit(X, y)