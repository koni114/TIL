## Part2 - Apache Spark와 데이터 병렬 - 분산처리
### 기초 환경 설정
- 필요한 환경 & 패키지
  - 파이썬
  - 주피터 노트북
  - 자바
  - Spark
  - Pyspark
- Anaconda 사이트에서 일괄적으로 설치가 가능

### 모빌리티 데이터 
- TLC Trip Record Data
  - 10+년 이상의 택시와 모딜리티 서비스 기록  
    2009년부터 2021년까지 모든 기록이 공개
- 매년 20GB씩 쌓이는 Dataset   
  승차와 하차 시간과 장소, 소요시간, 택시비와 같이 중요한 데이터를 포함
- 다운로드 URL  
  https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- 2020년도 3월 데이터 중 High Volume For-Hire Vehicle Trip Records (CSV) 데이터를 다운
- 해당 데이터는 Uber 등 대형 택시 운영 기업

#### 데이터 컬럼 확인
- `hvfhs_license_num` : high volume for hire service license
  - HV0002: Juno
  - HV0003: Uber
  - HV0004: Via
  - HV0005: Lyft
  - Uber 와 lyft 회사가 90% 이상임. Juno, via는 minor 함 
- `dispatching_base_num` : 어느 장소에서 dispatch 되는지
- `pickup_datatime` : 승객 승차 시간
- `dropoff_datetime` : 승객 하차 시간
- `PULocationID` : Pick Up Location ID
- `DOLocationID` : Drop off Location ID
- `SR_Flag` : Shared Riding 여부, 1.0 --> Yes, NaN(Not a Number) --> No
- mobility 데이터에 관심이 많은 경우는 Uber Movements Dataset 사용 권장  
  관공서나 연구를 위한 licence가 있음

#### 환경 셋팅
- [github.com/keon](https://github.com/keon/data-engineering) 에는 앞으로 사용할 코드들이 들어가 있음
- 해당 코드를 다운로드 받고, data-engineering 폴더에 data 폴더를 생성하고, 다운로드 받은 파일을 넣으면 됨