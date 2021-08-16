#-  img subplot으로 붙여서 이미지 출력하기
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

X_digits, y_digits = load_digits(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X_digits, y_digits)

cluster_n = 50
kmeans = KMeans(n_clusters=cluster_n)
X_digits_dist = kmeans.fit_transform(X_train)
representative_digits_idx = np.argmin(X_digits_dist, axis=0)
X_representative_digits = X_train[representative_digits_idx]

for idx, X_representative_digit in enumerate(X_representative_digits):
    plt.subplot(cluster_n // 10, 10, idx + 1)
    plt.imshow(X_representative_digit.reshape(8, 8), cmap="binary", interpolation="bilinear")
    plt.axis('off')

y_representative_digits = np.array([4])
