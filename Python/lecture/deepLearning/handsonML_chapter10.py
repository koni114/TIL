import keras.wrappers.scikit_learn
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#- fashion MNIST
fashion_mnist = tf.keras.datasets.fashion_mnist
(X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()

#- 간편하게 픽셀 강도를 255.0로 나누어 0 ~ 1 사이로 범위 조정
X_valid, X_train = X_train_full[:5000] / 255.0, X_train_full[5000:] / 255.0
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
X_test = X_test / 255.0

#- 클래스 이름의 리스트 생성
target_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat'
    ,'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

#- Sequential API 를 사용하여 모델 만들기
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=[28, 28]))
model.add(tf.keras.layers.Dense(300, activation='relu'))
model.add(tf.keras.layers.Dense(100, activation='relu'))
model.add(tf.keras.layers.Dense(10, activation='softmax'))

#- 다음과 같이 선언해서도 사용 가능
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=[28, 28]),
    tf.keras.layers.Dense(300, activation='relu'), #- 784 * 300 + 300
    tf.keras.layers.Dense(100, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

# target value 가 one-hot vector 로 수행되어 있다면, categorical_crossentropy,
# label encoding 으로 되어 있으면, sparse_categorical_crossentropy

# optimizer
# sgd 는 default 로 lr=0.01을 사용함
model.compile(loss='sparse_categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])

tf.keras.utils.plot_model(model)

#- model 객체 내 접근 함수
print(model.layers) #- 각 layer 객체 list
print(model.layers[1].name) #- 해당 layer name
weights, biases = model.layers[1].get_weights()
print(f"weights : {weights}, biases : {biases}")

history = model.fit(X_train, y_train, epochs=30, validation_data=(X_valid, y_valid))

#- 모델 실행 결과에 대한 검증 결과 확인
pd.DataFrame(history.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1)
plt.show()

model.evaluate(X_test, y_test)

X_new = X_test[:3]
y_proba = model.predict(X_new)
y_proba.round(2)

y_pred = model.predict_classes(X_new)
print(np.array(target_names)[y_pred])

##############################
## fetch_california_housing ##
##############################

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

housing = fetch_california_housing()
X_train_full, X_test, y_train_full, y_test = train_test_split(housing.data, housing.target)
X_train, X_valid, y_train, y_valid = train_test_split(X_train_full, y_train_full)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_valid = scaler.transform(X_valid)
X_test = scaler.transform(X_test)

input_ = tf.keras.layers.Input(shape=X_train.shape[1:])
hidden1 = tf.keras.layers.Dense(30, activation='relu')(input_)
hidden2 = tf.keras.layers.Dense(30, activation='relu')(hidden1)
concat = tf.keras.layers.Concatenate()([input_, hidden2])
output = tf.keras.layers.Dense(1)(concat)
model = tf.keras.Model(inputs=[input_], outputs=[output])

#- 일부 특성은 깊은 경로, 일부 특성은 짧은 경로를 사용하고 싶을 때,
#- 여러 개의 입력을 사용하면 됨
input_A = tf.keras.layers.Input(shape=[5], name='wide_input')
input_B = tf.keras.layers.Input(shape=[6], name='deep_input')
hidden1 = tf.keras.layers.Dense(30, activation='relu')(input_B)
hidden2 = tf.keras.layers.Dense(30, activation='relu')(hidden1)
concat = tf.keras.layers.concatenate([input_A, hidden2])
output = tf.keras.layers.Dense(1, name='output')(concat)
model = tf.keras.Model(inputs=[input_A, input_B], outputs=[output])

model.compile(loss='mse', optimizer=tf.keras.optimizers.SGD(learning_rate=0.003))

X_train_A, X_train_B = X_train[:, :5], X_train[:, 2:]
X_valid_A, X_valid_B = X_valid[:, :5], X_valid[:, 2:]
X_test_A, X_test_B = X_test[:, :5], X_test[:, 2:]
X_new_A, X_new_B = X_test_A[:3], X_test_B[:3]

history = model.fit((X_train_A, X_train_B), y_train, epochs=20,
                    validation_data=((X_valid_A, X_valid_B), y_valid))


mse_test = model.evaluate((X_test_A, X_test_B), y_test)

#- 모델 저장하기
model.save('my_keras_model.h5')

#- 모델 Load 하기
tf.keras.models.load_model('my_keras_model.h5')

#- callback 사용하기
checkpoint_cb = tf.keras.callbacks.ModelCheckpoint('my_keras_model.h5')
history = model.fit(X_train, y_train, epochs=20, callbacks=[checkpoint_cb])

#- save_best_only = True 사용시, 검증 세트에서 가장 결과가 좋은 모델만 저장
history = model.fit(X_train, y_train, epochs=10,
                    validation_data = (X_valid, y_valid),
                    callbacks=[checkpoint_cb])

#- 텐서보드
#- 프로그램을 수정해서 이벤트 파일(event file)이라는 특별한 이진 로그 파일에
#- 시각화하려는 데이터를 출력해야 함

#- 일반적으로 텐서보드 서버가 루트 디렉터리를 가리키고 프로그램은 실행할 때마다
#- 다른 서브디렉터리에 이벤트를 기록함

#- 루트 디렉토리 정의
#- 현재 날짜와 시간을 사용해 실행할 때마다 다른 서브 디렉토리 경로를 생성하는 간단한 함수도 만들어보자
#- 테스트 하는 하이퍼파라미터 값과 같은 추가적인 정보를 로그 디렉터리 이름으로 사용가능
import os
root_logdir = os.path.join(os.curdir, "my_logs")

def get_run_logdir():
    import time
    run_id = time.strftime('run_%Y_%m_%d_%H_%M_%S')
    return os.path.join(root_logdir, run_id)

run_logdir = get_run_logdir()
print(run_logdir)

tensorboard_cb = tf.keras.callbacks.TensorBoard(run_logdir)
history = model.fit(X_train, y_train, epochs=30,
                    validation_data=(X_valid, y_valid),
                    callbacks=[tensorboard_cb])

#- 10.3 신경망 하이퍼파라미터 튜닝하기
def build_model(n_hidden=1, n_neurons=30, learning_rate=3e-3, input_shape=[8]):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.InputLayer(input_shape=input_shape))
    for layer in range(n_hidden):
        model.add(tf.keras.layers.Dense(n_neurons, activation='relu'))
    model.add(tf.keras.layers.Dense(1))
    optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate)
    model.compile(loss='mse', optimizer=optimizer)
    return model

#- build_model() 함수를 사용해 KerasRegressor 클래스의 객체를 만듬
keras_reg = keras.wrappers.scikit_learn.KerasRegressor(build_model)
keras_reg.fit(X_train, y_train, epochs=100, validation_data=(X_valid, y_valid),
              callbacks=[tf.keras.callbacks.EarlyStopping(patience=10)])
mse_test = keras_reg.score(X_test, y_test)

#- random Search 를 이용한 하이퍼 파라미터 탐색
from scipy.stats import reciprocal
from sklearn.model_selection import RandomizedSearchCV

param_distribs ={
    'n_hidden': [0, 1, 2, 3],
    'n_neurons': np.arange(1, 100),
    'learning_rate': reciprocal(3e-4, 3e-2)
}

rnd_search_cv = RandomizedSearchCV(keras_reg, param_distribs, n_iter=10, cv=3)

from sklearn.datasets import load_iris
from sklearn.linear_model import Perceptron
iris = load_iris()
X = iris.data[:, (2, 3)]
y = (iris.target == 0).astype(np.int)
