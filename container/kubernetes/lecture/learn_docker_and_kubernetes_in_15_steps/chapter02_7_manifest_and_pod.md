# 매니페스트와 파드
- 매니페스트 작성하여 파드를 작성하는 방법을 알아보고 구체적인 동작을 확인해보자
- <b>매니페스트란, 쿠버네티스의 오브젝트를 생성하기 위한 메타 정보를 YAML이나 JSON으로 기술한 파일</b>
- 실제 파드를 단독으로 기동하는 매니페스트를 작성하는 경우는 많지 않으며, 보통 컨트롤러에 대한 매니페스트를 작성하는데 이때 파드에 대한 정보를 기술하는 부분이 포함. 이를 <b>파드 탬플릿</b>이라고 함
- 파드의 매니페스트를 기술하는 방법을 알고 있으면 컨트롤러를 사용할 때 도움이 됨. 그래서 이번 스텝에서는 파드를 단독으로 기동할 때 사용하는 매니페스트 기술법에 대해서 알아볼 것임

## 매니페스트 작성법
- 다음의 매니페스트는 YAML과 JSON 형식으로 기술한 것임.  
  `kubectl run nginx --image=nginx:latest --restart=Never`를 실행한 것과 같음
- 보통 YAML이 더 간결하기때문에 더 많이 사용됨
~~~YAML
apiVersion: v1
kind: Pod
metadata: 
  name: nginx
spec:
  containers:
  - name: nginx
    iamge: nginx:latest
~~~
- 매니페스트를 작성하는 방법은 쿠버네티스 API 레퍼런스에 기재된 내용과 밀접하게 연관되어 있음  
  https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.23/
- 이 링크에 기술된 내용은 쿠버네티스의 소스 코드로부터 생성된 API 사양
- URL의 끝에 있는 숫자 23는 API의 마이너 버전 번호이므로 이를 변경하면 다른 버전의 레퍼런스를 확인해 볼 수 있음

### 파드 API(Pod v1 core)
|     |     |
| --- | --- |
| 주요 항목 | 설명  |
| apiVersion | v1 설정 |
| kind | Pod 설정 |
| metadata | 파드의 이름을 지정하는 name은 필수 항목이며, 네임스페이스 내에서 유일한 이름이어야 함 |
| spec | 파드의 사양을 기술. 표 2 참고 |

### 파드의 사양(PodSpec v1 core)
- 파드의 사양 표에서 containers 가 복수형인 것에 주목해야 함. 이것은 여러 개의 컨테이너를 기술할 수 있음을 의미
- `initContainers`와 `volumes`도 마찬가지로 여러 개 정의할 수 있음  
  아래의 컨테이너 설정은 자주 사용하는 것 위주로 작성한 것임. 자세한 내용은 API 참고

|     |     |
| --- | --- |
| 주요 항목 | 설명  |
| containers | 컨테이너 사양을 배열로 기술. 표 3 참고 |
| initcontainers | 초기화 전용 컨테이너의 사양을 배열로 기술<br>내요은 containers와 동일. 표 3 참고 |
| nodeSelector | 파드가 배포될 노드의 레이블을 지정 |
| volumes | 파드 내 컨테이너 간에 공유할 수 있는 볼륨을 설정 |


### 컨테이너 설정(Container v1 core)
|     |     |
| --- | --- |
| 주요 항목 | 설명  |
| image | 컨테이너 사양을 배열로 기술. 표 3 참고 |
| name | 초기화 전용 컨테이너의 사양을 배열로 기술<br>내요은 containers와 동일. 표 3 참고 |
| livenessProbe | 파드가 배포될 노드의 레이블을 지정 |
| readinessProbe | 파드 내 컨테이너 간에 공유할 수 있는 볼륨을 설정 |
| ports | 외부로부터 요청을 전달받기 위한 포트 목록 |
| resources | CPU와 메모리 요구량과 상한치 |
| volumeMounts | 파드에 정의한 볼륨을 컨테이너의 파일 시스템에 마운트하는 설정.<br>복수 개 기술 가능 |
| command | 컨테이너 기동 시 실행할 커맨드<br>args가 인자로 적용 |
| args | command의 실행 인자 |
| env | 컨테이너 내에 환경 변수를 설정 |

## 매니페스트 적용 방법
- 매니페스트 파일을 K8s 클러스터에 전송하여 오브젝트를 만드는 방법은 다음과 같음
~~~shell
$ kubectl apply -f 매니페스트_파일명
~~~
- 매니페스트를 통해 오브젝트를 만드는 kubectl의 서브 커맨드로는 `create`와 `apply`가 있는데, 동일한 명의 오브젝트가 있는 경우, `apply`는 매니페스트의 내용에 따라 오브젝트의 스펙을 변경하는 한편, `create`는 에러를 반환함 
- 다음은 K8s의 오브젝트를 지우기 위한 명령어  
  `-f` 다음에 파일명 대신 URL을 쓰면 깃헙에서의 YAML 파일을 그대로 사용 가능
~~~shell
$ kubectl delete -f delete 파일명
~~~

## 파드의 동작 확인
- 아래 명령어를 통해 nginx 파드를 가동
~~~shell
$ kubectl apply -f nginx-pod.yml

$ kubectl get pods
# 결과
nginx     1/1     Running     0          106s
~~~
- 이 nginx 파드는 백그라운드로 돌면서 클러스터 네트워크의 TCP 80번 포트에서 요청을 대기
- 클러스터 네트워크는 K8s 클러스터를 구성하는 노드 간의 통신을 위한 패쇄형 네트워크. 다른 말로 파드 네트워크라고도 함
- <b>클러스터 네트워크에서 오픈한 포트는 K8s 클러스터를 호스팅하는 컴퓨터에서도 접근할 수 없음</b>
- 파드의 클러스터 네트워크의 IP 주소를 확인하고 싶은 경우에는 아래 예처럼 `-o wide` 옵션을 추가하면 됨 
- 여기서 얻은 IP 주소에 대해 curl로 접속을 시도해 보면 다음과 같이 타임아웃이 될 뿐임
~~~shell
## 파드의 IP 주소와 파드가 배포된 노드 표시
$ kubectl get po nginx -o wide

NAME    READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
nginx   1/1     Running   0          10m   172.17.0.3   minikube   <none>           <none>

# IP 주소를 지정해서 접근 테스트
# --> 해당 테스트를 vagrant 가상 환경에서 실행하면 동일 클러스터 내 이므로, 당연히 연결이 됨
# 클러스터 외부(host server)에서 접근하면 접근이 안됨

# host server(내 local comp)
curl -m 3 http://172.17.0.3/
curl: (7) Failed to connect to 172.17.0.3 port 80: Operation timed out
~~~
- K8s 클러스터 외부에서 클러스터 네트워크에 있는 파드의 포트에 접근하기 위해서는 서비스를 이용해야 함
- 이에 대해서는 스탭 09에서 다룸. 여기서는 실행 예 K8s 클러스터 내에 별도의 대화형 파드를 기동해서 nginx 파드에 접근해 볼 것임
~~~shell
# (1) 대화형 파드 기동
$ kubectl run busybox --image=busybox --restart=Never --rm -it sh

# (2) BusyBox에 있는 wget 명령어로 URL 접근 테스트
$ wget -q -O - http://172.17.0.4/
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
~~~
- 학습 환경 2처럼 멀티 노드로 구성된 환경에서도 노드의 경계를 넘어서 출력된 IP를 기반으로 파드 간 통신이 가능  
  다음의 `busybox`와 `nginx` 의 목록 출력 결과를 보면, IP 주소가 다른 것을 확인 가능
~~~shell
NAME      READY   STATUS    RESTARTS   AGE    IP           NODE       NOMINATED NODE   READINESS GATES
busybox   1/1     Running   0          119s   172.17.0.4   minikube   <none>           <none>
nginx     1/1     Running   0          11m    172.17.0.3   minikube   <none>           <none>
~~~
- 파드 간의 통신을 그림으로 표현하면 그림 1과 같음. 터미널에서 busybox 의 파드에 접속하여 wget 커맨드를 실행하여 nginx 파드의 HTTP TCP/80에 접속하고 있음

![img](https://github.com/koni114/TIL/blob/master/docker/img/docker_21.png)

- 정리하자면, 파드는 클러스터 네트워크 상의 IP 주소를 가지며 이 주소를 바탕으로 파드와 파드가 서로 통신할 수 있음
- 여기서 이용한 BusyBox는 도커 허브에 등록된 공식 이미지 중 하나
- 약 1MB밖에 되지 않는 이미지 안에 유용한 명령어들이 다수 포함되어 있어 임베디드 리눅스의 맥가이버 칼이라고 부름

## 파드의 헬스 체크 기능
- 파드의 컨테이너에는 애플리케이션이 정상적으로 기동 중인지 확인하는 기능, 즉 헬스 체크 기능을 설정할 수 있어, 이상이 감지되면 컨테이너를 강제 종료하고 재시작할 수 있음
- 이 기능을 기존의 시스템과 비교하면서 동작을 확인해보자
- 여러 개의 웹 서버의 앞단에서 요청을 받아드리는 로드벨런서는 주기적으로 요청을 보내 각 서버의 애플리케이션이 정상적으로 동작 중인지를 확인
- 이때 내부 에러(HTTP 상태 500)가 반복해서 반환하면 해당 서버로의 전송을 중지하고, 나머지 서버들에게만 요청을 전송하게 됨
- 이렇게 하여 서버 장애가 유저에 미치는 영향을 줄임
- 한편, 쿠버네티스에서는 노드에 상주하는 <b>kubelet</b>이 컨테이너의 헬스 체크를 담당

![img](https://github.com/koni114/TIL/blob/master/docker/img/docker_22.png)

- kubelet의 헬스 체크는 다음 두 종류의 프로브를 사용하여 실행 중인 파드의 컨테이너를 검사함
  - 활성 프로브(Liveness Probe)
    - 컨테이너의 애플리케이션이 정상적으로 실행 중인 것을 검사 
    - 검사에 실패하면 파드상의 컨테이너를 강제로 종료하고 재시작함
    - 이 기능을 사용하기 위해서는 매니페스트에 명시적으로 설정해야 함
  - 준비 상태 프로브 (Readiness Probe) 
    - 컨테이너의 애플리케이션이 요청을 받을 준비가 되었는지 아닌지를 검사
    - 검사에 실패하면 서비스에 의한 요청 트래픽 전송을 중지
    - 파드가 기동하고 나서 준비가 될 때까지 전송되지 않기 위해 사용
    - 이 기능을 사용하기 위해서는 매니페스트에 명시적으로 설정해야 함
 - 로드벨런서와 마찬가지로 HTTP로 헬스 체크를 하는 경우에는 예를 들어 http://파드IP주소:포트번호/healthz 를 정기적으로 확인하도록 하고 서버에는 이에 대한 적절한 응답을 반환하도록 구현
 - 그리고 파드의 컨테이너에는 프로브에 대응하는 핸들러를 구현해야 함
 - 이 핸들러는 컨테이너의 특성에 따라 다음 세 가지중 하나를 선택할 수 있음 

|     |     |
| --- | --- |
| 핸들러 명칭 | 설명  |
| exec | 컨테이너 내 커맨드를 실행. Exit 코드 0으로 종료하면 진단 결과는 성공으로 간주되며,<br>그 외의 값은 실패로 간주 |
| tcpSocket | 지정한 TCP 포트번호로 연결할 수 있다면, 진단 결과는 성공으로 간주 |
| httpGet | 지정한 포트와 경로로 HTTP GET 요청이 정기적으로 실행<br>HTTP 상태 코드가 200 이상 400 미만이면 성공으로 간주. 그 외에는 실패로 간주<br>지정 포트가 열려 있지 않은 경우도 실패로 간주 |

- 헬스 체크를 기술하는 방법을 아래 파일을 통해 알아보자
- 여기서 (1)의 이미지 애플리케이션에는 프로브에 대응하는 핸들러가 구현되어 있음
- 이는 Node.js로 간단하게 구현했는데 뒤에서 살펴볼 것임. 그리고 (2) 활성 프로브와 (3) 준비 상태 프로브에 관해 기술함
- 각각의 주요 항목은 아래 표에 정리함
~~~YAML
apiVersion: v1
kind: Pod
metadata:
  name: webapl
spec:
  containers:
  - name: webapl
    image: maho/webapl:0.1 # (1) 핸들러가 구현된 이미지
    livenessProbe:         # (2) 활성 프로브에 대한 핸들러 설정 
      httpGet: 
        path: /healthz
        port: 3000
      initialDelaySeconds: 3  # 처음으로 검사를 수행하기 전의 대기 시간
      periodSeconds: 5        # 검사 간격
    readinessProbe:           # (3) 준비 상태 프로브에 대한 핸들러 설정
      httpGet:
        path: /ready
        port: 3000
      initialDelaySeconds: 15
      periodSeconds: 6
~~~
- 기본 설정으로는 활성 프로브가 연속해서 3번 실패하면 kubelet 이 컨테이너를 강제 종료하고 재기동함
- 컨테이너가 재시작되면 컨테이너에 있었던 정보들은 별도로 저장하지 않는 이상 지워짐

### 프로브 대응 핸들러 기술 예
| 주요 항목 | 설명  |
| --- | --- |
| httpGet | HTTP 핸들러 |
| path<br>port | 핸들러의 경로<br>HTTP 서버의 포트번호 |
| tcpSocket | TCP 포트 번호 핸들러 |
| port | 감시 대상의 포트번호 |
| exec | 컨테이너 내의 커맨드 실행 핸들러 |
| command | 컨테이너의 커맨드를 배열로 기술<br>ex)<br>livenessProbe:<br>  exec:<br>    command:<br>    \- cat<br>    \- /tmp/healthy |
| initialDelaySeconds | 프로브 검사 시작 전 대기 시간 |
| periodSeconds | 검사 간격 |

- 구체적인 파라미터는 API 레퍼런스에 기재되어 있음  
  예를 들어, 시행 횟수나 타임아웃 등을 설정할 수 있음
- 헬스 체크는 <b>파드가 스케줄된 노드에 있는 kubelet이 수행함</b>. 노드의 하드웨어 장애 시에는 kubelet도 정지되기 때문에 노드의 장애 대책으로는 적합하지 않음
- 한편 컨트롤러의 관리 대상은 파드. 따라서 노드의 장애 대책을 위해서는 헬스 체크가 아닌 컨트롤러를 사용해야 함
- 이러한 용도로 자주 사용되는 컨트롤러가 디플로이먼트와 스테이트풀셋임
- 이제 실제 컨테이너를 기동하여 프로브의 동작을 확인해보자.  
  먼저 컨테이너를 빌드하기 위한 디렉터리를 만들고 다음 세 파일을 배치함.  
  아래 예에서 나오는 webapl 이하의 파일들은 잠시 뒤에 설명
~~~shell
# 헬스 체크 확인을 위한 파일 목록
$ tree hc-probe
hc-probe
|-- webapl
    |-- Dcokerfile
    |-- package.json
    |-- webapl.js
|-- webapl-pod.yml
# 1 directory, 4 files
~~~
- 아래 예에서는 파일 3에서 지정한 이미지 `image:maho/webapl:0.1`을 빌드해서 도커 허브 레지스트리에 등록하고 있음
~~~shell
$ docker build --tag koni114/webapl:0.1 . 
$ docker login
$ docker push koni114/webapl:0.1

# 결과
The push refers to repository [docker.io/koni114/webapl]
76b29987ef3f: Pushed 
1b79b8466154: Pushed 
345490e0c362: Pushed 
349964a5fc75: Pushing [=================================================> ]   51.4MB/51.74MB
ff768a1413ba: Pushed 
349964a5fc75: Pushed 

0.1: digest: sha256:1fe6080b358e13282088861fa52b982056fab216059f4f16708c014bbde3fd23 size: 1365
~~~
- 실행 예 9에서는 파드를 배포해서 헬스 체크의 프로브가 동작하는 것을 확인하고 있음  
  실제 운영 환경에서는 컨트롤러를 사용하지 않고 파드만을 배포하는 경우는 거의 없음  
  여기서는 프로브의 동작을 확인하기 위해 컨트롤러를 사용하지 않음
~~~shell
# 디렉터리를 이동하여 매니페스트를 적용
$ cd .. 
$ kubectl apply -f webapl-pod.yml

## pod 의 STATUS가 Running 이 될 떄까지 확인
#  READY 0/1 -> 1/1 이 됨. 처음에 0인 이유는 
# readinessProbe 가 아직 성공하지 못하여 READY 상태가 아닌 것으로 판정했기 때문

$ kubectl logs webapl -f

GET /healthz 200    ## LivenessProb에 의한 엑세스
GET /healthz 200    ## 5초 간격으로 요청
GET /healthz 200
GET /ready 500      ## 20초가 지나기 전에는 /ready가 500을 반환
GET /healthz 200
GET /ready 200      ## 6초 후 ReadinessProbe에 성공하여 READY 1/1 로 준비 완료
GET /healthz 200
GET /healthz 200
GET /ready 200
GET /healthz 200
...
~~~
- 다음은 `kubectl describe pod [pod명]` 명령어를 사용해 파드의 상세 정보 확인
~~~shell
$ kubectl describe pod [pod명]

  webapl:
    Container ID:   docker://01d077cbc6d2316ae5074be08fb52fa3fdacb453d5b07f0b5a01173bed8c4614
    Image:          maho/webapl:0.1
    Image ID:       docker-pullable://maho/webapl@sha256:2d90f1ef4d0b4b0dcf3372289e7552ef23de3a1910d747b3d42ee5e46b96d57a
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Sun, 27 Mar 2022 12:07:08 +0000
    Last State:     Terminated
      Reason:       Error
      Exit Code:    137
      Started:      Sun, 27 Mar 2022 12:05:42 +0000
      Finished:     Sun, 27 Mar 2022 12:07:07 +0000
    Ready:          True
    Restart Count:  2
    Liveness:       http-get http://:3000/healthz delay=3s timeout=1s period=5s #success=1 #failure=3
    Readiness:      http-get http://:3000/ready delay=15s timeout=1s period=6s #success=1 #failure=3
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-wfdhc (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  kube-api-access-wfdhc:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute for 300s
                             node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type     Reason     Age                  From               Message
  ----     ------     ----                 ----               -------
  Normal   Scheduled  <unknown>                               Successfully assigned default/webapl to minikube
  Warning  Unhealthy  59s (x6 over 2m34s)  kubelet, minikube  Liveness probe failed: HTTP probe failed with statuscode: 500
  Normal   Killing    59s (x2 over 2m24s)  kubelet, minikube  Container webapl failed liveness probe, will be restarted
  Normal   Pulled     29s (x3 over 3m18s)  kubelet, minikube  Container image "maho/webapl:0.1" already present on machine
  Normal   Created    29s (x3 over 3m18s)  kubelet, minikube  Created container webapl
  Normal   Started    28s (x3 over 3m18s)  kubelet, minikube  Started container webapl
  Warning  Unhealthy  13s (x3 over 3m1s)   kubelet, minikube  Readiness probe failed: HTTP probe failed with statuscode: 500
~~~
- Events 에서 Age는 해당 이벤트가 발생하고 지난 시간을 의미
- Age 24s 지점에서 Liveness probe failed는 애플리케잉션 기동이 완료되지 않아 타임아웃이 발생
- 이후 기동이 완료되어 probe에 성공하지만 로그에는 남지 않음
- 애플리케이션에서 20초 전에는 HTTP 500 을 반환하도롥 구현되어 있어, Age 20s 시점에서 Readiness probe에 실패한 기록이 남아 있음
- 6초 후 probe에 성공하지만 로그에는 남지 않음
- 활성 프로브가 반복해서 실패하면, kubelet은 새로운 컨테이너를 기동하고 실패를 반복하는 컨테이너를 강제 종료함. 
  예를 들어 애플리케이션의 로그에  `/healthz`가 3회 실패(HTTP 500) 발생한 경우
  연속 3회 `HTTP 500`이 출력된 시점에서 파드의 상세 정보를 출력해보면 kubelet이 컨테이너를 교체함
- 프로브를 통한 파드의 헬스 체크 동작을 알아보았는데, 여기서 사용된 Node.js 애플리케이션의 코드는 다음과 같음
  - `webapi.js` : Node.js 애플리케이션
  - `package.json` : Node.js의 의존 라이브러리를 기재한 패키지 파일
  - `Dockerfile`: 이미지 빌드 파일
~~~js
t express = require('express')
const app = express()
var start = Date.now()

// Liveness 프로브 핸들러
// 기동 후 40초가 되면, 500 에러를 반환한다.
// 그 전까지는 HTTP 200 OK를 반환한다.
// 즉, 40초가 되면, Liveness프로브가 실패하여 컨테이너가 재기동한다. 
//
app.get('/healthz', function(request, response) {
    var msec = Date.now() - start
    var code = 200
    if (msec > 40000 ) {
	code = 500
    }
    console.log('GET /healthz ' + code)
    response.status(code).send('OK')
})

// Rediness 프로브 핸들러
// 애플리케이션의 초기화 시간으로 
// 기동 후 20초 지나고 나서부터 HTTP 200을 반환한다. 
// 그 전까지는 HTTPS 200 OK를 반환한다.
app.get('/ready', function(request, response) {
    var msec = Date.now() - start
    var code = 500
    if (msec > 20000 ) {
	code = 200
    }
    console.log('GET /ready ' + code)
    response.status(code).send('OK')
})

// 첫 화면
//
app.get('/', function(request, response) {
    console.log('GET /')
    response.send('Hello from Node.js')
})

// 서버 포트 번호
//
app.listen(3000);
~~~
~~~JSON
{
  "name": "webapl",
  "version": "1.0.0",
  "description": "",
  "main": "webapl.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",
  "license": "ISC",
  "dependencies": {
    "express": "^4.16.3"
  }
}
~~~
~~~Dockerfile
## Alpine Linux  https://hub.docker.com/_/alpine/
FROM alpine:latest

## Node.js  https://pkgs.alpinelinux.org/package/edge/main/x86_64/nodejs
RUN apk update && apk add --no-cache nodejs npm

## 의존 모듈
WORKDIR /
ADD ./package.json /
RUN npm install
ADD ./webapl.js /

## 애플리케이션 기동
CMD node /webapl.js
~~~

## 초기화 전용 컨테이너
- 파드 내에 초기화만을 담당하는 컨테이너를 설정할 수도 있음
- 그러면 초기화만을 수행하는 컨테이너와 요청을 처리하는 컨테이너를 별도로 개발하여 각각 재사용 가능
- 예를 들어, 스토리지를 마운트할 때 스토리지 안에 새로운 디렉터리를 만들고, 소유자를 변경한 후 데이터를 저장하는 것과 같은 초기화 처리를 전담하게 할 수 있음
- 다음 아래의 yaml file에서 중간에 나오는 initContainers 에서 초기화 전용 컨테이너를 설정하고 있음
- 23번째 줄을 보면 초기화 전용 컨테이너가 공유 볼륨을 `/mnt` 에 마운트하고, 21번째 줄의 명령어로 디렉터리 `/mnt/html`을 만들고 소유자를 변경하고 있음
- 이 컨테이너는 명령어를 실행하고 바로 종료함. 그 후 메인 컨테이너가 기동하여 공유 볼륨을 마운트함
~~~YAML
# init-sample.yml
apiVersion: v1
kind: Pod
metadata:
  name: init-sample
spec:
  containers:
  - name: main           # 메인 컨테이너
    image: ubuntu
    command: ["/bin/sh"]
    args: [ "-c", "tail -f /dev/null"]
    volumeMounts:
    - mountPath: /docs   # 공유 볼륨 마운트 경로
      name: data-vol
      readOnly: false

  initContainers:        # 메인 컨테이너 실행 전에 초기화 전용 컨테이너를 기동 
  - name: init
    image: alpine
    ## 공유 볼륨에 디렉터리를 작성하고, 소유를 변경
    command: ["/bin/sh"]
    args: [ "-c", "mkdir /mnt/html; chown 33:33 /mnt/html" ]
    volumeMounts:
    - mountPath: /mnt    # 공유 볼륨 마운트 경로 
      name: data-vol
      readOnly: false

  volumes:               # 파드의 공유 볼륨
  - name: data-vol
    emptyDir: {}
~~~
- 아래 예시는 위의 파일인 매니페스트를 적용하고 있음. 그래서 초기화 전용 컨테이너에 의해 초기화된 볼륨을 메인 컨테이너에서 확인하고 있음
~~~shell
$ kubectl apply -f init-sample.yml
$ kubectl get po
$ kubectl exec -it init-sample -c main sh

# ls -al /docs/ 
total 12
drwxrwxrwx 3 root     root     4096 Mar 27 12:38 .
drwxr-xr-x 1 root     root     4096 Mar 27 12:38 ..
drwxr-xr-x 2 www-data www-data 4096 Mar 27 12:38 html
~~~

## 사이드카 패턴
- 이번에는 하나의 파드 안에 여러 개의 컨테이너를 동시에 실행시키는 패턴에 대해 살펴볼 것임
- 이는 파드라는 이름의 유래가 되는 기능이기도 함
- 앞서 살펴본 것은 초기화 전용 컨테이너가 처리를 완료하면 서비스 전용 컨테이너가 시작하는 구성 패턴이였음
- 이번에 살펴볼 패턴은 파드 내부에 있는 여러 개의 컨테이너가 동시에 시작함  
  어떠한 경우에 이러한 패턴이 사용될까? 
- 다음의 그림에서는 웹 서버 컨테이너와 최신 콘텐츠를 깃헙에서 다운받는 컨테이너가 하나의 파드에 묶여 있음  
  이러한 조합 패넡을 사이드카라고 함 

![img](https://github.com/koni114/TIL/blob/master/docker/img/docker_23.png)

- <b>사이드카 패턴의 장점은 여러 개의 컨테이너를 조합하여 사용함으로써 컨테이너의 재사용성이 높아지고, 생산성이 높아짐</b>
- 매번 필요에 맞는 컨테이너를 만드는 것이 아니라, 전에 만든 컨테이너를 재활용할 수 있어 단기간에 커다란 성과를 얻을 수 있음
- 위의 그림에서 nginx는 도커 공식 이미지이고, 이에 contents-clonet 이라는 사이드카 컨테이너를 개발하여 조합함
- 이 컨테이너는 깃헙으로부터 HTML을 정기적으로 다운받아서 최신 콘텐츠를 보관
- 이러한 컨테이너는 다른 애플리케이션에서도 활용할 수 있어 범용성이 높음 
- 또한 환경 변수로 콘텐츠를 다운받는 URL를 지정하면 재사용성이 더욱 높아짐
- 웹 서버와 contents-cloner를 조합하면 콘텐츠 개발자가 git push를 실행하는 것만으로 웹 서버의 콘텐츠를 업데이트할 수 있게 됨
- 그리고 공유 저장소를 사용하는 대신 각 노드의 저장 공간을 사용하기 때문에 성능에 이점을 가짐
- 이 때 <b>파드 안의 컨테이너별로 CPU 사용 시간을 제한하는 것이 가능</b>   
 예를 들면, 웹 서버의 응답 시간을 우선하고 남은 CPU 자원으로 HTML 컨텐츠를 다운로드하는 것이 가능
- `contents-cloner`를 셸 스크립트로 개발해보자. `webserver.yml`은 웹 서버와 contents-cloner를 사이드카 패턴으로 조합한 파드를 실행하기 위한 매니페스트임
~~~shell
# contents-cloner를 위한 디렉터리와 파일
sidecar
|-- Dockerfile
|-- contents-cloner
|-- webserver.yml
~~~
- 다음의 파일은 `contents-cloner`의 기능을 담당하는 셸 스크립트
- 이 코드는 환경 변수 `CONTENTS_SOURCE_URL`에 설정된 URL에 60초 간격으로 갱신 여부를 확인하여 다운로드 받음
- 갱신 여부를 확인하는 것과 다운로드 하는 기능은 git 명령어의 기능을 사용하고 있음
- 처음에는 `git clone`으로 모든 컨텐츠를 다운로드 받고, 이후에는 `git pull`로 변경점을 다운받음  
  여기서 한 걸음 나아간다면 앞서 살펴본 초기화 전용 컨테이너와 준비 상태 프로브 기능을 사용하여 `git clone`이 완료된 후부터 웹 서버가 요청을 받게 할 수도 있음
- 여기서는 해당 설정을 생략함
~~~shell
#!/bin/bash
# 최신 Web 데이터를 GitHub로부터 취득 

# 환경변수가 설정되어 있지 않으면 에러 종료
if [ -z $CONTENTS_SOURCE_URL ]; then
   exit 1
fi

# 처음에는 GitHub에서 클론 
git clone $CONTENTS_SOURCE_URL /data

# 이후에는 1준 간격으로 git pull을 수행
cd /data
while true
do
   date
   sleep 60
   git pull
done
~~~
- 이어서 아래 Dockerfile은 위 셸 스크립트를 바탕으로 이미지를 만듬
- 베이스 이미지로 ubuntu:16.04 공식 이미지를 사용하고 있음  
  컨테이너를 고속으로 가동하고 싶은 경우에는 더욱 작은 이미지를 사용하는 것이 좋음
- 아래 파일에서 사용한 ubuntu:16.04의 이미지의 크기는 120MB 정도인 반면 18.04는 65MB 정도로 반으로 줄었음
- Alpine의 크기는 6MB에 불과함. 하지만 애플리케이션에 필요한 패키지를 추가하다 보면 비슷한 사이즈가 되기도 함
~~~Dockerfile
## Contents Cloner Image
FROM ubuntu:16.04
RUN apt-get update && apt-get install -y git 
COPY ./contents-cloner /contents-cloner
RUN chmod a+x /contents-cloner
WORKDIR /
CMD ["/contents-cloner"]
~~~

