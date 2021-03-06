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
- 위의 Zookeeper instance 생성을 위한 docker-compose file 에 추가하면 됨
~~~yml
  kafka1:
    image: confluentinc/cp-kafka:7.0.0
    hostname: kafka1
    ports:
      - "9091:9091"
    environment:
      KAFKA_ADVERTISED_LISTENERS: LISTENER_DOCKER_INTERNAL://kafka1:19091,LISTENER_DOCKER_EXTERNAL://${DOCKER_HOST_IP:-127.0.0.1}:9091
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: LISTENER_DOCKER_INTERNAL:PLAINTEXT,LISTENER_DOCKER_EXTERNAL:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: LISTENER_DOCKER_INTERNAL
      KAFKA_ZOOKEEPER_CONNECT: "zookeeper:2181"
      KAFKA_BROKER_ID: 1
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    volumes:
      - ./data/kafka1/data:/tmp/kafka-logs
    depends_on:
      - zookeeper
  kafka2:
    image: confluentinc/cp-kafka:7.0.0
    hostname: kafka1
    ports:
      - "9092:9092"
    environment:
      KAFKA_ADVERTISED_LISTENERS: LISTENER_DOCKER_INTERNAL://kafka1:19092,LISTENER_DOCKER_EXTERNAL://${DOCKER_HOST_IP:-127.0.0.1}:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: LISTENER_DOCKER_INTERNAL:PLAINTEXT,LISTENER_DOCKER_EXTERNAL:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: LISTENER_DOCKER_INTERNAL
      KAFKA_ZOOKEEPER_CONNECT: "zookeeper:2181"
      KAFKA_BROKER_ID: 2
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    volumes:
      - ./data/kafka1/data:/tmp/kafka-logs
    depends_on:
      - zookeeper
  kafka3:
    image: confluentinc/cp-kafka:7.0.0
    hostname: kafka1
    ports:
      - "9093:9093"
    environment:
      KAFKA_ADVERTISED_LISTENERS: LISTENER_DOCKER_INTERNAL://kafka1:19093,LISTENER_DOCKER_EXTERNAL://${DOCKER_HOST_IP:-127.0.0.1}:9093
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: LISTENER_DOCKER_INTERNAL:PLAINTEXT,LISTENER_DOCKER_EXTERNAL:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: LISTENER_DOCKER_INTERNAL
      KAFKA_ZOOKEEPER_CONNECT: "zookeeper:2181"
      KAFKA_BROKER_ID: 2
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    volumes:
      - ./data/kafka1/data:/tmp/kafka-logs
    depends_on:
      - zookeeper
~~~
- `ports` : local com 과 docker 를 연결주기 위한 port 설정  
   3개의 kafka(broker)를 사용하기 위해 port를 9091, 9092, 9093 으로 설정
- `environment`
  - `KAFKA_ADVERTISED_LISTENERS` kafka listener 설정  
  docker_internal, docker_external 설정  
  kafka broker를 가리키는 사용 가능 주소 목록. kafka는 초기 연결시 이를 client에게 보냄
  - `KAFKA_LISTENER_SECURITY_PROTOCOL_MAP`: 
  - `KAFKA_ZOOKEEPER_CONNECT` : zookeeper 와 연결하기 위한 connection 정보 삽입
- `volumes` : kafka 와 local host 상의 directory mount 설정
- `depends_on` : zookeeper 뒤에 kafka 를 실행시키기 위해 설정
- 주의해야 할 사항
  - kafka broker id 는 동일한 id가 2개가 있으면 안됨
  - docker-compose 를 여러번 수행할 시 에러가 발생할 수 있는데, 이 때 `docker-compose rm -svf` 명령어를 실행하고 다시 수행해야 함
- kafka instance를 3개 만드는 것이므로, 위의 kafka1 instance option을 복사해서, `kafka2`, `kafka3`으로 만들고, 해당 port 를 각각 9092, 9093으로 변경하고, broker_id도 2, 3으로 변경

### kafka 클러스터 구축하기 - Kafdrop 
- kafka broker 를 조금 더 쉽게 관리해주는 tool --> kafdrop
- kafka를 web UI를 통해 눈으로 확인하게 해주는 tool
- kafdrop은 docker-hub에서 kafdrop으로 존재함 
- docker-compose file 에 추가해보자
~~~yml
kafdrop:
    image: obsidiandynamics/kafdrop
    restart: "no"
    ports:
      - "9000:9000"
    environment:
      KAFKA_BROKER_CONNECT: "kafka1:19091"
    depends_on:
      - kafka1
      - kafka2
      - kafka3
~~~
- `ports`: 9000:9000 으로 설정하게 되면, instance 실행시 localhost:9000 으로 실행 가능
- `depends_on`: kafka image 3개가 모두 설치된 이후에 설치되어야 함

### kafka 클러스터 구축하기 - Topic 만들기
- 클러스터 안에서 쓸 topic 만들어보기
- `docker-compose up -d` 로 입력시, 모든 image 들이 background 로 돌게 됨
- kafka topic 을 만들기 위해서는 kafka instance 안에서 만들어야 함
- 그러기 위해서는 `docker exec -it 03-kafka_kafka1_1` 명령어 사용  
  이는 docker 내 kafka의 이름(docker app에서 확인 가능)
~~~shell
# 03-kafka-kafka1-1
docker exec -it 03-kafka-kafka1-1 kafka-topics --bootstrap-server=localhost:19091 --create --topic first-cluster-topic --partitions 3 --replication-factor 1


~~~
- 위의 명령어 수행시 first-cluster-topic 이라는 topic 이 추가되며, partition도 3개가 추가되는 것을 확인 가능
- kafdrop 을 사용시, 굉장히 쉽게 관리가 가능

### Kafka 클러스터를 이용하는 Producer
- `cluster_producer.py` 생성하여, 3개의 kafka producer 를 사용할 수 있게 해보자
~~~Python
# cluster_producer.py
from kafka import KafkaProducer

brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]
topic_name = "first-cluster-topic"

producer = KafkaProducer(bootstrap_servers=brokers)
producer.send(topic_name, b"Hello cluster world")
producer.flush()
~~~
- 위의 cluster_producer.py 를 실행시키면, 메세지가 producer 로 전송됨

### Kafka 클러스터를 이용하는 Consumer
- `cluster_consumer.py`를 생성하여, consumer 를 만들어보자
~~~python
from kafka import KafkaConsumer
brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]
consumer = KafkaConsumer("first-cluster-topic", bootstrap_servers=brokers)

# 무한 루프를 돌면서 메세지를 확인하는 구문
for message in consumer:
    print(message)
~~~
- 위의 script 실행 전, docker instance 가 정상적으로 실행되고 있는지 확인

#### producer-consumer test
- 먼저 하나의 terminal 창에서 `python cluster_consumer.py` 실행
- 다른 하나의 terminal 창에서 `python cluster_producer.py`를 실행하면, 해당 스크립트에서 작성한 message가 정상적으로 송신되는 것을 확인

### kafdrop으로 메세지 확인하기
- kafdrop UI 에서 topic 클릭 후, View-Messages 를 클릭하면 각각의 message 들을 확인 가능

### CSV를 스트림으로 바꿔주는 Producer
- 저번에 만들어둔 클러스터를 활용해서 실습 진행
- 뉴욕 trip data를 이용해서 csv 파일을 stream 으로 변경해보는 실습 수행
- 새롭게 `trips` folder 를 만들고, 안에 `yellow_tripdata_2021_01.csv` 넣기
- csv 읽어오면서 stream event 를 동시에 발생시키면 알아보기 어렵기 때문에, sleep 사용

### 비정상 데이터 탐지 - Producer
- 반드시 consumer 와 producer 가 다른 서버(or program)일 필요는 없음  
  예를 들어, data feed 를 받아서 처리 후 다른 서비스에 전달을 하는 경우
- 앞선 예제들과 구분을 하기 위하여, 별도의 디렉토리를 만들어 `fraud_detection` 디렉토리를 생성하고, `payment_producer.py` 를 생성
- `payment_producer` 는 가상의 payment 데이터를 만들어, broker -> topic 에게 전달하는 역할 수행
- `payment_producer` 에서 생성된 데이터는 `fraud_detector` 에서 정상/비정상 유무를 판별하고 정상인 데이터는 `legit_processor` 에서 처리하며, 비정상 데이터는 `fraud_processor` 에서 처리
~~~python
from kafka import KafkaProducer
import datetime
import pytz
import time
import random
import json

brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]
producer = KafkaProducer(bootstrap_servers=brokers)
TOPIC_NAME = 'payments'

def get_time_date():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    kst_now = utc_now.astimezone(pytz.timezone("Asia/Seoul")) # 우리의 time zone 으로 변경됨
    date_str = kst_now.strftime("%m/%d/%Y")
    time_str = kst_now.strftime("%H:%M:%S")
    return date_str, time_str


def generate_payment_data():
    card = random.choice(["VISA", "MASTERCARD", "BITCOIN"])
    amount = random.randint(0, 100)
    to = random.choice(["me", "mom", "dad", "friend", "stranger"])
    return card, amount, to


while True:
    date_str, time_str = get_time_date()
    card, amount, to = generate_payment_data()
    new_data = {
        "DATE": date_str,
        "TIME": time_str,
        "CARD": card,
        "AMOUNT": amount,
        "TO": to
    }

    # data 를 python object 를 그대로 보낼 수 없음.
    # json 의 형태로 변경 한 후, utf-8 로 encoding 하는 과정을 거쳐야 함
    producer.send(TOPIC_NAME, json.dumps(new_data).encode('utf-8'))
    print(new_data)
    time.sleep(1)
~~~

### 비정상 데이터 탐지 - Detector
- `producer` 에서 생성된 msg 에서 `PAYMENT_TYPE` 이 `BITCOIN` 인 경우를 비정상으로 탐지하여 FRAUD_TOPIC 으로 전송하고, 나머지 정상인 경우는 LEGIT_TOPIC 으로 전송하는 예제를 만들어보자
~~~python
import time

from kafka import KafkaProducer, KafkaConsumer
import json

PAYMENT_TOPIC = "payments"
FRAUD_TOPIC = "fraud_payments"
LEGIT_TOPIC = "legit_payments"

brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]

consumer = KafkaConsumer(PAYMENT_TOPIC, bootstrap_servers=brokers)
producer = KafkaProducer(bootstrap_servers=brokers)


def is_suspicious(transactions):
    """
    데이터 수상 여부 확인 함수
    """
    if transactions["PAYMENT_TYPE"] == "BITCOIN":
        return True
    return False


for message in consumer:
    msg = json.loads(message.value.decode())
    topic = FRAUD_TOPIC if is_suspicious(msg) else LEGIT_TOPIC
    producer.send(topic, value=json.dumps(msg).encode('utf-8'))
    print(f"topic : {topic}, is_suspicious : {is_suspicious(msg)}")
    print(f"msg : {msg}")
    time.sleep(1)
~~~

### 비정상 데이터 탐지 - Processor
~~~python
# legit_processor.py
from kafka import KafkaConsumer
from fraud_detector import LEGIT_TOPIC
import json

brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]
consumer = KafkaConsumer(LEGIT_TOPIC, bootstrap_server=brokers)

for message in consumer:
    msg = json.loads(message.value.decode())
    py_type = msg["PAYMENT_TYPE"]
    to = msg['TO']
    amount = msg["AMOUNT"]
    if py_type == "VISA":
        print(f"[VISA] --> to : {to} - {amount}")
    elif py_type == "MASTERCARD":
        print(f"[MASTERCARD] --> to : {to} - {amount}")
    else:
        print("[ALERT] unable to process payments")
~~~
~~~python
from kafka import KafkaConsumer
from fraud_detector import FRAUD_TOPIC
import json

brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]
consumer = KafkaConsumer(FRAUD_TOPIC, bootstrap_server=brokers)

for message in consumer:
    msg = json.loads(message.value.decode())
    to = msg['TO']
    amount = msg["AMOUNT"]
    if msg["TO"] == "stranger":
        print(f"[ALERT] --> fraud detected ! to : {to} - {amount}")
    else:
        print(f"[PROCESSING BITCOIN] to : {to} - {amount}")
~~~
- 앞서 작성한 4개의 script를 실행시키면 스트리밍 결과의 데이터가 출력되는 것을 확인 가능

 ### 용어 정리
- listener
  - 특정 이벤트(특정한 사건)이 발생하기를 귀 귀울여 기다리다가 실행되는 컴포넌트(메소드, 함수)