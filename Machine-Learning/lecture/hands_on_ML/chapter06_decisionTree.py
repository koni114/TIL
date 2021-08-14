from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
import os

PROJECT_ROOT_DIR = "."
CHAPTER_ID = "decision_trees"

def image_path(img_name):
    os.path.join(PROJECT_ROOT_DIR, 'images', CHAPTER_ID, img_name)

iris = load_iris()
X = iris.data[:, 2:]
y = iris.target
tree_clf = DecisionTreeClassifier()
tree_clf.fit(X, y)

from sklearn.tree import export_graphviz, plot_tree
plot_tree(
    tree_clf,
    feature_names=iris.feature_names[2:],
    class_names=iris.target_names,
    rounded=True,
    filled=True
)

# DecisionTreeRegressor

iris = load_iris()
X = iris.data[:, 2:]
y = iris.data[:, 1:2]

from sklearn.tree import DecisionTreeRegressor
tree_reg = DecisionTreeRegressor(max_depth=2)
tree_reg.fit(X, y)

plot_tree(
    tree_reg,
    feature_names=iris.feature_names,
    class_names=iris.target_names,
    rounded=True,
    filled=True
)
