# Install Kubernetes Cluster on Ubuntu 22.04 with kubeadm

이해관계자: Anonymous
작성일시: December 6, 2022 3:09 PM
최종 편집일시: December 10, 2022 11:07 AM

### kubernetes 설치시, Master / Worker Node 최소 사양

- 메모리: 머신당 2GB 이상의 RAM
- CPU: control plane machine 에 최소 2개 이상의 CPU
- image 를 pull 하기 위하여 인터넷이 연결되어 있거나, private image registry 사용가능
- private 또는 public 으로 모든 machine 들의 network 가 연결되어 있어야 함

### 가이드 환경 구성

- 해당 가이드에서는 컨테이너화된 워크로드가 실행될 master node 1대, worker node 2대로 구성
- HA(High Availability) 구성시, control plane API end-point 는 node 가 3대 필요

| Server Role | Server Hostname | Specs | IP Address |
| --- | --- | --- | --- |
| Master Node | master | 4GB Ram, 2vcpus | 192.168.41.151 |
| Worker Node | worker-1 | 4GB Ram, 2vcpus | 192.168.41.152 |
| Worker Node | worker-2 | 4GB Ram, 2vcpus | 192.168.41.153 |
|  |  |  |  |

### #1) 우분투 서버 업그레이드

```bash
$ sudo apt update
$ sudo apt -y full-upgrade
$ [ -f /var/run/reboot-required ] && sudo reboot -f
```

### #2) kubelet, kubeadm 및 kubectl 설치

- 서버가 재부팅되면 Ubuntu 22.04 용 Kubernetes 리포지토리를 모든 서버에 추가

```bash
$ sudo apt install curl apt-transport-https -y

$ sudo curl -fsSLo /etc/apt/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg

$ curl -fsSL  https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/k8s.gpg
$ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
$ echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

- 그런 다음 필요한 패키지를 설치
    - `apt-mark` : 자동 업데이트를 막기 위함

```bash
$ sudo apt update
$ sudo apt install wget curl vim git kubelet kubeadm kubectl -y
$ sudo apt-mark hold kubelet kubeadm kubectl

# 삭제(참고)
$ sudo apt-get purge kubeadm kubelet kubectl
$ sudo apt autoremove
```

- kubectl의 버전을 확인하여 설치를 확인
    - 아래 같은 경우 kubectl, kubeadm 모두 v1.25.4 임

```bash
$ kubectl version --client && kubeadm version

WARNING: This version information is deprecated and will be replaced with the output from kubectl version --short.  Use --output=yaml|json to get the full version.
Client Version: version.Info{Major:"1", 
													   Minor:"25", 
														 GitVersion:"v1.25.4", 
														 GitCommit:"872a965c6c6526caa949f0c6ac028ef7aff3fb78", 
													   GitTreeState:"clean", 
														 BuildDate:"2022-11-09T13:36:36Z", 
														 GoVersion:"go1.19.3", 
														 Compiler:"gc", 
														 Platform:"linux/amd64"}
Kustomize Version: v4.5.7
	kubeadm version: &version.Info{Major:"1", 
																 Minor:"25", 
																 GitVersion:"v1.25.4", 
																 GitCommit:"872a965c6c6526caa949f0c6ac028ef7aff3fb78", 
																 GitTreeState:"clean", 
																 BuildDate:"2022-11-09T13:35:06Z", 
																 GoVersion:"go1.19.3", 
																 Compiler:"gc", 
																 Platform:"linux/amd64"}
```

### #3) Swap Space 비활성화

- `/proc/swaps` 에서 모든 스왑을 비활성화
    - why? 쿠버네티스의 kubelet 이 이러한 swap 상황을 처리하도록 만들어지지 않았기 때문
    - 쿠버네티스는 Pod 를 생성할 때, 필요한 만큼의 리소스를 할당 받아 사용하는 구조임
    따라서 메모리 Swap 을 고려하지 않고 설계되었기 때문에, 쿠버네티스 클러스터 Node 들은 모두 Swap 메모리를 비활성화 해주어야 함

```bash
$ sudo swapoff -a
```

- free 명령을 실행하여 스왑이 비활성화되었는지 확인

```bash
$ free -h

total        used        free      shared    buff/cache   available
Mem:         62Gi       593Mi        60Gi        69Mi       1.5Gi        61Gi
스왑:         0B          0B          0B
```

- Linux Swap Space 를 영구적으로 비활성화 
`/etc/fstab` 에 **swap.img ~ or swapfile ~**  부분을 주석처리 하면 됨
    - `**fstab` 파일?** 파일 시스템 정보를 저장하고 있으며, 리눅스 부팅시 마운트 정보를 저장하고 있음

```bash
$ sudo vim /etc/fstab
#/swap.img	none	swap	sw	0	 0
```

- 설정이 올바른지 확인(마운트를 제거했으므로, swap 부분에 GB 가 0 으로 나와야 함)

```bash
$ sudo mount -a
$ free -h
```

### #4) 커널 모듈 활성화

- 커널 모듈을 활성화하고 `sysctl` 을 구성함
- sysctl 은 커널의 변수 값을 제어하여 시스템을 최적화 할 수 있는 명령어
    - `overlay` : union mount(계층화된 파일 시스템) storage
    - `br_netfilter` : br 은 bridge 의 약어. 우리가 사용하고 있는 방화벽인 iptables 가 
                                 bridge driver 를 사용하여 통신을 하는 패킷들을 filter 할 수 있도록 하는 녀석
- ipv4, ipv6 network iptable 을 활성화시킴

```bash
# Enable kernel modules
$ sudo modprobe overlay
$ sudo modprobe br_netfilter

# Add some settings to sysctl
# kubernetes.conf file 에 아래와 같은 내용을 추가
$ sudo tee /etc/sysctl.d/kubernetes.conf<<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

# Reload sysctl
sudo sysctl --system
```

### #4) 컨테이너 런타임 설치(마스터 및 작업자 노드)

- Pod 에서 컨테이너를 실행하기 위해 Kubernetes 는 **컨테이너 런타임**을 사용함
지원되는 컨테이너 런타임은 다음과 같음
    - **Docker**
    - **CRI-O**
    - **Containerd**
- **한번에 하나의 런타임을 선택해야 함**

아래 컨테이너 런타임 설치 방법 중 적절한 런타임을 선택하여 사용

**#4-1) Docker Runtime 설치**

- 선택한 컨테이너 런타임이 Docker CE인 경우 아래 단계에 따라 구성하면 됨

```bash
# Add repo and Install packages
$ sudo apt update
$ sudo apt install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
$ sudo apt update
$ sudo apt install -y containerd.io docker-ce docker-ce-cli

# Create required directories
$ sudo mkdir -p /etc/systemd/system/docker.service.d

# Create daemon json config file
$ sudo tee /etc/docker/daemon.json <<EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF

# Start and enable Services
$ sudo systemctl daemon-reload 
$ sudo systemctl restart docker
$ sudo systemctl enable docker

# Configure persistent loading of modules
$ sudo tee /etc/modules-load.d/k8s.conf <<EOF
overlay
br_netfilter
EOF

# Ensure you load modules
$ sudo modprobe overlay
$ sudo modprobe br_netfilter

# Set up required sysctl params
$ sudo tee /etc/sysctl.d/kubernetes.conf<<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF
```

- Docker Engine 의 경우 Shim 인터페이스가 필요
[가이드](https://computingforgeeks.com/install-mirantis-cri-dockerd-as-docker-engine-shim-for-kubernetes/)를 참고하여 Mirantis cri-dockerd 를 설치할 수 있음
- Mirantis-cri-dockerd CRI 소켓 파일 경로는 `/run/cri-dockerd.sock` 이며, Kubernetes 클러스터를 구성할 때 사용함

**#4-2) CRI-O 런타임 설치**

- CRI-O 의 경우 아래 명령을 사용함

```bash
# Configure persistent loading of modules
$ sudo tee /etc/modules-load.d/k8s.conf <<EOF
overlay
br_netfilter
EOF

# Ensure you load modules
sudo modprobe overlay
sudo modprobe br_netfilter

# Set up required sysctl params
sudo tee /etc/sysctl.d/kubernetes.conf<<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF 

# Reload sysctl
$ sudo sysctl --system
$ OS="xUbuntu_22.04"
$ VERSION=1.24

$ echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /" > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
$ echo "deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$VERSION/$OS/ /" > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.list
$ curl -L https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$VERSION/$OS/Release.key | apt-key add - 
$ curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | apt-key add -

# Install CRI-O
$ sudo apt update
$ sudo apt install cri-o cri-o-runc

# Start and enable Service
$ sudo systemctl daemon-reload
$ sudo systemctl restart crio
$ sudo systemctl enable crio
$ systemctl status crio
```

****#4-3) containerd 설치****

- Docker 대신에 containerd 를 사용할 수도 있음. 이는 Docker 엔진 사용자에게 선호되는 방법임
    - `modprobe` : 리눅스 모듈 관리 명령어
    - `apt-key` : 특정 패키지를 인증할 때 사용하는 키를 관리하는 명령어

```bash
# Configure persistent loading of modules
$ sudo tee /etc/modules-load.d/k8s.conf <<EOF
overlay
br_netfilter
EOF

# Load at runtime
$ sudo modprobe overlay
$ sudo modprobe br_netfilter

# Ensure sysctl params are set
$ sudo tee /etc/sysctl.d/kubernetes.conf<<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

# Reload configs
$ sudo sysctl --system

# Install required packages
$ sudo apt install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates

# Add Docker repo
# docker 설치에 필요한 gpg-key 를 추가
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# docker repo 추가
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Install containerd
$ sudo apt update
$ sudo apt install -y containerd.io

# Configure containerd and start service
$ sudo su -
$ mkdir -p /etc/containerd
$ containerd config default>/etc/containerd/config.toml

# restart containerd
$ sudo systemctl restart containerd
$ sudo systemctl enable containerd
$ systemctl status containerd
```

- systemd cgroup driver 를 사용하기 위하여, 
/etc/containerd/config.toml 내에 다음의 부분을 수정

```bash
# config.toml 
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
...
SystemdCgroup = true  # true 로 수정
```

kubeadm 을 사용하는 경우 [kubelet 용 cgroup driver](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#configure-cgroup-driver-used-by-kubelet-on-control-plane-node) 를 수동으로 구성함
(설정하지 않아도 에러가 발생하지 않음)

### #5) 컨트롤 플레인 초기화(master node에서 실행)

**#5-1) 마스터로 사용할 서버에 로그인하고 br_netfilter 모듈이 로드되었는지 확인**

- ** br_netfilter 모듈
    - 이 커널 모듈을 사용하면 브릿지를 통과하는 패킷이 필터링 및 포트 전달을 위해 
    iptables에 의해 처리되고 클러스터의 쿠버네티스 Pod는 서로 통신 가능

```bash
$ lsmod | grep br_netfilter
```

**#5-2) kubelet 서비스를 활성화**
** 실행 한 후 kubelet 상태를 확인해보면 status=1/FAILURE 로 보이지만, 무시하고 다음 단계를 진행

```bash
$ sudo systemctl enable kubelet

● kubelet.service - kubelet: The Kubernetes Node Agent
     Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
    Drop-In: /etc/systemd/system/kubelet.service.d
             └─10-kubeadm.conf
     Active: activating (auto-restart) (Result: exit-code) since Thu 2022-12-08 19:42:56 KST; 9s ago
       Docs: https://kubernetes.io/docs/home/
    Process: 81132 ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS (code=exited, status=>
   **Main PID: 81132 (code=exited, status=1/FAILURE)**
        CPU: 58ms
```

**kubelet 서비스 오류 발생시, 확인 방법**

```dart
$ sudo systemctl enable kubelet
$ **journalctl -xeu kubelet**
```

- etcd(클러스터 데이터베이스) 및 API 서버를 포함하는 컨트롤 플레인 구성 요소를 실행할 머신을 초기화하려고 함

**#5-3) 컨테이너 이미지 가져오기**
→ 만약 노드에 CRI 소켓이 한 개인 경우에는 1번 방법을, 여러 개가 설치되어 있는 경우는 CRI를 지정하는 2번 방법을 선택하여 수행

1. CRI 소켓이 host server 에 1개만 있는 경우

```bash
$ sudo kubeadm config images pull
```

1. CRI 소켓이 host server 에 여러 개인 경우 
****→ `—cri-socket` 옵션을 사용하여 하나를 선택

```bash
# CRI-O
$ sudo kubeadm config images pull --cri-socket /var/run/crio/crio.sock

# Containerd
$ sudo kubeadm config images pull --cri-socket /run/containerd/containerd.sock

# Docker
$ sudo kubeadm config images pull --cri-socket /run/cri-dockerd.sock
```

**#5-4) kubeadm init 수행**

- 아래는 bootstrap cluster 를 구성하기 위하여 kubeadm init 수행시, 기본적인 kubeadm init 옵션임
    - `—control-plane-endpoint`
        - set the shared endpoint for all control-plane nodes. Can be DNS/IP
        - 모든 컨트롤 플레인 노드들이 공유하는 Endpoint 가 있는 경우 설정.
        DNS 또는 IP setting
    - `—pod-network-cidr`
        - Used to set a Pod network add-on CIDR
        - Pod 네트워크 대역을 CIDR 로 설정할 때 사용
    - `—cri-socket`
        - Use if have more than one container runtime to set runtime socket path
    - `—apiserver-advertise-address`
        - Set advertise address for this particular control-plane node’s API server
        - 특정 마스터 노드의 API Server 주소를 설정할 때 사용

**shared endpoint 가 없는 bootstrap**

- DNS endpoint 를 사용하지 않고 클러스터를 부트스트랩 하려면 다음을 실행

```bash
$ sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

**Bootstrap with shared endpoint (DNS name for control plane API)**

- 먼저 클러스터 endpoint DNS name 을 설정하거나 `/etc/hosts` 파일에 record 를 추가
- 예를 들어 shared endpoint 의 ip 주소가 172.29.20.5 이고 DNS 주소가 [k8s-cluster.com](http://k8s-cluster.com) 인 경우
다음과 같이 설정

```bash
$ sudo vim /etc/hosts
172.29.20.5 k8s-cluster.com
```

kubeadm init 을 통한 클러스터 생성

```bash
$ sudo kubeadm init \
   --pod-network-cidr=10.244.0.0/16 \
   --upload-certs \
   --control-plane-endpoint=k8s-cluster.computingforgeeks.com
```

- 참고:  10.244.0.0/16 이 네트워크 내에서 이미 사용 중인 경우, 위 명령에서 10.244.0.0./16 을 대체하여 다른 pod network CIDR 를 선택해야 함

**** runtime socket 를 지정하여 kubeadm init 수행시(참고)**

- Container runtime sockets
    - Docker : /run/cri-dockerd.sock
    - containerd : /run/containerd/containerd.sock
    - CRI-O : /var/run/crio/crio.sock
- 설정에 따라 선택적으로 Runtime 용 Socket file 을 전달하고 setup 정보에 의존하여 address 를 advertise 할 수 있음

```bash
# CRI-O
sudo kubeadm init \
  --pod-network-cidr=10.244.0.0/16 \
  --cri-socket /var/run/crio/crio.sock \
  --upload-certs \
  --control-plane-endpoint=k8s-cluster.computingforgeeks.com

# Containerd
sudo kubeadm init \
  --pod-network-cidr=10.244.0.0/16 \
  --cri-socket /run/containerd/containerd.sock \
  --upload-certs \
  --control-plane-endpoint=k8s-cluster.poscoict.com

# Docker
# Must do https://computingforgeeks.com/install-mirantis-cri-dockerd-as-docker-engine-shim-for-kubernetes/
sudo kubeadm init \
  --pod-network-cidr=10.244.0.0/16 \
  --cri-socket /run/cri-dockerd.sock  \
  --upload-certs \
  --control-plane-endpoint=k8s-cluster.computingforgeeks.com
```

- 다음은 초기화 명령 수행시 정상 작동하는 경우의 출력 예시
아래 출력부를 반드시 읽어 worker node join 시 참고!
- 순서를 보면 다음과 같음
    - Pulling images required for setting up a Kubernetes cluster
    - Generating certificate and key
        - apiserver
        - apiserver-kubelet-client
        - front-proxy-ca
        - front-proxy-client
        - etcd/ca
        - etcd/server
        - etcd/peer
        - etcd/healthcheck-client
        - apiserver-etcd-client
        - sa
    - kubeconfig
        - admin.conf
        - kubelet.conf
        - controller-manager.conf
        - scheduler.conf
    - kubelet-start
        - Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
        - Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
        - Starting the kubelet
    - control-plane
        - Pod manifest(kube-apiserver, kube-controller-manager, kube-scheduler) 생성
    - etcd
        - Pod manifest 생성
    - upload-config
    - upload-certs
    - mark-control-plane
    - bootstrap-token
    - kubelet-finalize
    - addons
        - CoreDNS
        - kube-proxy

```bash
....
[init] Using Kubernetes version: v1.24.3
[preflight] Running pre-flight checks
	[WARNING SystemVerification]: missing optional cgroups: blkio
[preflight] **Pulling images required for setting up a Kubernetes cluster**
[preflight] This might take a minute or two, depending on the speed of your internet connection
[preflight] You can also perform this action in beforehand using 'kubeadm config images pull'
[certs] Using certificateDir folder "/etc/kubernetes/pki"
[certs] **Pulling images required for setting up a Kubernetes cluster** "ca" certificate and key
[certs] Generating "apiserver" certificate and key
[certs] apiserver serving cert is signed for DNS names [k8s-cluster.computingforgeeks.com k8smas01.computingforgeeks.com kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 192.168.1.10]
[certs] Generating "apiserver-kubelet-client" certificate and key
[certs] Generating "front-proxy-ca" certificate and key
[certs] Generating "front-proxy-client" certificate and key
[certs] Generating "etcd/ca" certificate and key
[certs] Generating "etcd/server" certificate and key
[certs] etcd/server serving cert is signed for DNS names [k8smas01.computingforgeeks.com localhost] and IPs [192.168.1.10 127.0.0.1 ::1]
[certs] Generating "etcd/peer" certificate and key
[certs] etcd/peer serving cert is signed for DNS names [k8smas01.computingforgeeks.com localhost] and IPs [192.168.1.10 127.0.0.1 ::1]
[certs] Generating "etcd/healthcheck-client" certificate and key
[certs] Generating "apiserver-etcd-client" certificate and key
[certs] Generating "sa" key and public key
[kubeconfig] Using kubeconfig folder "/etc/kubernetes"
[kubeconfig] Writing "admin.conf" kubeconfig file
[kubeconfig] Writing "kubelet.conf" kubeconfig file
[kubeconfig] Writing "controller-manager.conf" kubeconfig file
[kubeconfig] Writing "scheduler.conf" kubeconfig file
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Starting the kubelet
[control-plane] Using manifest folder "/etc/kubernetes/manifests"
[control-plane] Creating static Pod manifest for "kube-apiserver"
[control-plane] Creating static Pod manifest for "kube-controller-manager"
[control-plane] Creating static Pod manifest for "kube-scheduler"
[etcd] Creating static Pod manifest for local etcd in "/etc/kubernetes/manifests"
[wait-control-plane] Waiting for the kubelet to boot up the control plane as static Pods from directory "/etc/kubernetes/manifests". This can take up to 4m0s
[apiclient] All control plane components are healthy after 11.005078 seconds
[upload-config] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config" in namespace kube-system with the configuration for the kubelets in the cluster
[upload-certs] Storing the certificates in Secret "kubeadm-certs" in the "kube-system" Namespace
[upload-certs] **Using certificate key:**
**62c529b867e160f6d67cfe691838377e553c4ec86a9f0d6b6b6f410d79ce8253**
[mark-control-plane] Marking the node k8smas01.home.cloudlabske.io as control-plane by adding the labels: [node-role.kubernetes.io/control-plane node.kubernetes.io/exclude-from-external-load-balancers]
[mark-control-plane] Marking the node k8smas01.home.cloudlabske.io as control-plane by adding the taints [node-role.kubernetes.io/master:NoSchedule node-role.kubernetes.io/control-plane:NoSchedule]
**[bootstrap-token] Using token: wbgkcz.cplewrbyxgadq8nu**
[bootstrap-token] Configuring bootstrap tokens, cluster-info ConfigMap, RBAC Roles
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to get nodes
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstrap-token] Configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstrap-token] Configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstrap-token] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
[kubelet-finalize] Updating "/etc/kubernetes/kubelet.conf" to point to a rotatable kubelet client certificate and key
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  **mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config**

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of control-plane nodes by copying certificate authorities
and service account keys on each node and then running the following as root:

  **kubeadm join k8s-cluster.computingforgeeks.com:6443 --token sr4l2l.2kvot0pfalh5o4ik \
    --discovery-token-ca-cert-hash sha256:1d2c7d5a14c5d717a676291ff5ac25e041386e6371d56bb5cc82d5907fdf62a1 \
    --control-plane** 

Then you can join any number of worker nodes by running the following on each as root:

**kubeadm join k8s-cluster.computingforgeeks.com:6443 --token sr4l2l.2kvot0pfalh5o4ik \
    --discovery-token-ca-cert-hash sha256:c692fb047e15883b575bd6710779dc2c5af8073f7cab460abd181fd3ddb29a18**
```

- 아래 명령어를 사용해 kubectl 의 config 구성

```bash
$ mkdir -p $HOME/.kube
$ sudo cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
$ sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

- cluster 상태 확인

```bash
$ kubectl cluster-info

Kubernetes master is running at https://k8s-cluster.computingforgeeks.com:6443
KubeDNS is running at https://k8s-cluster.computingforgeeks.com:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

- Master node 를 추가할 경우는 아래 명령어를 통해서 추가 가능

```bash
$ kubeadm join k8s-cluster.computingforgeeks.com:6443 --token sr4l2l.2kvot0pfalh5o4ik \
    --discovery-token-ca-cert-hash sha256:c692fb047e15883b575bd6710779dc2c5af8073f7cab460abd181fd3ddb29a18 \
    --control-plane
```

### #6) 쿠버네티스 네트워크 플러그인 설치

- 이번 가이드에서는 [Flannel 네트워크 플러그인](https://github.com/flannel-io/flannel) 을 사용함.
- 다른 [플러그인](https://kubernetes.io/docs/concepts/cluster-administration/addons/)을 사용할 수도 있음
- 설치 매니페스트를 다운로드함

```bash
$ wget https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
```

- Kubernetes 설치시 사용자가 customizing 한 podCIDR 을 사용하는 경우
(위에서 10.244.0.0/16 사용 안하는 경우), 
다운로드한 매니페스트의 네트워크와 일치하도록 네트워크를 수정해야 함

```bash
$ vim kube-flannel.yml
net-conf.json: |
    {
      **"Network": "10.244.0.0/16",**
      "Backend": {
        "Type": "vxlan"
      }
    }
```

- 그런 다음 필요한 리소스를 생성하여 Flannel 을 설치함

```bash
$ kubectl apply -f kube-flannel.yml

namespace/kube-flannel created
clusterrole.rbac.authorization.k8s.io/flannel created
clusterrolebinding.rbac.authorization.k8s.io/flannel created
serviceaccount/flannel created
configmap/kube-flannel-cfg created
daemonset.apps/kube-flannel-ds created
```

- 모든 Pod 가 실행 중인지 확인
준비되기까지 몇 초에서 몇 분 정도 걸릴 수 있음

```bash
$ kubectl get pods -n kube-flannel
NAME                    READY   STATUS    RESTARTS   AGE
kube-flannel-ds-pppw4   1/1     Running   0          2m16s
```

- 마스터 노드가 준비되었는지 확인

```bash
$ kubectl get nodes -o wide
```

### #7) worker node 추가

- control plane 이 준비되면 예약된 워크로드를 실행하기 위해 worker node 를 클러스터에 추가할 수 있음
- endpoint 주소가 DNS에 없으면 /etc/hosts 에 레코드를 추가함
(아래 추가 내용은 worker node 에 대한 것임)

```bash
$ sudo vim /etc/hosts
172.29.20.5 k8s-cluster.computingforgeeks.com  
```

- 제공된 join command 은 작업자 노드를 클러스터에 추가하는 데 사용됨 
(아래 명령어는 worker node 에서 수행)

```bash
$ kubeadm join k8s-cluster.computingforgeeks.com:6443 \
    --token sr4l2l.2kvot0pfalh5o4ik \
    --discovery-token-ca-cert-hash sha256:c692fb047e15883b575bd6710779dc2c5af8073f7cab460abd181fd3ddb29a18
```

```bash
[preflight] Reading configuration from the cluster...
[preflight] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -oyaml'
[kubelet-start] Downloading configuration for the kubelet from the "kubelet-config-1.21" ConfigMap in the kube-system namespace
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Starting the kubelet
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap...

This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.
```

```bash
$ kubectl get nodes
NAME                                 STATUS   ROLES    AGE   VERSION
k8s-master01.computingforgeeks.com   Ready    master   10m   v1.24.3
k8s-worker01.computingforgeeks.com   Ready    <none>   50s   v1.24.3
k8s-worker02.computingforgeeks.com   Ready    <none>   12s   v1.24.3

$ kubectl get nodes -o wide 
```

** 필요시 **join token 생성**

- token 이 만료된 경우 새 token 을 생성하여 worker node 에 [새로운 토큰을 생성하는 방법](https://computingforgeeks.com/join-new-kubernetes-worker-node-to-existing-cluster/)을 참조
- 기본적으로 kubeadm 수행 시 token 이 생성됨

### #8) 클러스터에 테스트 애플리케이션 배포

- 클러스터가 작동하는지 확인하기 위해 테스트 애플리케이션을 배포해 보자

```bash
$ kubectl apply -f https://k8s.io/examples/pods/commands.yaml
```

- 포드가 시작되었는지 확인

```bash
$ kubectl get pods
NAME           READY   STATUS      RESTARTS   AGE
command-demo   0/1     Completed   0          16s
```

### 설치 버전 참고

[config/images] Pulled [registry.k8s.io/kube-apiserver:v1.25.5](http://registry.k8s.io/kube-apiserver:v1.25.5)
[config/images] Pulled [registry.k8s.io/kube-controller-manager:v1.25.5](http://registry.k8s.io/kube-controller-manager:v1.25.5)
[config/images] Pulled [registry.k8s.io/kube-scheduler:v1.25.5](http://registry.k8s.io/kube-scheduler:v1.25.5)
[config/images] Pulled [registry.k8s.io/kube-proxy:v1.25.5](http://registry.k8s.io/kube-proxy:v1.25.5)
[config/images] Pulled [registry.k8s.io/pause:3.8](http://registry.k8s.io/pause:3.8)
[config/images] Pulled [registry.k8s.io/etcd:3.5.6-0](http://registry.k8s.io/etcd:3.5.6-0)
[config/images] Pulled [registry.k8s.io/coredns/coredns:v1.9.3](http://registry.k8s.io/coredns/coredns:v1.9.3)

## 용어 정리

- **CNI(Container Network Interface)**
    - 보통 Pod 는 여러 노드에 걸쳐 배포되는데 pod 는 서로 하나의 네트워크에 있는 것처럼 통신이 가능
- **Flannel**
    - 서로 다른 노드에 있는 pod 간 통신을 완성하기 위해 관련 기능을 제공하는 network-plugin 이 필요
    - Flannel 은 대표적인 CNI 종류 중 하나
- **bridge**
    - OSI 모델의 데이터 링크 계층에 있는 여러 개의 네트워크 세그먼트를 연결해 줌
    - Layer 2 switch 는 bridge 라는 용어와 같은 뜻으로 간헐적으로 사용됨
- **CIDR**
    - 사이더라고 부름
    - **Classless Inter-Domain Routing** 으로  클래스없는 도메인간 라우팅 기법이라는 뜻
    즉 네트워크 구분을 Class 로 하지 않는다는 것
    Class 는 CIDR 가 나오기 전 사용했던 네트워크 구분 체계
    - ex) --pod-network-cidr=10.244.0.0/16 는 뒤의 16bit 를 사용하여 
           네트워크를 구성할 수 있다는 의미