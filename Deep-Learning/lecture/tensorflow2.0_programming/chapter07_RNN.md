# Recurrent Neural Network: RNN
- 순환신경망은 지금까지 살펴본 네트워크와는 입력을 받아드리는 방식과 처리 방식에 차이가 있음
- RNN은 순서가 있는 데이터를 입력으로 받고, 같은 네트워크를 이용해 변화하는 입력에 대한 출력을 얻어냄
- 순서가 있는 데이터 : 음악, 자연어, 날씨, 주가 등
- 이번 장에서는 자연어 처리에 순환 신경망을 사용하는 방법을 알아보자

## 7.1 순환 신경망의 구조
- RNN은 되먹임 구조를 가지고 있다는 차이점이 있음.  
  되먹임 구조는 어떤 레이어의 출력을 다시 입력으로 받는 구조를 말함
- 기억해야할 것은 레이어의 출력값이 다음 입력을 받을 때의 RNN 네트워크에도 동일하게 전달되고 있다는 것
- 즉 RNN 네트워크는 처음 X1을 입력으로 받고 그 다음에는 X2와 이전 단계의 출력인 Y1, 그 다음에는 X3와 이전 단계의 출력은 Y2를 입력으로 받음
- 이 과정에서 RNN 네트워크는 동일하게 사용됨

![img](RNN.JPG)

- 순환 신경망은 입력과 출력의 길이에 제한이 없다는 특징이 있음  
  따라서 아래 그림과 같은 다양한 형태의 아키텍처 설계가 가능함
- 예를 들어 이미지에 대한 설명을 생성하는 설명 생성(Image Captioning), 문장의 긍정/부정을 판단하는 감성 분석(Sentimental Classification), 하나의 언어를 다른 언어로 번역하는 기계 번역(Machine Learning) 등이 있음

![img](various_RNN.JPG)

## 7.2 주요 레이어 정리
- 순환 신경망의 가장 기초적인 레이어는 SimpleRNN 레이어
- 실제로는 SimpleRNN 레이어보다 이것의 변종인 LSTM 레이어와 GRU 레이어가 주로 쓰임
- 자연어 처리를 위해서 꼭 알아둬야 할 임베딩(Embedding) 레이어도 알아보자

### 7.2.1 SimpleRNN 레이어
![img](simpleRNN.JPG)

- SimpleRNN 레이어는 가장 간단한 형태의 RNN 레이어
- 위의 그림은 각 단계에서 입력이 변할 때의 계산의 흐름을 보여줌
- x(t-1), x(t)는 SimpleRNN에 들어가는 입력을 나타내고, h(t-1), h(t)는 simpleRNN 레이어의 출력을 나타냄
- U, W는 입력과 출력에 곱해지는 가중치
- 단계 t에서의 SimpleRNN 레이어의 출력은 다음 수식으로 나타낼 수 있음

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=h_{t}&space;=&space;tanh(Ux_{t}&space;&plus;&space;Wh_{t-1})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?h_{t}&space;=&space;tanh(Ux_{t}&space;&plus;&space;Wh_{t-1})" title="h_{t} = tanh(Ux_{t} + Wh_{t-1})" /></a></p>

- 활성화 함수로는 tanh가 쓰임. 다른 활성화 함수를 사용할 수도 있음 
- 다음과 같이 한줄 코드로 simpleRNN 코드 사용 가능
~~~python
rnn1 = tf.keras.layers.SimpleRNN(units = 1, activation = 'tanh', return_sequences = True)
~~~
- `return_sequences`는 출력으로 시퀀스 전체를 출력할지 여부를 나타내는 옵션
- 간단한 예제를 살펴볼 것인데, 앞쪽 숫자 4개가 주어졌을 때 다음 숫자를 예측하는 간단한 '시퀀스 예측 모델'을 만들기 위해 SimpleRNN을 사용해보자
- [0.0, 0.1, 0.2, 0.3] -> [0.4]를 예측!
~~~python
import numpy as np
import tensorflow as tf
X = []
Y = []
for i in range(6):
  lst = list(range(i, i+4))
  X.append(list(map(lambda c: [c/10], lst)))
  Y.append((i+4)/10)

X = np.array(X)
Y = np.array(Y)
for i in range(len(X)):
  print(X[i], Y[i])
~~~
~~~python
model = tf.keras.Sequential([
    tf.keras.layers.SimpleRNN(units = 10, return_sequences = False, input_shape = [4,1]),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer = 'adam', loss = 'mse')
model.summary()
~~~
- `input_shape`는 여기서 각각 timesteps, input_dim을 나타냄  
  timesteps란 순환 신경망이 입력에 대해 계산을 반복하는 횟수 input_dim은 입력 벡터의 크기를 나타냄
- 예제 7.2에서 출력했던 X와 Y는 다음과 같았음
~~~python
[[0. ]
 [0.1]
 [0.2]
 [0.3]] 0.4
~~~
- 여기서 X는 [1,4,1] 차원의 벡터. 가장 첫 차원은 배치 차원이기 때문에 생략하면 두 번째의 4는 타임스텝, 세 번째의 1은 `input_dim`이 됨
- 그림으로 나타내면 다음과 같음

![img](simpleRNN2.JPG)

- 시퀀스 예측 모델은 4 타임스텝에 걸쳐 입력을 받고, 마지막에 출력값을 다음 레이어로 반환함
- 우리가 추가한 Dense 레이어에는 별도의 활성화함수는 없기 때문에 h3는 바로 y3가 됨
- 그리고 이 값과 0.4와의 차이가 mse가 됨
- 네트워크 정의가 완료되었으니, 훈련을 수행하자
~~~python
model.fit(X, Y, epochs=100, verbose=0)
print(Y)
print(model.predict(X))

[0.4 0.5 0.6 0.7 0.8 0.9]
[[0.37539446]
 [0.5094511 ]
 [0.6228687 ]
 [0.71814156]
 [0.7998563 ]
 [0.8719687 ]]
~~~
- X가 주어졌을 때 학습된 모델이 시퀀스를 어떻게 예측하는지 확인해보면 얼추 비슷하게 예측하고 있음을 확인할 수 있음
- 그렇다면, 학습 과정에서 본 적이 없는 테스트 데이터를 넣어보자
~~~python
print(model.predict(np.array([[[0.6], [0.7], [0.8], [0.9]]])))
print(model.predict(np.array([[[-0.1], [0.0], [0.1], [0.2]]])))

[[0.9369369]]
[[0.22399828]]
~~~
- 새로운 데이터에 대해서는 잘 예측하지 못함 --> 데이터를 더 추가해야함
- 실무에서는 SimpleRNN의 단점을 개선한 LSTM 레이어와 GRU 레이어등이 많이 쓰임

### 7.2.2 LSTM 레이어
- SimpleRNN 레이어의 치명적인 단점이 있는데, 입력 데이터의 길이가 길어질수록, 즉 데이터의 타임스텝이 커질수록 학습 능력이 떨어진다는 점  
이를 <b>장기의존성(Long-Term Dependency)</b> 이라고 하며 입력 데이터와 출력 데이터간의 길이가 멀어질수록 연관 관계가 적어짐
- 현재의 답을 얻기 위해 과거의 정보에 의존해야 하는 RNN이지만 과거 시점이 현재와 너무 멀어지면 문제를 풀기 힘들어지는 것
- SimpleRNN 레이어는 같은 가중치 W를 반복적으로 사용해서 출력값을 계산함  
  이런 가중치는 미분을 사용해서 오차를 구하는데, 미분시 chainRule에 의해서 미분값을 계속적으로 곱해주게 되고 이는 그레디언트 폭발(gradient exploding)이나 그레디언트 소실(gradient vanishing) 문제가 생김
- 그리고 활성화함수를 tanh 대신 ReLu를 사용하면 학습 자체가 불안정해짐
- 이러한 장기의존성 문제를 해결하기 위해 LSTM(Long Short Term Memory)가 1997년에 제안됨
- LSTM은 RNN에 비해서 복잡한 구조를 가지고 있는데, 가장 큰 특징은 출력 외에 LSTM 셀 사이에서만 공유되는 셀 상태(cell state)를 가지고 있다는 점
- simpleRNN은 cell 상태로 나타내면 다음과 같음

![img](simpleRNN_cell.JPG)


- 이에 비해 LSTM을 셀의 형태로 나타내면 아래와 같음. 꽤 복잡한 모양을 띔  
  여기서 c(t-1)과 c(t)가 바로 셀 상태를 나타내는 기호

![img](simpleRNN_cell2.JPG)

- SimpleRNN 셀에서 타임스텝의 방향으로 h(t)만 전달되고 있는 데 비해 LSTM 셀에서는 셀 상태가 c(t)인 평행선을 그리며 함께 전달되고 있음
- <b>이처럼 타임스텝을 가로지르며 셀 상태가 보존되기 때문에 장기의존성 문제를 해결할 수 있다는 것이 LSTM의 핵심 아이디어</b>
- LSTM 레이어에는 활성화함수로 tanh 외에 sigmoid 함수가 쓰임
- sigmoid는 0~1 사이의 값을 가지므로 정보가 통과하는 게이트 역할을 함
- 출력이 0이면 입력된 정보가 하나도 통과하지 못하는 것이며, 1이면 100% 통과 
- 타임스텝 t에서의 LSTM 레이어의 출력은 다음 수식으로 나타낼 수 있음

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=i_{t}&space;=&space;sigmoid(x_{t}U^{i}&space;&plus;&space;h_{t-1}W^{i})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?i_{t}&space;=&space;sigmoid(x_{t}U^{i}&space;&plus;&space;h_{t-1}W^{i})" title="i_{t} = sigmoid(x_{t}U^{i} + h_{t-1}W^{i})" /></a></p>

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=f_{t}&space;=&space;sigmoid(x_{t}U^{f}&space;&plus;&space;h_{t-1}W^{f})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_{t}&space;=&space;sigmoid(x_{t}U^{f}&space;&plus;&space;h_{t-1}W^{f})" title="f_{t} = sigmoid(x_{t}U^{f} + h_{t-1}W^{f})" /></a></p>

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=o_{t}&space;=&space;sigmoid(x_{t}U^{o}&space;&plus;&space;h_{t-1}W^{o})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?o_{t}&space;=&space;sigmoid(x_{t}U^{o}&space;&plus;&space;h_{t-1}W^{o})" title="o_{t} = sigmoid(x_{t}U^{o} + h_{t-1}W^{o})" /></a></p>

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=\widetilde{c}_{t}&space;=&space;tanh(x_{t}U^{\widetilde{c}}&space;&plus;&space;h_{t-1}W^{\widetilde{c}})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\widetilde{c}_{t}&space;=&space;tanh(x_{t}U^{\widetilde{c}}&space;&plus;&space;h_{t-1}W^{\widetilde{c}})" title="\widetilde{c}_{t} = tanh(x_{t}U^{\widetilde{c}} + h_{t-1}W^{\widetilde{c}})" /></a></p>

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=c_{t}&space;=&space;f_{t}&space;*&space;c_{t-1}&space;&plus;&space;i_{t}&space;*&space;\widetilde{c}_{t}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?c_{t}&space;=&space;f_{t}&space;*&space;c_{t-1}&space;&plus;&space;i_{t}&space;*&space;\widetilde{c}_{t}" title="c_{t} = f_{t} * c_{t-1} + i_{t} * \widetilde{c}_{t}" /></a></p>

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=h_{t}&space;=&space;tanh(c_{t})&space;*&space;O_{t}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?h_{t}&space;=&space;tanh(c_{t})&space;*&space;O_{t}" title="h_{t} = tanh(c_{t}) * O_{t}" /></a></p>

- i(t), f(t), o(t)는 각각 타임스텝 t에서의 Input, Forget, Output 게이트를 통과한 출력을 의미함
- ~c_{t}는 SimpleRNN에서도 존재하던 x(t)와 h(t-1)을 각각 U와 W에 곱한뒤에 tanh 활성화함수를 취해준 값으로, 셀 상태인 c^{t}가 되기 전의 출력값
- 마지막 두 줄은 셀 상태와 LSTM의 출력을 계산하는 가장 중요한 부분
- LSTM의 학습 능력을 확인하기 위해 살펴볼 예제 코드는 LSTM을 처음 제안한 논문에 나온 실험 여섯개 중 다섯 번째인 곱셈 문제(Multipliction problem)임 
- 이 문제는 말 그대로 실수에 대해 곱셈을 하는 문제인데, 고려해야 할 실수의 범위가 100개이고 그중에서 마킹된 두 개의 숫자만 곱해야 한다는 특이한 문제

![img](multiplication_problem.JPG)

- 위의 문제를 먼저 SimpleRNN에서 풀어보고, LSTM 레이어를 사용해보자
- 3000개의 데이터를 만들고, 2560개르 훈련 데이터, 나머지 440개를 테스트 데이터로 사용해보자
~~~python
X = []
Y = []
for i in range(3000):
  lst = np.random.rand(100)
  idx = np.random.choice(100, 2, replace = False)
  zeros = np.zeros(100)
  zeros[idx] = 1

  X.append(np.array(list(zip(zeros, lst))))
  Y.append(np.prod(zeros[idx]))

print(X[0], Y[0])
~~~
- 이제 SimpleRNN 레이어를 이용한 곱셈 문제 모델을 정의해보자

~~~python
model = tf.keras.Sequential([
    tf.keras.layers.SimpleRNN(units = 30, return_sequences = True, input_shape = [100, 2]),
    tf.keras.layers.SimpleRNN(units = 30),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer = 'adam', loss = 'mse')
model.summary()
~~~
- RNN 레이어를 겹치기 위해 첫 번째 SimpleRNN 레이어에서 `return_Sequences = True`로 설정된 것을 확인할 수 있음
- `return_sequences`는 레이어의 출력을 다음 레이어로 그대로 넘겨주게 됨. 네트워크의 구조는 다음과 같음

![img](simpleRNN_sequence.JPG)

- ho^{1} 이라고 돼 있는 부분에서 윗첨자에 해당하는 오른쪽 위의 숫자 1은 첫 번째 레이어를 의미함
- 첫번째 SimpleRNN은 모든 출력을 다음 레이어로 넘기기 때문에 두 번째 SimpleRNN 레이어도 각 타임스텝에 대해 아래쪽과 옆에서 오는 양방향의 입력을 정상적이게 받음
- 두 번째 레이어는 return_sequences 인수가 지정돼 있지 않기 때문에 기본값인 False가 돼서 마지막 계산값만 출력으로 넘기고 마지막의 Dense 레이어의 출력과 정답과의 평균 제곱 오차를 비교하고 오차를 줄이는 방향으로 네트워크 학습
- 실제로 학습을 수행해보자
~~~python 
X = np.array(X)
Y = np.array(Y)
history = model.fit(X[:2560], Y[:2560], epochs = 100, validation_split = 0.2)

import matplotlib.pyplot as plt
plt.plot(history.history['loss'], 'b-', label='loss')
plt.plot(history.history['val_loss'], 'r--', label='val_loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()

model.evaluate(X[2560:], Y[2560:])
prediction = model.predict(X[2560:2560+5])

for i in range(5):
  print(Y[2560+i], '\t', prediction[i][0], '\tdiff:', abs(prediction[i][0] - Y[2560+i]))

prediction = model.predict(X[2560:])
fail = 0
for i in range(len(prediction)):
  if abs(prediction[i][0] - Y[2560+i]) > 0.04:
    fail = fail + 1

print('correctness:', (440 - fail) / 440 * 100, '%')
~~~
- LSTM 레이어를 가지고 모델을 수행해보자
~~~python
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(units = 30, return_sequences = True, input_shape = [100, 2]),
    tf.keras.layers.LSTM(units = 30),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer = 'adam', loss = 'mse')
model.summary()history = model.fit(X[:2560], Y[:2560], epochs = 100, validation_split = 0.2)

history = model.fit(X[:2560], Y[:2560], epochs = 100, validation_split = 0.2)

import matplotlib.pyplot as plt
plt.plot(history.history['loss'], 'b-', label='loss')
plt.plot(history.history['val_loss'], 'r--', label='val_loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()ㄴ
~~~
- 훨씬 더 좋아진 것을 확인할 수 있음

### 7.2.3 GRU 레이어
- GRU(Gated Recurrent Unit) 레이어는 뉴욕대학교 조경현 교수 등이 제안한 구조
- GRU 레이어는 LSTM 레이어와 비슷한 역할을 하지만 구조가 더 간단하기 때문에 계산상의 이점이 있고 어떤 문제에서는 LSTM 레이어보다 좋은 성능을 보이기도 함
- 셀로 나타낸 GRU 레이어의 계산 흐름은 다음 그림과 같음

![img](GRU_sequence.JPG)

- LSTM과 가장 큰 차이점은 셀 상태가 보이지 않는다는 점
- GRU 레이어는 셀 상태가 없는 대신 h(t)가 비슷한 역할을 함. GRU 레이어에는 LSTM 레이어보다 sigmoid 함수가 하나 적게 쓰였는데, 이것은 게이트의 수가 하나 줄어들었음을 의미함
- 타임스텝 t에서의 GRU 레이어의 출력은 다음 수식으로 나타낼 수 있음

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=z_{t}&space;=&space;sigmoid(x_{t}U^{z}&space;&plus;&space;h_{t-1}W^{z})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?z_{t}&space;=&space;sigmoid(x_{t}U^{z}&space;&plus;&space;h_{t-1}W^{z})" title="z_{t} = sigmoid(x_{t}U^{z} + h_{t-1}W^{z})" /></a></p>

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=r_{t}&space;=&space;sigmoid(x_{t}U^{r}&space;&plus;&space;h_{t-1}W^{r})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?r_{t}&space;=&space;sigmoid(x_{t}U^{r}&space;&plus;&space;h_{t-1}W^{r})" title="r_{t} = sigmoid(x_{t}U^{r} + h_{t-1}W^{r})" /></a></p>

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=\widetilde{h_{t}}=&space;tanh(x_{t}U^{\widetilde{h}}&space;&plus;&space;(h_{t-1}&space;*&space;r^{t})W^{\widetilde{h}})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\widetilde{h_{t}}=&space;tanh(x_{t}U^{\widetilde{h}}&space;&plus;&space;(h_{t-1}&space;*&space;r^{t})W^{\widetilde{h}})" title="\widetilde{h_{t}}= tanh(x_{t}U^{\widetilde{h}} + (h_{t-1} * r^{t})W^{\widetilde{h}})" /></a></p>

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=h_{t}&space;=&space;(1&space;-&space;z_{t})*&space;h_{t-1}&space;&plus;&space;z_{t}&space;*&space;\widetilde{h_{t}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?h_{t}&space;=&space;(1&space;-&space;z_{t})*&space;h_{t-1}&space;&plus;&space;z_{t}&space;*&space;\widetilde{h_{t}}" title="h_{t} = (1 - z_{t})* h_{t-1} + z_{t} * \widetilde{h_{t}}" /></a></p>

- r(t)는 reset 게이트, z(t)는 Update 게이트를 통과한 출력
- Reset 게이트를 통과한 출력 r(t)는 이전 타임스텝의 출력인 h(t)에 곱해지기 때문에 이전 타임스텝의 정보를 얼마나 남길지를 결정하는 정도라고 생각할 수 있음
- Update 게이트의 출력 z(t)는 LSTM의 Input과 Forget 게이트의 출력의 역할을 동싱  수행하는 듯한 형태임
- 네번째 수식에서 tanh를 통과한 ~h(t)와 이전 타임스텝의 출력인 h(t-1)은 z(t) 값에 따라 최종 출력에서 각각 어느 정도의 비율을 점유할지 결정되기 때문
- 이제 GRU 레이어에서 앞서 푼 곱셈 문제를 얼마나 잘 푸는지 확인해보자
~~~python
model = tf.keras.Sequential([
    tf.keras.layers.GRU(units = 30, return_sequences = True, input_shape = [100, 2]),
    tf.keras.layers.GRU(units = 30),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer = 'adam', loss = 'mse')
model.summary()
~~~
- LSTM에 비해 파라미터 수가 23% 정도 감소한 수치임
- 이제는 실제로 학습시켜 보자
~~~python
X = np.array(X)
Y = np.array(Y)
history = model.fit(X[:2560], Y[:2560], epochs = 100, validation_split = 0.2)
~~~
- LSTM은 40 에포크 정도에서 가파르게 줄어들었던 것에 비해 GRU 네트워크는 20에포크 정도에서 값이 줄어들고, 값의 변화도 더 안정적임
- 정확도는 99%에 가까운 값이 나옴

### 7.2.4 임베딩 레이어
- 임베딩 레이어는 자연어를 수치화된 정보로 바꾸기 위한 레이어
- 자연어는 시간의 흐름에 따라 정보가 연속적으로 이어지는 시퀀스 데이터
- 자연어도 잘게 쪼갤 수 있는데, 띄어쓰기 단위인 단어와 몇 개의 문자를 묶어 파악하려는 n-gram 기법이 있음
- 예를 들어 3-gram 이면 "This is it" -> ["Thi", "his", "is ", "s i", "is", "is ", "s i", " it", "it."] 으로 쪼갤 수 있음 
- 딥러닝 기법이 발달한 이후는 n-gram 보다 단어나 문자 단위의 자연어 처리가 많이 사용되고 있음
- 임베딩 레이어보다 좀 더 쉬운 방법은 자연어를 구성하는 단위에 대해 정수 인덱스를 부여하는 것
- 예를 들어 "This is a cat" -> This : 0, is : 1, a : 2, cat : 3으로 인덱스 부여
- 이러한 정수 인덱스 값은 학습을 위해 신경망에 넣을 데이터로 변환할 때에는 5장 '분류'에서 배운 원-핫 인코딩을 이용해 변경해야 함
- 이러한 원-핫 인코딩은 메모리 차지가 워낙 크기 때문에 비효율적인데, 이에 비해 임베딩 레이어는 한정된 길이의 벡터로 자연어 구성 단위인 자소, 문자, 단어, n-gram 등을 표현할 수 있음
- 임베딩 레이어는 무한대의 단어를 표현할 수 있으며, 보통 임베딩 차원으로는 200 ~ 500 사이를 사용
- 임베딩 레이어는 정수 인덱스를 단어 임베딩으로 바꾸는 역할을 하기 때문에 정수 인덱스는 임베딩 레이어의 입력이 됨
- 임베딩 레이어는 정수 인덱스에 저장된 단어의 수만큼 단어 임베딩을 가지고 있다가 필요할 때 꺼내쓸 수 있는 저장공간과 같음
- 그런데 자연어에는 미리 정해놓을 수 없을 정도로 많은 단어가 있기 때문에 보통은 정수 인덱스로 저장하지 않는 단어에 대한 임베딩 값을 별도로 마련해 둠  
즉 임베딩 레이어 행 수가 10,000이라면 9,999는 미리 지정된 단어의 개수이고, 나머지 1은 지정되지 않은 단어를 위한 값. 이것을 <b>UNK(unknown)</b>이라고 함
- 구현에 따라서는 공백을 의미하는 패딩(padding) 값을 위한 인덱스를 하나 더 확보해야 할 수도 있음
- 임베딩 레이어에 대한 개념은 쉬운 편이지만 학습시키는 방법에는 여러 가지가 있음  
  대표적인 방법으로 Word2Vec, GloVe, FastText, ELMo 등이 있음

## 7.3 긍정, 부정 감성 분석
- 감성 분석(Sentiment Analysis)는 입력된 자연어 안에 주관적 의견, 감정 등을 찾아내는 문제
- 이 가운데 <b>극성(polarity) 감성 분석</b>은 문장의 긍정/부정이나 긍정/중립/부정을 분류
- 이번 절에서는 네이버의 박은정 박사가 2015년에 발표한 Naver sentiement movie corpus v1.0을 이용해 긍정/부정 감성 분석을 해보자
- 훈련 데이터로 15만 개, 테스트 데이터로 5만 개로 총 20만 개의 리뷰가 있음
- 리뷰 중 10만 개는 별점이 1-4로 부정적인 리뷰이고 나머지 10만개는 별점이 9-10으로 긍정적인 리뷰임
~~~python
import tensorflow as tf 
path_to_train_file = tf.keras.utils.get_file('train.txt', 'https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt')
path_to_test_file  = tf.keras.utils.get_file('text.txt', 'https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt')

train_text = open(path_to_train_file, 'rb').read().decode(encoding='utf-8')
test_text = open(path_to_test_file, 'rb').read().decode(encoding='utf-8')

print(train_text[:300])
~~~  
- 데이터의 각 행은 \t로 구분돼 있으 
- id -> 데이터의 고유한 id, document : 실제 리뷰 내용, label : 0(부정), 1(긍정)
- 이제 학습을 위한 훈련 데이터와 테스트 데이터를 만들어보자  
  우선 0,1만 존재하는 출력(Y)부터 처리해보자  
~~~python
train_Y = np.array([[int(row.split('\t')[2])]  for row in train_text.split('\n')[1:] if row.count('\t') > 0])
test_Y = np.array([[int(row.split('\t')[2])]  for row in test_text.split('\n')[1:] if row.count('\t') > 0])

print(train_Y.shape, test_Y.shape)
print(train_Y[:5])
~~~
- 첫 번째 줄과 두 번째 줄은 먼저 각 텍스트를 개행 문자(\n)로 분리한 다음 헤더에 해당하는 부분을 제외한 나머지([1:])에 대해 각 행을 처리함
- 각 행은 탭 문자(\t)로 나눠진 후에 2번째 원조를 정수로 변환하여 저장
- 마지막에는 `np.array`로 결과 리스트를 감싸서 네트워크에 입력하기 쉽게 만듬
- 다음으로는 입력으로 쓸 자연어를 토큰화(Tokenization)하고 정제(Cleaning)해야 함  
  토큰화란 자연어를 처리 가능한 작은 단위로 나누는 것으로, 여기서는 단어를 사용할 것이기 때문에 띄어쓰기 단위로 나누면 됨
- 정제란 원하지 않는 입력이나 불필요한 기호 등을 제거하는 것
- 정제를 위한 함수로는 김윤 박사의 CNN_sentence 깃허브 저장소의 코드 사용
~~~python
def clean_str(string, TREC=False):
    string = re.sub(r"[^가-힣A-Za-z0-9(),!?\'\`]", " ", string)     
    string = re.sub(r"\'s", " \'s", string) 
    string = re.sub(r"\'ve", " \'ve", string) 
    string = re.sub(r"n\'t", " n\'t", string) 
    string = re.sub(r"\'re", " \'re", string) 
    string = re.sub(r"\'d", " \'d", string) 
    string = re.sub(r"\'ll", " \'ll", string) 
    string = re.sub(r",", " , ", string) 
    string = re.sub(r"!", " ! ", string) 
    string = re.sub(r"\(", " \( ", string) 
    string = re.sub(r"\)", " \) ", string) 
    string = re.sub(r"\?", " \? ", string) 
    string = re.sub(r"\s{2,}", " ", string)
    string = re.sub(r"\'{2,}", "\'", string)
    string = re.sub(r"\'", "", string)    
    return string.strip() if TREC else string.strip().lower()


train_text_X = [row.split('\t')[1] for row in train_text.split('\n')[1:] if row.count('\t') > 0]
train_text_X = [clean_str(sentence, True) for sentence in train_text_X]
sentences = [sentence.split(' ') for sentence in train_text_X]
for i in range(5):
  print(sentences[i])
~~~
- 훈련 데이터의 처음 다섯 개를 출력해보면 구두점(.)과 같은 기호가 삭제되고 단어 단위로 나눠진 데이터가 생긴 것 확인 가능
- 네트워크에 입력하기 위한 데이터의 크기는 동일해야 하는데 현재는 각 문장의 길이가 다르기 때문에 문장의 길이를 맞춰줘야 함
- 이를 위해서는 적당한 길이의 문장이 어느 정도인지 확인하고, 긴 문장은 줄이고 짧은 문장에는 공백을 의미하는 패딩(padding)을 채워 넣어야 함
- 각 문장의 길이를 그래프로 그려보자
~~~python
import matplotlib.pyplot as plt
sentence_len = [len(sentence) for sentence in sentences]
sentence_len.sort()
plt.plot(sentence_len)
plt.show()

print(sum[int(l<=25) for l in sentence_len])
~~~
- 25단어 이하의 개수는 전체의 95% 정도이므로, 기준이 되는 문장의 길이를 25 단어로 잡고  
  이 이상은 생략, 이 이하는 패딩으로 길이를 25로 맞춰주면 임베딩 레이어에 넣을 준비가 끝남
- 또 처리해야 하는 부분은 각 단어의 길이를 조정하는 일인데, 예를 들어 "스파이더맨이", "스파이더맨을" 등의 단어를 "스파이터맨"으로 압축 시킬 것임
~~~python
sentences_new = []
for sentence in sentences:
  sentences_new.append([word[:5] for word in sentence[:25]])
sentences = sentences_new
for i in range(5):
  print(sentences[i])
~~~
- 앞에서 설명한 작업 중 짧은 문장을 같은 길이의 문장(25단어)으로 바꾸기 위한 패딩을 넣기 위해 `tf.keras`에서 제공하는 `pad_sequences`를 사용해 보겠음
- 또 모든 단어를 사용하지 않고 출현 빈도가 가장 높은 일부 단어만 사용하기 위해 `Tokenizer` 사용
~~~python
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer = Tokenizer(num_words=20000)
tokenizer.fit_on_texts(sentences)
train_X = tokenizer.texts_to_sequences(sentences)
train_X = pad_sequences(train_X, padding = 'post')

print(train_X[:5])
~~~
- `Tokenizer`는 데이터에 출현하는 모든 단어의 개수를 세고 빈도 수를 정렬해서 `num_words`에 지정된 만큼만 반환하고 나머지는 0으로 반환
- `tokenizer.fit_on_texts(sentences)`는 Tokenizer에 데이터를 실제로 입력
- `tokenizer.texts_to_sequences(sentences)` 는 문장을 입력받아 숫자를 반환
- 마지막으로 `pad_sequences()`는 입력된 데이터에 패딩을 더함
- `pad_sequences()` 의 `padding` 인수는 2가지가 있는데, `pre`는 문장의 앞에 패딩을 넣고, `post`는 문장의 뒤에 패딩을 넣음
- 이제 실제로 네트워크를 정의해보고 학습시켜보자  
  먼저 임베딩 레이어와 LSTM 레이어를 연결한 뒤, 마지막에 Dense 레이어의 소프트맥스 활성화함수를 사용해 긍정/부정을 분류하는 네트워크를 정의해보자
~~~python
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(20000, 300, input_length = 25),
    tf.keras.layers.LSTM(units = 50),
    tf.keras.layers.Dense(2, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(), loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
model.summary()
~~~
- `input_length` 인수를 25로 지정해서 각 문장에 들어있는 25개의 단어를 길이 300의 임베딩 벡터로 변환함
~~~python
history = model.fit(train_X, train_Y, epochs= 5, batch_size = 128, validation_split=0.2)
~~~
- 과적합이 심하게 일어남. 그 이유는 임베딩 레이어를 랜덤한 값에서부터 시작해서 학습시키기 때문에 각 단어를 나타내는 벡터의 품질이 좋지 않아서임
- 해결 방법은 임베딩 레이어를 별도로 학습시켜서 네트워크에 불러와 사용하거나 RNN이 아닌 CNN을 사용하는 방법이 있음
- 학습된 네트워크가 테스트 데이터를 평가하기 위하여 확인을 위해 `test_text`에도 `train_text`와 같은 변환 과정을 거쳐서 `test_X`를 만들고 `model_evaluate()`로 평가해 보자
~~~python
test_text_X = [row.split("\t")[1] for row in test_text.split('\n')[1:] if row.count("\t") > 0]
test_text_X = [clean_str(sentence) for sentence in test_text_X]
sentences = [sentence.split(' ') for sentence in test_text_X]
sentences_new = []
for sentence in sentences:
  sentences_new.append([word[:5] for word in sentence][:25])
sentences = sentences_new

test_X = tokenizer.texts_to_sequences(sentences)
test_X = pad_sequences(test_X, padding='post')

model.evaluate(test_X, test_Y , verbose = 0)

# 결과
[0.5710881352424622, 0.7980599999427795]
~~~ 
- 결과는 약 80%로 검증 데이터의 정확도와 비슷하게 나옴
- 이는 검증 데이터의 정확도와 비슷한 값. 그렇다면 임의의 문장에 대한 감성 분석은 어떨까?
~~~python
test_sentence = '재미있을 줄 알았는데 완전 실망했다. 너무 졸리고 돈이 아까웠다'
test_sentence = test_sentence.split(' ')
test_sentences = []
now_sentence = []
for word in test_sentence:
  now_sentence.append(word)
  test_sentences.append(now_sentence[:])

test_X_1 = tokenizer.texts_to_sequences(test_sentences)
test_X_1 = pad_sequences(test_X_1, padding = 'post', maxlen = 25)
prediction = model.predict(test_X_1)
for idx, sentence in enumerate(test_sentences):
  print(sentence)
  print(prediction[idx])

# 결과
['재미있을']
[0.53185356 0.4681464 ]
['재미있을', '줄']
[0.5092952  0.49070475]
['재미있을', '줄', '알았는데']
[0.47484526 0.52515477]
['재미있을', '줄', '알았는데', '완전']
[0.46557608 0.5344239 ]
['재미있을', '줄', '알았는데', '완전', '실망했다.']
[0.46557608 0.5344239 ]
['재미있을', '줄', '알았는데', '완전', '실망했다.', '너무']
[0.5061927  0.49380735]
['재미있을', '줄', '알았는데', '완전', '실망했다.', '너무', '졸리고']
[0.9407032  0.05929674]
['재미있을', '줄', '알았는데', '완전', '실망했다.', '너무', '졸리고', '돈이']
[0.9985127  0.00148729]
['재미있을', '줄', '알았는데', '완전', '실망했다.', '너무', '졸리고', '돈이', '아까웠다']
[9.992162e-01 7.837842e-04]
~~~
