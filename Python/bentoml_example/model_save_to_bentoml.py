import bentoml

from sklearn import svm
from sklearn import datasets

iris = datasets.load_iris()
X, y = iris.data, iris.target

# Train the model
clf = svm.SVC(gamma="scale")
clf.fit(X, y)

# save model to the BentoML local model store
# iris_clf model name 명으로 save 됨
# 이 때 자동적으로 version 이 generate 됨

saved_model = bentoml.sklearn.save_model("iris_clf", clf)
print(f"Model saved: {saved_model}")

# Model saved: Model(tag="iris_clf:obnnrycxlw3rplg6")

# model loading
model1 = bentoml.sklearn.load_model("iris_clf:obnnrycxlw3rplg6")
model2 = bentoml.sklearn.load_model("iris_clf:latest")


