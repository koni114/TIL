## Anomaly detection 
## Anomaly detection 이란
- Anomaly detection이란, Normal sample과 Abnormal sample을 구별해내는 무제를 의미
- 제조업, CCTV, 의료영상, Social Network 등 다양한 분야에서 응용이 되고 있음
- Anomaly detection 용어 외에도 다양한 용어가 비슷한 의미로 사용되고 있어 이 용어들을 기준에 따라 정리하고, 각 용어에 대해서 자세히 설명

## Anomaly detection 연구 분야 용어 정리 
- <b>Anomaly detection은 학습 데이터셋에 비정상적인 sample이 포함되는지, 각 sample이 label이 존재하는지, 비정상적인 sample의 성격이 정상 sample과 어떻게 다른지, 정상 sample의 class가 단일 class인지에 따라서 다른 용어를 사용</b>

## 학습시 비정상 sample의 사용여부 및 label 유무에 따른 분류 
### Supervised Anomaly Detection
- 데이터에 정상, 비정상 데이터와 label이 모두 존재하는 경우 Supervised Learning 방식이기 때문에 Supervised Anomaly Detection이라고 함
- Supervised Learning 방식은 다른 방법 대비 정확도가 높은 특징이 있음
- 그래서 높은 정확도를 요구하는 경우에 주로 사용되며, 비정상 sample을 다양하게 보유할수록 더 높은 성능을 달성할 수 있음
- 하지만 일반적인 산업 현장에서는 정상 sample보다 비정상 sample의 발생빈도가 현저히 적기 때문에 class-Imbalance 문제를 자주 겪게 됨
- 이러한 문제를 해결하기 위해 Data Augmentation, Loss function 재설계, Batch Sampling 등 다양한 연구가 수행되고 있음

### Semi-supervised(One-class) Anomaly detection
- Supervised Anomaly Detection 방식의 가장 큰 문제는 sample을 확보하는데 많은 시간과 비용이 든다는 것
- 제조업 같은 경우에는 수백만 장의 정상 sample이 취득되는 동안 단 1~2장의 비정상 sample이 취득되는 상황이 종종 발생
- 따라서 class-Imbalance가 매우 심한 경우 정상 sample만 이용해서 모델을 학습하기도 하는데, 이 방식을 One-class Classification이라고 함
- 이 방법론의 핵심 아이디어는 정상 샘플들을 둘러싸는 discriminative boundary를 설정하고, 이 boundary를 최대한 좁혀 boundary 밖에 있는 sample들을 모두 비정상으로 간주하는 것
- One-Class SVM이 One-Class Classification을 사용하는 대표적인 방법론으로 잘 알려져 있으며, 이 아이디어를 확장해 Deep Learning을 기반으로 One-class Classification 방법론을 사용하는 Deep SVDD 논문이 잘 알려져 있음
- 장점 : 비교적 활발하게 연구가 진행되고 있으며, 정상 sample만 있어도 학습이 가능
- 단점 : Supervised Anomaly Detection 방법론과 비교했을 때 상대적으로 양/불 판정 정확도가 떨어짐
#### 기타 방법론
- Energy-based 방법론
- Deep Autoencoding Gaussian Mixture Model 방법론
- Generative Adversarial Network 기반 방법론
- Self-Supervised Learning 기반

### Unsupervised Anoamly Detection
- 위에서 설명한 One-class(Semi-supervised) Anomaly Detection 방식은 정상 sample이 필요함
- 수많은 데이터 중에 어떤 것이 정상 sample인지 알기 위해서는 반드시 정상 sample에 대한 Label을 확보하는 과정이 필요
- 이러한 점에 주목해, 대부분의 데이터가 정상 sample이라는 가정을 하여 Label 취득 없이 학습을 시키는 Unsupervised Anomaly Detection 방법론도 연구가 이뤄지고 있음
- 가장 단순하게는 주어진 데이터에 대해 Principal Component Analysis를 이용하여 차원을 축소하고 복원을 하는 과정을 통해 비정상 sample을 검출할 수 있음
- Neural Network 기반으로는 대표적으로 Autoencoder 기반의 방법론이 주로 사용되고 있음 
- Autoencoder는 입력을 code 혹은 latent variable로 압축하는 Encoding과, 이를 다시 원본과 가깝게 복원해내는 Decoding 과정으로 진행이 되며 이를 통해 데이터의 중요한 정보들만 압축적으로 배울 수 있다는 점에서 데이터의 주성분을 배울 수 있는 PCA와 유사한 동작을 한다고 볼 수 있음
- Autoencoder를 이용하면 데이터에 대한 labeling을 하지 않아도 데이터의 주성분이 되는 정상 영역의 특징들을 배울 수 있음
- 이때, 학습된 autoencoder에 정상 sample을 넣어주면 잘 복원하므로 input과 output의 차이가 거의 발생하지 않는 반면, 비정상적인 sample을 넣으면 autoencoder는 정상 sample처럼 복원하기 때문에 input과 output 차이를 구하는 과정에서 차이가 도드라지게 발생하므로 비정상 sample을 검출할 수 있음
- 다만 Autoencoder의 code size(latent variable 의 dimesion) 같은 hyper parameter에 따라 전반적인 복원 성능이 좌우되기 때문에 양/불 판정 정확도가 Supervised Anomaly Detection에 비해 다소 불안정하다는 단점이 존재
- auto-encoder에 넣어주는 input과 output의 차이를 어떻게 정읳라지, 어느 loss function을 사용해 autoencoder를 학습시킬지 등 여러가지 요인에 따라 성능이 크게 달라질 수 있음
- 이렇듯 성능에 영향을 주는 요인이 많다는 약점이 있지만 별도의 labeing이 필요없다는 장점이 있음
- 장점 : Labeling 과정이 필요 없음. 단점 : 양/불 판정 정확도가 높지 않고 hyper parameter에 매우 민감

## 비정상 sample 정의에 따른 분류
- 이 분류는 기준이 엄밀하게 정의되어있지 않음
- 비정상 smaple을 정의하는 방식에 따라 크게 Novelty Detection과 Outlier Detection으로 구분
- 다만 두 방법론을 합쳐서 Anomaly Detection이라 부르기도 함
- Novelty Detection과 Outlier Detection은 용어가 가지는 뉘앙스의 차이가 존재하다고 느껴 예시를 통해 두 용어의 차이를 설명해보겠음
- 강아지를 normal class로 예를 들면, 현재 보유 중인 데이터셋에 이전에 없던 형태의 새로운 강아지가 등장하는 경우 Novel sample, Unseen sample 등으로 부를 수 있음
- 이러한 sample을 찾아내는 방법론을 Novelty Detection이라 부를 수 있음
- 강아지가 아닌 호랑이, 기린이 등장한다고 했을 때는 outlier sample, abnormal sample이라고 부름
- outlier detection : 등장할 가능성이 거의 없는, 데이터 오염이 발생했을 가능성이 있는 sample을 찾아 내는 연구와 관련된 용어 정로도 구분
- novelty detection : 지금까지 등장하지는 않았지만 충분히 등장할 수 있는 sample을 찾아내는 연구, 즉 오염이 되지 않은 상황을 가정하는 연구와 관련된 용어

## 정상 sample의 class 개수에 따른 분류
- 실제 환경에서는 정상 sample이 여러 개의 class로 구성될 수 있음
- 정상 sample이 multi-class인 상황에서도 위의 Novelty Detection, Outlier Detection 기준을 똑같이 적용할 수 있음. 보통 이러한 경우 정상 sample이라는 표현 대신 In-distribution sample이라는 표현을 사용함
- In-distribution 데이터 셋에 위의 예시 그림처럼 흰색 강아지만 있는 것이 아니라, 골든 레트리버, 닥스훈트, 도베르만, 말티즈 등 4가지 종류의 강아지 sample들이 존재한다고 가정하면, 불독 sample은 novel sample, 호랑이 sample은 outlier sample로 간주할 수 있음
- 이렇게 In-distribution 데이터셋으로 network를 학습 시킨 뒤, test 단계에서 비정상 sample을 찾는 문제를 Out-of-distribution Detection이라 부르며 학계에서는 널리 사용되는 주요 Benchmark 데이터 셋들을 이용하여 실험을 수행하고 있음
- 예를 들면 In-distribution 데이터 셋으로 CIFAR-10을 가정하고 Classifier를 학습시킴
- 그 뒤, 실내 이미지 데이터 셋인 LSUN, 숫자 관련 데이터 셋인 SVHN 등을 Out-of-distribution 데이터 셋으로 가정한 뒤 test 시에 In-distribution 데이터 셋인 CIFAR-10은 얼마나 정확하게 예측하는지, LSUN, SVHN 데이터 셋은 얼마나 잘 걸러낼 수 있는지를 살펴보는 방식으로 사용 
- 대부분의 연구에서 주로 사용하는 softmax 기반 classifier는 class 개수를 정해 놓고 가장 확률이 높은 class를 결과로 출력하는 방식이기 때문에, 위에서 예시로 들었던 4가지 종류의 강아지를 구분하는 classifier에 호랑이 이미지를 넣어주면 사람은 비정상 sample이라고 구분할 수 있는 반면 classifier는 4가지 class 중 하나의 class로 예측
- 이러한 Outlier sample을 걸러 내기 위해 Out-of-distribution Detection 알고리즘을 사용할 수 있음
- 또한 불독 이미지처럼 Novel한 sample이 관찰되었을 때 이를 걸러낸 뒤, classifier가 기존의 있는 4가지 class 대신 불독이 새로 추가된 5가지 class를 구분하도록 학습하는 Incremental learning 방법론과도 응용할 수 있음

![img](https://github.com/koni114/TIL/blob/master/Machine-Learning/img/anomaly_detection.PNG)

## Anomaly Detection의 다양한 적용 사례
- <b>Cyber-Intrusion-Detection</b> : 컴퓨터 시스템 상에 침입을 탐지하는 사례. 주로 시계열 데이터를 다루며 RAM, file system, log file 등 일련의 시계열 데이터에 대해 이상치를 검출하여 침입 탐지
- <b>Fraud Detection: </b> 보험, 신용, 금융 관련 데이터에서 불법 행위를 검출하는 사례. 주로 tabular 데이터를 다룸
- <b>Malware Detection : </b> 악성코드를 검출해내는 사례. Classification과 Clustering이 주로 사용되며 Malware tabular 데이터를 그대로 이용하기도 하고 이를 gray scale image로 변환하여 이용하기도 함
- <b>Medical Anomaly Detection :</b> 의료 영상, 뇌파 기록 등의 의학 데이터에 대한 이상치 탐지 사례. 주로 신호 데이터와 이미지 데이터를 다룸
- <b>Social Networks Anomaly Detection : </b>
- <b>Log Anomaly Detection : </b> 시스템이 기록한 log를 보고 실패 원인을 추적하는 사례. 주로 Text 데이터를 다루며 pattern matching 기반의 단순한 방법을 사용하여 해결할 수 있지만 failure message가 새로운 것이 계속 추가, 제외가 되는 경우에 딥러닝 기반 방법론을 사용하는 것이 효과적임.
- <b>IOT Big-Data Anomaly Detection :</b> 사물 인터넷에 주로 사용되는 장치, 센서들로부터 생성된 데이터에 대해 이상치를 탐지하는 사례. 주로 시계열 데이터를 다루며 여러 장치들이 복합적으로 구성이 되어있기 때문에 난이도가 높음.
- <b>Industrial Anomaly Detection : </b> 산업 속 제조업 데이터에 대한 이상치를 탐지하는 사례. 각종 제조업 도메인 이미지 데이터에 대한 외관 검사, 장비로부터 측정된 시계열 데이터를 기반으로 한 고장 예측 등 다양한 적용 사례가 있으며, 외관상에 발생하는 결함과, 장비의 고장 등의 비정상적인 sample이 굉장히 적은 수로 발생하지만 정확하게 예측하지 못하면 큰 손실을 유발하기 때문에 난이도가 높음.
- <b>Video Surveillance :</b> 비디오 영상에서 이상한 행동이 발생하는 것을 모니터링 하는 사례. 주로 CCTV를 이용한 사례가 주를 이루며, 보행로에 자전거, 차량 등이 출현하는 비정상 sample, 지하철역에서 넘어짐, 싸움 등이 발생하는 비정상 sample 등 다양한 종류의 비정상 케이스가 존재

## 이상치 탐지와 특이치 탐지를 위한 알고리즘 정리
### PCA(`inverse _transform() 메서드를 가진 다른 차원 축소 기법`)
- 보통 샘플의 recontruction error와 이상치의 recontruction error를 비교하면 후자가 훨씬 크다는 성질을 이용
- 이는 간단하고 종종 매우 효과적인 이상치 탐지 기법임

### Fast-MCD(Minimum convariance determinant)
- `EllipticEnvelope` 클래스에서 구현된 이 알고리즘은 이상치 감지에 유용
- 특히 데이터셋을 정제할 때 사용. 보통 샘플이 하나의 가우시안 분포에서 생성되었다고 가정함
- 또한 이 가우시안 분포에서 생성되지 않은 이상치로 이 데이터셋이 오염되었다고 가정함
- 알고리즘이 가우시안 분포의 파라미터(즉 정상치를 둘러싼 타원 도형) 추정할 때 이상치로 의심되는 샘플을 무시
- 이런 기법은 알고리즘이 타원형을 잘 추정하고 이상치를 잘 구분하도록 도움

### isolation Forest
- 고차원 데이터셋에서 이상치 감지를 위한 효율적인 알고리즘임
- 이 알고리즘은 무작위로 성장한 결정 트리로 구성된 랜덤 포레스트
- 각 노드에서 특성을 랜덤하게 선택한 다음(최솟값과 최댓값 사이에서) 랜덤한 임곗값을 골라 데이터셋을 둘로 나눔
- 이런 식으로 데이터셋은 점차 분리되어 모든 샘플이 다른 샘플과 격리될 때까지 진행됨
- 이상치는 일반적으로 다른 샘플과 멀리 떨어져 있으므로 (모든 결정 트리에 걸쳐) 평균적으로 정상 샘플과 적은 단계에서 격리됨

### LOF(local outlier Factor)
- 이 알고리즘도 이상치 탐지에 좋음. 주어진 샘플 주위의 밀도와 이웃 주위의 밀도를 비교
- 이상치는 종종 k개의 최근접 이웃보다 더 격리됨

### one-class SVM
- 이 알고리즘은 특이치 탐지에 잘 맞음

## 기억해야 할 용어 정리
- Out-Of-Distribution(OOD)
- supervised Anomaly Detection / semi-supervised Anomaly Detection / unsupervised Anomaly Detection
- In distribution sample : 정상 sample이 multi-class인 상황


## 참고해야 할 사항들
- 핸즈온 머신러닝에서 outlier detection과 novelty detection을 이상치가 포함된 데이터에서 학습하느냐, "깨끗"한 데이터에서 훈련하느냐로 나눔


## 참고 블로그 및 문헌
- https://hoya012.github.io/blog/anomaly-detection-overview-1/

