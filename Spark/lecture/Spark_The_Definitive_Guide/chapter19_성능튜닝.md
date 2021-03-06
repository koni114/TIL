# chapter19 성능 튜닝
- 이 장에서는 Job의 실행 속도를 높이기 위한 성능 튜닝 방법을 알아보자
- 모니터링과 마찬가지로 성능을 튜닝할 수 있는 다양한 방식이 존재함  
  예를 들어 네트워크가 엄청나게 빠른 환경이라면 가장 큰 비용이 드는 셔플 처리 시간이  
  줄어 더 빠르게 Spark Job을 처리할 수 있음
- 하지만 이러한 환경을 갖추는 것 자체가 쉽지가 않음
- 그러므로 코드나 설정 변경을 통한 성능 제어 방법을 알아야함 
- 사용자는 Spark Job의 모든 단계를 최적화 하고 싶어하는데, 그중 주요 영역을 꼽아보면 다음과 같음
  - 코드 수준의 설계(ex) RDD와 DataFrame 중 하나를 선택함)
  - 보관용 데이터
  - 조인
  - 집계
  - 데이터 전송
  - 애플리케이션별 속성
  - 익스큐터 프로세스의 JVM
  - 워커 노드
  - 클러스터와 배포 환경 속성
- Spark Job의 성능 튜닝 방법을 두 가지 유형으로 정의할 수 있음
  - 속성값을 설정하거나 런타임 환경을 변경해 간접적으로 성능을 높일 수 있음
  - 개별 Spark Job, 스테이지, 태스크 성능 튜닝을 시도하거나 코드 설계를 변경해 직접적으로 성능을 높일 수 있음 
    이 방식은 애플리케이션의 특정 영역에만 영향을 주므로 전체 Spark 애플리케이션이나 Spark Job에는 영향을 미치지 않음
- Job의 성능 향상을 확인하는 데 가장 좋은 방법 중 하나는 좋은 모니터링 도구와 잡 이력 추적 환경을 구성하는 것 
- 이력 정보가 없다면 잡의 성능이 실제로 향상되었는지 알기 어려울 수 있음

## 19.1 간접적인 성능 향상 기법
- Spark Job을 더 빠르게 실행하기 위해 할 수 있는 간접적인 성능 향상 기법이 있음
- 하드웨어 개선과 같은 뻔한 사항은 제외하며 사용자가 제어 가능한 사항을 집중적으로 알아보겠음

### 19.1.1 설계 방안
- 성능을 최적화하기 위해서는 좋은 설계 방안을 마련해야 함   
  때로는 이 단계를 무시하고 진행하는 경우가 있음
- 좋은 설계 방안으로 애플리케이션을 설계하는 것은 아주 중요함  
- 더 나은 Spark 애플리케이션을 개발할 수 있고 외부 환경이 변해도 계속해서 안정적이고  
  일관성 있게 실행할 수 있기 때문
- 앞선 몇몇 장에서 이미 설계 방안을 알아보았지만 다시 한번 되짚어보겠음

#### 스칼라 vs 자바 vs 파이썬 vs R
- 대규모 ETL 작업을 수행 후, 단일 머신에서 머신러닝을 수행하려면, python, R이 좋음
- 중요한 것은 Spark의 구조적 API는 어떤 언어에서던 비슷한 성능을 가지므로, 가장 편안하게 사용하는 언어나 상황에 따라 가장 적합한 언어를 사용하면 됨
- 만약 UDF를 사용하는 경우라면, R, Python보다 scala, java가 더 좋음  
  이유는 파이썬은 워커 노드에서 파이썬 프로세스를 실행하고, 해당 프로세스에서 데이터를 직렬화해 전송하고, 처리해 결과를 JVM에게 전달해주는 시간 자체가 더 들기 때문

#### DataFrame vs SQL vs Dataset vs RDD 
- 모든 언어에서 UDF를 사용하지 않는 이상 속도는 동일함
- 사용자가 직접 RDD 코드를 작성하는 것도받 spark의 최적화 엔진이 더 나은 RDD 코드를 만들어냄
- RDD를 사용하려면 파이썬은 사용하면 안됨. 비용도 많이 들고, 안정성까지 떨어질 수 있음

### 19.1.3 클러스터 설정
- 클러스터 설정은 큰 이점을 가져올 수 있는데, 하드웨어와 사용 환경에 따라 대응하기 어려울 수 있음
- 일반적으로 머신 자체의 성능을 모니터링 하는 것이 클러스터 설정을 최적화하는 데 가장 많이 도움이 됨

#### 클러스터/애플리케이션 규모 산정과 자원 공유
- 클러스터나 애플리케이션 수준에서 자원을 공유하는 방법에 따라 다양한 선택지가 존재함

#### 동적 할당
- Spark는 워크로드에 따라 애플리케이션이 차지할 자원을 동적으로 조절하는 메커니즘을 제공함
- 즉 사용자 애플리케이션은 더 이상 사용하지 않는 자원을 클러스터에 반환하고 필요 할 때 다시 요청할 수 있음
- 이 기능은 기본적으로 비활성화 되어 있는데, `spark.dynamicAllocation.enabled` 속성값을 `true`로 설정하면 모든 클러스터 매니저에서 사용가능

### 19.1.4 스케줄링
- 스케줄링 최적화는 연구와 실험이 필요한 영역임. 그렇기 때문에 여러 사용자가 자원을 더 효율적으로 공유하기 위해 `spark.scheduler.mode`의 속성 값을 FAIR로 설정하거나 애플리케이션에 필요한 익스큐터의 코어 수를 조정하기 위해 `--max-executor-cores` 인수를 사용하는 것 외에는 방법이 없음
- `--max-excutor-cores` 인수로 값을 설정해 사용자 애플리케이션이 클러스터 자원을 모두 쓰지 못하게 할 수 있음
- 클러스터 매니저에 따라 `spark.cores.max` 값을 설정해 기본값을 변경할 수 있음
- 클러스터 매니저는 스파크 애플리케이션의 최적화에 도움이 되는 스케줄링 설정을 제공함

### 19.1.5 보관용 데이터
- 조직의 동료들이 여러 가지 분석을 수행하기 위해 동일한 데이터셋을 여러 번 읽을 수 있음
- 프로젝트를 성공적으로 수행하려면 데이터를 효율적으로 읽어 들일 수 있도록 저장해야 함
- 그러므로 적절한 저장소 시스템과 데이터 포멧을 선택해야 함
- 데이터 파티셔닝이 가능한 데이터 포멧을 활용해야 함