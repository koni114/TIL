## Part3. 오픈소스를 통해 알아보는 MLOps의 구성요소
### Data Management 란
- ML Model 를 만들다보면 다양한 실험(feature engineering 등)을 통해 테스트를 해야하는 경우가 많음
- 이러한 process 마다 데이터를 저장해야 할 필요성이 생김
- 이런 데이터를 파일 명/ 디렉토리 명으로 구분하는 것도 좋지만, 더 좋은 방법이 존재
- ML 관련 버전 관리가 필요한 경우에 Git 을 사용하며, git을 Hosting 해주는 서비스(Github, GitLab, Bitbucket) 도 함께 사용하지만, 대용량 데이터를 올리기에는 적합하지 않다는 단점이 있음
(100MB의 용량 제한 존재)
- 따라서 어떤 경우에 데이터는 Google drive / S3 같은 곳에 저장하고 github에는 데이터를 다운받을 수 있는 정보를 작성하거나, git-lfs 를 월마다 지불하여 사용하는 방법이 있음
- 하지만 위의 방법도 불편한 점이 많이 존재하여, 최근에는 데이터의 버전과 데이터 메타 정보를 함께 관리 할 수 있는 tool이 나옴
- 대표적으로, <b>DVC, Pachyderm, Delta Lake, Dolt</b> 등이 있음

#### DVC
- Data Version Control
- open source
- Github, GitLab, Bitbucket 등의 대부분의 git 호스팅 서버와 연동
- 대부분의 스토리지와 호환(amazon s3, google drive, ...)
- Data pipeline 을 DAG 로 관리
- Git 과 유사한 인터페이스

#### DVC 저장 방식
![img](https://github.com/koni114/TIL/blob/master/MLOps/daily/img/mlops_1.png)
- 실제 data 는 Remote Data Storage 에 저장되며, 해당 데이터의 버전 등과 같은 메타 정보들만 git server 에 저장됨
- 명령어 같은 경우 git 과 거의 유사함
- python api 를 통해 python code로도 관리 가능

#### DVC 설치
- python 설치 필요
- git 설치 
~~~shell
sudo apt isntall git
git --version
 # git version 2.25.1 

 git --help # 정상 설치 확인
~~~
- dvc 설치
  - dvc 2.6.4 버전 다운
  - `dvc[all]` 에서 `[all]` 은 dvc의 remote storage 로 s3, gs, azure, oss, ssh 모두를 사용할 수 있도록 관련 패키지를 함께 설치하는 옵션 
~~~shell
pip install dvc[all]==2.6.4

dvc --version

dvc --help
~~~
