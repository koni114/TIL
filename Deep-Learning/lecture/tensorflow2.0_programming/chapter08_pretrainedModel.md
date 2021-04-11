# chapter08 사전훈련된 모델 다루기
- 최근 이미지 분류 문제에서 더 좋은 결과를 내고 있는 NASNet은 AutoML 기법을 사용해 최적의 네트워크 구조를 스스로 학습하기 때문에 훨씬 더 많은 훈련 시간이 필요
- pre-trained된 모델을 그대로 사용할 수도 있고, 전이 학습(Trasfer Learning)이나 신경 스타일 전이(Neural Style Transfer)처럼 다른 과제를 위해 재가공해서 사용할 수도 있음

## 텐서플로 허브
- 텐서플로에서 제공하는 텐서플로 허브(tensorflow Hub)는 재사용 가능한 모델을 쉽게 이용할 수 있는 라이브러리
- 텐서플로2.0을 사용하면 텐서플로 허브는 따로 설치할 필요가 없고 라이브러리를 바로 불러올 수 있음
- 다음 예제는 텐서플로 허브에서 사전 훈련된 MobileNet 모델을 불러오는 예제
~~~python
import tensorflow as tf
import tensorflow_hub as hub

mobile_net_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/2"
model = tf.keras.Sequential([
  hub.KerasLayer(handle=mobile_net_url, input_shape=(224, 224, 3), trainable=False)
])

model.summary()
~~~
~~~python
# 그림 8.2 좌측 전체 네트워크 구조 출력 코드
from tensorflow.keras.applications import MobileNetV2

mobilev2 = MobileNetV2()
tf.keras.utils.plot_model(mobilev2)
~~~
- `tensorflow_hub` 라이브러리를 `hub`라는 약어로 import 함
- 컨볼루션 신경망의 하나인 MobileNet 버전 2를 불러옴
- MobileNet은 계산 부담이 큰 컨볼루션 신경망을 연산 성능이 제한된 모바일 환경에서도 작동 가능하도록 네트워크 구조를 경량화 한 것
- MobileNet 버전 2는 버전 1을 개선했고 파라미터 수도 더 줄어듬
- 텐서플로 허브에 올라와 있는 모델은 `hub.KerasLayer()` 명령으로 `tf.keras`에서 사용 가능한 레이어로 변환할 수 있음
- `model.summary()`로 파라미터 개수를 확인해보면 354만 개 정도임. `ResNet-50`에는 2560만개, ResNet-152에는 6천만개의 파라미터가 존재하는 것에 비해서는 상대적으로 파라미터수가 적은편
- MobileNet은 ImageNet에 존재하는 1,000종류의 이미지를 분류할 수 있으며, 이 가운데 어떤 것에도 속하지 않는다고 판단될 때는 background에 해당하는 인덱스 0을 반환함
- MobileNet의 성능을 평가하기 위해 이미지를 학습시켰을 때 얼마나 적합한 라벨로 분류하는지 알아보자
- ImageNet의 데이터 중 일부만 모아놓은 ImageNetV2를 사용하자
- ImageNetV2는 아마존 메케니컬 터크를 사용해 다수의 참가자들에게서 클래스 예측값을 받아서 선별한 데이터
- 여기서는 각 클래스에서 가장 많은 선택을 받은 이미지 10장씩을 모아놓은 10,000장의 이미지가 포함된 TopImages 데이터를 사용하자
~~~python
# 8.2 ImageNetV2-TopImages 불러오기
# 8.2 ImageNetV2-TopImages 불러오기
import os
import pathlib
content_data_url = '/content/sample_data'
data_root_orig = tf.keras.utils.get_file('imagenetV2', 'https://s3-us-west-2.amazonaws.com/imagenetv2public/imagenetv2-top-images.tar.gz', cache_dir=content_data_url, extract=True)
data_root = pathlib.Path(content_data_url + '/datasets/imagenetv2-top-images-format-val')
print(data_root)
~~~
- `tf.keras.utils.get_file()` 함수로 ImageNetV2 데이터를 불러올 수 있음
- `extract=True` 로 지정했기 때문에 tar.gz 형식의 압축 파일이 자동으로 해제되어 구글 코랩 가상 머신에 저장됨
- 데이터를 잘 불러왔는지 확인해보자
~~~python
for idx, item in enumerate(data_root.iterdir()):
    print(item)
    if idx == 9:
        break
~~~
- 데이터 디렉터리 밑에 각 라벨에 대한 숫자 이름으로 하위 디렉터리가 만들어져 있는 것을 확인할 수 있음
- 하위 디렉터리는 0~999까지 총 1,000개임
- 라벨에 대한 숫자가 어떤 데이터를 뜻하는지에 대한 정보인 라벨 텍스트는 따로 불러와야 함
- MobileNet에서 사용된 라벨은 예제 8.4에서 역시 `tf.keras.utils.get_file()` 함수로 불러옴
~~~python
label_file = tf.keras.utils.get_file('label', 'https://storage.googleapis.com ')
~~~
- `img.imread(fileName)` : fileName은 filePath + fileName 인 string
- 9개의 사진을 랜덤으로 확인해보자
~~~python
import PIL.Image as Image
import matplotlib.pyplot as plt
import random

all_image_paths = list(data_root.glob('*/*'))
all_image_paths = [str(path) for path in all_image_paths]

# 이미지를 랜덤하게 섞음
random.shuffle(all_image_paths)

image_count = len(all_image_paths)
print('image_count:', image_count)

plt.figure(figsize=(12, 12))
for c in range(9):
  image_path = random.choice(all_image_paths)
  plt.subplot(3, 3, c+1)
  plt.imshow(plt.imread(image_path))
  idx = int(image_path.split('/')[-2]) + 1
  plt.title(str(idx) + ', ' + label_text[idx])
  plt.axis('off')
plt.show()
~~~
- 전통적으로 ImageNet 대회에서는 네트워크가 예측하는 값 중 상위 5개 이내에 데이터의 실제 분류가 포함되어 있으면 정답으로 인정하는 Top-5 정확도를 분류 정확도로 측정
- 요즘은 네트워크의 성능이 좋아져 Top-1 정확도를 많이 하는 추세
- 이번 예제에서는 Top-5, Top-1 정확도를 측정해보자
~~~python
import cv2
import numpy as np
top_1 = 0
top_5 = 0
for image_path in all_image_paths:
  img = cv2.imread(image_path)
  img = cv2.resize(img, dsize=(224, 224))
  img = img / 255.0
  img = np.expand_dims(img, axis = 0)
  top_5_predict = model.predict(img)[0].argsort()[::-1][:5]
  idx = int(image_path.split('/')[-2]) + 1
  if idx in top_5_predict:
    top_5 += 1
    if top_5_predict[0] == idx:
      top_1 += 1
  

print('Top-5 correctness:', top_5 / len(all_image_paths) * 100, '%')
print('Top-1 correctness:', top_1 / len(all_image_paths) * 100, '%')
~~~
- 첫 줄에서 임포트한 cv2는 OpenCV(Open Source Computer Vision) 라이브러리
- 이미지를 메모리에 불러오고 크기를 조정하는 등의 작업을 편하게 해주기 때문에 사용함
- 다음 예제는 MobileNet이 분류하는 라벨을 실제로 확인하고 Top-5 예측을 표시
~~~python
import cv2
plt.figure(figsize = (16, 16))  # 총 6개의 이미지 출력..

def softmax(x):
  e_x = np.exp(x - np.max(x))
  return e_x / e_x.sum(axis = 0)

for c in range(3):
  # 1. random으로 이미지 하나 선택
  image_path = np.random.choice(all_image_paths)
  # 2. 이미지 표시
  plt.subplot(3,2, c*2+1)
  plt.imshow(plt.imread(image_path))
  idx = int(image_path.split('/')[-2]) + 1
  plt.title(str(idx) + ' , ' + label_text[idx])
  plt.axis('off')

  # 3. 예측값 표시
  plt.subplot(3,2, c*2+2)
  img = cv2.imread(image_path)
  img = cv2.resize(img, dsize=(224, 224)) # 0~224 --> 225
  img = img / 255
  img = np.expand_dims(img, axis = 0)
  
  # 4. MobileNet을 이용한 예측
  logits = model.predict(img)[0]
  prediction = softmax(logits)

  # 5. 가장 높은 확률의 예측값 5개를 뽑음
  top_5_predict = prediction.argsort()[::-1][:5]
  print(top_5_predict)
  labels = [label_text[index] for index in top_5_predict]
  color = ['gray'] * 5
  if idx in top_5_predict:
    color[top_5_predict.tolist().index(idx)] = 'green'
  color = color[::-1]
  plt.barh(range(5), prediction[top_5_predict][::-1] * 100, color = color)
  plt.yticks(range(5), labels[::-1])
~~~

## 8.2 전이 학습
- 전이 학습(Transfer learning)은 미리 훈련된 모델을 다른 작업에 사용하기 위해 추가적인 학습을 시키는 것
- 이때 훈련된 모델은 데이터에서 유의미한 특징을 추출(feature Extractor)로 쓰이거나, 모델의 일부를 재학습 시키기도 함

### 8.2.1 모델의 일부를 재학습시키기
- 다시 재학습 시킬 시 데이터의 양이 많아질수록 freezing 시킬 레이어의 수가 줄어듬
- 전이 학습을 수행할 데이터는 스텐퍼드 대학의 Dog Dataset임  
  이 데이터는 2만여 개의 사진으로 구성돼 있으며 120가지 견종에 대한 라벨이 붙어 있음
- 케글에서 제공하는 데이터를 사용할 것인데, 케글에서 제공하는 파이썬 API를 사용하면 손쉽게 데이터를 받고 학습 결과를 캐글에 올릴 수 있음
- 캐글 API를 내려받기 위해서는 셀에서 다음과 같은 짧은 명령을 실행하면 됨
~~~python
!pip install kaggle
~~~
~~~python
import os
os.environ['KAGGLE_USERNAME'] = 'jaebig'
os.environ['KAGGLE_KEY'] = 'c56aa56b2f50367ec3f5de00df4d4b37'
!kaggle competitions download -c dog-breed-identification
~~~
~~~python
import PIL.Image as Image
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 12))
for c in range(9):
  image_id = label_text.loc[c, 'id']
  plt.subplot(3,3, c+1)
  plt.imshow(plt.imread('/content/train/' + image_id + '.jpg'))
  plt.title(str(c) + ' , ' + label_text.loc[c, 'breed'])
  plt.axis('off')
plt.show()
~~~
- 우선 전이 학습 전에 MobileNet V2의 모든 레이어의 가중치를 초기화한 상태에서 학습을 시켜보자
- 레이어 구조는 같지만 ImageNet의 데이터로 미리 훈련된 이미지 분류에 대한 지식은 전혀 없는 상태에서 학습시켜 보는 것
- 이번에는 `tf.keras`에서 MobileNet V2를 불러와서 학습시켜보자
- <b>KerasLayer로 불러오는 방법과 달리 네트워크를 각 레이어별로 분리해서 사용할 수 있기 때문에 좀 더 편리</b>
~~~python
from tensorflow.keras.applications import MobileNetV2
mobilev2 = MobileNetV2()
~~~
- 먼저 레이어의 가중치를 초기화
~~~python
for layer in mobilev2.layers[:-1]:
  layer.trainable = True

for layer in mobilev2.layers[:-1]:
  if 'kernel' in layer.__dict__:
    kernel_shape = np.array(layer.get_weights()).shape
    layer.set_weights(tf.random.normal(kernel_shape, 0, 1))
~~~
- 첫번째 for문은 모든 레이어를 훈련가능상태로 변경
- 두번째 for문은 kernel(가중치 w에 해당. bias는 mobileNet에서는 없음) 가중치를 평균이 0, 표준편차가 1인 random variable로 치환
- 이번 예제는 훈련 데이터의 모든 사진을 메모리에 올림  
  여기서 주의해야 할 점은 google colab은 고용량 램 모드로 사용할 경우 25GB의 메모리 사용 가능  
- 훈련 데이터를 모두 메모리에 올리게 되면 그 절반 정도를 사용하게 됨
- 테스트 데이터까지 동시에 올릴 경우 사용 가능한 메모리를 모두 사용했다는 메세지와 함께 코랩이 다운됨
- 메모리가 부족할 때도 학습을 시키기 위해서는 `ImageDataGenerator` 등을 사용해 파일을 디스크에서 읽어와서 학습시킬 수 있지만 속도가 매우 느림
- coLab에서 다운로드 받은 파일은 한동안 사라지지는 않음
~~~python
import cv2
train_X = []
for i in range(len(label_text)):
  img = cv2.imread('/content/train/' + label_text['id'][i] + '.jpg')
  img = cv2.resize(img, dsize=(224, 224))
  img = img / 255.0
  train_X.append(img)
train_X = np.array(train_X)
print(train_X.shape)
print(train_X.size * train_X.itemsize, 'bytes')
~~~
- MobileNet V2의 입력 형식에 맞는 (224, 224) 크기의 이미지 10,222장을 메모리에 올림
- train_X가 메모리에서 차지하는 크기는 약 12.GB로 코랩이 고용량 RAM 모드에서 제공하는 메모리의 절반 가량을 차지함
- 그 다음으로는 Y에 해당하는 라벨 데이터를 작성함
~~~python
unique_Y = label_text['breed'].unique().tolist()
train_Y  = [unique_Y.index(breed) for breed in label_text['breed']]
train_Y = np.array(train_Y)

print(train_Y[:10])
print(train_Y[-10:])
~~~
- label data를 index data 로 변경해줌
- 이제는 랜덤한 가중치를 적용시킨 가중치를 사용해 학습시킬 것임
~~~python
x = mobilev2.layers[-2].output
predictions = tf.keras.layers.Dense(120, activation='softmax')(x)
model = tf.keras.Model(inputs=mobilev2.input, outputs=predictions)

model.compile(optimizer='sgd', loss = 'sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()
~~~
- 첫번째 줄에서는 MobileNet V2에서 마지막 Dense 레이어를 제외하기 위해 뒤에서 두번째 레이어를 지정해서 그 레이어의 output을 x라는 변수에 저장
- 그 다음에는 120개의 Dense 레이어를 새롭게 만듬
- 위의 예제에서 레이어를 함수처럼 사용했는데, 이를 <b>함수형 API</b> 라고 함
- 입력부터 출력까지 일직선 구조라면 시퀀셜 모델을 사용해도 되지만, 그렇지 않은 경우에는 함수형 모델을 사용하여 모델의 입력, 출력 구조를 정의해야 함
- 함수형 모델을 정의하기 위해서는 연결에 필요한 모든 레이어를 준비한 다음, `tf.keras.Model()`의 인수인 inputs, outputs에 각각 입력과 출력에 해당하는 부분을 넣으면 `tf.keras`가 알아서 찾아서 모델을 만듬
- 이제는 실제 모델을 학습시켜 보자
~~~python
model.fit(train_X, train_Y, epochs = 10, batch_size = 32, validation_split = 0.25)
~~~
- 거의 맞추지 못하는 모습을 보임
- 이번에는 전이 학습(Transfer learning)을 이용하여 일부 가중치는 그대로 사용
~~~python
from tensorflow.keras.applications import MobileNetV2
mobilev2 = MobileNetV2()

x = mobilev2.layers[-2].output
predictions = tf.keras.layers.Dense(120, activation = 'softmax')(x)
model = tf.keras.Model(inputs = mobilev2.input, outputs = predictions)

for layer in model.layers[:20]:
  layer.trainable = False
for layer in model.layers[-20:]:
  layer.trainable = True

model.compile(optimizer='sgd', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()
~~~ 
- 훨씬 더 성능이 좋아진 것을 확인할 수 있음

### 8.2.2 특성 추출기
- 미리 훈련된 모델에서 데이터의 특징만 추출하고, 그 특징을 작은 네트워크에 통과시켜 정답을 예측하는 방법 
- 미리 추출된 특징은 디스크에 저장했다가 필요할 때 불러서 사용
- 학습할 때마다 전체 네트워크의 계산을 반복할 필요가 없기 때문에 계산 시간은 획기적으로 줄어들고, 메모리도 절약됨
- 다만 8.2.1절의 재학습 방법을 미리 훈련된 모델에서는 사용하기 어렵다는 단점도 있음
- 텐서플로 허브에서 Inception V3를 불러오자
- Inception은 2014년에 구글이 ImageNet 대회를 위해 GoogleNet이라는 이름으로 발표한 컨볼루션
- V3는 세번째로 개선된 버전임
- 텐서플로 허브에는 소프트맥스 Dense 레이어를 포함한 전체 네트워크와 소프트맥스 Dense 레이어가 없는 특징 추출기 네트워크가 있는데, 여기서는 특징 추출기 네트워크를 `KerasLayer`로 불러오겠음 
- `KerasLayer` 로 네트워크를 불러오면 `tf.keras`로 쉽게 편집할 수 없지만 여기서는 Inception 네트워크를 특징 추출기로만 사용하기 때문에 각 레이어를 편집할 필요가 없어 KerasLayer로 불러와도 상관없음
~~~python
# 8.23 텐서플로우 허브에서 사전 훈련된 Inception V3의 특징 추출기 불러오기
import tensorflow_hub as hub

inception_url = 'https://tfhub.dev/google/tf2-preview/inception_v3/feature_vector/4'
feature_model = tf.keras.Sequential([
    hub.KerasLayer(inception_url, output_shape=(2048,), trainable=False)
])
feature_model.build([None, 299, 299, 3])
feature_model.summary()
~~~
- 위의 설정에 의해서 Inception V3 특징 추출기는 이미지에서 2048 크기의 특징 벡터를 추출
- `summary()` 함수로 모델을 확인하기 위해서는 보통 `model.compile()`을 사용할 수 있지만 `build()`를 사용할 수도 있음
- 네트워크의 input_shape이 지정되지 않았기 때문에 `build()` 함수의 인수로 [None, 299, 299, 3]이라는 입력 데이터의 차원을 정의해서 넣음
- 첫 번째 차원은 무슨 숫자가 들어와도 배치 차원이기 때문에 상관없음
- 두 번째와 세 번째는 이미지의 크기를 의미함. 네 번째는 RGB의 3
- Inception V3의 파라미터 총 수는 MobileNet에 비해 훨씬 많기 때문에 이번에는 `ImageDataGenerator` 를 이용해 디스크에서 배치 크기만큼 읽어 들이는 방법을 사용
- <b>`ImageDataGenerator`는 라벨이 있는 데이터를 처리할 때 각 라벨의 이름을 하위 디렉터리로 가지고 있는 디렉터리를 받아 데이터를 처리</b>
- 따라서 kaggle에서 내려받은 데이터들을 해당 디렉터리별로 저장해야함
~~~python
a = np.array([99, 32, 5, 64])
arg = np.argsort(a)
print(arg)
print(np.sort(a))
print(a[arg])
~~~
- `plt.barh`  : 수평 막대 그래프로 표현, 값이 역방향 순으로 나옴을 주의하자
- `df.info()` : dataFrame의 간단 요약 정보 확인 가능
- `.nunique()` : pandas의 겹치지 않는 데이터의 count 수를 구할 수 있음   
- `.index('value')` : 해당 list 내에 들어있는 value의 index를 return
- `shutil.copy(file1.txt, file2.txt)` file1.txt -> file2.txt로 복사
~~~python
import os
import shutil

os.mkdir('/content/train_sub')

for i in range(len(label_text)):
    if os.path.exists('/content/train_sub/' + label_text.loc[i]['breed']) == False:
        os.mkdir('/content/train_sub/' + label_text.loc[i]['breed'])
    shutil.copy('/content/train/' + label_text.loc[i]['id'] + '.jpg', '/content/train_sub/' + label_text.loc[i]['breed'])
~~~
- 이제 ImageDataGenerator를 통해 train_sub 디렉터리의 이미지들을 이용해 훈련 데이터와 검증 데이터를 분리하고, 훈련 데이터는 이미지 보강(Image Augmentation)을 적용해 네트워크의 성능을 높여보자
~~~python
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from keras.applications.inception_resnet_v2 import preprocess_input

image_size = 299
batch_size = 32

train_datagen = ImageDataGenerator(rescale = 1./255., horizontal_flip = True, shear_range = 0.2,
                                   zoom_range = 0.2, width_shift_range = 0.2, height_shift_range = 0.2, validation_split=0.25)
valid_datagen = ImageDataGenerator(rescale=1./255., validation_split = 0.25)

train_generator = train_datagen.flow_from_directory(directory ='/content/train_sub/', subset="training", batch_size = batch_size, seed = 42, shuffle = True, class_mode = "categorical", target_size=(image_size, image_size))
valid_generator = valid_datagen.flow_from_directory(directory ='/content/train_sub/', subset="validation", batch_size = 1, seed = 42, shuffle=True, class_mode = 'categorical', target_size=(image_size,image_size))
~~~
- 동일한 ImageDataGenerator를 생성한 다음, 훈련/검증 데이터를 각각 사용  
  train_generator에는 training만, valid_generator는 validation_set만 사용
- 이렇게 똑같은 DataGenerator를 만드는 이유는 검증 데이터는 Data augmentation 없이 만들기 위함
- 이제 위에서 불러왔던 Inception V3를 이용해 특징 추출을 해야함
~~~python
batch_step = (7718 * 3) # batch_size
train_features = []
train_Y = []
for idx in range(batch_step):
  if idx % 100 == 0:
    print(idx)
  x, y = train_generator.next()
  train_Y.extend(y)

  feature = feature_model.predict(x)
  train_features.extend(feature)

train_features = np.array(train_features)
train_Y = np.array(train_Y)

print(train_features.shape)
print(train_Y.shape)
~~~
- 첫 줄에서는 `batch_step` 값을 지정. training 부분집합의 크기인 7718에 3을 곱해 충분히 보강이 될 수 있도록 함
- `batch_size(32)`로 나눠서 training 부분집합을 3번 정도 반복하여 특징 벡터를 뽑아냄
- `ImageDataGenerator`에 `next()`를 사용하면 다음에 올 값을 반환받을 수 있음
- 훈련 데이터에는 이미지의 분류에 해당하는 y 값이 있기 때문에 식의 좌변에서 x,y를 함께 받게 됨
- y값은 바로 train_Y에 저장해서 뒤에서 쓸 수 있게 함
- 검증 데이터를 변환하는 것은 다음과 같음
~~~python
valid_features = []
valid_Y = []
for idx in range(valid_generator.n):
  if idx % 100 == 0:
    print(idx)
  x, y = valid_generator.next()
  valid_Y.extend(y)

  feature = feature_model.predict(x)
  valid_features.extend(feature)

valid_features = np.array(valid_features)
valid_Y = np.array(valid_Y)
print(valid_features.shape)
print(valid_Y.shape)
~~~
- 이제 특징 벡터가 준비되었으니 분류를 위한 네트워크를 만들어보자
- 작은 시퀀셜 모델이면 충분함
~~~python
model = tf.keras.Sequential([
    tf.keras.layers.Dense(256, activation = 'relu', input_shape = (2048, )),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(120, activation = 'softmax')
])

model.compile(tf.optimizers.RMSProp(0.0001), loss='categorical_crossentropy', metrics = ['accuracy'])
model.summary()
~~~
- 특징 추출을 통해 데이터 차원을 축소시키고, 이를 네트워크 학습에 사용했으므로 학습 속도가 1/13으로 줄어듬
- 모델을 학습시키고 결과를 시각화 해보자
~~~python
# 8.29 분류를 위한 작은 Sequential 모델 학습
history = model.fit(train_features, train_Y, validation_data=(valid_features, valid_Y), epochs=10, batch_size=32)

import matplotlib.pyplot as plt
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], 'b-', label='loss')
plt.plot(history.history['val_loss'], 'r--', label='val_loss')
plt.xlabel('Epoch')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], 'g-', label='accuracy')
plt.plot(history.history['val_accuracy'], 'k--', label='val_accuracy')
plt.xlabel('Epoch')
plt.ylim(0.8, 1)
plt.legend()

plt.show()
~~~
- `ImageDataGenerator`는 라벨을 인덱스로 저장할 때 알파벳 순으로 정렬된 순서로 저장하기 때문에 여기서도 그에 맞게 unique_y를 정렬하겠음
~~~python
# 8.30 라벨 텍스트를 알파벳 순으로 정렬
unique_sorted_Y = sorted(unique_Y)
print(unique_sorted_Y)

# 8.31 Inception V3 특징 추출기-Sequential 모델의 분류 라벨 확인
import random
plt.figure(figsize=(16,16))
  
for c in range(3):
    image_path = random.choice(valid_generator.filepaths)
    
    # 이미지 표시
    plt.subplot(3,2,c*2+1)
    plt.imshow(plt.imread(image_path))
    real_y = image_path.split('/')[3]
    plt.title(real_y)
    plt.axis('off')
    idx = unique_sorted_Y.index(real_y)
    
    # 예측값 표시
    plt.subplot(3,2,c*2+2)
    img = cv2.imread(image_path)
    img = cv2.resize(img, dsize=(299, 299))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    
    # Inception V3를 이용한 특징 벡터 추출
    feature_vector = feature_model.predict(img)
    
    # Sequential 모델을 이용한 예측
    prediction = model.predict(feature_vector)[0]
    
    # 가장 높은 확률의 예측값 5개를 뽑음
    top_5_predict = prediction.argsort()[::-1][:5]
    labels = [unique_sorted_Y[index] for index in top_5_predict]
    color = ['gray'] * 5
    if idx in top_5_predict:
        color[top_5_predict.tolist().index(idx)] = 'green'
    color = color[::-1]
    plt.barh(range(5), prediction[top_5_predict][::-1] * 100, color=color)
    plt.yticks(range(5), labels[::-1])
~~~

### test Data 예측 후 submission.csv file 예측값 추가 예제
~~~python
# 8.33 submission.csv 파일 내용 확인
import pandas as pd
submission = pd.read_csv('sample_submission.csv')
print(submission.head())
print()
print(submission.info())

# 8.34 ImageDataGenerator가 처리할 수 있는 하위 디렉토리 구조로 데이터 복사
import os
import shutil

os.mkdir('/content/test_sub/')
os.mkdir('/content/test_sub/unknown/')

for i in range(len(submission)):
    shutil.copy('/content/test/' + submission.loc[i]['id'] + '.jpg', '/content/test_sub/unknown/')

# 8.35 ImageDataGenerator를 이용한 test 데이터 불러오기
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator

test_datagen=ImageDataGenerator(rescale=1./255.)
test_generator=test_datagen.flow_from_directory(directory="/content/test_sub/",batch_size=1,seed=42,shuffle=False,target_size=(299, 299))

# 8.36 test 데이터를 특징 벡터로 변환
test_features = []

for idx in range(test_generator.n):
    if idx % 100 == 0:
        print(idx)
        
    x, _ = test_generator.next()
    feature = feature_model.predict(x)
    test_features.extend(feature)

test_features = np.array(test_features)
print(test_features.shape)

# 8.37 특징 벡터로 test 데이터의 정답 예측
test_Y = model.predict(test_features, verbose=1)

# 8.38 Inception V3 특징 추출기-Sequential 모델의 test 데이터 분류 라벨 확인
import random
plt.figure(figsize=(16,16))
  
for c in range(3):
    image_path = random.choice(test_generator.filepaths)
    
    # 이미지 표시
    plt.subplot(3,2,c*2+1)
    plt.imshow(plt.imread(image_path))
    real_y = image_path.split('/')[3]
    plt.title(real_y)
    plt.axis('off')
    
    # 예측값 표시
    plt.subplot(3,2,c*2+2)
    img = cv2.imread(image_path)
    img = cv2.resize(img, dsize=(299, 299))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    
    # Inception V3를 이용한 특징 벡터 추출
    feature_vector = feature_model.predict(img)
    
    # Sequential 모델을 이용한 예측
    prediction = model.predict(feature_vector)[0]
    
    # 가장 높은 확률의 예측값 5개를 뽑음
    top_5_predict = prediction.argsort()[::-1][:5]
    labels = [unique_sorted_Y[index] for index in top_5_predict]
    color = ['gray'] * 5
    plt.barh(range(5), prediction[top_5_predict][::-1] * 100, color=color)
    plt.yticks(range(5), labels[::-1])

# 8.39 submission 데이터프레임에 예측값 저장
for i in range(len(test_Y)):
    for j in range(len(test_Y[i])):
        breed_column = unique_sorted_Y[j]
        submission.loc[i, breed_column] = test_Y[i, j]

# 8.40 submission 데이터 확인
print(submission.iloc[:5, :5])

# 8.41 submission 데이터프레임을 csv 파일로 저장
submission.to_csv('dogbreed_submission_inceptionV3_epoch10_299.csv', index=False)
~~~

## 8.3