# chapter06 Convolution NN
## 6.1 특징 추출
- Fashion MNIST 같은 이미지 데이터에서는 어떤 특징을 찾을 수 있을까요?
- 과거 Vision 연구에서는 특징을 찾기 위한 다양한 방법이 개발됨
- 이미지에서 사물의 외곽선에 해당하는 특징을 발견하면 물체 감지 알고리즘을 만들 수 있음
- 다른 예로 SIFT 알고리즘은 이미지의 회전과 크기에 대해 변하지 않는 특징을 추출해서 두 개의 이미지에서 서로 대응되는 부분을 찾아냄
- <b>이런 특징 추출 기법 중 하나인 컨볼루션 연산은 각 픽셀을 본래 픽셀과 그 주변 픽셀의 조합으로 대체하는 동작</b>
- 이때 연산에 쓰이는 작은 행렬을 필터(filter) 또는 커널(Kernel)이라고 함
- 각 필터의 생김새에 따라 수직선/수평선 검출, 흐림(blur) 효과, 날카로운 이미지 효과 등을 줄 수 있음
- 이런 필터들은 경험적 지식을 통해 직접 손으로 값을 넣어준 결과임
- 이것을 <b>수작업으로 설계한 특징(Hand-crafted feature)</b> 이라고 함
- 수작업으로 설계한 특징에는 3가지 문제점이 존재
  - 적용하고자 하는 분야에 대한 전문적인 지식이 필요
  - 시간과 비용이 많이듬
  - 한 분야에서 효과적인 특징을 다른 분야에 적용하기 어려움
- 딥러닝 기반의 컨볼루션 연산은 이러한 문제점들을 모두 해결함. 네트워크가 특징을 추출하는 필터를 자동으로 생성함
- 학습을 계속하면 네트워크를 구성하는 각 뉴런들은 입력한 데이터에 대해 특정 패턴을 잘 추출할 수 있도록 적응하게 됨

## 6.2 주요 레이어 정리
- 지금 까지는 2개의 레이어를 배움 --> Dense, Flatten
- 분류를 위한 컨볼루션 신경망은 특징 추출기(feature extractor)와 분류기(classifier)가 합쳐져 있는 형태
- 이 가운데 특징 추출기의 역할을 하는 것은 conv layer와 pooling layer. Dense layer는 분류기 역할을 함
- 특징 추출기에서는 conv-pooling이 교차되어 배치됨
- 분류기에서는 Dense layer 사이에 과적합을 막기 위해 dropout layer가 배치됨
- 마지막 Dense layer 뒤에는 dropout layer가 배치되지 않음

### 6.2.1 컨볼루션 레이어
- 말 그대로 컨볼루션 연산을 하는 레이어
- 여기서 사용하는 필터는 사람이 미리 정해놓는 것이 아니라 네트워크 학습을 통해 자동으로 추출됨
- 따라서 코드에서 지정해야 하는 것은 필터의 개수 정도임
- 필터의 수가 많으면 다양한 특징을 추출할 수 있음
- <b>새로운 이미지의 마지막 차원 수는 필터의 수와 동일함</b> 일반적인 컨볼루션 신경망은 여러 개의 컨볼루션 레이어를 쌓으면서 뒤쪽 레이어로 갈수록 필터의 수를 점점 늘리기 때문에 이미지의 마지막 차원 수는 점점 많아짐
- 컨볼루션 레이어는 다른 레이어와 마찬가지로 `tf.keras.layers`에서 임포트 할 수 있음
- 2차원 이미지를 다루는 컨볼루션 레이어를 생성하는 코드는 다음과 같음
~~~python
conv1 = tf.keras.Conv2D(kernel_size=(3, 3), strides=(2, 2), padding='valid', filters = 16)
~~~
- Conv2D 레이어를 생성할 때 주요 인수는 kernel_size, strides, padding, filters 4가지
- `kernel_size`는 filter 행렬의 크기. 앞의 숫자는 높이, 뒤의 숫자는 너비  
  숫자를 하나만 사용할 경우 높이와 너비를 동일하게 해당 숫자로 사용한다는 의미
- `strides`는 계산 과정에서 한 스탭마다 이동하는 크기
- `padding`은 컨볼루션 연산 전에 입력 이미지 주변에 빈 값을 넣을지 지정하는 옵션  
  `valid`와 `same` 두 가지 옵션 중 하나를 사용
  - `valid`는 우리가 봐온 것과 동일한 방식으로 빈 값을 사용하지 않음  
  - `same`은 빈 값을 넣어서 <b>출력 이미지의 크기를 입력과 같도록 보존함</b>
  - 빈 값으로 0이 쓰이는 경우에 제로 패팅(zero padding)이라고 부름
- `filters`는 필터의 개수. 많을수록 많은 특징을 추출할 수 있지만, 너무 많으면 성능 저하 및 과적합이 발생할 수 있음
- 가장 유명한 CNN 중 하나인 VGG는 네트워크가 깊어질수록 필터의 수를 2배씩 늘려 나감

### 6.2.2 풀링 레이어
- 이미지를 구성하는 픽셀 중 인접한 픽셀들은 비슷한 정보를 갖고 있는 경우가 많음
- 이런 이미지의 크기를 줄이면서 중요한 정보를 남기기 위하여 subsampling 수행
- 이 과정에서 사용되는 레이어가 풀링 레이어(pooling layer)임
- 풀링 레이어에는 Max 풀링 레이어, Average 풀링 레이어 등이 있음. 이 가운데 컨볼루션 레이어에는 Max 풀링이 많이 쓰임
- 다음은 MaxPool2D 레이어의 생성 코드임
~~~python
pool1 = tf.keras.layers.MaxPool2D(pool_size=(2,2), strides = (2,2))
~~~
- `pool_size` 는 한 번에 Max 연산을 수행할 범위
- <b>풀링 레이어에는 가중치가 존재하지 않기 때문에 따로 학습되지 않으며, 네트워크 구조에 따라 생략되기도 함</b> 

### 6.2.3 드롭아웃 레이어
- 드롭아웃 레이어는 네트워크의 과적합을 막기 위한 딥러닝 연구자들의 노력의 결실임
- 드롭아웃 레이어는 앞에서 인용한 것처럼 학습 과정에서 무작위로 뉴런의 부분집합을 제거하는 것임
- 네트워크가 학습할 때 같은 레이어에 있는 뉴런들은 결괏값에 의해 서로 같은 영향을 받음
- 따라서 각 뉴런의 계산 결과를 모두 더해서 나오는 결괏값은 한쪽으로 치우치게 됨
- <b>이를 막기 위한 드롭아웃 레이어는 학습 과정에서는 확률적으로 일부 뉴런에 대한 연결을 끊고, 테스트할 때는 정상적으로 모든 값을 포함해서 계산함</b>
- 다음은 드롭아웃 레이어 생성 코드임
~~~python
pool1 = tf.keras.layers.Dropout(rate=0.3)
~~~
- `rate` 는 제외할 뉴런의 비율
- AlexNet, VGG, GoogleNet, DenseNet 등 모든 거의 주요 컨볼루션 신경망에 사용됨
- dropout layer도 가중치가 없기 때문에 학습되지 않음

## 6.3 Fasion MNIST 데이터 세트에 적용하기
- Fasion_MNIST 데이터 가져오기
~~~python
import tensorflow as tf

fashion_mnist = tf.keras.datasets.fashion_mnist 
(train_X, train_Y), (test_X, test_Y) = fashion_mnist.load_data()

train_X = train_X / 255
test_X  = test_X  / 255
~~~
- 이번 예제에서는 Conv2D 레이어로 연산을 해야하므로, 이미지는 보통 채널을 가지고 있고, Conv2D 레이어는 채널을 가진 형태의 데이터를 받도록 기본적으로 설정되어 있기 때문에 예제 6.5에서는 채널을 갖도록 데이터의 shape을 바꿈
~~~python
print(train_X,shape, test_X.shape)

train_X = train_X.reshape(-1, 28, 28, 1)
test_X  = test_X.reshape(-1, 28, 28, 1)

# reshape 이후
print(train_X.shape, test_X.shape)
~~~
~~~python
import matplotlib.pyplot as plt
plt.figure(figsize = (10, 10))
for i in range(16):
  plt.subplot(4, 4, i+1)
  plt.imshow(train_X[i].reshape(28, 28), cmap = 'gray')
plt.show()

print(train_Y[:16])
~~~
- 그래프를 그리기 위한 데이터는 2차원이어야 함 --> `reshape` 적용
- 그리드는 위에서 아래, 왼쪽에서 오른쪽 순서대로 그려짐
- 이제 모델을 생성할텐데, 먼저 비교를 위해 풀링 레이어 없이 컨볼루션 레이어만 사용한 모델을 정의해보자
~~~python
model = tf.keras.Sequential([
  tf.keras.layers.Conv2D(input_shape=(28, 28, 1), kernel_size= (3, 3), filters = 16),
  tf.keras.layers.Conv2D(kernel_size= (3, 3), filters = 32),
  tf.keras.layers.Conv2D(kernel_size= (3, 3), filters = 64),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(units = 128, activation = 'relu'),
  tf.keras.layers.Dense(units = 10, activation = 'softmax')
])

model.compile(optimizer = tf.keras.optimizers.Adam(), 
              loss ='sparse_categorical_crossentropy', 
              metrics = ['accuracy'])
model.summary()
~~~
- 구글 코랩에서는 GPU 사용이 가능
- 다음의 명령어를 통해 colab에서 사용가능한 GPU spec을 확인할 수 있음
~~~python
!nvidia-smi

Fri Feb 12 06:58:58 2021       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 460.39       Driver Version: 460.32.03    CUDA Version: 11.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla T4            Off  | 00000000:00:04.0 Off |                    0 |
| N/A   59C    P8    11W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
~~~
- GPU는 Tesla T4. 좋은 사양의 GPU임. Tesla K80보다 4배 빠름
- 이제 실제 모델을 학습시켜 보자
~~~python
history = model.fit(train_X, train_Y, epochs = 25, validation_split = 0.25)

import matplotlib.pyplot as plt
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], 'b-', label = 'loss')
plt.plot(history.history['val_loss'], 'r--', label = 'val_loss')
plt.xlabel('Epoch')
plt.legend()

plt.subplot(1, 2, 2)

plt.plot(history.history['accuracy'], 'g-', label = 'accuracy')
plt.plot(history.history['val_accuracy'], 'k--', label = 'val_accuracy')
plt.xlabel('Epoch')

plt.ylim (0.7, 1)
plt.legend()

plt.show()
~~~
- 모델의 학습에는 epoch당 7초 정도가 걸림
- 참고로 같은 환경에서 하드웨어 가속기 없이 실행했을 때는 약 3분 ~ 3분 20초 정도가 걸림
- 약 25배 ~ 28배 정도의 속도의 차이가 나기 때문에 하드웨어 가속기 설정은 필수임
- 모델 학습 결과 전형적인 과적합 형태를 띄고 있으므로, drop-out layer + pooling layer를 추가해서 다시 모델을 구축하고 학습시켜보자
~~~python
model = tf.keras.Sequential([
  tf.keras.layers.Conv2D(input_shape=(28, 28, 1), kernel_size= (3, 3), filters =  32),
  tf.keras.layers.MaxPool2D(strides=(2,2)),
  tf.keras.layers.Conv2D(kernel_size= (3, 3), filters = 64),
  tf.keras.layers.MaxPool2D(strides=(2,2)),
  tf.keras.layers.Conv2D(kernel_size= (3, 3), filters = 128),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(units = 128, activation = 'relu'),
  tf.keras.layers.Dropout(rate = 0.3),
  tf.keras.layers.Dense(units = 10, activation = 'softmax')
])

model.compile(optimizer = tf.keras.optimizers.Adam(), loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
model.summary()
~~~ 
- MaxPool layer와 Dropout layer를 추가했지만, 큰 성능을 얻지는 못함.
- 다음 장에서는 퍼포먼스를 높이기 위한 여러 방법을 알아보자

## 6.4 퍼포먼스 높이기
- CNN에서 퍼포먼스를 높일 수 있는 방법 중 '더 많은 레이어 쌓기'와 이미지 보강(Image Augmentation) 기법을 사용해보자

### 6.4.1 더 많은 레이어 쌓기
- VGG는 단순한 구조이면서도 성능이 괜찮기 때문에 지금도 이미지의 특징 추출을 위한 네트워크에서 많이 사용되고 있음
- 다음은 VGG 형태를 띈 CNN 모형을 생성한 예제 코드임
~~~python
model = tf.keras.Sequential([
  tf.keras.layers.Conv2D(input_shape=(28, 28, 1), kernel_size=(3, 3), filters=32, padding='same', activation = 'relu'),
  tf.keras.layers.Conv2D(kernel_size=(3, 3), filters=64, padding='same', activation = 'relu'),
  tf.keras.layers.MaxPool2D(strides=(2,2)),
  tf.keras.layers.Dropout(rate = 0.5),
  tf.keras.layers.Conv2D(kernel_size=(3, 3), filters=128, padding='same', activation = 'relu'),
  tf.keras.layers.Conv2D(kernel_size=(3, 3), filters=256, padding='valid', activation = 'relu'),
  tf.keras.layers.MaxPool2D(strides=(2,2)),
  tf.keras.layers.Dropout(rate = 0.5),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(units = 512, activation='relu'),
  tf.keras.layers.Dropout(rate = 0.5),
  tf.keras.layers.Dense(units = 256, activation='relu'),
  tf.keras.layers.Dropout(rate = 0.5),
  tf.keras.layers.Dense(units = 10, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()
~~~
- VGGNet은 여러 개의 구조로 실험했는데 그중 19개의 레이어가 겹쳐진 VGG-19가 가장 깊은 구조임
- VGG-19는 특징 추출기의 초반에 컨볼루션 레이어를 2개 겹친 뒤 풀링 레이어 1개를 사용하는 패턴을 2차례, 그 후 컨볼루션 레이어를 4개 겹친 뒤 풀링 레이어 1개를 사용하는 패턴을 3차례 반복함
- 여기서는 대상 이미지가 적기도 하고,  연산 능력의 한계도 있기 때문에 컨볼루션 레이어를 2개 겹치고 풀링 레이어를 1개 사용하는 패턴을 2차례 반복함
- 그다음 dropout과 pooling 레이어를 적절히 배치함(VGG-7 정도됨)

### 6.4.2 이미지 보강(image augmentation)
- `tf.keras`에는 이미지 보강 작업을 쉽게 해주는 `ImageDataGenerator`가 있음
~~~python
from tensorflow.keras.preprocessing.image import ImageGenerator
import numpy as np

image_generator = ImageGenerator(
        rotation_range     = 10,
        zoom_range         = 0.10,
        shear_range        = 0.5,
        width_shift_range  = 0.10,
        height_shift_range = 0.10,
        horizontal_flip    = True,
        vertical_flip      = False)

augment_size = 100
x_augmented = image_generator.flow(np.tile(train_X[0].reshape(28*28), 100).reshape(-1, 28, 28, 1), np.zeros(augment_size), batch_size=augment_size, shuffle=False).next()[0]
~~~
- 세로축을 뒤집는 `vertical_flip` 인수는 적용하지 않음. 그 이유는 MNIST Data는 전부 반듯한 데이터만 있기 때문에 오히려 성능을 떨어트릴 수 있음
- `flow()`는 실제로 보강된 이미지 생성. 이 함수는 Interator라는 객체를 만드는데, 이 객체에서는 값을 순차적으로 꺼낼 수 있음
- 꺼내는 방법은 `next()`를 사용하는 것. 한번에 생성할 이미지의 양인 `batch_size`를 위에서 설정한 `augmented_size`와 같은 100으로 설정했기 때문에 `next()` 로 꺼내는 이미지는 100장이 됨
- 나머지 부분은 `matplotlib.pyplot`으로 생성된 보강 이미지를 그래프로 그려주는 부분
- 실제로 훈련 데이터 이미지를 보강하기 위해 다량의 이미지를 생성하고 학습을 위해 훈련 데이터에 추가해보자
~~~python
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

image_generator = ImageDataGenerator(
        rotation_range     = 10,
        zoom_range         = 0.10,
        shear_range        = 0.5,
        width_shift_range  = 0.10,
        height_shift_range = 0.10,
        horizontal_flip    = True,
        vertical_flip      = False)

augment_size = 30000

randidx = np.random.randint(train_X.shape[0], size = augment_size)
x_augmented = train_X[randidx].copy()
y_augmented = train_Y[randidx].copy()
x_augmented = image_generator.flow(x_augmented, np.zeros(augment_size), 
                                   batch_size = augment_size, shuffle = False).next()[0]

# 원래 데이터에 x_train image augmentation data를 추가

train_X = np.concatenate((train_X, x_augmented))
train_Y = np.concatenate((train_Y, y_augmented))

print(train_X.shape)
~~~ 
- `randinx`는 정수로 구성된 넘파이 array임
- 원본 데이터에 영향을 주지 않기 위해 `.copy()` 사용
- 이제 ImageDataGenerator로 보강된 훈련 데이터를 학습시켜보면 됨