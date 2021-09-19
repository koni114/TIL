## Attention Is All You need
- 2021년 기준으로 최신 고성능 모델들은 Transformer 아키텍처를 기반으로 하고 있음
  - GPT: Transformer의 디코더(Decoder) 아키텍처를 활용
  - BERT: Transformer 의 인코더(Encoder) 아키텍처를 활용
- 2015년 Attention 매커니즘이 발전한 이후부터는 입력 시퀀스 전체에서 정보를 추출하는 방향으로 발전

### 기존 Seq2Seq 모델들의 한계점
- Seq2Seq라고 부르는 이유는 특정한 Sequence vector에서 특정한 Sequence Vector를 만들어내기 때문에 Seq2Seq라고 부를 수 있음
- 단어가 차례대로 타임 스텝마다 입력되면 hidden state가 출력되고, 출력된 hidden state 값이 다음 타임 스텝의 입력값으로 활용되는 구조
- 마지막 단어가 나타났을 때 출력되는 hidden state가 전체 문장을 대표하는 hidden state, 즉 context vector로서 활용될 수 있음 
- context vector에서 부터 출발하는 디코더 파트에서는 단어가 입력될 때마다 hidden state를 만들어 출력을 만들어냄
- context vector v에 소스 문장의 정보를 압축하려고 하면 병목(bottleneck)이 발생하여 성능 하락의 원인이 됨   
- 마지막 단어(<eos>)가 나올 때의 hidden state의 값을 하나의 Context vector로 활용하여 디코딩시 활용하는 개념

#### 문제상황
- 하나의 문맥 벡터가 소스 문장의 모든 정보를 가지고 있어야 하므로 성능이 저하됨
  
#### 해결방안
- 매번 소스 문장에서의 출력 전부를 입력으로 받으면 어떨까?
- 최신 GPU는 많은 메모리와 빠른 병렬 처리를 지원함

### 트랜스포머
- 2021년 기준으로 현대의 자연어 처리 네트워크에서 핵심이 되는 논문
- 트랜스포머는 RNN이나, CNN을 전혀 필요로 하지 않음. attention 기법 만을 사용함
  - 대신 Positional Encoding을 사용
- BERT와 같은 향상된 네트워크에서도 채택되고 있음
- 인코더와 디코더로 구성됨
  - Attention 과정을 여러 레이어에서 반복함   

### 트랜스포머의 동작 원리: 입력 값 임베딩(Embedding)
- 논문의 저자는 임베딩 차원을 512차원으로 설정함. 이 값은 사용하는 사람마다 다를 수 있음
- RNN을 사용하지 않는다면 위치 정보를 포함하고 있는 임베디딩을 사용해야 함
- 이를 위해 트랜스포머에서는 Postitional Encoding을 사용 

### Multi-Head Attention layer
- attention은 특정 단어가 다른 단어들과 어떤 연관성을 가지는지 구하는 것이라고 할 수 있음
- 이 때 Query, Key, Value로 구분함
- Query는 물어보는 주체, Key는 대상, Value는 가중치 합(?)으로 볼 수 있음
- 예를 들어 I am a teacher라는 문장에서 I가 나머지 단어들과의 연관성을 계산 할 때, I는 query이고 나머지 단어들은 key임
- 각각의 key와 query의 행렬곱을 통해 attention score를 계산하고 value와 곱해 최종 attention score를 계산
- Scaled Dot-Product Attention 수행 process
  - Query와 Key 행렬의 행렬 곱 수행
  - scaling
  - 필요하다면 Masking 수행
  - Softmax를 취함으로서 key-value 중에 어떤 단어와 가장 연관성이 높은지 확률 계산
  - 최종 Value값과의 곱을 통해 attention score 계산
- 어떠한 문장이 들어왔을 때, 이 값들은 Query, Key, Value로 구분  
  이 때 head 개수 만큼의 차원을 생성하고 마지막으로 입력값과 출력값을 같게 해주기 위해 일자로 붙임(concat)
- Multi-head attention 층은 transformer에서 여러 층에 사용되는데  
  층의 위치(인코더이냐 디코더이냐)에 따라서 query, key, value 값이 조금씩 달라지는 것을 제외하고 연산 방법등은 같음
- 예를 들어 디코더의 multi-head attention은 쿼리는 출력 문장의 단어가 되는 것이며, key는 인코더의 출력값을 사용

#### multi-head attention 계산 식
- Attention(Q, K, V) = softmax(QK^T/sqrt(d_k))V 
  - Q matrix와 K matrix를 곱해서 attention energy 값을 구함
  - d_k는 key matrix의 차원 값인데, 나눠주는 이유는 softmax 함수가 0에 가까울수록 gradient 값이 커지는 반면, 왼쪽, 오른쪽으로 이동하면 기울기가 많이 줄어들기 때문에 Gradient Vanishing 문제를 해결 가능하기 때문
  - 마지막으로 해당 attention energy 값에서 V matrix를 행렬 곱함
- head(i) = Attention(QW_(i)^Q, KW_i^K, VW_i^V)
  - 서로 다른 컨셉의 head 개수 만큼의 attention을 만들어냄
- Multi-head(Q, K, V) = concat(head1, ..., headh) * Wo
  - 최종 출력을 입력 차원과 동일하게 만들기 위해 concat 

### Multi-Head attention 계산 과정
- Q, K, V 값 만들기
  - 예를 들어 love라고 하는 단어 하나를 multi-head attention 계산을 수행한다고 하자
  - love의 임베딩 차원은 4차원(논문 상에서는 512차원이라고 함), head를 2개로 한다고 했을 때  
    Query, Key, Value 차원은 (4 / 2) = 2차원이 됨
  - 즉 Wquery, Wkey, Wvalue의 차원은 4 x 2 가 되며(가중치다!), 최종 Q, K, V 차원은 1x2
  - love(1x4) x Wquery, Wkey, Wvalue(4x2) = Q,K,V(1x2)
- Q, K의 행렬곱을 통해 attention energy matrix 도출
  - Q(1x2 matrix) * K^T(2x1 matrix) 를 통해 attention energy(단어들의 연관성) 도출
  - 해당 값을 sqrt(dk)로 나눠주고(normalization) softmax 취해주면 연관성의 확률 값이 도출됨
- Value matrix를 최종 곱해주고 더함(weighted sum)
  - attent energy(1x1) x V(1x2) = Attention(1x2)

### Masking
- 마스크 행렬을 사용하여 특정 단어를 무시할 수 있도록 함
- attention energies matrix와 동일한 크기의 mask matrix를 만들어내고, 각각 element wise 연산 수행
- 연산에 적용하고 싶지 않은 값 위치에 음수값을 배치해두면 활성화되지 않음