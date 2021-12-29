## Docker 와 Kubernetes 
### MLOps에서 쿠버네티스가 필요한 이유 
- Reproducibility
  - 실행 환경의 일관성 & 독립성 
- Job Scheduling
  - 스케줄 관리, 병렬 작업 관리, 유후 작업 관리
- Auto-healing & Auto-scaling
  - 장애 대응, 트래픽 대응
- 도커와 쿠버네티스를 활용하면 다음과 같은 기능들을 쉽게 구현이 가능

### Containerization & Container란 무엇일까
- Containerization
  - 컨테이너화 하는 기술
- Container
  - 격리된 공간에서 프로세스를 실행시킬 수 있는 기술
- 지금은 나의 ML code를 independent 하도록 정보를 모두 담은 실행 환경 자체를 하나의 패키지로 만드는 기술로 이해해도 무방

### Container Orchestration
- 수많은 도커 컨테이너를 어떤 역할을 하는 컨테이너는 어디에 배치할 것인가를 지휘하는 것을 말함
- kubernetes 가 container orchestration의 거의 대세가 됨
- Container Orchestration 기술은 여러 명이 함께 서버를 공유하며 각자 모델 학습을 돌리고자 할 때, GPU가 남았는지 매번 확인하거나, 학습이 끝나면 서버 자원을 깔끔하게 정리하고 나오거나, 이러한 귀찮은 일들을 할 필요없이 수많은 컨테이너 들을 정해진 룰에 따라서 관리해 주는 것이라고 이해해도 됨

### Docker의 기본 개념
- Build Once, Run Anywhere
- 도커에서 제공하는 패키징 방식을 통해, 하나의 어플리케이션을, 이 어플리케이션이 dependent한 것 들을 하나로 묶은 docker image 형태로 build 함으로써 어떤 OS, 환경에서 사용 가능
- docker image로 만드는 것을 dockerize 한다라고 말하자
- ML 모델의 제품화 서비스를 고려해야 할 때, docker는 필수

### Docker 실습 환경 준비
- docker는 linux container 기반의 기술이기 때문에 MacOS나 windows 위에서 수행되려면 VM 위에서 돌아가야 함
- VirtualBox 를 사용해 VM을 하나 띄우고, ubuntu 로 띄운 다음에 여러가지 실습을 진행할 예정
- VirtualBox 설치
  - 6.1.26 버전 설치
- ubuntu 20.04 설치
  - Desktop image download  
  - .iso 로 생성되는 파일이 download 됨
  - 다운 받는데 5분 이상 걸릴 수도 있음
- virtualBox 를 켜서 새로 만들기 버튼 클릭
- 종류는 linux, 버전은 ubuntu(64-bit로 고정)
- 메모리 크기는 8GB로 선택
- 하드 디스크 -> 지금 새 가상 하드 디스크 만들기 선택
- 하드 디스크 종류 -> VDI 선택
- 물리적 하드 드라이브에 저장 -> 동적 할당 선택
- 파일 위치 및 크기 -> 10.00GB 
- 완료 후 시작 버튼 클릭 후, 우측 버튼 아이콘을 선택한 후, 추가 버튼 클릭 후, 다운로드 경로를 찾아서 ubuntu 파일 선택하면, ubuntu가 실행됨 

- Mac : https://docs.docker.com/desktop/mac/install
