from sklearn import datasets
import numpy as np
iris = datasets.load_iris()
X = iris["data"][:, (2, 3)]
y = iris["target"]

#- 모든 샘플에 편향 추가 xo = 1
X_with_bias = np.c_[np.ones([len(X), 1]), X]

test_ratio = 0.2
validation_ratio = 0.2
total_size = len(X_with_bias)

test_size = int(total_size * test_ratio)