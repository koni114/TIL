# chapter04 회귀
- 회귀는 영국의 유전학자이자 통계학자인 프랜시스 골턴이 '평균으로부터의 회귀'라는  
  개념을 설명하며 부모의 키 평균과 자녀의 키 평균을 비교하면 자녀의 키는 부모의 키보다 평균에 가까워지려는,  
  평균으로 되돌아오려는 경향이 있다는 사실을 지적함

## 선형 회귀
- 텐서플로를 쓰지 않고 선형회귀선 구하기
- 데이터는 2018년도 지역별 인구증가율과 고령인구비율
~~~python
import matplotlib.pyplot as plt
population_inc = [0.3, -0.78, 1.26, 0.03, 1.11, 15.17, 0.24, -0.24, -0.47, -0.77, -0.37, -0.85, -0.41, -0.27, 0.02, -0.76, 2.66]
population_old = [12.27, 14.44, 11.87, 18.75, 17.52, 9.29, 16.37, 19.78, 19.51, 12.65, 14.74, 10.72, 21.94, 12.83, 15.51, 17.14, 14.42]
plt.plot(population_inc, population_old, 'bo')
plt.xlabel('Population Growth Rate')
plt.ylabel('Elderly Growth Rate')
plt.show()
~~~ 
- 극단치를 제거하자
~~~python
import matplotlib.pyplot as plt
population_inc = [0.3, -0.78, 1.26, 0.03, 1.11, 0.24, -0.24, -0.47, -0.77, -0.37, -0.85, -0.41, -0.27, 0.02, -0.76, 2.66]
population_old = [12.27, 14.44, 11.87, 18.75, 17.52, 16.37, 19.78, 19.51, 12.65, 14.74, 10.72, 21.94, 12.83, 15.51, 17.14, 14.42]
plt.plot(population_inc, population_old, 'bo')
plt.xlabel('Population Growth Rate')
plt.ylabel('Elderly Growth Rate')
plt.show()
~~~
- 앞의 복잡한 수식과 최소제곱법을 쓰지 않고도  텐서플로를 이용하면 회귀선을 구할 수 있음
~~~python
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import random

X = [0.3, -0.78, 1.26, 0.03, 1.11, 0.24, -0.24, -0.47, -0.77, -0.37, -0.85, -0.41, -0.27, 0.02, -0.76, 2.66]
Y = [12.27, 14.44, 11.87, 18.75, 17.52, 16.37, 19.78, 19.51, 12.65, 14.74, 10.72, 21.94, 12.83, 15.51, 17.14, 14.42]

# a와 b를 랜덤한 값으로 초기화함
a = tf.Variable(random.random())
b = tf.Variable(random.random())

# 잔차의 제곱의 평균을 반환하는 함수
def compute_loss():
  y_pred = a * X + b
  loss = tf.reduce_mean((Y - y_pred) ** 2)
  return loss

optimizer = tf.optimizers.Adam(lr = 0.07)
for i in range(1000):
  optimizer.minimize(compute_loss, var_list = [a, b])

  if i % 100 == 99:
    print(i, "a:", a.numpy(), 'b:', b.numpy(), 'loss:', compute_loss().numpy())

line_x = np.arange(min(X), max(X), 0.01)
line_y = a * line_x + b

# 그래프를 그림
plt.plot(line_x, line_y, 'r-')
plt.plot(X, Y, 'bo')
plt.xlabel('Population Growth Rate (%)')
plt.ylabel('Elderly Population Rate (%)')
plt.show()
~~~
- 최적화 함수는 손실을 최소화해주는 과정을(복잡한 미분 계산 및 가중치 업데이트)를 자동으로 진행해주는 편리한 도구
- <b>텐서플로2.0은 여러 곳에 분산되어 있던 optimizer를 tf.optimizers 아래로 모았음</b>
~~~
optimizer = tf.optimizers.Adam(lr = 0.07)
~~~
- 여기서는 Adam optimizer를 불러왔는데, 다른 최적화 함수들에 비해서 우수하다고 알려져 있음
- 적당한 학습률(learning Rate, lr)을 넣으면 Adam은 안정적이고 효율적이게 학습함  
  보통 0.1에서 0.0001 사이의 값을 사용함
- `optimizer.minimize` 함수에서 첫번째 인수는 손실 함수를 입력하고, 두 번째 인수는 학습할 가중치를 입력함

## 4.2 다항 회귀
- 비선형 회귀 중 하나
- 위의 선형 회귀에서(ax+b) 2차 함수인(ax^2+bx+c)를 회귀선으로 써보자
- 위의 코드에서 조금만 고치면 됨
~~~python
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import random

X = [0.3, -0.78, 1.26, 0.03, 1.11, 0.24, -0.24, -0.47, -0.77, -0.37, -0.85, -0.41, -0.27, 0.02, -0.76, 2.66]
Y = [12.27, 14.44, 11.87, 18.75, 17.52, 16.37, 19.78, 19.51, 12.65, 14.74, 10.72, 21.94, 12.83, 15.51, 17.14, 14.42]

# a와 b를 랜덤한 값으로 초기화함
a = tf.Variable(random.random())
b = tf.Variable(random.random())
c = tf.Variable(random.random())

# 잔차의 제곱의 평균을 반환하는 함수
def compute_loss():
  y_pred = a * X*X + b*X  + c
  loss = tf.reduce_mean((Y - y_pred) ** 2)
  return loss

optimizer = tf.optimizers.Adam(lr = 0.07)
for i in range(1000):
  optimizer.minimize(compute_loss, var_list = [a, b, c])

  if i % 100 == 99:
    print(i, "a:", a.numpy(), 'b:', b.numpy(), 'c:', c.numpy(), 'loss:', compute_loss().numpy())

line_x = np.arange(min(X), max(X), 0.01)
line_y = a * line_x * line_x + b * line_x + c

# 그래프를 그림
plt.plot(line_x, line_y, 'r-')
plt.plot(X, Y, 'bo')
plt.xlabel('Population Growth Rate (%)')
plt.ylabel('Elderly Population Rate (%)')
plt.show()
~~~

## 4.3 딥러닝 네트워크를 이용한 회귀
- 3장에서 만든 AND, OR, XOR 연산을 하는 네트워크처럼 여기서도 딥러닝 네트워크를 만들 수 있음
- `tf.keras`의 레이어와 시퀀셜 모델을 사용해 간단한 코드를 작성해보자
~~~python
import tensorflow as tf
import numpy as np

X = [0.3, -0.78, 1.26, 0.03, 1.11, 0.24, -0.24, -0.47, -0.77, -0.37, -0.85, -0.41, -0.27, 0.02, -0.76, 2.66]
Y = [12.27, 14.44, 11.87, 18.75, 17.52, 16.37, 19.78, 19.51, 12.65, 14.74, 10.72, 21.94, 12.83, 15.51, 17.14, 14.42]

model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=6, activation = 'tanh', input_shape=(1,)),
    tf.keras.layers.Dense(units=1)
])

model.compile(optimizer=tf.keras.optimizers.SGD(lr=0.1), loss = 'mse')
model.summary()

model.predict(X)
~~~
- 학습이 잘된 것인지 그래프를 그려보자
~~~python
import matplotlib.pyplot as plt

line_x = np.arange(min(X), max(X), 0.01)
line_y = model.predict(line_x)

plt.plot(line_x, line_y, 'r-')
plt.plot(X, Y, 'bo')
plt.xlabel('Population Growth Rate (%)')
plt.ylabel('Elderly Population Rate (%)')
plt.show()
~~~
- 데이터 정규화 수행시, 검증 데이터도 훈련데이터의 평균과 표준편차를 기반으로 정규화를 수행해야 함
- 기존 코드에 정규화를 수행하자
~~~python
x_mean = train_X.mean(axis = 0)
x_std  = train_X.std(axis = 0)

train_X -= x_mean
train_X /= x_std

test_X  -= x_mean
test_X  /= x_std

y_mean = train_Y.mean(axis = 0)
y_std  = train_Y.std(axis  = 0)

train_Y -= y_mean
train_Y /= y_std

test_Y -= y_mean
test_Y /= y_std

print(train_X[0])
print(train_Y[0])
~~~
- 다음은 정규화된 데이터를 기반으로 모델을 정의
~~~python
model = tf.keras.Sequential([
     tf.keras.layers.Dense(units=52, activation = 'relu', input_shape=(13, )),
     tf.keras.layers.Dense(units=39, activation = 'relu'),
     tf.keras.layers.Dense(units=26, activation = 'relu'),
    tf.keras.layers.Dense(units = 1)
])

model.compile(optimizer = tf.keras.optimizers.Adam(lr=0.07), loss = 'mse')
model.summary()
~~~
- 다음은 `model.fit()`를 통해 모델을 학습
- `validation_split = 0.25`로 줌으로써 train dataset의 25%를 검증용 데이터로 사용
- 각 에포크의 학습 결과 출력에 loss와 함께 val_loss가 출력됨
- 출력의 경향을 보면 loss는 계속적으로 감소하지만, val_loss는 loss보다 항상 높은 값을 유지하며 항상 감소하지는 않음
~~~python
import matplotlib pyplot as plt
plt.plot(history.history['loss'], 'b-', label='loss')
plt.plot(history.history['val_loss'], 'r--', label = 'val_loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()
~~~
- 테스트 데이터를 이용해 회귀 모델을 평가해보자
~~~python
model.evaluate(test_X, test_Y)

# 결과
4/4 [==============================] - 0s 3ms/step - loss: 0.3056
0.3055945634841919
~~~
- 손실값이 0.3이 나오는 것을 확인  
  최초 validation set의 loss 값이 0.6에 비하면 많이 좋아짐을 확인
- 네트워크가 Y값을 얼마나 잘 예측하는지 확인하기 위해 실제 예측 가격과 예측 주택 가격을 1:1로 비교해보자
~~~python
pred_Y = model.predict(test_X)

plt.figure(figsize = (5,5))
plt.plot(test_Y, pred_Y, 'b.')
plt.axis([min(test_Y), max(test_Y), min(test_Y), max(test_Y)])

# y = x에 해당하는 대각선
plt.plot([min(test_Y), max(test_Y)], [min(test_Y), max(test_Y)], ls="--", c=".3")
plt.xlabel('test_Y')
plt.ylabel('pred_Y')
plt.show()
~~~
- 과적합을 줄이기 위해서는 callback 함수를 사용할 수 있음
- 콜백함수는 모델을 학습할 때 epoch가 끝날 때마다 호출됨
- `model.fit()` 함수에 `callbacks` 인수를 사용해 콜백 함수의 리스트를 지정할 수 있음
~~~python
history = model.fit(train_X, train_Y, epochs= 25, batch_size = 32, validation_split = 0.25,
callbacks = [tf.keras.callbacks.EarlyStopping(patience = 3, monitor='val_loss')])
~~~
- `patience` : 몇 번의 에포크를 기준으로 삼을 것인지 확인
- `monitor` : 어떤 값을 지켜볼 것인지에 대한 인수
- 여기서는 val_loss가 3회 연속으로 최고 기록을 갱신하지 못한다면 학습은 멈추게 됨