# 쿠버네티스 첫걸음
- 도커와 쿠버네티스의 관계를 직접 체험해보자. 여기서는 앞서 실행해본 이미지 hello-world를 쿠버네티스의 커맨드 `kubectl`로 실행해 볼 것임

## 클러스터 구성 확인
- K8s 클러스터의 구성을 확인해보자. 실행 예 1에서는 `kubectl clutser-info`를 실행하여 마스터의 IP 주소, 내부 DNS의 엔드포인트를 확인해보자
~~~shell
$ kubectl cluster-info

# 출력 결과
Kubernetes control plane is running at https://127.0.0.1:51704
CoreDNS is running at https://127.0.0.1:51704/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
~~~
- 출력 결과 오류가 나는 경우 `kubectl` 과 마스터가 통신할 수 없는 경우일 수 있음  
- 해결방안 
  - 미니쿠베를 사용하는 경우, `minikube delete` , `minikube start`를 실행해보자
  - `minikube delete`, -> home directory의 `.kube`, `.minikube`를 지우고 `minikube start` 실행
  - Vagrant의 리눅스에서 미니쿠베 사용하기를 이용하고 있다면, `minikube delete` -> `minikube start --vm-driver none`를 입력하여 재실행
- 이어서 K8s 의 구성을 `kubectl get node`로 확인. 미니쿠베에서는 K8s 클러스터를 제어하는 마스터 노드와 컨테이너가 실행되는 워커 노드가 `minikube`란 이름의 노드 하나에 포함. 그래서 아래와 같이 출력됨
~~~shell
$ kubectl get node

# 결과
NAME       STATUS   ROLES                  AGE   VERSION
minikube   Ready    control-plane,master   13m   v1.23.3
~~~

## 파드 실행
- <b>파드는 쿠버네티스에서 컨테이너를 실행하는 최소 단위</b>
- 아래 실행 예시는 kubectl을 사용하여 hello-world 컨테이너를 쿠버네티스에서 돌리고 있음  
  커맨드의 옵션은 도커와 아주 다르지만, 같은 결과가 출력되는 것을 확인 가능
~~~shell
$ kubectl run hello-world --image=hello-world -it --restart=Never
~~~

### 위의 명령어 상세 설명  

|     |     |     |
| --- | --- | --- |
| 번호  | 값   | 해설  |
| (1) | kubectl | K8s 클러스터를 조작하기 위해 사용되는 커맨드 |
| (2) | run | 컨테이너 실행을 명령하는 서브 커맨드 |
| (3) | hello-world | 쿠버네티스 오브젝트의 이름(파드나 컨트롤러 등) |
| (4) | --image=hello-world | 컨테이너의 이미지. 쿠버네티스에서는 파드 단위로 컨테이너가 기동되며 리포지터리명이 생략된 경우에는 경우에는 도커 허브를 사용 |
| (5) | -it | 도커에서의 -it 과 마찬가지로, -i는 키보드를 표준 입력에 연결하고, -t는 유사 터미널과 연결하여 대화 모드 설정. 옵션 `--restart=Never` 인 경우에만 유효하며, 그 외에는 백그라운드로 실행 |
| (6) | --restart=Never | 이 옵션에 따라 파드의 가동 방법 변경. Never는 직접 파드가 기동되며 Always 나 OnFailure 는 컨트롤러를 통해 파드가 가동 |

- 위의 파드를 다시한 번 실행하면, 에러가 발생함. --> 파드가 이미 존재한다는 내용
~~~shell
$ kubectl run hello-world --image=hello-world -it --restart=Never

# 결과
Error from server (AlreadyExists): pods "hello-world" already exists
~~~
- 원인이 무엇인지 살펴보기 위해 `kubectl get pod`를 실행해보자. 여기서 사용된 커맨드 `get`은 이어서 지정하는 오브젝트의 목록을 출력하라는 의미로 사용
~~~shell
$ kubectl get pod

# 결과
NAME          READY   STATUS      RESTARTS   AGE
hello-world   0/1     Completed   0          15m
~~~
- 위에서 `STATUS`가 `Completed`라고 나오지만, `hello-world`의 파드가 아직 있는 것을 확인가능  
  즉 종료한 pod가 남아있다는 얘기
- 파드를 지우고 다시 실행해보자
~~~shell
$ kubectl delete pod hello-world 

# 결과
pod "hello-world" deleted

$ kubectl run hello-world --image=hello-world -it --restart=Never

# 결과
Hello docker ! 
...
~~~
- `docker run` 에서 `--rm` 이라는 옵션을 지정하면 실행 후 종료된 컨테이너를 자동으로 지워주는 것처럼 `kubectl run`에서도 마찬가지임
- 다음은 파드 종료 후 자동으로 해당 파드를 삭제해주는 옵션 `--rm`을 추가한 예제
~~~shell
$ kubectl run hello-world --image=hello-world -it --restart=Never --rm
~~~
- `kubectl run` 명령어를 입력하고 결과가 표시될 때까지의 흐름은 다음과 같으며 도커 명령어와 비슷함
  - kubectl이 쿠버네티스에게 명령을 전달
  - 노드에 이미지가 없으면 원격 리포지터리(Docker hub)에서 다운로드 
  - 노드의 containered가 컨테이너를 실행 
  - kubectl 이 터미널에 메세지를 표시
- 쿠버네티스의 특징 중 하나는 <b>개인의 PC, 퍼블릭 클라우드, 온프레미스의 모든 환경에서 동일한 kubectl 명령어로 조작할 수 있다는 점</b>
- `-it` 명령어를 생략해서 파드를 실행하면, 백그라운드에서 실행됨. 이떄 파드의 컨테이너가 표준 출력(STDOUT)으로 출력한 메세지들은 로그로 보존됨
- 로그를 출력하려면 `kubectl logs <파드명>`을 실행하면 됨





