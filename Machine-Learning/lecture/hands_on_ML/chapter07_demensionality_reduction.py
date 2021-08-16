#- 차원 축소(Dimensionality Reduction)
#- SVD(특잇값 분해)를 이용하여 주성분 뽑아내기
from sklearn.datasets import load_iris
import numpy as np
iris = load_iris()
X = iris.data
y = iris.target
X_centered = X - X.mean(axis=0)
U, s, Vt = np.linalg.svd(X_centered)

c1 = Vt.T[:, 0]
c2 = Vt.T[:, 1]

#- 2개의 주성분으로 정의된 평면에 데이터를 투영
W2 = Vt.T[:, :2]
X2D = X_centered.dot(W2)


# 사이킷런을 이용해서 주성분 만들기
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X2D = pca.fit_transform(X)
print(X2D)

print(pca.explained_variance_ratio_)

#- 차원 축소를 하지 않고 PCA 계산 후 분산을 95%로 유지하는데 필요한 최소한의 차원 수 계산
pca = PCA()
pca.fit(X, y)
cumsum = np.cumsum(pca.explained_variance_ratio_)
d = np.argmax(cumsum >= 0.95) + 1
print(f"분산 95% 이상 주성분 수 : {d}")

pca = PCA(n_components=0.95)
X_reduced = pca.fit_transform(X)
print(X_reduced)

#- MNIST 데이터셋을 154차원으로 압축하고, inverse_transform() 메서드를 사용
pca = PCA(n_components = 154)
X_reduced = pca.fit_transform(X_train)
X_recovered = pca.inverse_transform(X_reduced)

#- random PCA
rnd_pca = PCA(n_components=154, svd_solver="randomized")
X_reduced = rnd_pca.fit_transform(X)

#- Incremental PCA
from sklearn.decomposition import IncrementalPCA
n_batches = 10
inc_pca = IncrementalPCA(n_components=2)
for X_batches in np.array_split(X, n_batches):
    inc_pca.partial_fit(X_batches)
X_reduced = inc_pca.transform(X)
X_reduced


for X_batch in np.array_split(X, n_batches):
    inc_pca.partial_fit(X_batch)
X_reduced = inc_pca.transform(X)


X_mm = np.memmap(filename, dtype='float32', mode='readonly', shape=(m, n))
batch_size = m // n_batches
inc_pca = IncrementalPCA(n_components=154, batch_size=batch_size)
inc_pca.fit(X_mm)


from sklearn.decomposition import KernelPCA
rbf_pca = KernelPCA(n_components=2, kernel="rbf", gamma=0.04)
X_reduced = rbf_pca.fit_transform(X)
print(X_reduced)

#- KPCA + LogisticRegression
from sklearn.decomposition import KernelPCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

clf = Pipeline([
    ("kpca", KernelPCA(n_components=2)),
    ("log_reg", LogisticRegression())
])

param_grid = [{
    "kpca__gamma": np.linspace(0.03, 0.05, 10),
    "kpca__kernel": ["rbf", "sigmoid"]
}]

grid_search = GridSearchCV(clf, param_grid, cv=3)
grid_search.fit(X, y)
print(f"best param: {grid_search.best_params_}")
