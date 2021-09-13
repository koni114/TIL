#- chapter13 CNN

"""
아래 코드는 확실히 이해하기!
- 각 컬러 채널의 픽셀 강도는 0 ~ 255 사이의 값을 가진 바이트 하나로 표현되며, 이 특성을 255로 나누어
  0에서 1 사이의 실수로 바꿈
- 그다음 두 개의 7 x 7 필터를 만듬
  - 하나는 가운데 흰 수직선
  - 하나는 가운데 흰 수평선
- 텐서플로 저수준 딥러닝 API 중 하나인 tf.nn.conv2d() 함수를 사용해 필터를 두 이미지에 적용
- 마지막으로 만들어진 특성 맵 중 하나를 그래프로 그리기. 오른쪽 위에 있는 이미지와 비슷함
"""
#- 2개의 sample 이미지 로드
from sklearn.datasets import load_sample_image
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

china = load_sample_image('china.jpg') / 255
flower = load_sample_image('flower.jpg') / 255

images = np.array([china, flower])
batch_size, height, width, channels = images.shape

#- 필터를 두 개 만듬
filters = np.zeros(shape=(7, 7, channels, 2), dtype=np.float32)
filters[:, 3, :, 0] = 1 # 수직선
filters[3, :, :, 1] = 1 # 수평선

outputs = tf.nn.conv2d(images, filters, strides=1, padding="SAME")

print(f"images.shape : {images.shape}")
print(f"filter.shape : {filters.shape}")

plt.imshow(outputs[0, :, :, 1], cmap="gray")
plt.show()

"""
필터를 직접 지정했지만, 실제 CNN 에서는 보통 훈련 가능한 변수로 필터를 정의함
tf.keras.layers.Conv2D 층 사용
"""
conv = tf.keras.layers.Conv2D(filters=32, kernel_size=3,
                              strides=1, padding="same", activation='relu')

"""
예를 들어 
"""
