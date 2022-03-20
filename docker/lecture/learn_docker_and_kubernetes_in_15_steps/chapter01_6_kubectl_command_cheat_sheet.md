# kubectl 커맨드 치트 시트
- K8s 클러스터에게 명령을 내릴 때는 kubectl를 사용
- 이번 절에서는 kubectl의 사용법을 치트 시트 형식으로 정리  
- `kubectl` 커맨드는 쿠버네티스 적합성 인증을 통과한 클라우드 서비스와 소프트웨어 제품군에서 모두 이용 가능  
  이 치트 시트는 커맨트 레퍼런스, 리소스 타입, kubectl 공식 치트 시트 등의 자료를 참고하여 정리

## kubectl 커맨드의 기본
- `kubectl` 커맨드의 기본 구조는 다음과 같이 세 부분으로 구성됨  
  - 커맨드로 동작을 지정
  - 리소스 타입과 이름으로 대상이 되는 오브젝트 지정
  - 옵션을 지정
~~~shell
$ kubectl <(1) 커맨드><(2) 리소스 타입> [이름] [(3) 옵셥]
~~~

## 커맨드
- kubectl 의 첫 번째 파라미터로 지정할 수 있는 커맨드 정리
|     |     |     |
| --- | --- | --- |
| 커맨드 | 사용 예 | 개요  |
| get | kubectl get -f &lt;매니페스트 \| 디렉터리&gt;<br>getkubectl get &lt;리소스 타입&gt;<br>getkubectl get &lt;리소스 타입&gt; &lt;이름&gt;<br>getkubectl get &lt;리소스 타입&gt; &lt;이름&gt; &lt;옵션&gt; | get은 지정한 오브젝트의 목록을 한 줄에 하나씩 출력 |
| describe | kubectl describe -f &lt;매니페스트 \| 디렉터리&gt;<br>getkubectl describe &lt;리소스 타입&gt;<br>getkubectl describe &lt;리소스 타입&gt; &lt;이름&gt;<br>getkubectl describe &lt;리소스 타입&gt; &lt;이름&gt; &lt;옵션&gt; | describe의 경우, get보다도 자세한 정보를 출력 |
| apply | kubectl apply -f &lt;매니페스트&gt; | 매니페스트에 기술된 오브젝트가 존재하지 않으면 생성, 존재하면 변경 |
| create | kubectl create -f &lt;파일명&gt; | 매니페스트에 기술된 오브젝트를 생성.<br>이미 있는 경우에는 에러를 반환 |
| delete | kubectl delete -f &lt;파일명&gt; <br>kubectl delete &lt;리소스타입&gt;&lt;이름&gt; | 매니페스트에 기술된 오브젝트 삭제 |
| config | kubectl config get-contexts<br>kubectl config use-context &lt;콘텍스트명&gt; | 접속 대상이 되는 콘텍스트(K8s 클러스터, 네임스페이스, 유저)의 목록을 출력하거나 선택 |
| exec | kubectl exec -it &lt;파드명&gt; \[-c 컨테이너명\] &lt;커맨드&gt; | 컨테이너에 대화형으로 커맨드를 실행<br>파드 내에 컨테이너가 여러 개 있는 경우 \[-c\]를 컨테이너명을 지정<br>컨테이너명은 \`kubectl get describe\` &lt;파드명&gt; 으로 확인 가능 |
| run | kubectl run &lt;이름&gt; --image=&lt;이미지명&gt; | 파드를 실행 |
| logs | kubectl logs &lt;파드명&gt; \[-c 컨테이너명\] | 컨테이너의 로그 표시 |

## 리소스 타입
### 파드 관련 리소스 타입