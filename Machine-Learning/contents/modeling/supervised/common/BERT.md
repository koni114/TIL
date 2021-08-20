## BERT(Bidirectional Encoder Representations from Transformer)
- Transformer의 Bidirectional Encoder임을 알 수 있음
- Bidirectional의 의미는 양방향, Encoder는 문장을 숫자로 변환하는 모듈을 의미하므로, 즉 문장을 양방향으로 이해해서, 문장을 숫자로 변환하는 tranformer라는 것을 알 수 있음

### Transformer
- transformer는 2017년에 구글에서 공개한 인코더, 디코더 구조를 지닌 모델
- Attention is All You need라는 논문을 통해서 공개가 됨
- encoder는 문장을 양방향으로 처리하고, decoder는 왼쪽에서 오른쪽 단 방향으로 처리한다는 큰 차이점이 있음 
- BERT가 양방향 처리를 하는데 있어서는 GPT-1의 영향이 있었음

### GPT-1
- GPT-1은 2018년 OpenAI에서 transformer의 decoder 구조를 사용해서 만든 자연어 처리 모델
- GPT-1은 generative training으로 학습된 model이 얼마나 자연어 처리 능력이 우수한지 보여준 우수한 모델
- 기본적으로 문장을 데이터로 사용하며, 단어를 하나씩 읽어 가며 다음 단어를 예측하는 방법으로 모델이 학습됨
- 이런 학습 방식은 별도의 label이 필요가 없어, 비지도 학습이라 할 수 있음
- 다음에서 볼 수 있듯이 한 문장만 가지고도 여러 학습 데이터를 만들어 낼 수 있음
  - train Data          /   Label
  -  youtube                 deep
  -  youtube deep          learning
  -  youtube deep learning tutorial
- 문장에서 현재 위치의 단어 다음에 위치한 단어를 예측하는 방식으로 학습되기 때문에 사람이 직접 labeling 할 필요가 없음
- GPT-1은 이렇게 현재 위치의 단어 다음에 위치한 단어를 예측하는 방법으로 학습이 됨
- GPT-1의 학습 시에 가장 필요한 건 엄청난 양의 데이터, 물론 질적으로 좋은 데이터를 선별하는 노력도 중요
- 인터넷 상에는 텍스트가 정말 어마어마하게 많고 질 좋은 데이터를 선별하는 기술도 함께 발전하기 떄문에 GPT는 앞으로도 아주 각광받을 모델

### GPT-1
- 

## 용어 정리
- generative model
  - 데이터 X가 생성되는 과정을 두 개의 확률모형 P(Y), P(X|Y)로 정의하고, 베이즈룰을 사용해 P(Y|X)를 간접적으로 도출하는 모델을 가리킴
  - generative model은 레이블 정보가 있어도 되고, 없어도 구축할 수 있음
  - 전자를 지도학습기반의 generative model이라고 하며 선형판별분석(LDA)가 대표적인 사례
  - 후자는 비지도학습 기반의 generative model이라고 하며 gaussian mixture model, topic modeling이 대표적인 사례 
  - generative model은 가정이 많으며, 그 가정이 실제 현상과 맞지 않는다면 성능이 떨어질 수 있지만, 가정이 잘 구축되어 있다면 이상치에도 강건하고 학습데이터가 적은 상황에서도 좋은 예측 성능을 보일 수 있음
  