"""
batch_size 로 요청한 만큼 n_steps 길이의 여러 시계열을 만듬
각 시계열에는 타임 스텝마다 하나의 값만 (모든 시계열은 단변량 데이터)
이 함수는 [배치 크기, 타임 스텝 수, 1] 크기의 넘파이 배열을 반환함
각 시계열은 진폭이 같고 진동수와 위상이 랜덤한 두 개의 sin 곡선을 더하고 약간의 잡음 추가
"""
import numpy as np
import tensorflow as tf

batch_size = 20
n_steps = 50

def generate_time_series(batch_size, n_steps):
    freq1, freq2, offsets1, offsets2 = np.random.rand(4, batch_size, 1)
    time = np.linspace(0, 1, n_steps)

    series = 0.5 * np.sin((time - offsets1) * (freq1 * 10 + 10))
    series += 0.2 * np.sin((time - offsets2) * (freq2 * 20 + 20))
    series += 0.1 * (np.random.rand(batch_size, n_steps) - 0.5)

    return series[..., np.newaxis].astype(np.float32)

"""
X_train 은 7000개의 시계열을 담음 [7000, 50, 1]
X_vaild 는 2,000개, X_test 는 1,000개
각 시계열마다 하나의 값을 예측해야 하기 때문에 타깃은 열 벡터(y_train 은 [7000, 1] 크기) 
"""

n_steps = 50
series = generate_time_series(10000, n_steps + 1)
X_train, y_train = series[:7000, :n_steps], series[:7000, -1]
X_valid, y_valid = series[7000:9000, :n_steps], series[7000:9000, -1]
X_test, y_test = series[9000:, :n_steps], series[9000:, -1]

y_pred = X_valid[:, -1]
np.mean(tf.keras.losses.mean_squared_error(y_valid, y_pred))

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=[50, 1]),
    tf.keras.layers.Dense(1)
])

model.compile(loss='mse',
              optimizer='adam')

model.fit(X_train, y_train , epochs=30, validation_data=(X_valid, y_valid))

y_pred = model.predict(X_test)
np.mean(tf.keras.losses.mean_squared_error(y_test, y_pred))

#- 간단한 RNN 구현하기
model = tf.keras.Sequential([
    tf.keras.layers.SimpleRNN(1, input_shape=[None, 1])
])

model = tf.keras.Sequential([
    tf.keras.layers.SimpleRNN(1, input_shape=[None, 1])
])

"""
모든 순환 층에서 return_sequences=True 설정해야 함
그렇지 않으면 3D 배열이 아닌 2D 배열이 출력되고 다음 순환 층이 3D 형태로 시퀀스를 받지 못하여 작동 안됨
"""
model = tf.keras.models.Sequential([
    tf.keras.layers.SimpleRNN(20, return_sequences=True, input_shape=[None, 1]),
    tf.keras.layers.SimpleRNN(20, return_sequences=True),
    tf.keras.layers.SimpleRNN(1)
])

model.compile(loss='mse',
              optimizer='adam')

model.fit(X_train, y_train , epochs=30, validation_data=(X_valid, y_valid))

"""
메모리 셀 안의 층 정규화 구현해보기
- 사용자 정의 메모리 셀을 정의
- call 메서드가 두 개의 매개변수를 받는 것을 제외하고는 일반적인 층
  현재 타임 스텝의 inputs 과 이전 타임 스텝의 은닉 states 
- 간단한 RNN 셀의 경우 이전 타임 스텝의 출력과 동일한 하나의 텐서를 담고 있음
- 다른 셀의 경우 여러 상태 텐서를 가질 수 있음
- 셀은 state_size 속성과 output_size 속성을 가져야 함
- 간단한 RNN 에서는 둘 다 모두 유닛 개수와 동일함

- LNSimpleRNNCell 클래스는 다른 사용자 정의 층과 마찬가지로 keras.layers.Layer 클래스 상속
- 생성자는 유닛 개수와 활성화 함수를 매개변수로 받고 state_size 와 output_size 속성을 설정한 다음 활성화 함수 없이
  SimpleRNNCell 을 만듬
-  
"""
class LNSimpleRNNCell(tf.keras.layers.Layer):
    def __init__(self, units, activation='tanh', **kwargs):
        super().__init__(**kwargs)
        self.state_size = units
        self.output_size = units
        self.simple_rnn_cell = tf.keras.layers.SimpleRNNCell(units,
                                                             actavtion=None)
        self.layer_norm = tf.keras.layer.LayerNormalization()
        self.activation = tf.keras.activations.get(activation)

    def call(self, inputs, states):
        outputs, new_states = self.simple_rnn_cell(inputs, states)
        norm_outputs = self.activation(self.layer_norm(outputs))
        return norm_outputs, [norm_outputs] #- 하나는 출력, 하나는 은닉 상태

"""
사용자 정의 셀을 사용하려면 keras.layers.RNN 층을 사용
"""

model = tf.keras.models.Sequential([
    tf.keras.layers.RNN(LNSimpleRNNCell(20), return_sequences=True,
                        input_shape=[None, 1]), #- 입력 차원 1
    tf.keras.layers.RNN(LNSimpleRNNCell(20), return_sequences=True),
    tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(10))
])

"""
tf.keras.layers.RNN을 제외한 모든 순환 층과 케라스에서 제공하는 모든 셀은
dropout, recurrent_dropout 매개변수를 지원
dropout : 입력에 적용하는 드랍아웃 비율을 정의
recurrent_dropout : 은닉층 상태에 대한 드롭아웃 비율 정의
"""

"""
- LSTM cell 사용
"""
model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(20, return_sequences=True, input_shape=[None, 1]),
    tf.keras.layers.LSTM(20, return_sequences=True),
    tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(10))
])


model = tf.keras.models.Sequential([
    tf.keras.layers.RNN(tf.keras.layers.LSTMCell(20), return_sequences=True,
                        input_shape=[None, 1]), #- 입력 차원 1
    tf.keras.layers.RNN(tf.keras.layers.LSTMCell(20), return_sequences=True),
    tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(10))
])







