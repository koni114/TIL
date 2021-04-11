# chapter05 분류
- 와인 데이터세트를 기반으로 레드 와인/화이트 와인 여부를 구분하는 분류 모델을 만들어보자
- 해당 데이터는 케라스와 텐서플로에 탑재되어 있지 않기 때문에 외부에서 데이터를 불러오고 정제하는 과정을 거쳐야 함
~~~python
import pandas as pd
red = pd.read_csv('http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv', sep= ';')
white = pd.read_csv('http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv', sep= ';')

print(red.head())
print(white.head())
~~~
- 데이터 정제 및 분석을 위한 라이브러리인 pandas를 import 함
- 두 데이터를 합치는 작업을 수행해보자. 이 때 red wine인지, white wine인지 구분해 주는 속성을 추가
~~~python
red['type'] = 0
white['type'] = 1

wine = pd.concat([red, white])
print(wine.describe())
~~~
- white wine과 red wine의 개수가 몇개인지 확인해보자
~~~python
plt.hist(wine['type'])
plt.xticks([0, 1])
plt.show()
print(wine['type'].value_counts())
~~~
- `value_counts()` 함수를 통해 type 컬럼의 카티널리티 별 개수를 알 수 있음
- 데이터의 파악을 도와주는 함수인 pandas의 info 함수를 이용해서 데이터 구성을 파악하자
~~~
print(wine.info())

<class 'pandas.core.frame.DataFrame'>
Int64Index: 6497 entries, 0 to 4897
Data columns (total 13 columns):
 #   Column                Non-Null Count  Dtype  
---  ------                --------------  -----  
 0   fixed acidity         6497 non-null   float64
 1   volatile acidity      6497 non-null   float64
 2   citric acid           6497 non-null   float64
 3   residual sugar        6497 non-null   float64
 4   chlorides             6497 non-null   float64
 5   free sulfur dioxide   6497 non-null   float64
 6   total sulfur dioxide  6497 non-null   float64
 7   density               6497 non-null   float64
 8   pH                    6497 non-null   float64
 9   sulphates             6497 non-null   float64
 10  alcohol               6497 non-null   float64
 11  quality               6497 non-null   int64  
 12  type                  6497 non-null   int64  
dtypes: float64(11), int64(2)
memory usage: 710.6 KB
None
~~~
- 데이터가 전부 non-null이며, 수치형으로 구성되어 있으므로, 전체 데이터에 대해서(train) 표준화 진행
~~~python
wine_norm = (wine - wine.min()) / (wine.max() - wine.min())
print(wine_norm.head())
print(wine_norm.describe())
~~~
- 이제 정규화된 데이터를 랜덤하게 섞은 후, 학습을 위해 넘파이로 변환
~~~python
wine_shuffle = wine_norm.sample(frac = 1)
print(wine_shuffle.head(5))
wine_np = wine_shuffle.to_numpy()
print(wine_np[:5])


      fixed acidity  volatile acidity  citric acid  ...   alcohol   quality  type
2455       0.330579          0.160000     0.198795  ...  0.231884  0.500000   1.0
4348       0.314050          0.153333     0.313253  ...  0.159420  0.500000   1.0
320        0.181818          0.013333     0.144578  ...  0.333333  0.666667   1.0
3307       0.462810          0.106667     0.174699  ...  0.434783  0.000000   1.0
1099       0.396694          0.293333     0.228916  ...  0.202899  0.333333   0.0

[5 rows x 13 columns]
[[0.33057851 0.16       0.19879518 0.15030675 0.03654485 0.15972222
  0.43317972 0.18912666 0.27131783 0.20224719 0.23188406 0.5
  1.        ]
 [0.31404959 0.15333333 0.31325301 0.19325153 0.05481728 0.20833333
  0.32718894 0.21746674 0.20155039 0.14044944 0.15942029 0.5
  1.        ]
 [0.18181818 0.01333333 0.14457831 0.00766871 0.05315615 0.04861111
  0.1359447  0.10776942 0.68992248 0.21910112 0.33333333 0.66666667
  1.        ]
 [0.46280992 0.10666667 0.1746988  0.12116564 0.04651163 0.42708333
  0.46543779 0.13186813 0.13953488 0.08988764 0.43478261 0.
  1.        ]
 [0.39669421 0.29333333 0.22891566 0.01380368 0.14451827 0.01388889
  0.02764977 0.18411413 0.37209302 0.16853933 0.20289855 0.33333333
  0.        ]]
~~~
- pandas의 sample 함수는 전체 데이터프레임에서 frac 인수로 지정된 비율만큼 랜덤하게 행을 뽑음
- 이제 데이터를 훈련 데이터와 테스트 데이터로 나눔
- 검증 데이터는 keras에서 자동으로 떼서 만들 것이기 때문에 여기서는 train/test로만 나눔
- 학습을 위해 각 데이터를 입력과 출력인 X, Y로도 분리해야 함
~~~python
train_idx = int(len(wine_np) * 0.8)
train_X, train_Y = wine_np[:train_idx, :-1], wine_np[:train_idx, -1]
test_X, test_Y = wine_np[train_idx:, :-1], wine_np[train_idx:, -1]

print(train_X[0])
print(train_Y[0])

print(test_X[0])
print(test_Y[0])

train_Y = tf.keras.utils.to_categorical(train_Y, num_classes = 2)
test_Y  = tf.keras.utils.to_categorical(test_Y, num_classes = 2)

print(train_Y[0])
print(test_Y[0])
~~~
- `tf.keras.utils`에서 불러오는 `to_categorical`은 정답 행렬을 one-hot encoding으로 변환
- `num_classes` 인수는 정답 클래스의 개수
- 모델 구조에 대한 특별한 이슈가 없기 때문에 앞서 사용했던 시퀀셜 모델 사용
~~~python
model = tf.keras.Sequential([
    tf.keras.layers.Dense(units = 48, activation='relu', input_shape = (12,)),
    tf.keras.layers.Dense(units = 24, activation='relu'),
    tf.keras.layers.Dense(units = 12, activation='relu'),
    tf.keras.layers.Dense(units = 2, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(lr = 0.07), loss = 'categorical_crossentropy', metrics=['accuracy'])
model.summary()
~~~
- 분류 모델이기 때문에 마지막 레이어의 활성화함수로 softmax를 사용
- 분류에서 가장 많이 쓰이는 이 함수는 출력값들을 자연로그의 밑인 e의 지수로 사용해 계산한 뒤 모두 더한 값으로 나눔
- 이렇게 나온 결괏값들은 총합이 1.0인 확률값이 됨
- 다음은 softmax 수식 계산식임

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=P(Z)&space;=&space;\frac{e^{zj}}{\sum_{K}^{k=1}e^{zk}}(for&space;i&space;=&space;1,2,...,K)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(Z)&space;=&space;\frac{e^{zj}}{\sum_{K}^{k=1}e^{zk}}(for&space;i&space;=&space;1,2,...,K)" title="P(Z) = \frac{e^{zj}}{\sum_{K}^{k=1}e^{zk}}(for i = 1,2,...,K)" /></a></p>

- 예를 들어, [2, 1, 0]이라는 값이 있을 경우 소프트맥스로 변환한다면

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=sum&space;=&space;\sum_{k=1}^{K}&space;e^{zk}&space;=&space;e^{2}&space;&plus;&space;e^{1}&space;&plus;&space;e^{0}&space;=&space;11.1073" target="_blank"><img src="https://latex.codecogs.com/gif.latex?sum&space;=&space;\sum_{k=1}^{K}&space;e^{zk}&space;=&space;e^{2}&space;&plus;&space;e^{1}&space;&plus;&space;e^{0}&space;=&space;11.1073" title="sum = \sum_{k=1}^{K} e^{zk} = e^{2} + e^{1} + e^{0} = 11.1073" /></a></p>
<p align = 'center'></p>

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=softmax&space;=&space;\frac{e^{zj}}{\sum_{k=1}^{K}&space;e^{k}}&space;=&space;[\frac{e^{2}}{sum},&space;\frac{e^{1}}{sum},&space;\frac{e^{0}}{sum}]&space;=&space;[0.67,&space;0.24,&space;0.09]" target="_blank"><img src="https://latex.codecogs.com/gif.latex?softmax&space;=&space;\frac{e^{zj}}{\sum_{k=1}^{K}&space;e^{k}}&space;=&space;[\frac{e^{2}}{sum},&space;\frac{e^{1}}{sum},&space;\frac{e^{0}}{sum}]&space;=&space;[0.67,&space;0.24,&space;0.09]" title="softmax = \frac{e^{zj}}{\sum_{k=1}^{K} e^{k}} = [\frac{e^{2}}{sum}, \frac{e^{1}}{sum}, \frac{e^{0}}{sum}] = [0.67, 0.24, 0.09]" /></a></p>

- 소프트맥스 함수는 max 함수와 비슷하게 큰 값을 강조하고 작은 값은 약화하는 효과를 갖음
- e를 밑으로 하는 지수 함수를 취하기 때문에 위의 효과가 발생하며, 0이나 음수에도 적용 가능함
- 지수함수는 큰 값은 강조하고, 작은 값은 약화하는 효과가 있음

### 엔트로피와 정보이론
- 정보이론에서의 엔트로피는 불확실한 정보를 숫자로 정량화하려는 노력이자 하나의 도구
- 엔트로피는 쉽게 말하면 확률의 역수에 로그를 취한 값
- 어떤 사건 X가 일어날 확률을 p(x), 엔트로피를 h(x)라고 할 때, 엔트로피는 아래의 식으로 정의할 수 있음

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=h(x)&space;=&space;log\frac{1}{p(x)}&space;=&space;-&space;log&space;p(x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?h(x)&space;=&space;log\frac{1}{p(x)}&space;=&space;-&space;log&space;p(x)" title="h(x) = log\frac{1}{p(x)} = - log p(x)" /></a></p>

- 확률에 역수를 취해주는 이유는 <b>확률이 높은 사건일수록 정보량(놀라움)이 적다고 판단하기 때문</b>
- 내일 비가 올 확률이 1%일 때, 비가 오지 않을 확률은 99%일 것임
- 이때 각 사건의 정보량은 다음과 같음
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=h(Rain)&space;=&space;-log0.01&space;=&space;4.605" target="_blank"><img src="https://latex.codecogs.com/gif.latex?h(Rain)&space;=&space;-log0.01&space;=&space;4.605" title="h(Rain) = -log0.01 = 4.605" /></a></p>

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=h(Not&space;Rain)&space;=&space;-log0.99&space;=&space;0.010" target="_blank"><img src="https://latex.codecogs.com/gif.latex?h(Not&space;Rain)&space;=&space;-log0.99&space;=&space;0.010" title="h(Not Rain) = -log0.99 = 0.010" /></a></p>

- 즉 비가 오는 경우가 비가 오지 않는 경우보다 약 460배 놀라운 사건이 됨
- 엔트로피의 기대값은 각 엔트로피에 확률을 곱해준 값임   
  통계에서 기대값의 정의는 각 사건이 벌어졌을 때의 이득과 그 사건이 벌어질 확률을 곱한 값이기 때문
- 수식으로 나타내면 다음과 같음
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=E(X)&space;=&space;-p(x)logp(x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(X)&space;=&space;-p(x)logp(x)" title="E(X) = -p(x)logp(x)" /></a></p>

- 위의 비 사건의 엔트로피를 계산하면 비오는 사건은 0.0461, 비가 안오는 사건의 엔트로피는 0.0099로 비가 오는 사건의 엔트로피가 높은 것을 확인할 수 있음
- 이렇게 엔트로피가 더 높은 사건을 정보 획득 측면에서 더 가치 있는 사건으로 분류할 수 있음
- 이 경우 엔트로피의 양만큼 비가 올 확률에 대한 예측값을 조정해서 결과적으로 다음에 얻을 엔트로피를 낮추려고 노력함
- 높은 엔트로피는 높은 불확실성을 의미하기 때문에 엔트로피를 줄이면 불확실성이 낮아지고 의미 있는 정보를 얻을 수 있음

### cross-entropy 손실
- 크로스 엔트로피는 엔트로피의 기댓값과 비슷하지만 약간 다른 점이 있음
- 로그 부분에 p(x)를 곱하는 것이 아니라 q(x)를 곱함
- 여기서 q(x)란 분류 네트워크가 예측한 라벨의 확률값
- 범주의 수를 n이라고 할 때 범주에 대한 크로스 엔트로피(Categorical Cross Entropy, CCE)의 식은 다음과 같음
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=CCE&space;=&space;-\frac{1}{n}\sum_{j&space;=&space;1}^{n}p(x)log&space;q(x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?CCE&space;=&space;-\frac{1}{n}\sum_{j&space;=&space;1}^{n}p(x)log&space;q(x)" title="CCE = -\frac{1}{n}\sum_{j = 1}^{n}p(x)log q(x)" /></a></p>
- 예를들어 실제 레드 와인일 때, 네트워크가 레드 와인일 확률을 0.87, 화이트와인일 확률을 0.13으로 예측 했을 때의 cross-entropy 값은 다음과 같음
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=CCE&space;=&space;-\frac{1}{2}(1.0&space;*log0.87&space;&plus;&space;0.0&space;*&space;log0.13)&space;=&space;0.0696" target="_blank"><img src="https://latex.codecogs.com/gif.latex?CCE&space;=&space;-\frac{1}{2}(1.0&space;*log0.87&space;&plus;&space;0.0&space;*&space;log0.13)&space;=&space;0.0696" title="CCE = -\frac{1}{2}(1.0 *log0.87 + 0.0 * log0.13) = 0.0696" /></a></p>

- 반대로 실제가 화이트와인일 때, 레드 와인일 확률이 0.6, 화이트 와인일 확률을 0.4로 예측하면, 

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=-\frac{1}{2}(0.0&space;*log0.6&space;&plus;&space;1.0&space;*&space;log0.4)&space;=&space;0.4581" target="_blank"><img src="https://latex.codecogs.com/gif.latex?-\frac{1}{2}(0.0&space;*log0.6&space;&plus;&space;1.0&space;*&space;log0.4)&space;=&space;0.4581" title="-\frac{1}{2}(0.0 *log0.6 + 1.0 * log0.4) = 0.4581" /></a></p>

- 즉 CCE도 낮을수록 더 좋은 값이고 네트워크는 손실을 낮추기 위하여 노력함
- 따라서 CCE가 낮을수록 예측을 잘하는 네트워크가 됨

## 5.2 다항 분류
- 와인의 색깔 대신 와인의 품질을 예측해보자
~~~python
print(wine['quality'].describe())
print(wine['quality'].value_counts())

count    6497.000000
mean        5.818378
std         0.873255
min         3.000000
25%         5.000000
50%         6.000000
75%         6.000000
max         9.000000
Name: quality, dtype: float64
6    2836
5    2138
7    1079
4     216
8     193
3      30
9       5
Name: quality, dtype: int64
~~~
~~~python
plt.hist(wine['quality'], bins = 7, rwidth = 0.8)
plt.show()
~~~
- 모든 범주에 대한 세세한 분류는 어려우므로, 범주를 크게 세 가지로 재분류하자
- 품질 3~5는 나쁨, 7~9는 좋음, 6은 보통
~~~python
wine.loc[wine['quality'] <= 5, 'new_quality'] = 0
wine.loc[wine['quality'] == 6, 'new_quality'] = 1
wine.loc[wine['quality'] >= 7, 'new_quality'] = 2
~~~
- 데이터프레임에 쓰이는 `loc`은 특정한 데이터의 인덱스를 골라내는 역할을 함  
  대괄호 안에 인수 하나만 넣으면 행, 두 개 넣으면 행과 열을 골라냄
~~~python
data = [['Apple', 11], ['Banana', 23], ['Coconut', 35]]
df = pd.DataFrame(data, columns=['Fruit', 'Count'])
print(df)
print()
print(df.loc[0])
print()
print(df.loc[0, 'Fruit'])

# [OUT]
     Fruit  Count
0    Apple     11
1   Banana     23
2  Coconut     35

Fruit    Apple
Count       11
Name: 0, dtype: object

Apple
~~~

## 5.3 Fasion MNIST
- Fasion MNIST는 MNIST에 영향을 받아 만들어진 데이터세트로, 손글씨가 아닌 옷과 신발, 갑ㅇ의 이미지 등을 모아 둠
- 그레이스케일 이미지라는 점과 범주의 수가 10개라는 점, 각 이미지의 크기가 28 x 28 픽셀이라는 점은 MNIST와 동일하지만 좀 더 어려운 문제로 평가됨
- Fasion MNIST는 tf.keras에 기본 탑재되어 있음
~~~python
fashion_mnist = tf.keras.datasets.fashion_mnist
(train_X, train_Y), (test_X, test_Y) = fashion_mnist.load_data()

print(len(train_X), len(test_X))
~~~
- 훈련 데이터는 60,000장, 테스트 데이터는 10,000장의 패션 이미지를 포함하고 있음
- 이 데이터가 어떻게 생겼는지 확인해야함
~~~python
plt.imshow(train_X[0], cmap='gray')
plt.colorbar()
plt.show()
print(train_Y[0])
~~~
- `matplotlib.pyplot`의 `imshow()` 함수로 이미지를 그래프의 형태로 표시할 수 있음
- 다음으로는 데이터를 정규화하자. 여기서는 최댓값과 최솟값을 이미 알고 있으므로, 이미지의 각 픽셀값을 255로 나누기만 하면 0.0 ~ 1.0 사이의 값으로 정규화됨
~~~python
train_X /= train_X / 255
test_X /= test_X / 255
~~~
- 이번 분류 모델 생성에서는 따로 one-hot encoding을 하지 않음  
  기존의 Y data가 label encoding 되어 있으므로, 그대로 진행
- 이러한 데이터를 받아서 처리하기 위해서는 간단한 수정이 필요
~~~python
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(units = 128, activation='relu'),
    tf.keras.layers.Dense(units = 10, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(), loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
model.summary()
~~~
- `sparse_categorical_crossentropy` 를 쓰면 별도의 데이터 전처리 없이 희소 행렬을 나타내는 데이터를 정답 행렬로 사용할 수 있음
- `Flatten`이라는 레이어를 사용하여 2차원 array를 -> 1차원으로 변환
- Adam의 learing Rate를 따로 지정하지 않음. 기본 default 값은 0.001

~~~python
# 6. loss, val_loss, accuracy, val_accuracy 그래프로 확인
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

# 7. 분류 모델 평가
model.evaluate(test_X, test_Y)
~~~
