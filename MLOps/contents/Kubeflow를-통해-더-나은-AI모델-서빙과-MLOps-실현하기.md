# Kubeflow를 통해 더 나은 AI 모델 서빙과 MLOPs 실현하기
- Naver D2의 AiSuite: Kubeflow를 통해 더 나은 AI 모델 서빙과 MLOps 실현하기 영상을 듣고 나름대로 정리한 자료

## Contents
- 왜 Kubeflow 기반의 AI Platform 인가?
- KFServing 으로 대규모 ML 서비스 서빙하기
- KubeFlow로 MLOps 실현하기
- Multi-Tenant Kubeflow 
- HDFS를 k8s 볼륨으로 사용하기 위한 AIuxio 연동
- Future work

## Hadoop 기반 사내 AI 플랫폼
- 네이버에서는 데이터 센터를 직접 운영하고 있고, Hadoop 기반 AI 사내 빅데이터 플랫폼을 운영하고 있음
- 전사의 다양한 서비스들이 해당 플랫폼을 이용하고 있음

### Naver 사내 AI 플랫폼 설명
- `Cuve`: 사내 분산 저장 플랫폼. --> 수많은 네이버 서비스들의 로그가 저장됨
- `CQuery`: Cuve 저장소의 로그를 SQL로 조회하기 위한 프레임워크
- `C3`, `C3S`: 사내 분산 처리 플랫폼
  - 다양한 Hadoop eco-system 지원
  - Spark, Mapreduce, HDFS
  - YARN, Apache Slider 를 통해 docker container 를 위한 orchestration 지원
- `C3DL` : 사내 분산 머신러닝 플랫폼
![img](https://github.com/koni114/TIL/blob/master/MLOps/contents/img/image_01.png)

- `AiSP` : 사내 머신러닝 서빙 플랫폼
  - 하루 수억 건의 머신러닝 인퍼런스 요청을 처리 
- `AI Suite` : 사내 머신러닝 파이프라인 플랫폼
  - `AI FEATURE` -> `AI TRAINING` -> `AI SERVING`

### 한계점
- Hadoop은 빅데이터 처리를 하기 위해 만들어진 플랫폼
- 컨테이너 오케스트레이션의 제약
  - 배포, 스케일링, 모니터링 등 컨테이너 관리 기능의 한계
- 컨테이너 네트워킹을 위한 추가 개발 필요  
  - 오버레이 네트워크 지원을 위해 Flunnel 및 DNS 등을 직접 커스터마이징 해야함
- GPU 스케줄링의 한계
  - Hadoop 내 GPU 지원의 한계로, GPU 스케줄러를 직접 개발해서 사용함  
- 서빙 플랫폼 운영시 겪은 어려운 점들
  - 블루/그림 배포로 인한 한계점(급격한 캐시 성능 저하, 리소스 2배 필요)
  - 오토스케일러 X, 요청이 급격하게 증가했을 때 수동으로 대응 필요  
- ML 파이프라인 제공의 어려움
  - 인프라 관리 팀이 아닌, 유저가 직접 모듈을 추가하기 어려움(모듈 로직 외 프론트엔드 로직 등의 추가 개발이 필요) 

### kubeflow 란? 
- 쿠버네티스 위에서 학습, 하이퍼 파라미터 튜닝, 서빙, 파이프라인을 지원하는 플랫폼

![img](https://github.com/koni114/TIL/blob/master/MLOps/contents/img/image_02.png)

### Kubeflow의 장점
- '1. 다양한 ML 프레임워크 지원
  - `Tensorflow`, `PyTorch`, `ONNX`, `scikit-learn`, `MXNet`, `XGBoost`, `Chainer`, `NVIDIA Triton` 
  - 사용자가 입맛에 맞게 자신이 원하는 프레임워크를 사용 가능
- '2. Kubeflow 대쉬보드 제공
  - 사용자 문서를 추가하거나 새로운 탭을 추가하는 등 커스터마이징도 손쉽게 가능
- '3. K8s 컨테이너 오케스트레이션
  - CNI(Container Network Interface) 플러그인을 통한 네트워크 구성 제공 
  - Prometheus 호환을 통한 손쉬운 모니터링 구성 제공
  - 라이브니스, 레디니스 프로브, 사이드카 컨테이너 기능
  - Istio를 통한 카나리 배포 지원
  - Knative를 통한 오토스케일링, 제로 스케일, 서버리스 지원
- '4. GPU 지원 용이
  - Nvidia, AMD GPU 디바이스 플러그인 지원
  - 노드 레이블과 노드 셀렉터를 이용해 GPU 종류별 스케일링 가능
- '5. 다양한 k8s 에코시스템
  - Istio, Knative, Argo CD, Deepops, Helm, Kubespray 등
  - k8s 에서 유용하게 사용할 수 있는 새로운 프레임워크들이 활발하게 개발되고 공유되고 있음

## KFServing 으로 대규모 ML 서비스 서빙하기
### KFServing 이란? 
- kubeflow의 대표적인 서빙 프레임워크로, kubernetes와 service mash network framework인 Istio, serverless framework 인 Knative가 있음
- KFServing 은 kubernetes와 Istio를 기반으로 다양한 ML 프레임워크를 지원하고, 추상화된 인터페이스를 지원
- 최근에 명칭이 KServe로 변경됨
![img](https://github.com/koni114/TIL/blob/master/MLOps/contents/img/image_03.png)

### 기존 서빙 플랫폼과의 비교
#### AiSp
![img](https://github.com/koni114/TIL/blob/master/MLOps/contents/img/image_04.png)

- 크게 클라이언트 라이브러리(C++, Python)와 Tensorflow, LightGBM 기반 모델 서버로 구성
- 클라이언트 라이브러리
  - c++, Python 언어 제공 
  - 서버들을 찾기 위한 서비스 디스커버리
  - 클라이언트 사이드에서의 로드 벨런싱  
  - gRPC로 통신하기 위한 proto-buffer 데이터 직렬화
  - 모니터링, 캐시
- 모델 서버
  - Tensorflow, ONNX, LightGBM 기반 framework를 제공하며, HDFS에서 모델을 로딩한 후, gRPC로 통신

![img](https://github.com/koni114/TIL/blob/master/MLOps/contents/img/image_05.png)

- 클라이언트 사이드 로드벨런싱은 네트워크가 균등하게 분산되어 한 곳에 집중되지 않고, network hook이 줄어든다는 장점이 있지만,  
  각 클라이언트마다 랜덤하게 부하를 분산하기 때문에 부하 분산이 완전히 균등하지 않고 서버 추가시 service discovery까지 시간이 걸림
- KFServing은 ingress gateway를 통한 서버 사이드 로드벨런싱을 수행함  
  모든 서버에 부하가 균등하게 분산됨
- gRPC, REST API를 통한 단일 진입점 제공하여 어떤 프로그래밍 언어든 사용가능  

![img](https://github.com/koni114/TIL/blob/master/MLOps/contents/img/image_06.png)

- 기존에는 서빙 관련한 매트릭을 제공하기 위하여 클라이언트 라이브러리에서 프로메테우스 관련 로직들을 직접 구현하여 제공  

![img](https://github.com/koni114/TIL/blob/master/MLOps/contents/img/image_07.png)

- 기존에서는 container 수를 증가시키거나 자원 할당량을 증가시킬 때, 직접 수동으로 증가시켜야 하는 반면,  
  KFServing에서는 CPU 사용량, 트래픽 기반 오토스케일링 지원

![img](https://github.com/koni114/TIL/blob/master/MLOps/contents/img/image_08.png)

- 블루/그린 배포 -> 카나리 배포방식의 적용 가능 

### KFServing 환경 구축하기
- Prometheus 를 통한 모니터링 지표 수집
  - Prometheus Operator : ServiceMonitor 와 Pod Monitor라는 CRDs 통해서 손쉽게 모니터링 타겟을 설정하도록 지원 
- 모니터링 타겟
  - kube-state-metrics: k8s API 서버에서 k8s 오브젝트 지표 수집
  - metrics-servers: kubelet 에서 노드, 컨테이너 지표 수집  
  - DCGM exporter: GPU 지표 수집
  - Knative serving metrics: Knative 지표 수집
  - Istio service mesh metrics: Istio 지표 수집

![img](https://github.com/koni114/TIL/blob/master/MLOps/contents/img/image_09.png)

- Grafana 커스텀 대시보드 구성
  - CPU, 메모리, GPU, 네트워크 사용량, 처리량, 응답시간, CPU throttling 과 같은 지표를 한눈에 볼 수 있게 제공
  - metrics-server, kube-state-metrics, Istio, Knative serving, DCGM exporter 와 같은 여러 모니터링 소스로부터의 지표를 조합하여 구성 
- Kubeflow 대시보드 모니터링 구성
  - kubeflow 대시보드를 통해 서버의 리소스, 트래픽 상태 뿐만 아니라 오브젝트 상태, 로그, YAML에 대한 정보제공
  - KFserving 버전 0.6으로 업그레이드 필요
- 캐싱
  - 결과를 캐싱하여 응답시간을 줄임(네이버 쇼핑 딥러닝 모델 서빙에 적용시 평균 응답시간이 50% 감소)
  - 서비스 별로 독립적인 Redis 서버를 사용하도록 구성
- 캐싱 구성 과정
  - InferenceService CRD에서 사이드카 컨테이너 설정을 할 수 없는 문제
  - annotation을 붙이면, 어드미션 웹 훅을 통해 컨테이너 생성 요청시 Redis를 사이드카 컨테이너로 동작시키도록 구현

![img](https://github.com/koni114/TIL/blob/master/MLOps/contents/img/image_10.png) 

![img](https://github.com/koni114/TIL/blob/master/MLOps/contents/img/image_11.png)

- 실서비스 성능 테스트
  - 네이버 쇼핑에서 사용되는 딥러닝 모델로 성능 테스트 진행
  - AiSP와 동일한 전/후 처리 로직을 동일한 언어로 구현 
  - 분산 부하 테스트 툴 Locust로 실서비스와 동일한 트래픽을 가해 응답시간 측정
  - 기존 플랫폼과 비교해 성능 저하를 우려했으나 부하 테스트 결과, 동일한 서버 자원으로 평균 응답시간이 동일함

## 용어 정리
- argo
  - 컨테이너 워크플로우 솔루션
  - 컨테이너 기반으로 빅데이터 분석, CI/CD, 머신러닝 파이프라인을 만들 때 유용하게 사용할 수 있는 오픈 소스 솔루션
- ONNX(Open Neural Netowrk Exchange, 우노)
  - Tensorflow, PyTorch 와 같은 서로 다른 DNN 프레임워크 환경에서 만들어진 모델들을 서로 호환해서 사용할 수 있도록 도와주는 공유 플랫폼         
- CNI(Container Network Interface)
  - 쿠버네티스 네트워크에 오버레이 네트워크를 구성해주고 파드와 호스트 인터페이스를 연결해주는 녀석
- Prometheus
  - 매트릭을 저장하기 위한 모니터링 시스템 
- gRPC
  - 구글에서 개발한 어느 환경에서 실행할 수 있는 최신 오픈 소스 고성능 RPC 프레임워크
  - RPC : Remote Procedure Call의 약자. 별도의 원격 제어를 위한 코딩 없이 다른 주소 공간에서 함수나 프로시저를 실행할 수 있게하는 프로세스 간 통신 기술
  - MSA 구조 서비스를 만들게 되면, 다양한 언어와 프레임워크로 개발되는 경우가 있는데, 이러한 구조에 RPC를 이용하여 언어에 구애받지 않고, 원격에 있는 프로시저를 호출하여 고유 프로그램의 개발에 집중할 수 있께 해주는 기술
  - gRPC는 RPC 시스템에서와 마찬가지로 서비스를 정의하고, 서비스를 위한 매개변수와 반환 값을 가지는 메서드를 만든다는 아이디어를 가지고 있음 
- 클라이언트 사이드 로드벨런싱 vs 서버사이드 로드벨런싱
  - 서버사이드 로드벨런싱
    - 하드웨어: L4, L7 스위치를 이용한 방식  
    - 요청: client -> NAT(주소변조) -> L4 -> serve
    - 응답: server -> NAT(주소변조) -> L4 -> client
    - 소프트웨어: HA proxy를 이용한 방식
    - 응답시 쿠키에 서버 정보를 추가. 쿠키를 사용하여 로드 벨런싱함
  - 클라이언트 사이드 로드벨런싱
    - 스위치에서 하던 분산 역할을 클라이언트 측에서 처리
    - 클라이언트가 서버 목록중에 접속할 서버를 선택하여, 접속하지 못하는 경우 다른 서버로의 접속을 시도  
- 블루/그린 배포
  - 블루를 구버전, 그린을 신버전으로 지칭하여 붙여진 이름으로 운영 환경에 구버전과 동일하게 신버전의 인스턴스를 구성한 후, 로드벨런서를 통해 신버전으로 모든 트래픽을 전환하는 배포 방식임
  - 블루-그린 배포를 위해서는 시스템 자원이 두 배로 필요하며, 새로운 환경에 대한 테스트가 전제되어야 함
- 카나리 배포
  - 신버전의 제공 범위를 늘려가면서 모니터링 및 피드백 과정을 거칠 수 있음  
  - 로드벨런서를 통해 신버전의 제품을 경험하는 사용자를 조절할 수 있는 것이 특징으로 신버전을 특정 사용자 혹은 단순 비율에 따라 구분해 제공할 수 있음


## 참조 링크
- https://deview.kr/2021/sessions/465
- 