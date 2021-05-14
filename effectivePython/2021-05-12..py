# subprocess.run
#- subprocess의 주된 목적은 현재 소스코드안에서 다른 포로세스를 실행하게 해주며,
#- 그 과정에서 데이터의 입출력을 제어하기 위함
import subprocess

# subprocess.run(*popenargs,
#     input=None,
#     capture_output=False,
#     timeout=None,
#     check=False, **kwargs)

#- popenargs: 명령어 실행
#- stdin, stdout, stderr: 표준 입력, 출력, 오류를 설정(데이터를 중간에 가로채서 다른 곳으로 보낼 수 있음
#- input: 입력데이터 설정
#- capture_output: True 라면 run 메소드에 의해 실행된 결과값을 변수에 저장 가능
#- shell: shell화면 출력 여부
#- cwd: 현재 실행중인 디렉토리 반환
#- timeout: 지정시간 이후에 해당프로세스가 정지되거나 삭제됨
#- check: True라면 CalledProcessError 예외가 발생
#- encoding: subprocess는 결과를 바이너리 형태로 반환하는 이를 원하는 코딩방식으로 바꿔줌
#- text: True 라면 결과값을 string의 형태로 출력
import subprocess

result = subprocess.run(['echo', '자식 프로세스에게 보내는 인사'],
                        capture_output=True,
                        encoding='utf-8')

thread.join() #- thread가 종료할 떄까지 기다림