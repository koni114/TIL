"""
케라스를 사용해 ResNet-34 CNN 구현하기
- 일반적으로 사전 훈련된 모델을 사용하지만 직접 한 번 구현해 보기
"""
import tensorflow as tf


#- 1. ResidualUnit 층을 만듬
class ResidualUnit(tf.keras.layers.Layer):
    def __init__(self, filters, strides=1, activation='relu', **kwargs):
        super().__init__(**kwargs)
        self.activation = tf.keras.activations.get(activation)
        self.main_layers = [
            tf.keras.layers.Conv2D(filters, 3, strides=strides,
                                   padding='same', use_bias=False),
            tf.keras.layers.BatchNormalization(),
            self.activation,
            tf.keras.Conv2D(filters, 3, strides=1,
                            padding='same', use_bias=False),
            tf.keras.layers.BatchNormalization()]
        self.skip_layers = []
        if strides > 1:
            self.skip_layers = [
                tf.keras.layers.Conv2D(filters, 1, strides=strides,
                                       padding='same', use_bias=False),
                tf.keras.layers.BatchNormalization()]

    def call(self, inputs):
        Z = inputs
        for layer in self.main_layers:
            Z = layer(Z)
        skip_Z = inputs
        for layer in self.skip_layers:
            skip_Z = layer(skip_Z)

        return self.activation(Z + skip_Z)

#- Sequential 클래스를 통해 ResNet-34 모델 구현
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(64, 7, strides=2, input_shape=[244, 244, 3],
                                 padding='same', use_bias=False))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.Activation('relu'))
model.add(tf.keras.layers.MaxPool2D(pool_size=3, strides=2, padding='same'))
prev_filters = 64
for filters in [64] * 3 + [128] * 4 + [256] * 6 + [512] * 3:
    strides = 1 if filters == prev_filters else 2
    model.add(ResidualUnit(filters, strides=strides))
    prev_filters = filters
model.add(tf.keras.layers.GlobalAvgPool2D())
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(10, activation='softmax'))

model = tf.keras.applications.resnet50.ResNet50(weights='imagenet')