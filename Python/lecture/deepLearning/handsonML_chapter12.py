"""
tensorflow python API 정리

- 고수준 딥러닝 API
tf.keras
tf.estimator

- 저수준 딥러닝 API
tf.nn
tf.losses
tf.metrics
tf.optimizers
tf.train
tf.initializers

- 입출력과 전처리
tf.data
tf.feature_column
tf.audio
tf.image
tf.io
tf.queue

- 텐서보드 시각화
tf.summary

- 배포와 최적화
tf.distribute
tf.saved_model
tf.autograph
tf.graph_util
tf.lite
tf.quantization
tf.tpu
tf.xla

- 특수한 데이터 구조
tf.lookup
tf.nest
tf.ragged
tf.sets
tf.sparse
tf.strings

- 선형 대수와 신호 처리를 포함한 수학 연산
tf.math
tf.linalg
tf.signal
tf.random
tf.bitwise

- 그 외
tf.compat
tf.config
"""
import keras.activations

"""
12.2.1 텐서와 연산
- tf.constant() 함수로 텐서를 만들 수 있음
- 예를 들면 다음은 두 개의 행과 세 개의 열을 가진 실수 행렬을 나타내는 텐서
"""
#- tf.Tensor는 크기와 데이터 타입(dtype)를 가짐
import tensorflow as tf
t = tf.constant([[1., 2., 3.], [4., 5., 6.]])
print(t.shape)
print(t.dtype)

#- 인덱스 참조 -> numpy 와 매우 비슷
print(t[:, 1:])

#- 컬럼 하나 선택 시 numpy 가 아닌 tensor 로 유지하고 싶은 경우
print(t[..., 1, tf.newaxis])

#- 모든 종류의 텐서 연산이 가능
#- @ --> 행렬 곱셈을 위해 파이썬 3.5에 추가됨 : tf.matmul()과 동일
print(t + 10)
tf.square(t)
t @ tf.transpose(t)

"""
12.2.2 텐서와 넘파이
- 텐서는 넘파이와 사용하기가 편리함. 넘파이 배열로 텐서를 만들 수 있고 그 반대도 가능함
- 넘파이 배열에 텐서플로 연산을 적용할 수 있고 텐서에 넘파이 연산을 적용할 수 있음
"""
import numpy as np
a = np.array([1., 2., 3.])
tf.constant(a)
t.numpy()

tf.square(a)
np.square(t)

"""
12.2.3 타입 변환
- 타입 변환이 자동으로 수행되면 성능을 크게 감소시킬 수 있으므로, 텐서플로는 어떤 타입 변환도 자동으로 수행하지 않음
- 호환되지 않는 타입의 텐서로 연산을 실행하면 예외가 발생함
- 예를 들어 실수 텐서와 정수 텐서를 더할 수 없음
- 32비트 실수와 64비트 실수도 더할 수 없음
"""

tf.constant(2.) + tf.constant(40) #- error
tf.constant(2.) + tf.constant(40., dtype=tf.float64)

#- 타입 변환이 필요한 경우, tf.cast() 함수 사용
t2 = tf.constant(40., dtype=tf.float64)
tf.constant(2.0) + tf.cast(t2, tf.float32)

"""
12.2.4 변수
- 지금까지 본 tf.tensor 는 변경이 불가능한 객체
- 즉 텐서의 내용을 바꿀 수 없음. 따라서 일반적인 텐서로는 역전파로 변경되어야 하는 신경망의 가중치를 구현할 수 없음
- 또한 시간에 따라 변경되어야 할 다른 파라미터도 있음
- 이럴 때는 tf.Variable이 필요한 이유

- tf.Variable 은 tf.Tensor 와 비슷하게 작동함
- 동일한 연산을 수행할 수 있고 넘파이와도 잘 호환됨. 하지만 tf.Variable 은 assign() 메서드를 사용하여 
- 변숫값을 바꿀 수 있음

- assign_add(), assign_sub() 메서드 사용
- assign 메서드나 scatter_update(), scatter_nd_update() 를 사용하여 개별 원소를 수정 가능
- 중요한 것은 직접 수정은 안됨!
- tf.Variable 은 사실 tf.tensor 를 사용하여 만들어지며, 변수의 값을 증가시키거나 원소의 값을 바꾸면   
  새로운 텐서가 만들어짐
  
- 케라스는 add_weight() 메서드로 변수 생성을 대신 처리해주기 때문에 실전에서 변수를 직접 만드는 일을 드뭄
- 또한 모델 파라미터는 일반적으로 옵티마이저가 업데이트하므로 수동으로 변수를 업데이트 하는 일은 매우 드뭄
"""
v = tf.Variable([[1., 2., 3.], [4., 5., 6.]])
print(v)

v.assign(2 * v)
v[0, 1].assign(42)
v[:, 2].assign([0., 1.])
v.scatter_nd_update(indices=[[0, 0], [1, 2]], updates=[100., 200.])

"""
12.2.5 다른 데이터 구조
- 희소 텐서(tf.SparseTensor) : 대부분 0으로 채워진 텐서를 효율적으로 나타냄
- 텐서 배열(tf.TensorArray)  : 텐서의 리스트. 기본적으로 고정된 길이를 가지지만 동적으로 바꿀 수 있음
- 레그드 텐서(tf.RaggedTensor) : 리스트의 리스트를 나타냄. 텐서에 포함된 값은 동일한 데이터 타입을 가져야 하지만  
리스트의 길이는 다를 수 있음
- 문자열 텐서(string tensor) : Unicode 가 아닌 바이트 문자열을 나타냄. 즉 자동으로 UTF-8로 인코딩됨
- 집합(set) : 일반적인 텐서로 나타냄. 
- 큐(queue) : 큐는 단계별로 텐서를 저장함. 텐서플로는 여러 종류의 큐를 제공  
             FIFOQueue, PriorityQueue, RandomShuffleQueue, PaddingFIFOQueue 등
             tf.queue 패키지에 포함되어 있음
"""

"""
12.3 사용자 정의 모델과 훈련 알고리즘
- 후버 손실 함수를 마치 없는 것처럼 생각하고 직접 구현해보기
- ** 레이블과 예측을 매개변수로 받는 함수를 만들고, 텐서플로 연산을 사용해 샘플의 손실 계산 

- 중요한 것은 성능을 위해 벡터화해서 구현해야 하며, 
  텐서플로 그래프의 장점을 활용하려면 텐서플로 연산만 사용해야 함  

- 전체 손실의 평균이 아니라, 샘플마다 하나의 손실을 담은 텐서를 반환하는 것이 좋음
- 이렇게 해야 필요할 때 케라스가 클래스 가중치나 샘플 가중치를 적용할 수 있음 
"""

model = tf.keras.models.Sequential([])


def huber_fn(y_true, y_pred):
    error = y_true - y_pred
    is_small_error = tf.abs(error) < 1
    squared_loss = tf.square(error) / 2
    linear_loss = tf.abs(error) - 0.5
    return tf.where(is_small_error, squared_loss, linear_loss)


model.compile(loss=huber_fn, optimizer='nadam')
model.fit([...])

"""
12.3.2 사용자 정의 요소를 가진 모델을 저장하고 로드하기
- 케라스가 함수 이름을 저장하므로 사용자 정의 손실 함수를 사용하는 모델은 아무 이상 없이 저장됨
- ** 모델은 로드 할 때는 함수 이름과 실제 함수를 매핑한 딕셔너리를 전달해야함! 

- HuberLoss class
- 모델 저장 시 케라스는 손실 객체의 get_config() 메서드를 호출하여 반환된 설정을 HDF5 파일에 JSON 형태로 저장
- 모델을 로드하면 HuberLoss 클래스의 from_config() 클래스 메서드를 호출함
- 이 메서드는 기본 손실 클래스(Loss)에 구현되어 있고 생성자에게 **config 매개변수를 전달해 클래스의 인스턴스를 만듬
"""
model = tf.keras.models.load_model("my_model_with_a_custom_loss.h5",
                                   custom_objects={"huber_fn": huber_fn})

#- 만약 특정 파라미터를 받는 사용자 정의 손실 함수를 만들고 싶으면 closer 로 구현
def create_huber(threshold=1.0):
    def huber_fn(y_true, y_pred):
        error = y_true - y_pred
        is_small_error = tf.abs(error) < threshold
        square_error = tf.square(error) / 2
        linear_loss = threshold * tf.abs(error) - threshold ** 2 / 2
        return tf.where(is_small_error, square_error, linear_loss)
    return huber_fn


model.compile(loss=create_huber(2.0), optimizer='adam')

#- 조심해야 할 것은 파라미터 값은 저장되지 않으므로, 모델을 로드할 때 threshold 값을 직접 지정해야 함
model = tf.keras.models.load_model("my_model_with_a_custom_loss.h5",
                                   custom_objects={"huber_fn": create_huber(2.0)})

#- 위의 문제는 keras.losses.Loss 클래스를 상속하고 get_config() 메서드를 구현해서 해결할 수 있음
class HuberLoss(tf.keras.losses.Loss):
    #- kwargs 를 부모 클래스의 생성자에게 전달 --> 손실함수의 name, 개별 샘플의 손실을 모으기 위한 reduction 알고리즘 등
    def __init__(self, threshold=1.0, ** kwargs):
        self.threshold = threshold
        super().__init__(**kwargs)

    #- call() 은 레이블과 예측을 받고 모든 샘플의 손실을 계산하여 반환
    def call(self, y_true, y_pred):
        error = y_true - y_pred
        is_small_error = tf.abs(error) < self.threshold
        square_error = tf.square(error) / 2
        linear_loss = self.threshold * tf.abs(error) - self.threshold ** 2 / 2
        return tf.where(is_small_error, square_error, linear_loss)

    #- 매핑된 딕셔너리를 반환
    def get_config(self):
        base_config = super().get_config()
        return {**base_config, "threshold": self.threshold}

#- model.compile 시 클래스의 인스턴스를 사용할 수 있음
model.compile(loss=HuberLoss(2.), optimizer='nadam')

#- 모델을 로드할 때 클래스 이름과 클래스 자체를 매핑해 주어야 함
model = tf.keras.models.load_model("my_model_with_a_custom_loss.h5",
                                   custom_objects={"HuberLoss": HuberLoss})

"""
12.3.3 활성화 함수, 초기화, 규제, 제한을 커스터마이징하기
- 손실, 규제, 제한, 초기화, 지표, 활성화 함수, 층, 모델과 같은 대부분의 케라스 기능은 유사한 방법으로 커스터마이징 가능
- tf.zeros_like : tensor 크기 만큼 0으로 채운 tensor return

- 매개변수는 사용자가 정의하려는 함수의 종류에 따라 다름
- 만들어진 사용자 정의 함수는 보통의 함수와 동일하게 사용할 수 있음
- 손실, 활성화 함수, 층, 모델의 경우 call() 메서드를 구현해야 함
"""
# 사용자 정의 활성화 함수
def my_softplus(z):
    return tf.math.log(tf.exp(z) + 1.0)

# 사용자 정의 글로럿 초기화
def my_glorot_initializer(shape, dtype=tf.float32):
    stddev = tf.sqrt(2. / (shape[0] + shape[1]))
    return tf.random.normal(shape, stddev=stddev, dtype=dtype)

# 사용자 정의 l1 규제
def my_l1_regularizer(weights):
    return tf.reduce_sum(tf.abs(0.01 * weights))

# 양수인 가중치만 남기는 사용자 정의 제한
def my_positive_weights(weights):
    return tf.where(weights < 0., tf.zeros_like(weights), weights)


#- 만들어진 사용자 정의 함수는 보통의 함수와 동일하게 사용할 수 있음
#- 활성화 함수는 Dense 층의 출력에 적용되고 다음 층에 그 결과가 전달됨
#- 해당 층의 가중치는 초기화 함수에서 반환된 값으로 초기화됨
#- 훈련 스텝마다 가중치가 규제 함수에 전달되어 규제 손실을 계산하고 전체 손실에 추가
#- 제한 함수가 훈련 스텝마다 호출되어 층의 가중치를 제한한 가중치 값으로 바뀜
layer = tf.keras.layers.Dense(30, activation=my_softplus,
                              kernel_initalizer=my_glorot_initializer,
                              kernel_regularizer=my_l1_regularizer,
                              kernel_constraint=my_positive_weights)

#- factor 하이퍼 파라미터를 저장하는 l1 규제를 위한 간단한 클래스 예
#- 이 경우, 부모 클래스에 생성자와 get_config() 메서드가 정의되어 있지 않기 때문에 호출할 필요 없음
#- 만약 Regularizer 클래스를 상속한 다른 규제 클래스를 상속하여 사용자 정의 규제를 만든다면
#- get_config() 메서드를 호출해야 함

class MyL1Regularizer(tf.keras.regularizers.Regularizer):
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, weights):
        return tf.reduce_sum(tf.abs(self.factor * weights))

    def get_config(self):
        return {'factor': self.factor}

"""
12.3.4 사용자 정의 지표
- 훈련하는 동안 각 배치에 대해 케라스는 지표를 계산하고 에포크가 시작할 때부터 평균을 기록함
- 이 방식이 대부분 들어 맞지만 항상 그런것은 아님
- 예를 들어 이진 분류기의 정밀도를 생각해볼 때, 
  - 모델이 첫 번째 배치에서 5개 양성 예측을 만들고 4개를 맞췄다면 80%
  - 두 번째 배치에서 3개의 양성 예측을 만들었는데 모두 틀렸으면 0%
  - 두 정밀도를 평균하면 40% 를 얻지만, 모델의 진짜 정밀도 값이 아님
  - 4 / 8  = 50% 임!
- 결과적으로 진짜 양성 개수와 거짓 양성 개수를 기록하고 필요할 때 정밀도를 계산할 수 있는 객체가 필요  

- 스트리밍 지표를 만들고 싶다면,  keras.metrics.Metric 클래스를 상속
- 지표를 간단한 함수로 정의하면 앞서 우리가 수동으로 했던 것처럼 케라스가 배치마다 자동으로 이 함수 호출하고 
  에포크 동안 평균을 기록함
- HuberMetric 클래스를 정의하는 유일한 이점은 threshold 를 저장하는 것임
"""

precision = tf.keras.metrics.Precision()
precision([0, 1, 1, 1, 0, 1, 0, 1], [1, 1, 0, 1, 0, 1, 0, 1])
precision([0, 1, 0, 0, 1, 0, 1, 1], [1, 0, 1, 1, 0, 0, 0, 0])

#- result() : 현재 지푯값 얻을 수 있음
#- variables() : 변수 확인
#- reset_states() : 변수 초기화

precision.result()
precision.variables
precision.reset_states()

#- 다음은 전체 후버 손실과 지금까지 처리한 샘플 수를 기록하는 클래스
#- 생성자
#  - add_weight() 메서드를 사용하여 여러 배치에 걸쳐 지표의 상태를 기록하기 위한 변수 생성
#  - 후버 손실의 합, 후버 손실의 샘플 수를 기록함
#  - 케라스는 속성으로 만들어진 모든 tf.Variable 을 관리

#- update_state
#  - 이 클래스를 함수처럼 사용할 때 호출됨
#  - 배치의 레이블과 예측을 바탕으로 변수를 업데이트 함

#- result
#  - 최종 결과를 계산하고 반환
#  - 이 예에서는 모든 샘플에 대한 평균 후버 손실값
#  - 이 지표 클래스를 함수처럼 사용하면 먼저 update_state() 메서드가 호출되고 그다음 result() 메서드가 호출됨

class HuberMetric(tf.keras.metrics.Metric):
    def __init__(self, threshold=1.0, **kwargs):
        super().__init__(**kwargs)
        self.threshold = threshold
        self.huber_fn = create_huber(threshold)
        self.total = self.add_weight("total", initializer='zeros')
        self.count = self.add_weight("count", initializer='zeros')

    def update_state(self, y_true, y_pred, sample_weight=None):
        metric = self.huber_fn(y_true, y_pred)
        self.total.assign_add(tf.reduce_sum(metric))
        self.count.assign_add(tf.cast(tf.size(y_true), tf.float32))

    def result(self):
        return self.total / self.count

    def get_config(self):
        base_config = super().get_config()
        return {**base_config, "threshold": self.threshold}


"""
12.3.5 사용자 정의 층
- 텐서플로에서는 없는 특이한 층을 가진 네트워크를 만들어야 할 때가 있음
- 이런 경우 사용자 정의 층을 만듬
- 동일한 층 블럭이 여러 번 반복되는 네트워크를 만들 경우 각각의 층 블럭을 하나의 층으로 다루는 것이 편리함
- ex) A, B, C, A, B, C, A, B, C 순서대로 구성되어 있다면 A, B, C를 사용자 정의 층 D로 구성하고
- D, D, D로 구성된 모델을 만들 수 있음

- keras.layers.Flatten 이나 keras.layers.ReLU와 같은 층은 가중치가 없음
- 가중치가 필요없는 사용자 정의 층을 만드는 가장 간단한 방법은 파이썬 함수를 만든 후 keras.layers.Lambda 층으로 감싸는 것 
"""

#- 지수 함수를 적용하는 층
#- 이 사용자 정의 층을 시퀀셜 API, 함수형 API, 서브클래싱 API 에서 보통의 층과 동일하게 사용 가능
exponential_layer = tf.keras.layers.Lambda(lambda x: tf.exp(x))

#- 활성화 함수로도 사용 가능
#- activation = tf.exp, activation=tf.keras.activations.exponential,
#-              activation="exponential"

#- 상태가 있는 층을 만드려면 keras.layers.Layer 를 상속해야 함
#- 예를 들면 다음 클래스는 Dense 층의 간소화 버전을 구현한 것

#- 생성자
#  - 모든 하이퍼파라미터를 매개변수로 받음
#  - ** kwargs 매개변수를 추가하는 것도 중요
#  - 이를 통해 input_shape, trainable, name 과 같은 기본 매개변수들을 처리할 수 있음
#  - activation 매개변수를 keras.activations.get() 함수를 사용해 적절한 활성화 함수로 바꿈
#    - "selu", "relu" 같은 문자열이나, 객체를 받음

#- build()
#  - 가중치마다 add_weight() 메서드를 호출하여 층의 변수를 만드는 것
#  - 층이 처음 사용될 때 호출됨
#  - 이 시점에 케라스가 층의 입력 크기를 알고 있을 것이므로 build 메서드의 입력으로 크기를 전달
#  - 가중치를 민들 때 크기가 꼭 필요한 경우가 종종 있음
#  - 예를 들어 연결 가중치(kernel)을 만들려면 이전 층의 뉴런 개수를 알아야 함
#  - 이 크기는 입력의 마지막 차원 크기에 해당되며, 부모의 build() 메서드를 호출해야 함
#  - 이를 통해 층이 만들어졌다는 것을 케라스가 인식함

#- call()
#  - 이 층에 필요한 연산을 수행

#- compute_output_shape()
#  - 이 층의 출력 크기를 반환
class MyDense(tf.keras.layers.Layer):
    def __init__(self, units, activation=None, **kwargs):
        super().__init__(**kwargs)
        self.units = units
        self.activation = tf.keras.activations.get(activation)

    def build(self, batch_input_shape):
        self.kernel = self.add_weight(
            name='kernel', shape=[batch_input_shape[-1], self.units],
            initializer='glorot_normal')
        self.bias = self.add_weight(
            name='bias', shape=[self.units], initializer="zeros")
        super().build(batch_input_shape)

    def call(self, X):
        return self.activation(X @ self.kernel + self.bias)

    def compute_output_shape(self, batch_input_shape):
        return tf.TensorShape(batch_input_shape.as_list()[:-1] + [self.units])

    def get_config(self):
        base_config = super().get_config()
        return {**base_config, "units": self.units,
                "activation": keras.activations.serialize(self.activation)}

#- 다음 예는 두 개의 입력과 세 개의 출력을 만드는 층
#- 함수형 API, 서브클래싱 API에서만 사용 가능
class MyMultiLayer(tf.keras.layers.Layer):
    def call(self, X):
        X1, X2 = X
        return [X1 + X2, X1 * X2, X1 / X2]

    def compute_output_shape(self, batch_input_shape):
        b1, b2 = batch_input_shape
        return [b1, b1, b1]

#- 훈련과 테스트에서 다르게 동작하는 층(ex) Drop-out, Batch-Normalization)인 경우,
#- call 메서드에서 training 매개변수를 추가하여 훈련인지 테스트인지 결정해야 함

"""
12.3.6 사용자 정의 모델
- keras.Model 클래스를 상속하여 생성자에서 층과 변수를 만들고, 모델이 해야 할 작업을 call() 메서드에 구현
- 예를 들어 skip connection 이 있는 잔차 블록 층을 가진 모델을 만든다고 가정해보자

- 입력이 첫 번째 완전 연결 층을 통과
- 두 개의 완전 연결 층과 스킵 연결로 구성된 residual block 전달
- 동일한 잔차 블록에 세 번 더 통과
- 두 번째 잔차 블록을 지나 마지막 출력이 완전 연결된 출력 층에 전달
- ** (이런 구조는 실제 사용되는 것은 아니며, 모델 생성 예시를 위해 가정)
"""
#- 먼저 residual Block 층 생성
class ResidualBlock(tf.keras.layers.Layer):
    def __init__(self, n_layers, n_neurons, **kwargs):
        super().__init__(**kwargs)
        self.hidden = [tf.keras.layers.Dense(n_neurons, activation='elu',
                                             kernel_initializer="he_normal")
                       for _ in range(n_layers)]

    def call(self, inputs):
        Z = inputs
        for layer in self.hidden:
            Z = layer(Z)
        return inputs + Z


#- 서브클래싱 API 를 사용해 모델 정의
class ResidualRegressor(keras.Model):
    def __init__(self, output_dim, **kwargs):
        super().__init__(**kwargs)
        self.hidden1 = tf.keras.layers.Dense(30, activation='elu',
                                             kernel_initalizer='he_normal')
        self.block1 = ResidualBlock(2, 30)
        self.block2 = ResidualBlock(2, 30)
        self.out = tf.keras.layers.Dense(output_dim)

    def call(self, inputs):
        Z = self.hidden1(inputs)
        for _ in range(1 + 3):
            Z = self.block1(Z)
        Z = self.block2(Z)
        return self.out(Z)

#- save, load 를 사용하고 싶다면 get_config() 구현 필요
#- 또한 save_weights(), load_weights() 메서드를 사용해 가중치를 저장하고 로드할 수 있음

# Model 클래스는 Layer 클래스의 서브 클래스이므로, 모델을 층처럼 정의할 수 있음
# 하지만 모델은 compile(), fit(), evaluate(), predict() 메서드와 같은 추가적인 기능이 있음
# 또한 get_layers(), save() 메서드가 있음

"""
12.3.7 모델 구성 요소에 기반한 손실과 지표
- 앞서 정의한 사용자 손실과 지표는 모두 레이블과 예측을 기반으로 함
- 은닉층의 가중치, 활성화 함수 등과 같이 모델의 구성 요소에 기반한 손실을 정의해야 할 때가 있음
- 이런 손실은 규제나 모델의 내부 상황을 모니터링 할 때 유용 
- add_loss() 메서드에 그 결과를 전달함

- 예를 들어 5개의 은닉층과 출력층으로 구성된 회귀용 MLP 모델을 만들어보자
- 이 모델은 맨 위의 은닉층에 보조 출력을 가짐
- 보조 출력에 연결된 손실을 재구성 손실(reconstruction loss) 라고 부르겠음
  이는 재구성과 입력 사이의 평균 제곱 오차
- 재구성 손실을 주 손실에 더해서 회귀 작업에 직접적으로 도움이 되지 않는 정보일지라도 모델이 은닉층을 통과하면서
  가능한 많은 정보를 유지하도록 유도함
- 이런 손실이 이따금 일반화 성능을 향상시킴  
"""

# 사용자 정의 재구성 손실을 가지는 모델을 만드는 코드
#- 생성자
#  - 다섯 개의 은닉층, 하나의 출력층으로 구성된 심층 신경망 생성

#- build()
#  - 완전 연결 층을 하나 더 추가하여 모델의 입력을 재구성하는데 사용
#  - 유닛 개수는 입력 개수와 같아야 함
#  - 이런 재구성 층을 build() 메서드에서 만드는 이유는 이 메서드가 호출되기 전까지는 입력 개수를 알 수 없기 때문

#- call()
#  - 입력이 다섯 개의 은닉층에 모두 통과함
#  - 그다음 결괏값을 재구성 층에 전달하여 재구성을 만듬
#  - 재구성 손실을 계산하고 add_loss() 메서드를 사용해 모델의 손실 리스트에 추가
#  - 재구성 손실이 주 손실을 압도하지 않도록 0.05를 곱하여 크기를 줄임
#  - 메서드 마지막에서 은닉층의 출력을 출력층에 전달하여 얻은 출력값을 반환

class ReconstructingRegressor(tf.keras.Model):
    def __init__(self, output_dim, **kwargs):
        super().__init__(**kwargs)
        self.hidden = [tf.keras.layers.Dense(30, activation='selu',
                                             kernel_initializer="lecun_normal")
                       for _ in range(5)]
        self.out = tf.keras.layers.Dense(output_dim)

    def build(self, batch_input_shape):
        n_inputs = batch_input_shape[-1]
        self.reconstruct = tf.keras.layers.Dense(n_inputs)
        super().build(batch_input_shape)

    def call(self, inputs):
        Z = inputs
        for layer in self.hidden:
            Z = layer(Z)
        reconstruction = self.reconstruct(Z)
        recon_loss = tf.reduce_mean(tf.square(reconstruction - inputs))
        self.add_loss(0.05 * recon_loss)
        return self.out(Z)

"""
12.3.8 자동 미분을 사용하여 그레디언트 계산하기
"""

#- 3w1^2 + 2w1w2
def f(w1, w2):
    return 3 * w1 ** 2 + 2 * w1 * w2

#- w1에 대한 도함수 : 6w1 + 2w2
#- w2에 대한 도함수 : 2w1
#- w1, w2 = (5, 3)일 때 , 그레디언트 벡터 --> (36, 10)

#- 신경망은 수만 개의 파라미터를 가진 매우 복잡한 함수이며, 손으로 직접 도함수를 계산하는 것은 불가능
#- 한가지 대안으로 각 파라미터가 바뀔 때마다 함수의 출력이 얼마나 바뀌는지 측정하여 도함수의 근사값을 계산하는 것

w1, w2 = 5, 3
eps = 1e-6

(f(w1 + eps, w2) - f(w1, w2)) / eps
(f(w1, w2 + eps) - f(w1, w2)) / eps

#- 자동 미분 사용
w1, w2 = tf.Variable(5.), tf.Variable(3.)
with tf.GradientTape() as tape:
    z = f(w1, w2)
gradients = tape.gradient(z, [w1, w2])
print(gradients)

#- 두 번 호출되면 에러가 발생함
#- gradient 메서드가 호출된 후에는 자동으로 테이프가 즉시 지워짐
gradients = tape.gradient(z, [w1, w2])
gradients = tape.gradient(z, [w1, w2]) #- error

#- gradient() 메서드를 한 번 이상 호출해야 한다면, persistent = True 로 지정
with tf.GradientTape(persistent=True) as tape:
    z = f(w1, w2)

dz_dw1 = tape.gradient(z, w1)
dz_dw2 = tape.gradient(z, w2)
del tape

#- tf.Variable 이 아닌 객체에 대해서 z의 그레디언트를 계산하는 경우 None return
c1, c2 = tf.constant(5.), tf.constant(3.)
with tf.GradientTape() as tape:
    z = f(c1, c2)

gradients = tape.gradient(z, [c1, c2]) #- [None, None] return

#- tape.watch 를 사용하여 관련된 모든 연산을 기록하도록 강제할 수 있음
with tf.GradientTape() as tape:
    tape.watch(c1)
    tape.watch(c2)
    z = f(c1, c2)

gradients = tape.gradient(z, [c1, c2])

"""
12.4 텐서플로 함수와 그래프
- 일반적으로 텐서플로 함수는 일반 파이썬 함수보다 훨씬 빠르게 실행됨
- 특히 복잡한 연산 수행시 더 두드러짐
- 파이썬 함수를 빠르게 실행하려면 텐서플로 함수로 변환하자
- 사용자 정의 손실, 지표, 층 또는 다른 어떤 사용자 정의 함수를 작성하고 이를 케라스 모델에 사용할 때 케라스는 이 함수를 
  자동으로 텐서플로 함수로 변환함
"""
# 입력의 세 제곱을 계산하는 함수 만들기
def cube(x):
    return x ** 3

cube(2)
cube(tf.constant(2.0))

# tf.function() 을 활용하여 파이썬 함수를 텐서플로 함수로 바꿔보자
tf_cube = tf.function(cube)
tf_cube(tf.constant(2.0))

# 다른 방법으로 tf.function 데코레이터가 실제로는 널리 사용됨
@tf.function
def tf_cube(x):
    return x ** 3

#- 원본 파이썬 함수를 다시 호출하려면 python_function 속성으로 참조 가능
tf_cube.python_function(2)