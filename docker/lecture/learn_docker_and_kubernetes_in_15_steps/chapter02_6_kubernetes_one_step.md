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

## 컨트롤러에 의한 파드 실행
- `kubectl run`에 옵션을 지정하면 파드를 디플로이먼트 컨트롤러(= 디플로이먼트)의 제어하에 실행하는 것이 가능
- 이 때 사용하는 옵션이 `--restart=Always` 임. 한편 파드만을 독립적으로 실행하고 싶을 때는 `--restart=Never` 옵션을 주면 됨
- 파드가 정지되었을 때 재기동시킬 필요가 있는지에 따라 옵션을 주면 됨
- `kubectl run`의 옵션 `--restart=`를 생략하면 기본값으로 Always로 실행됨. 즉 기본적으로 디플로이먼트에 의해 파드가 기동됨
~~~shell
$ kubectl run hello-world --image=hello-world
~~~
- 디플로이먼트를 만들 때는 `kubectl create deployment --image hello-world hello-world` 를 사용  
  **(2022.03.27 기준, 위의 명령어를 수행해야 디플로이먼트가 생성됨)
~~~shell
$ kubectl create deployment --image hello-world hello-world
$ kubectl get all

# 결과
NAME                               READY   STATUS             RESTARTS      AGE
pod/hello-world                    0/1     CrashLoopBackOff   3 (50s ago)   109s
pod/hello-world-649b9bfb9c-wkfww   0/1     Completed          0             7s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   21m

NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/hello-world   0/1     1            0           7s

NAME                                     DESIRED   CURRENT   READY   AGE
replicaset.apps/hello-world-649b9bfb9c   1         1         0       7s
~~~
- 4개의 오브젝트가 출력됨.
  - `deployment.apps/hello-world` : 디플로이먼트 오브젝트의 이름은 hello-world임. 이 컨트롤러는 레플리카셋 컨트롤러와 함께 파드를 관리하며 이미지의 버전, 파드의 개수 등이 목표 상태가 되도록 관리
  - `replicaset.apps/hello-world-649b9bfb9c` : 디플로이먼트와 함께 만들어진 레플리카셋 오브젝트의 이름은 `hello-world-649b9bfb9c` 임. 디플로이먼트 오브젝트의 이름 뒤에 해시 문자열이 붙어 유일한 이름을 부여받음  
  레플리카셋은 디플로이먼트와 함께 파드의 수가 지정한 개수가 되도록 제어  
  유저가 직접 레플리카셋을 조작하는 것은 권장되지 않음
  - `pod/hello-world-649b9bfb9c-wkfww` : 파드 안에는 하나 혹은 여러 개의 컨테이너가 실행됨  
    여기서는 `hello-world-649b9bfb9c-wkfww` 라는 이름을 부여받음. 레플리카셋 오브젝트의 이름 뒤에 추가적인 해시 문자열이 추가되어 역시 유일한 이름을 부여받음
- 컨테이너 `hello-world`가 출력한 메세지는 `kubectl logs 파드명` 으로 확인가능
~~~shell
$ kubectl logs po/hello-world-649b9bfb9c-wkfww
~~~
- 이 `hello-world` 컨테이너가 디플로이먼트에 의해 어떻게 제어되는지 살펴보자
- 명령어 `kubectl get deploy.po` 는 디플로이먼트와 파드 프로젝트의 목록을 출력  
~~~
$ kubectl get deploy,po

NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/hello-world   0/1     1            0           13m

NAME                               READY   STATUS             RESTARTS        AGE
pod/hello-world                    0/1     CrashLoopBackOff   7 (4m10s ago)   15m
pod/hello-world-649b9bfb9c-wkfww   0/1     CrashLoopBackOff   7 (2m40s ago)   13m
~~~
- `kubectl run`을 실행할 때 옵션 `--replicas=숫자`를 생략했기 떄문에 기본값으로 1이 설정
- `AVAILABLE` 컬럼의 값은 0이라고 나오는데, 이는 파드가 기동에 실패했음을 의미. 무슨 문제가 있는 것일까?
- 다음은 kubectl get deployment 각 항목의 의미

|     |     |
| --- | --- |
| 항목명 | 설명  |
| NAME | 디플로이먼트의 오브젝트명 |
| DESIRED | 희망 파드 개수, 디플로이먼트를 만들 때 설정한 파드 수 |
| CURRENT | 현재 실행 중인 파드의 개수, 재기동 대기 등을 포함한 모든 파드 수 |
| UP-TO-DATE | 최근에 업데이트된 파드의 개수. 즉 컨트롤러에 의해 조정된 파드 수 |
| AVAILABLE | 사용 가능한 파드 개수. 즉 정상적으로 기동되어 서비스 가능한 파드 수 |
| AGE | 오브젝트가 만들어진 후 경과 시간 |

- 아래는 파드에 대한 각 항목이 의미하는 바를 정리한 내용.  
  실행 예 13에서 STATUS 열에 `CrashLoopBackOff`라고 표시되어 있는데, 이는 `hello-world` 파드가 어떤 문제 떄문에 재시작을 반복하고 있는 상태임을 의미

|     |     |
| --- | --- |
| 항목명 | 설명  |
| NAME | 파드의 오브젝트명 |
| READY | 기동 완료 수. 분자와 분모의 형태로 숫자가 표시.<br>분자 측은 파드 내의 컨테이너가 기동된 개수이며, 분모 측은 파드 내의 정의한 컨테이너의 총 개수.<br>즉 0/1 의 의미는 파드에 컨테이너가 하나 정의되었으나 기동하지 않았음을 의미 |
| STATUS | 파드의 상태. CrashLoopBackOff라는 것은 컨테이너가 재시작을 반복하여 다음 재시작 전에 대기하고 있는 상태를 의미. 컨테이너를 기동할 때 리눅스의 프로세스 관리로 인해 CPU 부하가 많이 발생.<br>따라서 문제 상황에서 계속된 반복에 의한 CPU 부하를 막기 위해 일정한 간격을 두고 재시작 실행 |
| RESTARTS | 파드가 재시작된 횟수 |
| AGE | 파드 오브젝트가 만들어진 후 경과 시간 |

- 디플로이먼트로 관리되는 파드들은 보통 웹 서버나 앱 서버처럼 상시로 가동되어야 하는 경우가 많음
- 그런데 컨테이너 hello-world는 메세지를 출력하고 바로 종료하기 때문에 디플로이먼트가 몇 번이나 파드를 재시작하면서 STATUS가 CrashLoopBackOff가 되어 대기 상태가 된 것임
- 디플로이먼트는 관리 중인 파드가 종료되면, 지정된 파드의 개수를 유지하기 위해 파드를 재기동함
- 따라서 처음부터 컨테이너 hello-world는 디플로이먼트 컨트롤러에 맞지 않는 워크로드를 가진다고 볼 수 있음
- `hello-world`를 지우고, 디플로이먼트에 적합한 워크로드를 가지는 파드를 만들어보자
- 디플로이먼트를 지우기 위해서는 `kubectl delete deployment <오브젝트명>` 을 실행
- kubectl 커맨드는 명령어를 조합하는 원리가 일관적이여서 외우기 쉬움. 디플로이먼트를 지웠다면, 동시에 레플리카셋도 같이 삭제됨
~~~
$ kubectl get deployment
NAME          READY   UP-TO-DATE   AVAILABLE   AGE
hello-world   0/1     1            0           31m

$ kubectl delete deployment hello-world
deployment.apps "hello-world" deleted
~~~
- 웹 서버 파드를 5개 기동해보자. 하나의 파드에 문제가 발생해도, 디플로이먼트가 파드 개수가 5개가 되도록 유지시켜줌
~~~shell
$ kubectl run webserver --image=nginx --replicas=5
~~~
- ** 위의 명령어 수행시, `replicas` flag가 적용되지 않음  
  다음의 명령어를 수행
~~~shell
$ kubectl create deployment --image=nginx webserver;kubectl scale --replicas=5 deployment/webserver

NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/webserver   5/5     5            5           33s

NAME                             READY   STATUS             RESTARTS         AGE
pod/hello-world                  0/1     CrashLoopBackOff   16 (3m56s ago)   61m
pod/webserver-7c4f9bf7bf-7h5jw   1/1     Running            0                33s
pod/webserver-7c4f9bf7bf-cq88w   1/1     Running            0                33s
pod/webserver-7c4f9bf7bf-h56bx   1/1     Running            0                33s
pod/webserver-7c4f9bf7bf-pzxtl   1/1     Running            0                33s
pod/webserver-7c4f9bf7bf-z9jpx   1/1     Running            0                33s
~~~
- 하나의 웹 서버 파드를 지워보자. 파드가 삭제되자 새로운 파드가 자동으로 만들어지는 것을 확인 가능
~~~shell
$ kubectl delete po webserver-7c4f9bf7bf-cq88w webserver-7c4f9bf7bf-7h5jw

pod "webserver-7c4f9bf7bf-7h5jw" deleted
pod "webserver-7c4f9bf7bf-cq88w" deleted

$ kubectl get deploy,po

NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/webserver   4/5     5            4           106s

NAME                             READY   STATUS              RESTARTS        AGE
pod/hello-world                  0/1     CrashLoopBackOff    16 (5m9s ago)   62m
pod/webserver-7c4f9bf7bf-d8jfb   0/1     ContainerCreating   0               7s
pod/webserver-7c4f9bf7bf-h56bx   1/1     Running             0               106s
pod/webserver-7c4f9bf7bf-pzxtl   1/1     Running             0               106s
pod/webserver-7c4f9bf7bf-rtnnz   1/1     Running             0               7s
pod/webserver-7c4f9bf7bf-z9jpx   1/1     Running             0               106s
~~~
- 파드는 일시적인 존재로 그 자체가 되살아난 것이 아니라, 새로운 파드가 만들어진 것임
- 따라서 컨테이너의 애플리케이션은 기본적으로 stateless 해야함
- 지금까지 만든 오브젝트들(디플로이먼트, 레플리카셋, 파드)을 지우는 방법은 다음과 같음
~~~shell
$ kubectl delete deployment webserver
~~~

## 잡에 의한 파드 실행
- hello-world 컨테이너는 메세지를 출력하고 종료하는 단발성 형태의 워크로드. 이에 적합한 쿠버네티스의 컨트롤러로 잡 컨트롤러가 있음
- `kubectl run`의 옵션으로 `--restart=OnFailure` 를 지정하면, 잡 컨트롤러의 제어하에 파드가 기동됨
- 잡 컨트롤러는 파드가 비정상 종료 하면 재시작하며, 파드가 정상 종료 할 때까지 지정한 횟수만큼 재실행
- 아래 수행 결과는 잡 컨트롤러의 파드 hello-world 가 정상 종료함. `kubectl get all`로 종료된 파드 목록을 출력하거나 잡의 로그를 참조하는 것이 가능
~~~shell
$ kubectl create job hello-world --image=hello-world 
$ kubectl run hello-world --image=hello-world --restart=OnFailure

$ kubectl get pods
NAME                           READY   STATUS             RESTARTS      AGE
hello-world                    0/1     Completed          0             2m5s
hello-world-649b9bfb9c-rw2v2   0/1     CrashLoopBackOff   4 (50s ago)   2m42s

pod/hello-world                  0/1     Completed   0          2m18s
pod/hello-world-bfjc8            0/1     Completed   0          2m25s
job.batch/hello-world   1/1           5s         2m25s
~~~
- 잡 컨트롤러는 컨테이너의 프로세스 종료 코드 값으로 성공과 실패를 판정
- 아래 예시를 보면 job-1은 정상 종료, job-2는 비정상 종료 하도록 셸 스크립트를 사용하고 있음
- job-1은 COMPLETIONS가 1/1이 되어 잡이 수행 완료된 반면 job-2 는 30초가 지나도 0임
- 이때 `kubectl get po`를 실행해 보면 job-2의 파드가 계속 재시작하는 것을 알 수 있음
~~~shell
$ kubectl create job job-0 --image=ubuntu -- /bin/bash -c "exit 0"
$ kubectl get jobs

$ kubectl create job job-1 --image=ubuntu -- /bin/bash -c "exit 1" 
$ kubectl get jobs

$ kubectl get po 
~~~

