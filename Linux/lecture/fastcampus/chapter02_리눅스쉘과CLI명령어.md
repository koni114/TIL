## chapter02 - 리눅스 쉘과 CLI 명령어
### 기본 명령어 - 파일 시스템 구조
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_07.png)

- link의 유형 개념
- 하드링크  
  - 용량을 두배로 차지하지도 않고, 실수로 파일을 삭제하더라도 원본은 삭제되지 않음
  - 사용 사례가 그렇지 많지는 않음. 백업의 경우에 간간히 사용
- 소프트링크(심볼릭 링크)
  - 직접적으로 파일을 바라보는 것이 아니라, 파일을 가리키는 포인터가 만들어지게 됨
  - 파일의 불필요한 복사를 방지하여 파일 시스템을 유연하게 활용하거나 여러 디렉토리에서 동일한 라이브러리를 요구할 경우 등 사용

### 기본 명령어 - 파일 시스템 구조(inode 맛보기)
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_08.png)

- inode 초간단 개념
- inode --> 리눅스에서 파일을 관리하는 구조체
- 우리는 리눅스에서 `hello.txt` 라는 파일을 명령어 등을 통해서 접근하는데, 실제로는 중간에 inode를 거쳐서 접근함
- hellolink 라는 하드 링크가 있다면, 이는 hello.txt와 동일한 inode의 주소값을 가리키게 되고, 이는 다시 파일 DATA를 가리키게 됨 
- hellosymlink(소프트 링크)는 hello.txt와 다른 inode를 카리킴 이 inode는 다시 hello.txt의 inode를 가리킴

## 사용자, 그룹 및 권한(명령어)
### 사용자 계정 - superuser 와 user
- 슈퍼유저란? 
  - 시스템 운영 관리자 계정으로 일반적으로 리눅스 운영체제에서는 루트(Root) 유저를 말함
  - 관리자 권한을 이반 사용자 권한과 구분하며 사용자의 부주의로 발생하는 시스템 손상과 바이러스, 악성코드의 침입에 의한 피해를 보호 
- `whoami` - 내가 누구인지 내 계정 확인
- `id` - 내가 갖고있는 권한(포함된 그룹) 확인

### 사용자 계정 - 권한의 대여 - sudoer
- `sudo visudo`  
  슈퍼유저의 권한을 편집
- 설정파일을 통한 변경
  - 사용자 권한
  - %그룹 권한
~~~shell
$ sudo cat /etc/suduers
~~~
- 특정 사용자 별로 권한을 줄 수도 있음.
- 특정 사용자만 sudo 명령어를 사용하게 하거나, 특정 명령어만 sudo를 사용하게 할 수 있음.
- 해당 설정파일을 통한 변경은 되도록이면 자제하는 것이 좋음  
  보안 등에 취약해질 수 있음
- 이럴 때는 사용자를 sudo 권한에 추가하는 것을 추천
  - `useradd -aG user1 sudo`  # Ubuntu
  - `useradd -aG user1 wheel` # Amazon AMI

### 사용자 계정 - 권한의 대여 - su
- `su[username]`
  - 사용자의 권한을 대여(즉, 사용자로 로그인 한 것과 같은 효과)
  - 언제 사용하느냐? 관리자가 사용자 계정을 관리하고 이슈/장애를 분석할 때 
- 사용방법
  - `su user2`  
    user2의 id로 로그인 한다(user2의 pw 필요)
  - `su -user2`  
    user2의 id로 로그인 한다(user2의 home 디렉토리 사용)
  - `su`, `su root`  
    root의 id로 로그인한다. (root의 pw 필요. 하지만 우분투는 root 암호 비활성화) 
