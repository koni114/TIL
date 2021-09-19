import tensorflow as tf


tf.keras.layers.SimpleRNN(1, input_shape=[None, 1])

"""
순환 신경망은 어떤 길이의 타임 스텝도 처리할 수 있음.
"""