## Kafka CLI
### Zookeeper Console 에서 사용하기
- 다운로드 받은 kafka_2.13-3.0.0 directory 로 이동해 zookeeper 를 실행시켜보자
~~~shell
cd bin    # bin dir 로 이동
./zookeeper-server-start.sh 
~~~
- 위의 명령어 수행시, 다음과 같은 에러 발생
- `USAGE: ./zookeeper-server-start.sh [-daemon] zookeeper.properties`  
  즉, zookeeper.preperties 를 옵션으로 설정하여 실행 필요
- config directory 밑에 zookeeper.properties 가 존재하는데, 이를 확인해보자
- 해당 파일 내용을 보면 다음과 같이 property가 설정되어 있음을 확인
~~~conf
dataDir=/tmp/zookeeper
clientPort=2181
maxClientCnxns=0
admin.enableServer=false
~~~
- config parameter 정보
  - `dataDir` : zookeeper 가 snapshot 을 저장하거나 log 를 저장하는 폴더 지정
  - `clientPort` : client가 어떤 port 를 써서 연락을 할 것인지 지정
  - `maxClientCnxns` : max client Connections. 0의 의미는 쓰지 않는다는 의미  
    숫자를 지정하게 되면 zookeeper와 통신하는 client의 수를 제한  
    production 환경에서는 지정하는 것이 보안 상 좋음
  - `admin.enableServer` : admin server를 열지 말지 결정  
- zookeeper 를 실행해보자
~~~
./bin/zookeeper-server-start.sh -daemon config/zookeeper.properties
~~~

### Kafka Broker 시작하기
~~~shell
./bin/kafka-server-start.sh
~~~
- 위의 명령어를 실행시키면, 다음과 같은 오류 발생  
  `./bin/kafka-server-start.sh [-daemon] server.properties [--override property=value]*`
- 즉 kafka-server properties 를 옵션으로 할당해 주어야 함  
  config directory 밑에 server.properties 가 존재하는데, 이를 확인해보자
- 해당 파일을 보면 다음과 같이 property가 설정되어 있음을 확인
~~~conf
############################# Server Basics #############################
broker.id=0
num.network.threads=3
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600
############################# Log Basics #############################
log.dirs=/tmp/kafka-logs
num.partitions=1
num.recovery.threads.per.data.dir=1
offsets.topic.replication.factor=1
transaction.state.log.replication.factor=1
transaction.state.log.min.isr=1
log.retention.hours=168
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000
zookeeper.connect=localhost:2181
zookeeper.connection.timeout.ms=18000
group.initial.rebalance.delay.ms=0
~~~
- config parameter 정보
  - `broker.id` : kafka cluster 안에 여러 개의 broker 가 사용되는 경우, unique하게 설정해 주어야 함
  - `num.network.threads` : network request 받을 때, 몇 개의 thread를 사용할 것인지
  - `num.io.threads` : request 처리(disk I/O 포함)시 thread 설정 개수
  - `socket.send/receive/request.buffer/max.bytes`
  - `log.dirs` : kafka log directory
  - `num.partitions` : topic 당 log partition 수
  - `offsets.topic.replication.factor` : replication factor 수
  - `log.segment.bytes` : log segment 최대 byte 크기
  - `zookeeper.connect` : 연결할 zookeeper port
~~~shell
./bin/kafka-server-start.sh -daemon ./config/server.properties 
~~~
- kafka server 정상 작동 확인
~~~shell
netstat -an | grep 2181
~~~
- tcp46 -> 2181 port 의 server 가 정상적으로 띄어 있는 것을 확인

### Topic 만들기
- 다음의 옵션을 설정하여, topic 생성 가능
- `bootstrap-server` 설정은 클라이언트가 접근하는 토픽의 메타데이터를 요청하여 원하는 브로커를 찾기 위한 설정. 즉 broker의 host:host 정보이 리스트 형태의 값을 가짐
~~~shell
$ bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --topic first-topic --partitions 1 --replication-factor 1
~~~
- topic list 확인
~~~shell
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
~~~
- topic 세부 사항 등 확인
~~~shell
bin/kafka-topics.sh --describe --bootstrap-server localhost:9092
~~~

### Producer CLI
- kafka producer 사용해보기. producer를 사용하여 메세지를 보내보기
- 앞서 `first-topic` 으로 생성하였음. 
- 아래 진행할 내용들은 zookeeper, kafka-server(broker) 가 실행되어있고, `first-topic` 이라는 이름의 topic이 생성되어 있음을 가정
- `bin` 디렉토리 밑에 `kafka-console-producer.sh` 라는 shell이 있음  
  해당 shell로 kafka producer 생성 가능
- producer 실행/생성
~~~shell
./bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic first-topic
~~~
- 메세지를 입력하면, topic 으로 보내짐(post)
~~~
>kafka is fun 
>kafka is fun too 
~~~

### Consumer CLI
- kafka consumer 사용해보기. 
~~~shell
./bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic first-topic  
~~~
- consumer 생성 후, producer 에서 메세지를 post 하면 consumer에서 message를 받을 수 있는 것을 확인 가능

### Consumer Group CLI
- kafka의 Consumer Group 을 보기 위해서는 `kafka-consumer-groups.sh` 을 실행시켜 확인
~~~shell
./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
~~~
- 현재는 consumer-group 이 하나도 없기 때문에 나오지 않음
- consumer group을 만들어보자
~~~shell
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first-topic
~~~
- 위의 명령어를 사용하면, `console-consumer-26722` 의 결과로 컨슈머가 생성된 것을 확인 가능
- consumer group 을 따로 지정하지 않으면 unique 한 consumer group 이 생성되므로, 위의 `console-consumer-26722` 가 consumer group이 됨
- 만약 group을 명시하고 싶다면, `--group [group name]` 으로 명시해주면 됨
~~~shell
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first-topic --group first-group
~~~
- consumer의 first-group의 상세 정보를 확인하려면 `--describe group first-group` 으로 확인
~~~shell
./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group first-group
~~~

### Consumer와 Partitions
- 2개의 consumer 와(2개의 terminal 창) 2개의 producer 를 기반으로 학습해보기
- 2개의 consumer 를 동일한 group으로 묶게되면 producer 가 message 를 해당 group 으로 post 했을 때, 하나의 consumer 에만 post 됨  
그 이유는 topic 이 가지고 있는 partition 이 하나만 있기 때문. 이 partition은 반드시 한 개의 consumer 와 매핑되기때문
- 따라서 이를 방지하기 위해 partition이 여러 개여야 함  
  partition 개수가 2인 second-topic 생성
~~~shell
# topic 생성.
# 이 때, partition 의 개수를 2개 이상해야 consumer group 내에 분산 처리됨
 ./bin/kafka-topics.sh --create --topic second-topic --bootstrap-server localhost:9092 --partitions 2 --replication-factor 1
~~~
~~~shell
# producer_1
./bin/kafka-console-producer.sh --topic second-topic --bootstrap-server localhost:9092
~~~
~~~shell
# producer_2 --> producer_1 과 동일
./bin/kafka-console-producer.sh --topic second-topic --bootstrap-server localhost:9092
~~~
~~~shell
# consumer_1
./bin/kafka-console-consumer.sh --topic second-topic --bootstrap-server localhost:9092 --group second-group
~~~
~~~shell
# consumer_2
./bin/kafka-console-consumer.sh --topic second-topic --bootstrap-server localhost:9092 --group second-group
~~~

- 이렇게 되면 consumer가 message를 균등하게 받아 분산처리가 가능하게 됨 
