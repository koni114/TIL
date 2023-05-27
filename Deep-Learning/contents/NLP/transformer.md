## transformer
## Sequence-to-Sequence
- 어떤 sequence들을 다른 sequence로 mapping하는 알고리즘
- 예를 들어 영어로 작성된 문장을 번역하는 Translation이 가장 많이 언급되는 application
- 정보를 압축하는 encoder와 이를 통해 새로운 data를 생성해내는 decoder 부분으로 나눠져 있음
- 번역으로 예를들면, 압축되는 정보들은 단어 및 어간에 관한 정보들로 표현
- 많은 시계열 분석에 LSTM을 적용할때 잘 작동하는 경우가 많지만, LSTM에 encoder에서 decoder로 들어가는 과정에서
  전달되는 정보에서 소실되는 시간 정보들이 생기게 됨
- 예를 들어 output sequence를 얻기 위해서는 단어의 매핑만으로 충분한 것이 아니라, keyword와 중요한 부분들에 대한 정보가 필요

## Attention
- input data의 중요 부분을 수치로 표현해서 output으로 넘겨주는 방식
- output sequence를 생성해내는 매 Time step마다 이전 input time step들을 다시 보고 
  중요하다는 부분을 참고해서 output을 생성하는 방식
- 구현시 어떻게 '이 부분이 중요한지'를 수치로 표현할 지 알아야 함
- dot product attention을 정리해 보자

- encoder의 hidden state와 decoder의 hidden state 함수가 얼마나 유사한 지를 표현하기 위한 
  내적으로 시작
- 유사도를 비교할 때, 내적을 많이 사용한다는 점을 알고 있으면 좋음
- dot product attention은 내적을 사용하지만, attention 함수들도 있으니 찾아보면 좋음
- 이렇게 얻은 attention score를 softmax 함수에 넣어서 attention value 값을 구하여 decoder의 hidden state 차원 밑에  
  그대로 붙이고 이를 output 계산의 input으로 넣으면 attention 알고리즘이 마무리 됨

## [Transformer]
- RNN, LSTM의 약점으로 많이 언급된 것은 단어를 순차적으로 입력받아 이를 계산하기 때문에
  병렬 처리가 어렵다는 점이였음.
- 하지만 이 순차적으로 입력받는 것이 각 input의 위치정보를 반영할 수  있게 해줌
- transformer는 순차적으로 data를 넣는 것이 아니라, sequence를 한번에 넣음으로써 병렬처리가 가능하면서도
  attention 등의 구조를 통해 어떤 부분이 중요한지를 전달하여 위치정보를 반영할 수 있게 됨

1. Embedding
  - data를 임의의 N-dimension data로 만듬

2.  positional encoding
  - 데이터의 위치정보와 embedding된 데이터를 sin, cos function 형태로 만듬
  - 다음 layer의 input으로 전달
  - embedding시 위치 정보를 함께 넣어주자라는 내용
  - transformer는 해당 input의 위치를 반영한 pre-processing을 할 수 있게됨

3. Encoder
  - Multi-head Self attention / add & normalize / position-wise FFNN 모듈로 구성
  3.1 Multi-head self attention
  - self-attention은 encoder로 들어간 벡터와 encoder로 들어간 모든 벡터를 연산해서 attention score를 구함
  - 이런 self-attention을 통해 각 input data의 유사도를 구할 수 있음
  - ex) 'The Animal didn't cross the street, because it was so tired' 라는 문장에서
    it이 무엇에서 오는건지, it이 Animal인지 street 을 가리키는 것인지 알기 위해 독해를 하는 것과 유사
  - 이를 위해 attention 함수의 Query(Q), Key(K), Value(V)를 의미하는 weight 행렬과
    'scaled Dot-product Attention' 방식으로 연산하여 Attention value matrix (a)를 만들어냄
  - 이 과정에서 d_model개의 차원을 num_heads로 나눠지는 갯수만큼의 그룹으로 묶어 d_model/num_head 개의
    attention value matrix를 뽑아냄
  - 여러 head를 가지는 attention value matrix를 뽑아냄으로써 다양한 관점으로 연산을 할 수 있게 만듬
  - 이렇게 여러 개로 나온 attention value matrix는 다시 d_model 차원으로 합쳐짐
 3.2 add & normalize
  - residual connection과 layer normalization임
    - Residual Connection은 cnn 에서 resnet에서 사용됨
    - 연산을 한 부분과 안 하는 부분이 합쳐지도록 만든 것
 3.3 FFNN - fully connected layer

4. decoder
- encoder와 비슷하지만, 크게 2가지 차이점이 있음
  - Multi-head self attention에 masked가 들어갔다는 점이 첫 번째 차이





