"""
Char-RNN 모델 만들어보기
"""
import tensorflow as tf
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 1. 데이터셋 만들기
# 케라스의 get_file() 함수를 사용하여 셰익스피어 작품을 모두 다운로드 하자
shakespeare_url = 'https://homl.info/shakespeare'
filepath = tf.keras.utils.get_file('shakespeare.txt', shakespeare_url)
with open(filepath) as f:
    shakespeare_text = f.read()

#- 모든 글자를 정수로 인코딩
#  케라스의 Tokenizer 클래스를 사용함
#  클래스의 객체를 텍스트에 훈련해야 함. 텍스트에서 사용되는 모든 글자를 찾아 각기 다른 글자 ID에 매핑
#  ID는 1부터 시작해 고유한 글자 개수까지 만들어짐

"""
char_level = True : 단어 수준 인코딩 대신 글자 수준 인코딩을 만듬
이를 통해 텍스트에 있는 고유 글자 개수와 전체 글자 개수를 알 수 있음
tokenizer.texts_to_sequences(['text']) --> 
"""
#-
#- 기본적으로 텍스트를 소문자로 바꿈
import numpy as np
tokenizer = tf.keras.preprocessing.text.Tokenizer(char_level=True)
tokenizer.fit_on_texts(shakespeare_text)

#- 문자 수준 인코딩
tokenizer.texts_to_sequences(['First'])
tokenizer.sequences_to_texts([[20, 6, 9, 8, 3]])

# 고유 문자 개수
max_id = len(tokenizer.word_index)
print(f"max_id : {max_id}")

# 전체 문자 개수
dataset_size = tokenizer.document_count
print(f"dataset_size : {dataset_size}")

# 전체 텍스트를 인코딩하여 글자를 ID로 나타냄
[encoded] = np.array(tokenizer.texts_to_sequences([shakespeare_text])) - 1

"""
데이터 쪼개기
- 처음 90%를 훈련 세트로 사용해보자, 나머지는 검증 세트
"""
# 한번에 한 글자씩 반환하는 tf.data.Dataset 객체 만들기
train_size = dataset_size * 90 // 100
dataset = tf.data.Dataset.from_tensor_slices(encoded[:train_size])

#- 데이터셋의 window() 메서드를 이용해 긴 시퀀스를 작은 많은 텍스트 원도로 변환
#- 데이터셋의 샘플은 짧은 부분 문자열
#- RNN 은 부분 문자열 길이 만큼만 역전파를 위해 펼쳐짐

#- 윈도우 생성해보기
#- n_step 을 튜닝할 수 있으며, 해당 길이 이상만큼의 패턴은 RNN 은 학습할 수 없으므로 너무 짧게 만들면 안됨
#- drop_remainder=True : 모든 윈도우가 동일하게 101 개의 문자를 포함하도록 함

n_steps = 100
window_length = n_steps + 1 # target = 1글자 앞의 input
dataset = dataset.window(window_length, shift=1, drop_remainder=True)

#- dataset.window 함수를 사용하면 각각 101개의 ID로 편성된 데이터셋 생성
#  리스트의 리스트와 비슷한 중첩 데이터셋이며, 이런 구조는 데이터셋 메서드를 호출하여 원도를 변환할 때 유용
#  (예를 들어 섞거나 배치를 만듬)
#  하지만 모델은 데이터셋이 아니라 텐서를 기대하기 때문에 데이터셋 바로 사용 불가능
#  따라서 중첩 데이터셋을 flat dataset으로 변환하는 `flat_map()` 호출

#  flat_map에 lambda ds: ds.batch() 함수를 전달하면 중첩 데이터셋을 플랫 데이터셋으로 변환함
#  ex) {{1, 2}, {3, 4, 5, 6}} -> {[1, 2], [3, 4], [5, 6]}
dataset = dataset.flat_map(lambda window: window.batch(window_length))

# 윈도를 배치로 만들고 입력과 타깃을 분리
# 입력은 처음 100의 글자, 타깃은 마지막 100개의 글자
batch_size = 32
dataset = dataset.shuffle(10000).batch(batch_size)
dataset = dataset.map(lambda windows: (windows[:, :-1], windows[:, 1:]))

# 고유한 글자 수가 적기 때문에 원-핫 벡터를 사용해 글자를 인코딩
dataset = dataset.map(
    lambda X_batch, Y_batch: (tf.one_hot(X_batch, depth=max_id), Y_batch)
)

dataset = dataset.prefetch(1)

"""
이전 글자 100개를 기반으로 다음 글자를 예측하기 위해 
유닛 128개, GRU 층 2개, dropout, recurrent_dropout 에 20% 적용
출력층은 TimeDistributed 적용한 Dense 층
- 텍스트에 있는 고유한 글자 수는 39개이므로 해당 층은 39개의 유닛을 가져야 함
  각 글자에 대한 확률을 출력
- 타임 스텝에서 출력 확률의 합은 1이어야 하므로 Dense 층의 출력에 소프트맥스 함수를 적용
- `sparse_categorical_crossentropy` 손실과 Adam 옵티아미저 사용해 compile 호출
"""
model = tf.keras.models.Sequential([
    tf.keras.layers.GRU(128, return_sequences=True, input_shape=[None, max_id],
                        dropout=0.2, recurrent_dropout=0.2),
    tf.keras.layers.GRU(128, return_sequences=True,
                        dropout=0.2, recurrent_dropout=0.2),
    tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(max_id, activation='softmax'))
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')
history = model.fit(dataset, epochs=20)

"""
Char-RNN model 사용하기
- 셰익스피어가 쓴 텍스트에서 다음 글자를 예측하는 모델이 있음
- 모델 예측하기 위해 앞에 전처리를 수행해 주어야 함
"""
def preprocess(texts):
    X = np.array(tokenizer.texts_to_sequences(texts)) - 1
    return tf.one_hot(X, max_id)

X_new = preprocess(["How are yo"])
Y_pred = model.predict_classes(X_new)
tokenizer.sequences_to_texts(Y_pred + 1)[0][-1]

"""
가짜 셰익스피어 텍스트를 생성해보기
- Char-RNN 모델을 사용해 새로운 텍스트를 생성하려면 초기 텍스트를 주입하고 모델이 가장 가능성 있는 다음 글자 예측
- 이 글자를 텍스트 끝에 추가하고 늘어난 텍스트를 모델에 전달하여 다음 글자를 예측
- 실제로 이렇게 하면 같은 단어가 계속 반복되는 경우가 많음
- 대신 텐서플로의 tf.random.categorical() 함수를 사용해 모델이 추정한 확률을 기반으로 다음 글자를 무작위로 선택
- categorical() 함수는 클래스의 로그 확률을 전달하면 랜덤하게 클래스 인덱스를 샘플링
- 생성된 텍스트의 다양성을 더 많이 제어하려면 temperature 라고 불리는 숫자로 로짓을 나눔
- temperature 는 원하는 값으로 설정할 수 있는데, 0에 가까울수록 높은 확률을 가진 글자를 선택
- temperature 가 매우 높으면 모든 글자가 동일한 확률을 가짐
- 다음 next_char() 함수는 이 방식을 사용해 다음 글자를 선택하고 입력 텍스트에 추가
"""

def next_char(text, temperature=1):
    X_new = preprocess([text])
    y_proba = model.predict(X_new)[0, -1:, :]
    rescaled_logits = tf.math.log(y_proba) / temperature
    char_id = tf.random.categorical(rescaled_logits, num_samples=1) + 1
    return tokenizer.sequences_to_texts(char_id.numpy())[0]

"""
stateful RNN 
- Dataset 을 만들 때 window() 메서드에서 shift=n_steps 지정
- shuffle method 호출 X
- batch(32)라고 호출하면 32개의 연속적인 윈도가 같은 배치에 들어가므로 윈도우가 끝난 지점부터 다음 배치가 계속되지 않음
- 첫 번째 배치는 윈도 1에서 32까지 포함하고, 두 번째 배치는 윈도 33부터 64까지 포함함
- 따라서 각 배치의 첫 번째 윈도를 생각하면 연속적이지 않음
- 각 배치의 첫번째 윈도우를 생각하면 (윈도 1과 33)은 연속적이지 않음을 알 수 있음
- 이 문제에 대한 가장 간단한 해결책은 하나의 윈도를 갖는 배치를 만드는 것

# 상태가 있는 RNN 만들기
- stateful = True 로 지정
- batch_input_shape 매개변수를 지정 해야 함
- epoch 끝마다 텍스트를 다시 시작하기 전에 상태를 재설정해야하므로, callback 함수를 사용하여 처리
"""
dataset = tf.data.Dataset.from_tensor_slices(encoded[:train_size])
dataset = dataset.window(window_length, shift=n_steps)

"""
IMDb 리뷰 데이터 셋 가져오기
리뷰 : 50,000개
25,000, 25,000개
- X_train 은 리뷰들의 리스트임. 이미 전처리되어 있음
- 각 리뷰는 넘파이 정수 배열로 표현됨. 각 정수는 하나의 배열
- 빈도에 따라 정렬하여 indexing
"""
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.imdb.load_data()
word_index = tf.keras.datasets.imdb.get_word_index()
id_to_word = {id_ + 3: word for word, id_ in word_index.items()}
for id_, token in enumerate(("<pad>", "<sos>", "<unk>")):
    id_to_word[id_] = token

" ".join([id_to_word[id_] for id_ in X_train[0][:10]])


"""
전처리를 모델 자체에 포함시키는 방법
"""
# 1. 텐서플로 데이터셋을 이용해 원본 IMDb 리뷰를 텍스트로 적재
import tensorflow_datasets as tfds
datasets, info = tfds.load("imdb_reviews", as_supervised=True, with_info=True)
train_size = info.splits['train'].num_examples

# 2. 전처리 함수 만들기
# 2.1 각 리뷰에서 처음 300 글자만 남김. why? 처음 한두 문장에서 리뷰가 긍정적인지 아닌지 판단 가능하기 때문
# 2.2 정규식을 사용해 <br/> 태그 -> 공백, 문자와 작은 따옴표가 아닌 다른 모든 문자를 공백으로 변경
# 2.3 리뷰를 공백으로 나눔. 이때 ragged tensor 가 반환
# ragged tensor --> Tensor 의 list
# 2.4 ragged tensor 를 dense tensor 로 변경 후 동일한 길이가 되도록 패딩 토큰 "<pad>"로 모든 리뷰를 패딩

def preprocess(X_batch, y_batch):
    X_batch = tf.strings.substr(X_batch, 0, 300)
    X_batch = tf.strings.regex_replace(X_batch, b"<br\\s*/?>", b" ")
    X_batch = tf.strings.regex_replace(X_batch, b"[^a-zA-Z']", b" ")
    X_batch = tf.strings.split(X_batch)
    return X_batch.to_tensor(default_value=b"<pad>"), y_batch

#- 3. 어휘 사전 구축
# 전체 훈련 세트를 한 번 순회 --> preprocess() 함수 적용하고 Counter()로 개수 check

from collections import Counter
vocabulary = Counter()
for X_batch, y_batch in datasets['train'].batch(32).map(preprocess):
    for review in X_batch:
        vocabulary.update(list(review.numpy()))

# 가장 많이 등장하는 단어 세 개 확인
vocabulary.most_common()[:3]

# 4. 어휘 사전 중에서 가장 많이 등장하나는 단어 10,000개만 남기고 삭제
vocab_size = 10000
truncated_vocabulary = [
    word for word, count in vocabulary.most_common()[:vocab_size]]

# 5. 각 단어를 ID로 바꾸는 전처리 단계를 추가
# 1,000개의 oov 버킷을 사용하는 룩업 테이블을 만듬

words = tf.constant(truncated_vocabulary)
word_ids = tf.range(len(truncated_vocabulary), dtype=tf.int64)
vocab_init = tf.lookup.KeyValueTensorInitializer(words, word_ids)
num_oov_buckets = 1000
table = tf.lookup.StaticVocabularyTable(vocab_init, num_oov_buckets)

# this, movie, was 는 룩업 테이블에 있으므로 이 단어들의 ID는 10,000보다 작음
#- ffannntatis 는 없기 때문에 10,000 보다 크거나 같은 ID를 가진 oov 버킷 중 하나에 매핑

table.lookup(tf.constant([b"This movie was ffannntatis".split()]))

#- 6. 리뷰를 배치로 묶고, preprocess() 함수를 사용해 단어의 짧은 시퀀스로 바꿈
#- 앞서 만든 테이블을 사용하는 encode_words() 함수로 단어를 인코딩
#- 배치를 프리패치함

def encode_words(X_batch, y_batch):
    return table.lookup(X_batch), y_batch

train_set = datasets['train'].batch(32).map(preprocess)
train_set = train_set.map(encode_words).prefetch(1)

#. 7. 모델 훈련
# 첫 번째 층은 임베딩으로 변환하는 Embedding 층
# 임베딩 행렬은 단어 ID당 (vocab_size + num_oov_buckets) 하나의 행과 임베딩 차원당 하나의 열을 가짐
# 모델의 입력은 [배치 크기, 타임 스텝 수] 크기를 가진 2D 텐서
# Embedding 층의 출력은 [배치 크기, 타임 스텝 수, 임베딩 크기] 를 가진 3D 텐서

#- 나머지는 GRU 층 2개, 마지막 GRU 층은 타임 스텝의 출력만 반환
#- 출력층은 시그모이드 활성화 함수를 사용하는 하나의 뉴런

embed_size = 128
model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(vocab_size + num_oov_buckets, embed_size, input_shape=[None]),
    tf.keras.layers.GRU(128, return_sequences=True),
    tf.keras.layers.GRU(128),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(train_set, epochs=5)

"""
nnlm-en-dim50 문장 임베딩 모듈 버전 1을 감성 분석 모델에 사용해보기
"""

import tensorflow_hub as hub
model = tf.keras.Sequential([
    hub.KerasLayer('https://tfhub.dev/google/tf2-preview/nnlm-en-dim50/1',
                   dtype=tf.string, input_shape=[], output_shape=[50]),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

datasets, info = tfds.load("imdb_reviews", as_supervised=True, with_info=True)
train_size = info.splits['train'].num_examples
batch_size = 32

train_set = datasets['train'].batch(batch_size).prefetch(1)
history = model.fit(train_set, epochs=5)

"""
기본적인 인코더-디코더 모델 만들기
"""

import tensorflow_addons as tfa
import numpy as np


embed_size = 128
vocab_size = 10000

encoder_inputs = tf.keras.layers.Input(shape=[None], dtype=np.int32)
decoder_inputs = tf.keras.layers.Input(shape=[None], dtype=np.int32)
sequence_lengths = tf.keras.layers.Input(shape=[None], dtype=np.int32)

embeddings = tf.keras.layers.Embedding(vocab_size, embed_size)
encoder_embeddings = embeddings(encoder_inputs)
decoder_embeddings = embeddings(decoder_inputs)

encoder = tf.keras.layers.LSTM(512, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_embeddings)
encoder_state = [state_h, state_c]

sampler = tfa.seq2seq.sampler.TrainingSampler()

decoder_cell = tf.keras.layers.LSTMCell(512)
output_layer = tf.keras.layers.Dense(vocab_size)
decoder = tfa.seq2seq.basic_decoder.BasicDecoder(decoder_cell, sampler,
                                                 output_layer=output_layer)

final_outputs, final_state, final_sequence_lengths = decoder(
    decoder_embeddings, initial_state=encoder_state,
    sequence_length=sequence_lengths)

Y_proba = tf.nn.softmax(final_outputs.rnn_output)
model = tf.keras.Model(inputs=[encoder_inputs, decoder_inputs,
                               sequence_lengths], outputs=[Y_proba])
