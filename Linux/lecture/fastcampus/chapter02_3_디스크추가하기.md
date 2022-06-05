# 디스크 추가하기
- 디스크 추가같은 경우는 가상 환경이나 클라우드 환경에서 빈번하게 발생함
- 기본이 되는 블록 스토리지 추가하는 방법에 대해서 알아보자
- VM 에서
  - usb 추가하기
  - 하드디스크 추가하기
  - 파일시스템 (ext3, ext4, ntfs, fat 등) 및 포맷, 파티션(fdisk 까지만)
  - /etc/fstab 을 통한 자동 마운트 
- 배울 명령어
  - `mount`, `usb-media`, `dmesg`, `lsusb` 
- AWS 클라우드 에서(EC2)
  - 로컬 스토리지 용량 추가하기
  - 스토리지 용량 다이나믹 확대하기 

## 파일시스템 개요
### 디바이스 유형 - 인터페이스
- IDE(Integrated Drive Electronics) : IBM PC AT 호환기의 HDD, CD-ROM, ...
- SATA(Serial Advanced Technology Attachment): 직렬 방식의 규격
- SCSI(Small Computer System Interface): 주변 장치의 연결을 위해 사용하던 ANSI 표준 규격

### 디바이스 유형 - 장치 파일, 블록/캐릭터 디바이스
- 리눅스에서는 모든 디바이스가 파일 시스템을 통해 표시가 되고 연결이 됨. `dev` 디렉토리에 모두 연결이 됨
- 블록 디바이스: 하드 디스크, CD/DVD, USB 등 블록이나 섹터 단위로 데이터를 전송하는 디바이스
- 캐릭터 디바이스: 키보드, 마우스, 프린터 등의 입출력 장치로 바이트 단위로 데이터를 전송하는 디바이스
- 한단계 더 내려가서, 리눅스 시스템에서 하드웨어 인터페이스와 디렉토리 구조를 보면,   
  블록 디바이스는 앞글자가 `b`, 캐릭터 디바이스는 `c`로 시작함
~~~shell
$ cd /dev
$ ls -al sda*

brw-rw---- 1 root disk 8, 0  6월  5 17:23 sda
brw-rw---- 1 root disk 8, 1  6월  5 17:23 sda1
brw-rw---- 1 root disk 8, 2  6월  5 17:23 sda2
brw-rw---- 1 root disk 8, 5  6월  5 17:23 sda5

$ ls -al tty*
crw-rw-rw- 1 root tty     5,  0  6월  5 17:23 tty
crw--w---- 1 root tty     4,  0  6월  5 17:23 tty0
crw--w---- 1 root tty     4,  1  6월  5 17:23 tty1
crw--w---- 1 root tty     4, 10  6월  5 17:23 tty10
crw--w---- 1 root tty     4, 11  6월  5 17:23 tty11
~~~

### 리눅스의 장치파일(디바이스) 관리
- `/dev`
  - sr0 - cd-rom 이며, 뒤의 숫자는 넘버링 
  - hda1 - PAPA 방식 HDD1 (파티션1) --> hda 형태는 보기 힘듬 
  - sda1 - SATA 방식 HDD1 (파티션2) --> 대부분의 시리얼 방식을 사용함. 하드 디스크 개수에 따라 a, b, c.. 가 붙음
  - sda2 - SATA 방식 HDD1 (파티션2) --> 1, 2, 3, 4는 파티션을 의미
  - tty - 터미널
- `/dev/input`
  - 입력 디바이스들
- `/dev/block`
  - 블록 디바이스들(디스크)
- `/dev/char`
  - 케릭터 디바이스들(입력, 입출력)   

### 디스크 파티션
- 파티션은 하드디스크를 논리적으로 구분하기 위한 단위. 이를 통해 하나의 하드디스크에서 MacOS 나 Window 를 듀얼부팅 하는 등 여러가지 일들이 가능하게 됨

### USB 추가하기
- 최근 우분투에서는 USB가 자동으로 마운트됨
- 터미널에서 추가된 usb disk를 확인하고 싶다면, 자동으로 된 경우 `media` directory 에 해당 볼륨명으로 자동 연결됨

### USB 추가하기 - 디바이스 확인 명령어
- `fdisk`
- `mount`
- `unmount`

### 디스크 추가하기 - 준비과정(디스크 확인)
- 디스크 확인하기, 용량 확인, 파일 시스템 확인
- `fdisk -l`