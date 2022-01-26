## chapter01 Kafka 소개
### Kafka에 대해서 알아보자
- 분산 데이터 스트리밍 플랫폼

#### 전통적인 아키텍처
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_27.png)

- 시스템 B가 시스템 A로부터 데이터를 요청할 때, 동기 방식의 경우는 request 수행 시, response 가 올 때까지 기다리는 방식을 취함  
  이는 REST API 방식과 같은 방법을 사용
- 만약 Async 방식을 사용해야 하는 경우에는 Message Queue 를 이용하거나 Batch Processing 을 사용
- 이 때 A, B 시스템에 데이터가 쌓이게 되면 이를 Data Lake에 저장함(pipeline)
- 시스템 C를 새로 만들게 되면, B로 데이터를 전송하는 연결고리를 만들어 주어야 하며, 마찬가지로 Data Lake 에 저장해 주어야 함

#### 전통적인 아키텍처의 문제점
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_28.png)

- 시스템을 더할수록 기하급수적으로 복잡해짐
- 여러가지 통신 프로토콜을 지원해야 함(HTTP, gRPC, TCP, MQ)
- 데이터 포멧도 다름(CSV, JSON, XML)
- <b>Point-of-failure 가 많음</b>
- 예를 들어 시스템 A, B, C, D, E, F 각각의 신뢰도가 99% 일 때, 해당 시스템을 묶었을 때의 신뢰도는 99% ^ 6 = 94.1%
- 또한 연결고리 상에서 어디서 에러가 나는지 모니터링하기가 매우 어려움

#### Kafka 소개
- LinkedIn에서 개발, Apache Software 로 넘오가 2011년 오픈소스화
- Apple, eBay, Uber, AirBnB, Netflix 등에서 사용중
- 분산 스트리밍 플랫폼
  - Source 시스템은 kafka로 메세지를 보내고
  - Destination 시스템은 Kafka로부터 메세지를 받음 
- 확장성이 있고, 장애 허용(fault tolerant) 하며, 성능이 좋음  

#### Kafka 이용한 아키텍처
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_29.png)
- 시스템간 의존성을 간접적으로 만듬
- 확장성: 새 시스템을 더할 때마다 복잡도가 선형적으로 올라감
- kafka를 이용해 통신 프로토콜을 통합하기 쉬움

#### kafka의 장점들
- 확장성: 하루에 1조개의 메세지를 처리할 수 있음. Petabyte의 데이터를 처리 가능
- 메세지 처리 속도 - 2MS
- 가용성(avaliability) - 클러스터 환경에서 작동
- 데이터 저장 성능 - 분산 처리, 내구성, 장애 허용(fault tolerant)

#### Kafka 사용 예
- 시스템간 메세지 큐
  - consumer 의 처리속도는 매우 낮은데, producer 데이터 제공 속도는 매우 빠른 경우, 
    queue 에 쌓아두고 순차적으로 처리하는 경우
- 로그 수집
  - MSA에서 발생하는 로그를 kafka를 사용해서 로그 처리 
- 스트림 프로세싱 
- 이벤트 드리븐 기능들
- Netflix: 실시간 모니터링
- Expedia: 이벤트 드리븐 아키텍처
- Uber: 실시간 가격 조정, 실시간 수요 예축

### Kafka의 구조
#### Kafka의 구성
- Topic
- Kafka Broker
- Kafka Producer
- Kafka Consumer
- Kafka Partition
- Kafka Message
- Kafka Offset
- Kafka Consumer Group
- Kafka Cluster
- Zookeeper

#### Kafka를 이용한 아키텍처
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_30.png)

#### Kafka Topic
- 하나의 channel 이나 folder 라고 볼 수 있음
- producer 와 consumer 가 소통을 하는 하나의 채널
- topic 은 데이터 스트림이 어디에 Publish 될지 정하는데 쓰임
  - topic 은 file system의 directory 의 개념과 유사 
- Producer 는 topic을 지정하고 메세지를 게시(post)
- Consumer는 topic으로부터 메세지를 받아옴
- kafka의 메세지는 디스크에 정렬되어 저장되며, 새로운 메세지가 도착하면 지속적으로 로그에 기록

#### Kafka Broker
- Topic 은 broker 로 부터 serving이 됨

#### Kafka Producer & Consumer
- Producer 는 Message 를 topic 으로 보내는 역할을 하는 클라이언트 어플리케이션   
  메세지를 어느 파티션에 넣을지 결정(key)
- Consumer 는 메세지를 소비하는 역할 수행(클라이언트 어플리케이션)

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_36.png)

- Consumer는 따로 group을 지정하지 않으면 독립적인 새로운 consumer group이 생성됨
- 각 counsumer group 은 모든 파티션으로부터 데이터를 받을 수 있고, consumer는 지정된 파티션으로부터 데이터를 받을 수 있음  
- 위의 그림에서 Consumer group 1 은 P1, P2, P3, P4 의 데이터를 받을 수 있으며, 각각 consumer1, consumer2 는 지정된 데이터(p1, p3), (p2, p4) 만 받을 수 있음
- 또한 partition 을 consumer에게 균등하게 배분하기 위하여 <b>rebalancing</b> 수행


#### Kafka Partition
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_31.png)

- kafka 의 topic 은 partition 으로 나뉘게 됨
- partition 은 disk 에 어떻게 저장이 되는지 가르는 기준이 됨
- 카프카의 토픽은 파티션의 그룹이라고 볼 수 있음
- 디스크에는 파티션 단위로 저장
- 파티션마다 commit log 가 쌓이게 됨
- 파티션에 쌓이는 기록들은 정렬이 되어 있고 불변(immutable)함
- 파티션의 모든 기록들은 Offset 이라는 ID를 부여 받음

#### kafka Message & offset
- message 는 kafka가 가지는 실제 데이터를 의미하며, 이 때 정렬 순서 메타 정보를 offset 이라고 함
- message 는 Byte의 배열
- 흔히 단순 String, JSON, Avro 사용
- Avro 은 타입이 있는 JSON 이라고 보면 됨 
- 카프카 메세지의 크기에는 제한이 없음
- 하지만 성능을 위해 작게 유지하는 것을 추천
- 데이터는 사용자가 지정한 시간만큼 저장함(Retention Period)
- Topic 별로 지정도 가능
- Consumer 가 데이터를 받아가고 나서도 데이터는 저장됨
- Retention Period 가 지나면 자동으로 삭제  
  만약 retention period 가 지난 데이터의 경우, Data lake 에서 확인이 필요 

#### Kafka Consumer group
- 여러 개의 consumer 가 모여 group 을 형성할 수 있음


#### Kafka cluster
- kafka 는 고가용성과 확장성을 위해 cluster 형성

#### Zookeeper
- kafka 의 여러 요소들을 설정하고 정하는데 사용됨

### kafka Cluster
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_32.png)

- 카프카 클러스터는 여러개의 카프카 브로커(서버)를 가질 수 있음
- 카프카 토픽을 생성하면 모든 카프카 브로커에 생성됨
- 카프카 파티션은 여러 브로커에 걸쳐서 생성

#### Key가 없는 Messages
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_33.png)

- Producer가 메세지를 게시하면 메세지가 key가 없는 경우 Round-Robin 방식으로 파티션에 분배됨
 
#### Key가 있는 Messages
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_34.png)

- 같은 key를 가지는 메세지들은 같은 파티션에 보내지게 됨

#### Replication Factor
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_35.png)

- kafka cluster 에는 Replication factor 를 지정할 수 있음
- Replication factor 는 동일한 partition을 몇 개의 Topic 에 저장할 것인가를 의미함.   
  예를 들어 factor가 2인 경우, 2개의 topic에 동일한 partition 이 저장되게 됨
- 위의 그림은 broker가 3, replication factor가 2인 경우에 해당 
- partition이 망가져도, 모든 parition 을 온전히 messaging 하게 됨

#### Partition leader
- 각 브로커는 복제된 파티션중 대표를 하는 파티션 리더를 가지게 됨
- 모든 Read/Write 는 파티션 리더를 통해 이루어지게 됨
- 다른 파티션들은 파티션 리더를 복제
 
### kafka zookeeper
- Consumer와 통신, 메타데이터 정보 저장, 카프카 상태관리
- zookeeper는 분산 시스템
  - 분산 시스템간의 정보 공유, 상태 체크, 서버들 간의 동기화
  - 분산 시스템의 일부이기 때문에 동작을 멈춘다면 분산 시스템에 영향을 미치므로, 클러스터로 구성됨
  - 클러스터는 홀수로 구성되어 문제가 생겼을 경우 과반수가 가진 데이터를 기준으로 일관성 유지 
- zookeeper가 하는 일
  - 클러스터 관리: 클러스터에 존재하는 브로커를 관리하고 모니터링
  - Topic 관리: 토픽 리스트를 관리하고 토픽에 할당된 파티션과 Replication 관리
  - 파티션 리더 관리: 파티션의 리더가 될 브로커를 선택하고, 리더가 다운될 경우 다름 리더를 선택
  - 브로커들끼리 서로를 발견할 수 있도록 정보 전달

### kafka 설치
- `bin` 폴더 안에 있는 bash shell이 실제 사용할 shell
- `window` 에서는 `bat` 파일을 사용하면 됨
- 예를 들어, kafka 를 실행하고 싶으면, `kafka-server-start.sh` 파일 실행