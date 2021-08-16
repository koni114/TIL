## postgreSQL
### postgreSQL이란?
- 오픈 소스 객체-관계형 데이터베이스 시스템(ORDBMS)로, 다른 관계형 데이터베이스 시스템과 달리, 연산자, 복합 자료형, 집계 함수, 자료형 변환자, 확장 기능 등 다양한 데이터베이스 객체를 사용자가 임의로 만들 수 있는 기능을 제공

### PostgreSQL 구조
- 클라이언트/서버 모델을 사용. 서버는 데이터베이스 파일들을 관리하며 클라이언트 애플리케이션에서 들어오는 연결을 수용하고, 클라이언트를 대신하여 데이터베이스 액션을 수행
- 서버는 다중 클라이언트 연결을 처리할 수 있는데, 서버는 클라이언트의 연결 요청이 오면 각 커넥션에 대해 새로운 프로세스를 fork함
- 그리고 클라이언트는 기존 서버와의 간섭 없이 새로 생성된 서버 프로세스와 통신하게 됨

### PostgreSQL의 기능
- 관계형 DBMS의 기본적인 기능인 트랜잭션과 ACID(Atomicity, Consistency, Isolation, Durability)를 지원함
- ANSI:2008 규격을 상당 부분 만족시키고 있으며, 전부 지원하는 것을 목표로 하고 있음
- PostgreSQL은 기본적인 신뢰도와 안정성을 위한 기능 뿐만 아니라 진보적인 기능이나 학술적 연구를 위한 기능도 많이 가지고 있음. 주요 기능을 열거해보면 아래와 같음
- 주요 기능
  - Nested transactions (savepoints)
  - Point in time recovery
  - Online/hot backups, Parallel restore
  - Rules system (query rewrite system)
  - B-tree, R-tree, hash, GiST method indexes
  - Multi-Version Concurrency Control (MVCC)
  - Tablespaces
  - Procedural Language
  - Information Schema
  - I18N, L10N
  - Database & Column level collation
  - Array, XML, UUID type
  - Auto-increment (sequences),
  - Asynchronous replication
  - LIMIT/OFFSET
  - Full text search
  - SSL, IPv6
  - Key/Value storage
  - Table inheritance
- 최대 DB 크기(Database Size) : 무제한
- 최대 테이블 크기(Table Size) : 32TB
- 최대 레코드 크기(Row Size) : 1.6TB
- 최대 컬럼 크기(Field size) : 1 GB
- 테이블당 최대 레코드 개수 : 무제한
- 테이블당 최대 컬럼 개수 : 250 ~ 1600개
- 테이블당 최대 인덱스 개수 : 무제한

### PostgreSQL 특징
- Portable
  - PostgreSQL은 ANSI C로 개발되었으며, 지원하는 플랫폼의 종류는 Windows, Linux, MAC OS/X, Unix 등 다양한 플랫폼 지원
- Reliable
  - 트랜잭션 속성인 ACID에 대한 구현 및 MVCC
  - 로우 레벨 라킹 등이 구현
- Scalable
  - PostgreSQL의 멀티 비전에 대해 사용이 가능
  - 대용량 데이터 처리를 위한 Table Partitioning과 Tables Space 기능 구현이 가능
- Secure
  - DB 보안은 데이터 암호화, 접근 제어 및 감시의 3가지로 구성  
  - 호스트-기반의 접근 제어, Object-level 권한, SSL 통신을 통한 클라이언트와 네트워크 구간의 전송 데이터를 암호화 등 지원
- Recovery & Availiability
  - Streaming Replication을 기본으로 동기식, 비동기식 Hot Standby 서버를 구축 가능
  - WAL Log 아카이빙 및 Hot Back up을 통해 Point in time recovery 가능
- Advanced
  - pg_upgrade를 통해 업그레이드를 할 수 있으며, 웹 또는 C/S기반의 GUI 관리 도구를 제공하여 모니터링 및 관리는 물론 튜닝까지 가능
  - 사용자 정의 Procedural로 Perl, Java, Php 등의 스크립트 언어 지원이 가능    

### postgreSQL vs MySQL vs sqlLite 
- postgreSQL은 객체 관계형(object-relational) 데이터베이스임
- 즉 기본적으로는 관계형 데이터베이스지만 객체 데이터베이스와 연관되는 기능도 포함하고 있음  
  예를들어 테이블 상속 및 함수 오버로딩도 포함하고 있음
- 동시성(Concurrency)를 특징으로 갖고 있음. 동시에 여러 작업을 효율적으로 처리할 수 있음. ACID 준수라고도 하는 트랜잭션의 원자성(Atomicity), 일관성(Consistency), 격리성(Isolation), 내구성(Durability)를 보장하는 MVCC(Multiversion Concurrency Control) 덕분에 읽기에 대한 잠금 없이 이를 달성할 수 있음
- MySQL과 같이 숫자, 문자열, 날짜와 시간 타입을 지원. 또는 기하학적인 도형, 네트워크 주소, 비트 문자열, 텍스트 검색, JSON 항목과 몇가지 특이한 데이터 타입을 지원하기도 함
- 장점은 다른 RDBMS보다 좀 더 표준 SQL을 구현하는 것을 목표로 하고 있음

### PostgreSQL 장점
- PostgreSQL은 전체 핵심 SQL:2011 규정에 필요한 179개의 기능 중 160개를 지원
- 오픈소스 및 커뮤니티가 이끄는 DB. 완전한 오픈소스 프로젝트인 PostgreSQL의 소스코드는 대부분 커뮤니티에서 개발. 
- 확장성. 사용자는 카탈로그 기반 작업과 동적 로드 사용을 통해 PostgreSQL을 프로그래밍 방식으로 즉시 확장할 수 있음
- 데이터 무결성이 중요한 경우 RDBMS 중 PostgreSQL을 강력하게 추천함
- 다른 도구들과 통합되어야 하는 경우 적합. postgreSQL은 다양한 프로그래밍 언어 및 플랫폼과 호환
- 즉 데이터베이스를 다른 운영체제로 마이그레이션 하거나 특정 도구와 통합이 필요한 경우 다른 DBMS 보다 PostgreSQL 데이터베이스를 사용하는 것이 더 쉽게 작업할 수 있음
- 복잡한 작업 연산을 수행하는 경우 적합. 데이터웨어하우스 및 온라인 트랜잭션 처리와 같은 복잡한 작업에 적합한 선택이 될 수 있음

### PostgreSQL 단점
- PostgreSQL은 속도에 민감한 경우 적합하지 않음. PostgreSQL은 속도를 희생하며 확장성과 호환성을 염두하고 설계됨. 프로젝트에 가능한 가장 빠른 읽기 작업이 필요한 경우 PostgreSQL은 최선의 선택이 아닐 수 있음
- 간단한 설정이 필요한 경우 적합하지 않음. 광범위한 기능들과 표준 SQL에 대한 강력한 준수로 인해 PostgreSQL은 간단한 데이터베이스 설정에 대해서도 많은 작업이 필요
- 속도가 중요한 경우, MySQL이 더 실용적인 선택이 될 수 있음


### 용어 정리
- ACID
  - 데이터베이스 트랜잭션들이 안정적으로 수행된다는 것을 보장하기 위한 성질을 가리키는 약어. 
  - 원자성 ( Atomicity ) : 트랜잭션과 관련된 작업들이 모두 수행되었는지 아니면, 모두 실행이 안되었는지를 보장하는 능력.  
  ex) 자금 이체는 성공할 수도 실패할 수도 있지만, 중간 단계까지 실행되고 실패하는 일은 없도록 하는 것.
  - 일관성 ( Consistency ) : : 트랜잭션이 실행을 성공적으로 완료하면 언제나 일관성 있는 데이터베이스 상태로 유지하는 것.  
  ex) 무결성 제약이 모든 계좌는 잔고가 있어야 한다면, 이를 위반하는 트랜잭션은 중단된다.
  - 고립성 ( Isolation ) : 트랜잭션을 수행 시 다른 트랜잭션의 연산 작업이 끼어들지 못하도록 보장하는 것. 즉, 트랜잭션 밖에 있는 어떤 연산도 중간 단계의 데이터를 볼 수 없음을 의미한다.
  - 지속성 ( Durability ) : DBMS가 사용자에게 트랜잭션 커밋(commit) 응답을 했을 경우, 설사 데이터베이스 객체에 대한 해당 변경 사항이 디스크에 반영(flush) 되기 전에 시스템 장애가 발생하였더라도 해당 트랜잭션의 커밋은 보장 되어야 한다는 속성.  
  DBMS는 트랜잭션의 지속성을 제공하기 위해 로그(log)라고 하는, 즉, 데이터베이스 객체의 갱신 작업에 대한 기록을 관리한다. 커밋된 트랜잭션에 의해 갱신된 내용이 디스크에 미처 반영되기 전에 시스템 장애가 발생하면, 시스템 재 구동 시에 로그를 판독하여 변경된 내용을 복구하게 된다.  
