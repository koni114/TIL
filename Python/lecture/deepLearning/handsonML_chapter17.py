"""
under-complete auto-encoder 를 통해 PCA 수행
- 다음 코드는 3D dataset -> PCA -> 2D 투영하는 간단한 선형 오토인코더를 만드는 코드
"""
import tensorflow as tf
encoder = tf.keras.models.Sequential([tf.keras.layers.Dense(2, input_shape=[3])])
decoder = tf.keras.models.Sequential([tf.keras.layers.Dense(3, input_shape=[2])])
autoencoder = tf.keras.models.Sequential([encoder, decoder])
autoencoder.compile(loss='mse', optimizer=tf.keras.optimizers.SGD(learning_rate=0.1))

# 가상으로 생성한 간단한 3D 데이터셋에 훈련
# 그 다음 이 모델을 사용해 동일한 데이터셋을 인코딩(2D로 투영)
# 동일한 데이터셋이 입력과 타깃에도 사용된다는 것을 주목
history = autoencoder.fit(X_train, X_train, epochs=20)
codings = encoder.predict(X_train)

"""
keras 를 사용하여 적층 오토인코더 구현하기
- 패션 MNIST 데이터셋에서 SELU 활성화 함수를 사용해 적층 오토인코더를 만듬
"""

#- fashion MNIST
fashion_mnist = tf.keras.datasets.fashion_mnist
(X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()

#- 간편하게 픽셀 강도를 255.0로 나누어 0 ~ 1 사이로 범위 조정
X_valid, X_train = X_train_full[:5000] / 255.0, X_train_full[5000:] / 255.0
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
X_test = X_test / 255.0


stacked_encoder = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=[28, 28]),
    tf.keras.layers.Dense(100, activation='selu'),
    tf.keras.layers.Dense(30, activation='selu')
])

stacked_decoder = tf.keras.models.Sequential([
    tf.keras.layers.Dense(100, activation='selu', input_shape=[30]),
    tf.keras.layers.Dense(28 * 28, activation='sigmoid'),
    tf.keras.layers.Reshape([28, 28])
])

stacked_ae = tf.keras.models.Sequential([stacked_encoder, stacked_decoder])
stacked_ae.compile(loss='binary_crossentropy',
                   optimizer=tf.keras.optimizers.SGD(learning_rate=1.5))

history = stacked_ae.fit(X_train, X_train, epochs=10, validation_data=(X_valid, X_valid))

"""
- 패션 MNIST에서 변이형 오토인코더 만들어보기
"""
# 먼저 Mu, gamma(log(sigma^2))가 주어졌을 때, 코딩을 샘플링하는 사용자 정의 층 선언
# 평균이 Mu 이고 표준편차가 sigma 인 정규분포에서 코딩 벡터를 샘플링
import keras.backend as K
class Sampling(tf.keras.layers.Layer):
    def call(self, inputs):
        mean, log_var = inputs
        return K.random_normal(tf.shape(log_var)) * K.exp(log_var / 2) + mean

codings_size = 10

#- encoder 생성
inputs = tf.keras.layers.Input(shape=[28, 28])
z = tf.keras.layers.Flatten()(inputs)
z = tf.keras.layers.Dense(150, activation='selu')(z)
z = tf.keras.layers.Dense(100, activation='selu')(z)
codings_mean = tf.keras.layers.Dense(codings_size)(z)
codings_log_var = tf.keras.layers.Dense(codings_size)(z)
codings = Sampling()([codings_mean, codings_log_var])
# 조사 목적으로 codings_mean, codings_log_var 사용하며, 실제 사용하는 값은 codings
variational_encoder = tf.keras.Model(inputs=[inputs],
                                     outputs=[codings_mean, codings_log_var, codings])

#- decoder 생성
decoder_inputs = tf.keras.layers.Input(shape=[codings_size])
x = tf.keras.layers.Dense(100, activation='selu')(decoder_inputs)
x = tf.keras.layers.Dense(150, activation='selu')(x)
x = tf.keras.layers.Dense(28 * 28, activation='sigmoid')(x)
outputs = tf.keras.layers.Reshape([28, 28])(x)
variational_decoder = tf.keras.Model(inputs=[decoder_inputs], outputs=[outputs])

# 변이형 오토인코더 모델 생성
_, _, codings = variational_encoder(inputs)
reconstructions = variational_decoder(codings)
variational_ae = tf.keras.Model(inputs=[inputs], outputs=[reconstructions])

latent_loss = -0.5 * K.sum(
    1 + codings_log_var - K.exp(codings_log_var) - K.square(codings_mean),
    axis=-1)

variational_ae.add_loss(K.mean(latent_loss) / 784.)
variational_ae.compile(loss="binary_crossentropy", optimizer='rmsprop')

history = variational_ae.fit(X_train, X_train, epochs=50,
                             batch_size=128, validation_data=(X_valid, X_valid))


"""
패션 MNIST 데이터셋으로 간단한 GAN 만들어보기
"""

# 생성자와 판별자를 만들어야 함
# 생성자는 오토인코더의 디코더와 비슷함. 판별자는 일반적인 이진 분류기
# 각 훈련 반복의 두 번째 단계에서 생성자와 판별자가 연결된 전체 GAN 모델이 필요

codings_size = 30

generator = tf.keras.models.Sequential([
    tf.keras.layers.Dense(100, activation='selu', input_shape=[codings_size]),
    tf.keras.layers.Dense(150, activation='selu'),
    tf.keras.layers.Dense(28 * 28, activation='sigmoid'),
    tf.keras.layers.Reshape([28, 28])
])

discriminator = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=[28, 28]),
    tf.keras.layers.Dense(150, activation='selu'),
    tf.keras.layers.Dense(100, activation='selu'),
    tf.keras.layers.Dense(1, activation='sigmoid'),
])

gan = tf.keras.models.Sequential([generator, discriminator])

# 이 모델들을 컴파일 해야 함
# 판별자는 이진 분류기이므로, 이진 크로스 엔트로피 손실을 사용
# 생성자는 gan 모델을 통해서만 훈련되기 때문에 따로 컴파일을 할 필요가 없음

# gan 모델도 이진 분류기이므로 이진 크로스 엔트로피 손실을 사용
# 중요한 것은 두 번째 단계에서 판별자를 훈련하면 안됨! 따라서 gan 모델을 컴파일하기 전에 판별자가 훈련되지 않도록 해야함

discriminator.compile(loss='binary_crossentropy', optimizer='rmsprop')
discriminator.trainable = False
gan.compile(loss='binary_crossentropy', optimizer='rmsprop')

# 훈련이 일반적인 반복이 아니니, 사용자 정의 훈련 반복문을 만들어야 함
# 이를 위해 먼저 이미지를 순회하는 Dataset 을 만들어야 함
batch_size = 32
dataset = tf.data.Dataset.from_tensor_slices(X_train).shuffle(1000)
dataset = dataset.batch(batch_size, drop_remainder=True).prefetch(1)


def train_gan(gan, dataset, batch_size, codings_size, n_epochs=50):
    generator, discriminator = gan.layers
    for epoch in range(n_epochs):
        for X_batch in dataset:
            # 단계 1 - 판별자 훈련
            noise = tf.random.normal(shape=[batch_size, codings_size])
            generated_images = generator(noise)
            X_fake_and_real = tf.concat([generated_images, X_batch], axis=0)
            y1 = tf.constant([[0.]] * batch_size + [[1.]] * batch_size)
            discriminator.trainable = True
            discriminator.train_on_batch(X_fake_and_real, y1)

            # 단계 2 - 생성자 훈련
            noise = tf.random.normal(shape=[batch_size, codings_size])
            y2 = tf.constant([[1.]] * batch_size)
            discriminator.trainable = False
            gan.train_on_batch(noise, y2)

train_gan(gan, dataset, batch_size, codings_size)
