# chapter03 쿠버네티스의 기본
## 아키텍처
![img](https://github.com/koni114/TIL/blob/master/docker/img/docker_15.png)

- 다음은 쿠버네티스 업스트림의 기본 구성. 퍼블릭 클라우드의 쿠버네티스 관리 서비스에는 이외에 추가적인 컴포넌트들이 있지만, 업스트림의 핵심 기능이 가장 중점이 됨
- 다음은 멀티 노드 K8s에서 마스터를 포함한 모든 노드에서 동작하는 파드의 목록을 출력한 결과
~~~shell
$ kubectl get pods --all-namespaces --sort-by=.spec.nodeName -o=custom-columns=NODE:.spec.nodeName,NAME:.metadata.name,IMAGE:.spec.containers[0].image
~~~
![img](https://github.com/koni114/TIL/blob/master/docker/img/docker_10.png)

- `NODE`: 각 노드의 역할을 의미 제어를 담당하는 master와 실행을 담당하는 node1, node2가 존재
- `NAME`: 컨테이너의 실행 단위인 파드의 이름. 네임스페이스(Namespace) 내에서 유일한 이름이 되도록 해시 문자열이 추가로 붙기도 함
- `IMAGE`: 컨테이너의 이미지와 태그
- 앞의 파드의 목록들은 업스트림 쿠버네티스에서 실행한 결과임. 퍼블릭 클라우드의 쿠버네티스 관리 서비스에서 실행해 보면 마스터에서 돌아가는 파드는 표시되지 않고, 각 업체가 독자적으로 추가한 파드도 있어 다소 다른 결과를 확인할 수 있지만, 코어는 동일
- 미니쿠베(minikube)에서 실행하는 경우, 하나의 가상 서버에서 동작하고 있기 때문에 노드가 전부 동일
- 또한 위에서 표시되는 것은 '파드'라 불리는 컨테이너에서 실행되는 것이기 때문에 리눅스 프로세스로 동작하는 부분은 포함되지 않음

### 쿠버네티스를 구성하는 기본 컴포넌트와 플러그인
| 구성요소 | 개요  |
| --- | --- |
| kubectl | k8s 클러스터를 조작하기 위한 도구로 가장 빈번하게 이용되는 커맨드 라인 인터페이스 |
| kube-apiserver | kubectl 등의 API 클라이언트로부터 오는 REST 요청을 검증하고, API 오브젝트를 구성하고 상태를 보고함 |
| kube-scheduler | 쿠버네티스의 기본 스케줄러, 새로 생성된 모든 파드에 대해 실행할 최적의 노드를 선택<br>스케줄러는 파드가 실행 가능한 노드를 찾은 다음 점수를 계산하여 가장 점수가 높은 노드를 선택 |
| kube-controller-manager | 컨트롤러를 구동하는 마스터상의 컴포넌트 |
| cloud--controller-manager | API를 통해서 클라우드 서비스와 연계하는 컨트롤러로, 클라우드 업체에서 개발 |
| etcd | K8s 클러스터의 모든 관리 데이터는 etcd에 저장됨. 이 etcd는 CoreOS가 개발한 분산 키/값 저장소로 신뢰성이 요구되는 핵심 데이터의 저장 및 접근을 위해 설계됨 |
| kubelet | kubelet는 각 노드에서 다음과 같은 역할 수행<br>\- 파드의 컨테이너 실행<br>\- 파드와 노드의 상태를 API 서버에 보고<br>\- 컨테이너의 동작을 확인하는 프로브 실행<br>\- 내장된 cAdvisor를 통해 매트릭 수집 및 공개 |
| kube-floxy | kube-floxy는 각 노드에서 동작하며 로드밸런싱 기능 제공<br>\- 서비스와 파드의 변경을 감지하여 최신 상태로 유지<br>\- iptables 규칙을 관리<br>\- 서비스명과 ClusterIP를 내부 DNS에 등록 |
| coredns | 파드가 서비스 이름으로부터 IP 주소를 얻기 위해 사용됨.<br>버전 1.11부터, kube-dns 대신 coredns가 사용. <br>이전의 kube-dns가 부족했던 신뢰성, 보안성, 유연성이 coredns에서 개선됨<br>CoreDNS 프로젝트는 CNCF가 관리 |

### 애드온 컴포넌트
| 구성요소 | 개요  |
| --- | --- |
| kube-flannel | 모든 노드에서 실행되어 여러 노드 사이의 IPv4 네트워크를 제공<br>이에 따라 컨테이너(파드)는 K8s 클러스터 내부에서 사용되는 IP 주소를 바탕으로 다른 노드에 있는 파드와 통신 가능 |
| calico-kube-controllers | calico를 위한 컨트롤러, 데이터 스토어로서 etcd를 이용하기 위해 사용 |
| calico-node | 모든 노드에서 실행되어 노드 간 파드의 통신, 라우팅, 네트워크 접근 관리 기능을 제공 |
| kubernetes-dashboard | Web 대시보드 |
| metric-server | K8s 클러스터 전체로부터 매트릭을 수집 |

## 참고: 멀티 노드 k8s 클러스터를 PC에 구축
- 학습 환경 2에서는 CNCF의 쿠버네티스 프로젝트가 배포하는 업스트림 코드를 사용하여 PC에서도 동작하는 소규모 멀티 노드 쿠버네티스 클러스터 환경을 구축
- 가상 환경 구축은 `Vagrant`, `Ansible` 사용. 이번 절에서 사용할 코드들은 github 저장소에 저장되어 있음
- 다음 그림은 구성할 환경의 소프트웨어 스택. 자동화 도구(Vagrant, Ansible)에 의해 음영 부분에 해당되는 소프트웨어들이 자동으로 설치됨

![img](https://github.com/koni114/TIL/blob/master/docker/img/docker_09.png)

- 다음은 표 1에 PC 환경, 표 2에 설치할 소프트웨어, 표 3에 도커와 쿠버네티스의 버전, 표 4에는 가상 NFS 서버를 설치하기 위해 필요한 스펙 정리. 

### 표1
|     |     |
| --- | --- |
| 필요 항목 | 조건  |
| PC 하드웨어 | Windows PC 또는 MAC |
| CPU | Intel Core i5 이상, 가상화 지원 기능(VT) |
| RAM(메모리) | 최소 8GB, 추천 16GB |
| 운영체제 | macOS High Sierra 버전 10.13 이상<br>Windows 10 버전 1803 이상 64bit |
| 인터넷 환경 | 브로드밴드 접속 환경(50Mbps 이상) |

### 표2
| OS  | 패키지 | 최저 버전 |
| --- | --- | --- |
| Windows 10 | virtualbox | 5.2.8 |
|     | Vagrant | 2.1.2 |
|     | git | 2.9.0 |
| MacOS | virtualBox | 5.1.10 |
|     | Vagrant | 2.0.3 |
|     | git | 2.17.0 |

### 표3
| 소프트웨어 | 조건  |
| --- | --- |
| 리눅스 | Ubuntu16.04 LTS x86_64 |
| 도커  | Community Edition 버전 18.06.1-ce |
| 쿠버네티스 | 버전 1.14.0 |

### 표4
| 노드  | 항목  | 요건  |
| --- | --- | --- |
| 마스터 | 호스트 이름 | master |
|     | 리눅스 | ubuntu 16.04 LTS x86_64 |
|     | Host Only(Private) IP 주소 | 172.16.20.11 |
|     | vCPU | 2   |
|     | 메모리 | 1GB |
| Node #1 | 호스트 이름 | node1 |
|     | 리눅스 | ubuntu 16.04 LTS x86_64 |
|     | Host Only(Private) IP 주소 | 172.16.20.12 |
|     | vCPU | 1   |
|     | 메모리 | 1GB |
| Node #2 | 호스트 이름 | node2 |
|     | 리눅스 | ubuntu 16.04 LTS x86_64 |
|     | Host Only(Private) IP 주소 | 172.16.20.13 |
|     | vCPU | 1   |
|     | 메모리 | 1GB |


## 용어 정리
- 업스트림
  - 클라이언트나 로컬 컴퓨터에서 서버나 원격 호스트로 데이터를 보내는 것을 말함
  - 업스트림 전송은 여러 형태를 취할 수 있으며, 데이터가 로컬 시스템에서 서버로 전송되는 속도를 업스트림 속도라고 함
  - <b>쿠버네티스에서는 코어 쿠버네티스(포크된 저장소)를 의미함. 보편 생태계, 다른 코드, 서드파티 도구에 의존하는 코어 쿠버네티스 코드베이스를 의미</b>
- NFS
  - Network File System
  - 옛날에는 서버하나만 구축해도 많은 공간을 차지하여 클라이언트들은 여유 공간이 없었음
  - 그래서 개발한 것이 클라이언트가 서버의 공간을 자신의 자원처럼 사용이 가능하게 만듬  
  - 네트워크 상에 연결된 다른 컴퓨터의 하드 디스크를 내 컴퓨터의 하드처럼 사용하는 것
  - 네트워크에 연결된 리눅스끼리 NFS를 통해 파일을 공유 가능
- CNCF ( Cloud Native Computing Foundation )
  - 리눅스 재단 소속의 비영리 단체 