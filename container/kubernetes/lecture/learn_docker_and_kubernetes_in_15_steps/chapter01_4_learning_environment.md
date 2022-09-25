# 이 책의 학습 환경
## 이 책에서 다루는 OSS 목록
### Ansible
- K8s 클러스터, GlusterFS 클러스터 등 여러 가상 머신이 연계하는 환경을 자동으로 설정하기 위해 사용
- NFS 서버, 미니쿠베 등에서도 패키지 인스톨에 사용

### Docker Community Edition
- 도커 학습 환경 및 쿠버네티스용 컨테이너 실행 환경으로 사용
- Docker CE는 무료이며 다운로드 해서 사용 가능, Docker EE는 서브 스크립션 구입이 필요

### 도커 툴박스(Docker Toolbox)
- Window용 도커 학습 환경에 사용. Docker CE로 교체될 전망. Window와 Mac 의 공통 환경을 만들 수 있도록 도커 툴박스를 채용

### 도커 컴포즈(Docker Compose)
- 여러 도커 컨테이너를 조합하여 기동할 수 있도록 만든 개발자용 오케스트레이션 tool
- 이 책에서는 private registry를 다룰 때 사용

### 일라스틱서치(Elastic Search)
- 미니쿠베의 로그 보관을 위한 add-on 용도로 사용
- 메모리 사용량은 2.4GB로 큰 편이기 때문에 학습 환경에서의 설치는 추천하지 않음

### Fluentd
- 미니쿠베의 로그를 일래스틱서치(Elasticsearch)에 전송하기 위한 툴

### GlusterFS
- 확장 가능한 분산 파일 시스템
- K8s 클러스터에서는 Heketi를 사용하여 logical volume의 동적 프로비저닝을 실행

### Grafana
- 오픈 소스 데이터 시각화 웹 프로그램으로, 미니쿠베의 애드온으로서 기동
- 미니쿠베에서는 influxDB와 Heapster를 연계하여 시계열 데이터를 시각적으로 표시

### Hyper-V
- Window의 하이퍼바이저로, Window용 Docker CE를 리눅스 커널을 기동하기 위해 사용
- 책에서는 Mac과의 공통 환경을 우선해서 채용을 보류

### Heapster
- 쿠버네티스 노드에서 가동 정보를 수집하는 컴포넌트
- 버전 1.13에서 metrics-server로 대체

### Heketi
- GlusterFS의 라이프 사이클을 관리하기 위해 만들어진 RESTFUL한 관리 인터페이스 제공
- 쿠버네티스의 퍼시스턴트 볼륨 요청과 스토리지 클래스와 연계하여, 동적 프로비저닝을 실현하기 위해 사용

## 용어 정리
- 프로비저닝(provisioning)
  - 사용자의 요구에 따라 미리 시스템 자원을 할당, 배치, 배포해 두었다가 즉시 사용할 수 있게끔 준비해 두는 것을 말함 