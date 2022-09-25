# 학습환경 1
- 싱글 노드 구성의 미니쿠베 설치
- 학습 환경 1은 미니쿠베(Minikube)를 사용하여 단일 노드로 구성된 쿠버네티스 구축
- 도커 설치는 `Docker Desktop for Mac` 사용
- 쿠버네티스의 경우에는 CNCF가 배포하는 업스트림 코드를 사용해서 학습 환경 구축

## Docker Desktop for Mac 설치
- '1. Docker Community Edition for Mac 설치
- '2. virtualBox 설치
- '3. kubectl 명령어 설치  
  - 설치 방법은 CNCF의 쿠버네티스 페이지에 기재되어 있음
  - macOS 의 패키지 매니저인 Homebrew를 사용하여 설치 가능
~~~shell
$ brew install kubernetes-cli
~~~
- '4. 미니쿠베 설치
  - 최신 버전의 미니쿠베 설치  
    다운로드 받은 minikube directory를 `/usr/local/bin` 에 이동 후 기존 Dir 삭제
~~~shell
$ brew install minikube darwin-amd64 && chmod +x minikube && sudo cp minikube /usr/local/bin && rm minikube

# 미니쿠베 설치 확인
$ minikube version

# 결과
minikube version: v1.25.2
~~~
- '5. Vagrant 설치
  - virtualbox의 자동화 도구인 Vagrant 설치 
  - https://www.vagrantup.com/download/html
- '6. git 설치

## Vagrant의 리눅스에서 미니쿠베 사용하기
- 여기서는 Vagrant 와 Ansible 이라는 자동화 도구를 사용
- 사용된 코드는 https://github.com/Jpub/15_DandK/tree/master/vagrant-minikube
- 주의사항(** 중요)
  - `minikube.yaml` 파일에서 `minikube` 설치시 version 지정해야 함  
  - As-Is : `https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64`
  - To-Be : `https://storage.googleapis.com/minikube/releases/v1.25.2/minikube-linux-amd64`


### 설치 순서
- minikube가 부팅되기까지 3~5분 정도의 시간이 걸림
~~~shell
$ git clone https://github.com/Jpub/15_DandK.git
$ cd 15_Dandk/vagrant-minikube
$ vagrant up           # 해당 명령어를 vagrant-minikube dir 위치에서 실행해야함
                       # 약 5분 ~ 10분정도 소요
$ vagrant ssh
$ docker version       # -- Docker CE 확인
$ sudo minikube start  #  
~~~

### 사용 방법
- 미니쿠베가 구성한 쿠버네티스에 액세스하려면 `vagrant ssh`로 가상 서버에 들어가 kubectl 커맨드를 사용하면 됨
- 가상 서버와 PC간의 파일 공유를 위해 가상 서버의 경로 `/vagrant`에 호스트의 `Vagrantfile`에 있는 디렉터리를 마운트함
~~~shell
$ vagrant ssh

$ kubectl get node                 # 노드 목록 표시 --> (오래 걸림)
$ kubectl get pod --all-namespaces # 모든 pod 목록 표시

# 결과
NAMESPACE     NAME                               READY   STATUS    RESTARTS        AGE
kube-system   coredns-64897985d-fwcjq            1/1     Running   1 (5m1s ago)    5m26s
kube-system   etcd-minikube                      1/1     Running   1 (5m6s ago)    5m38s
kube-system   kube-apiserver-minikube            1/1     Running   1 (4m56s ago)   5m40s
kube-system   kube-controller-manager-minikube   1/1     Running   1 (5m6s ago)    5m38s
kube-system   kube-proxy-hzqls                   1/1     Running   1 (5m6s ago)    5m26s
kube-system   kube-scheduler-minikube            1/1     Running   1 (4m56s ago)   5m38s
kube-system   storage-provisioner                1/1     Running   1 (5m6s ago)    5m37s

$ vagrant halt                     # minikube 가상 서버 정지
$ vagrant destroy                  # 미니쿠베 가상 서버 삭제    
~~~ 

## minikube 사용 방법

### 미니쿠베 옵션
- 다음 표에는 핵심이 되는 명령어들을 정리. 관련 내용은 `minikube -h` 를 실행해도 확인할 수 있음
~~~shell
$ minikube start
$ minikube stop
$ minikube delete
$ minikube status
$ minikube ip
$ minikube ssh
$ minikube addons list
$ minikube dashboard
~~~

### 미니쿠베 기동
- Windows에서는 커맨드 프롬포트에서, macOS에서 터미널에서 `minikube start`를 입력
~~~shell
$ minikube start
$ minikube status
$ kubectl get node
~~~
- Vagrant로 기동한 가상 머신 위에서 미니쿠베를 기동하는 경우, Vagrantfile이 있는 디렉터리로 이동하여 가상 머신을 기동하고 로그인 후 미니쿠베 기동
- kubectl 커멘드는 가상 머신 내에서 사용할 수 있음
~~~shell
# Vagrantfile 위치로 이동
$ vagrant up
$ vagrant ssh
$ sudo minikube start 
~~~

### 미니쿠베 정지와 제거
- 미니쿠베를 다 사용한 후에는 가상 머신을 정지시켜 점유하던 자원을 해제해주어야 함
- 종료할 때의 상태는 재부팅 후 복원됨(**). 즉 정지하기 전에 배포한 K8s 클러스터의 디플로이먼트, 서비스, 파드 등의 이어서 기동됨
~~~shell
$ minikube stop   # 미니쿠베 가상 머신 종료
~~~
- 실습을 진행하면서 미니쿠베가 응답이 없는 경우가 있는데, 가상 머신을 지우고 다시 시작하는 것이 좋음
~~~shell
$ minikube delete # 미니쿠베 가상 머신 삭제 
~~~
- 삭제해도 문제가 해결되지 않을 때는 미니쿠베의 운영체제 이미지를 지우고 다시 시작
~~~shell
$ minikube delete && rm -fr ~/.minikube
~~~
- Vagrant-Minikube는 다음 순서로 중지
~~~shell
$ sudo minikube stop 
$ exit
$ vagrant halt
~~~
- Vagrant가 만든 가상 머신을 지우려면 다음과 같이 실행
~~~shell
$ exit             # 가상 머신에서 아웃  
$ vagrant destroy  # 가상 머신 삭제
$ vagrant up       # 가상 머신 기동
~~~

### 대시보드
- 쿠버네티스의 구조를 이해하는 데 매우 유용한 시각정 정보를 제공
- CPU와 메모리 사용량에 대한 시계열 그래프를 보기 위해 `metrics-server` 를 먼저 기동해야 함
- 그리고 미니쿠베 대시보드를 실행하면 PC의 브라우저에서 대시보드에 접속
~~~shell
# host server에서 실행
$ minikube addons enable metrics-server

# Opening kubernetes dashboard in default browser ... 
$ minikube dashboard
~~~
- 대시보드에서 네임스페이스를 '모든 네임스페이스'로 선택하고, 개요를 클릭하면 화면 표시됨
- `metrics-server`를 기동하지 않았다면 CPU와 메모리 사용량 그래프는 표시되지 않음
- `metrics-server`를 기동하고 그래프가 표시될 때까지는 약 5분 정도의 시간이 걸림  
  이는 정보를 수집하고 통계를 내기 위해 필요한 시간임
- Vagrant-minikube 환경에서는 minikube 앞에 `sudo`를 붙여야함
- PC의 브라우저에서 가상 머신 안의 대시보드에 접근하기 위해서는 가상 머신의 IP 주소 `172.16.10.10`를 사용
- 다음 순서에 따라 대시보드를 위한 파드를 기동. 마지막 명령어는 포그라운드로 돌기 때문에 이후 단계는 다른 터미널을 열고 작업해야 함
~~~shell
$ sudo minikube addons enable metrics-server
$ sudo minikube dashboard --url
~~~
- 새로운 터미널을 열고 `vagrant ssh`로 로그인 후 다음 커맨드를 실행하면 가상 서버의 IP 주소에서 접근 가능
- fore-ground로 돌아가기 때문에 대시 보드에 접근하는 동안 터미널은 계속 돌도록 나둬야 함
~~~shell
# k8s 클러스터 외부로부터 접속을 위한 프록시 기동
$ kubectl proxy --address="0.0.0.0" -p 8001 --accept-hosts='^*$' -n kube-system
~~~
- 그러면 다음 URL로 Vagrant-Minikube 의 대시보드에 액세스 할 수 있음
- http://172.16.10.10:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/#/overview?namespace=default

### 로그 분석
- 미니쿠베는 통합 검색 엔진인 ElasticSearch, 로그 수집 도구인 Fluentd, 데이터 시각화 및 분석 도구인 Kibana 기반의 로그 수집 및 분석 환경을 플러그인으로 제공
- elasticSearch 같은 경우, 약 2.4GB의 메모리를 필요로 함 
- 미니쿠베가 만드는 가상 서버는 2GB의 메모리를 사용하도록 설정되기 때문에 그대로는 EFK를 사용할 수 없다  
  따라서 minikube의 가상 머신을 삭제 후 8GB를 할당하여 재시작
~~~shell
$ minikube delete

$ minikube start --memory=8192
~~~
- 미니쿠베 기동시 EFK를 기동시킴. `minikube start`를 실행한 후 쿠버네티스가 완전히 기동할 때까지는 2~3분의 시간 소요
- 준비가 완료된 것을 확인하기 위해 다음 커맨드를 실행하여 모든 pod가 Running 인지를 확인
~~~shell
$ kubectl get po --all-namespace
$ minikube addons enable efk
~~~
