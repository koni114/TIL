## chapter03 컨텐츠 기반 모델

### 통계 기반의 단점
- TF-IDF와 같은 모델의 단점
- 대규모 말뭉치를 다룰 때, 메모리상의 문제가 발생
  - 높은 차원을 가짐. 매우 sparse한 형태의 데이터
  - 예) 100만개의 문서를 다루는 경우: 100만개의 문서에 등장한 모든 단어를 추출해야하고 이떄 단어의 수는 1문서당 새로운 단어가 10개면 1000만개의 말뭉치가 형성됨
  - 즉 100만 x 1000만의 매트릭스가 형성
- 한번에 학습 데이터 전체를 진행함
  - 큰 작업을 처리하기 어려움
  - GPU와 같은 병렬처리를 기대하기 힘듬
- 학습을 통해서 개선하기가 어려움  

### 추론기반의 방법(Word2Vec)
- 추론: 주변 단어(맥락)이 주어졌을 때, "?" 에 무슨 단어가 들어가는지를 추측하는 작업
- ex) you say goodbye and I say hello라는 맥락이 주어졌을 때, you와 goodbye 사이에 있는 say를 예측하거나(CBOW 모델) say가 주어졌을 때 양 옆의 You, goodbye를 예측하는 것(skip-gram)을 말함
- 잘못 예측한 경우, 학습을 통해서 점점 모델을 개선

### Word2Vec 정의
- Word2Vec은 단어간 유사도를 반영하여 단어를 벡터로 바꿔주는 임베딩 방법론
- 원-핫 벡터의 sparse matrix의 단점을 해소하고자 저차원의 공간에 벡터로 매핑하는 것이 특징
- Word2Vec은 비슷한 위치에 등장하는 단어들은 비슷한 의미를 가진다 라는 가정을 통해 학습을 진행함
- 저차원에 학습된 단어의 의미를 분산하여 표현하기에 단어 간 유사도를 계산할 수 있음
- 추천시스템에는 단어를 구매 상품으로 바꿔서 구매한 패턴에 Word2Vec을 적용해서 비슷한 상품을 찾을 수 있음

### Word2Vec - CBOW, Skip-gram
- 결과적으로는 skip gram을 많이 사용하며, 논문 상에서도 성능 차이가 많이 발생한다고 함
- CBOW는 주변에 있는 단어를 통해 중간에 있는 단어들을 예측하는 방법. 반대로 Skip-gram은 중간에 있는 단어로 주변 단어들을 예측하는 방법
- ex) You say goodbye and I say hello
- 주변 단어: (you, goodbye)
- 중심 단어: (say)
- 윈도우 크기 : 주변을 몇 칸까지 볼 지에 대한 크기 (1). 만약 2면 중심단어를 기준으로 양옆 2칸까지 보겠다는 의미

### CBOW 모델 생성 방법
- One Hot vector 형태의 입력값을 받음
- One Hot vector 형태의 입력값을 Win과 곱함. 여기서의 Win은 신경망 모형에서의 Weight를 말함  
  차원의 크기는 사용자가 지정
~~~python
import numpy as np
input1 = np.array([1, 0, 0, 0, 0, 0, 0]) #= You
input2 = np.array([0, 0, 1, 0, 0, 0, 0]) #- goodbye

W_in = np.random.randn(7, 3)
h_1 = np.matmul(input1, W_in)
h_2 = np.matmul(input2, W_in)

print((h_1 + h_2) / 2)

#- hidden state의 값을 W_out과 곱해서 Score를  추출
W_out = np.random.randn(3, 7)
score = np.matmul(h, W_out)
print(np.round(score, 4))

#- Score에 softamx를 취해 각 단어가 나올 확률을 계산함
def softmax(x):
    exp_x = np.exp(x)
    sum_exp_x = np.sum(exp_x)
    y = exp_x / sum_exp_x
    return y

pred = softmax(score)
print(np.round(pred, 4))

#- 정답 레이블과 Loss를 가지고 Backpropagation 과정을 통해서 Weight를 업데이트
ans = [0, 1, 0, 0, 0, 0, 0]   
ds = np.round(pred - ans, 4)
print(ds)

#- Softmax의 Backpropagation 값 ds = Pi - yi
#- 정답과 예측값의 cross-entropy를 계산
def cross_entropy_error(y, t):
    '''
    y : prediction
    t : target
    '''
    delta = 1e-7
    return np.sum(t * np.log(y + delta)) / y.shape[0]

cross_entropy_error(pred, ans)

#- 계산한 Loss를 통해 Backpropagation 과정을 통해서 Weight를 업데이트
#- Softmax의 Backpropagation 값(Pi - yi)
#  - ds : [0.174, -0.8788, 0.0988, 0.1765, 0.2168, 0.1134, 0.0982]
#  - dw_out(Delta for W_out) = np.outer(Hidden Layer, ds)
dW_out = np.outer(h, ds)   #- weight에 대한 output 계산 가능 
print(np.round(dW_out, 4))

da = np.dot(ds, W_out.T)  #- hidden layer에 대한 역전파 값을 계산
print(np.round(ds, 4))

dw_1 = np.round(np.outer(np.array([1, 0, 0, 0, 0, 0, 0, 0]), (da/2)), 4) 
print(dw_1)

dw_2 = np.round(np.outer(np.array([0, 0, 1, 0, 0, 0, 0, 0]), (da/2)), 4) 
print(dw_2)

learning_rate = 1
W_in_new = W_in - learning_rate * dw_1
W_in_new = W_in_new - learning_rate * dw_2
print(np.round(W_in_new, 4))
~~~
- 이러한 과정을 iteration 만큼 수행하여 가중치 값이 적절하게 업데이트 할 때까지 반복함
- 또한 이러한 과정을 window 만큼 계속 이동하여 수행

### Skip-gram 
- 위의 CBOW와 나머지는 동일하고, input data가 1개의 one-hot vector로 구성되며, output vector는 2개의 one-hot vector로 구성


### Word2Vec 실습
- `gensim` package를 활용하여 수행 가능

### 컨텐츠 기반 모델 장점
- 협업필터링은 다른 사용자들의 평점이 필요한 반면에, 자신의 평점만을 가지고 추천시스템을 만들 수 있음
- item의 feature를 통해서 추천을 하기에 추천이 된 이유를 설명하기 용이함
- 사용자가 평점을 매기지 않은 새로운 item이 들어올 경우에도 추천이 가능 

### 컨텐츠 기반 모델 단점
- item의 feature를 추출해야 하고 이를 통해 추천하기 떄문에 제대로 feature를 추출하지 못하면 정확도가 낮음
- 그렇기에 Domain knowledge가 분석시에 필요할 수 있음
- 기존의 item과 유사한 item 위주로만 추천하기에 새로운 장르의 item을 추천하기 어려움
- 새로운 사용자에 대해서 충분한 평점이 쌓이기 전까지는 추천하기 힘듬



