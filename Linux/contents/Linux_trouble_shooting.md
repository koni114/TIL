# docker container 에서 systemctl 명령어 수행시 에러 발생
- docker container 에서 System has not been booted with systemd as init system (PID 1). Can't operate Failed to connect to bus: Host is down 발생 오류
- 정식 Linux OS 가 아니라서 systemd 를 가지고 작업을 하기에는 적합한 환경이 아니기 때문에 발생 
- Linx 는 오랫동안 initd 가 최초의 프로세스로 기능했으나 근래에는 systemd 가 역할을 물려받아 대체됨  
 그러나 여전히 init 프로세스가 이 역할을 하고 있어 호환성에 문제가 있음
