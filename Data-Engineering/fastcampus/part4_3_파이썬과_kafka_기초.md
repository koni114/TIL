## chapter03 파이썬과 kafka 기초
### 파이썬으로 Producer 만들기
- 데이터를 전송하는 경우에는 byte-code 로 전송하는 것이 좋음
~~~python
# producer.py
from kafka import KafkaProducer

# bootstrap server 와 port 이름을 parameter 로 입력
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

producer.send('first-topic', b'hello-world from python')
producer.flush()
~~~

### 파이썬으로 Consumer 만들기
~~~python
from kafka import KafkaConsumer

# consumer 는 python generator 역할을 함
consumer = KafkaConsumer('first-topic', bootstrap_servers=['localhost:9092'])

for messages in consumer:
    print(messages)
~~~
- 계속적으로 producer.py script를 실행시키면, offset 번호가 순차적으로 변경되면서 처리되는 것을 확인 가능
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_37.png)

### 도커 설치
- 카프카 클러스터를 만드는 방법에 대해서 알아보자
- 그 안에서 broker 등 여러가지를 만들어보자. 즉, 분산된 환경에서 kafka를 만드는 방법에 대해서 알아보자
- local 환경에서 분산 환경을 만들어보기 위해, docker 를 사용해보자
- docker 를 이용해서 kafka instance를 만들어 볼 것임
- 구글에 docker install 로 검색하여 다운로드 받아서 설치해 주면 됨

### Kafka cluster 구축 준비
- docker 를 이용해서 kafka cluster를 만듬
- 이를 위해서는 zookeeper 를 위한 instance 하나를 만들고, kafka cluster에는 broker 3가지(3개의 server)를 만들어보자
- 3가지의 kafka broker는 1개의 topic, 2개의 partition 을 만들어보자
- replication-factor도 2개 정도로 만들어보자
- local 환경에서(1개의 서버, 컴퓨터) docker 의 가상환경 여러개를 만들어 실습을 진행하고 있지만, 향후 실제 production 에서는 여러 대의 서버에서 수행(분산 처리)될 것임 
- 우선 앞선 실습에서 실행된 zookeeper, kafka-server 를 stop 하자

### kafka 클러스터 구축하기-Zookeeper 
- 다음의 docker-compose file 을 작성하여 `docker-compose up` 명령어 수행
- `docker-compose.yml` file 을 다음과 같이 작성
~~~yml
version: '3'
services:
  zookeeper:
    image: zookeeper:3.7
    hostname: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOO_MY_ID: 1
      ZOO_PORT: 2181
      ZOO_SERVERS: server.1=zookeeper:2888:3888
    volumes:
      - ./data/zookeeper/data:/data
      - ./data/zookeeper/datalog:/datalog
~~~

### kafka 클러스터 구축하기-kafka broker
- kafka-instance docker 3개를 띄어보자
- kafka image 는 docker hub 에서 사용할 것인데, cp-kafka 사용  
  버전은 7.0.0 사용
- confluent 는 kafka를 만든 팀이 나와서 설립한 별도 회사 
- `ports` 는 host 와 docker 를 연결해주기 위한 port