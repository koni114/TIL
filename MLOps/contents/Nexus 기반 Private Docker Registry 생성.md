# Nexus 기반 Private Docker Registry 생성

작성일시: November 7, 2022 8:23 PM
최종 편집일시: November 7, 2022 9:40 PM

### 1. repository 폴더 생성

```bash
$ sudo mkdir -p /nexus-data
```

### 2. Nexus container 생성

```bash
$ docker run --name nexus -d -p 5001:5001 -p 8081:8081 -v /Users/heojaehun/nexus-data:/nexus-data -u root sonatype/nexus3
```

- **5001: nexus registry port**
- **8081: Nexus web port**
- `/nexus-data`: volume mount (Nexus 데이터가 저장되는 경로)
- `/root` : user
- `sonatype/nexus3` : image pull

### 3. Nexus Web 접속

- http://localhost:8081 → Nexus web 접속(시간이 좀 걸림)
- admin password 확인

```bash
$ cat /nexus-data/admin.password
```

- 초기 암호로 접속 후 암호 변경

### 4. Create Blob Store

[Configuration] → [Repository] → [Blob Stores] → [Create Blob Store]

[.docker-hosted] blob 생성
 Type : `File`
 Name : `docker-hosted` 
→ Save 버튼 클릭 

[.docker-hub] blob 생성
Type : `File` 
Name : `docker-hub` > Save

### 5. Create repository

- [Configuration] → [Repository] → [Repositories] → [Create repository] 클릭
- .docker(hosted) 선택 
→ Name : `docker-hosted` 
→ HTTP : 5001 
→ Blob store : `docker-hosted`  
→ Enable Docker V1 API 체크
- docker(proxy) 선택
→ Name : `docker-proxy`
→ Enable Docker V1 API 체크
→ Remote storage : [https://registry](https://registry)-1.docker.io
→ Docker Index : `Use Docker Hub` 선택
→ Blob store : docker-hub
- [Configuration] → [Security] → [Realms] 설정
Docker Bearer Token Realm 을 Active 로 변경 → Save
- Nexus 를 이용한 Private Docker Registry 구축은 3개의 저장소가 필요
    
- **hosted(Local)** : 내부에서 생성한 도커 이미지 파일을 배포(Push) 함
- **proxy(Remote)** : 외부의 도커 저장소의 이미지들을 저장하고 내부 사용자에게 전달함(Cache 역할)
- **group(Repos)** : 다수의 hosted, proxy 저장소를 묶어 단일 경로를 제공

### 6. docker 권한 변경

- Nexus 와 HTTP 통신을 위한 변경

```bash
$ sudo vi /etc/docker/daemon.json
{
	"insecure-registries" : ["192.168.31.81:5001"]
}
```

- docker daemon socket (`/var/run/docker.sock`) 연결 시 권한 거부 오류 해결을 위해 
아래와 같이 설정

```bash
$ sudo groupadd docker              # docker group 이 없다면 생성
$ sudo usermod -aG docker "user"    # docker group 에 해당 사용자를 추가
$ newgrp docker                     # 로그아웃 후 다시 로그인하거나 명령어를 실행시켜야 적용됨
$ sudo systemctl restart docker     # docker daemon 재시작
```

### 7. docker 저장소 로그인

```bash
$ docker login localhost:5001 # docker 저장소 로그인 (HJH/*******)
```

### 8. docker image 생성

```bash
$ docker pull busybox
$ docker images
$ docker tag 2bd29714875d localhost:5001/busybox:v1
```

### 9. docker image push

```bash
$ docker push localhost:5001/busybox:v1
```

### 10. docker image pull

```bash
$ docker rmi localhost:5001/busybox:v1
$ docker images
```