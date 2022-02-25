# boto3 정리
## boto3란? 
- AWS 서비스와 쉽게 통합할 수 있도록하는 Python 용 SDK
- Python 어플리케이션을 S3, DynamoDB, SQS 및 많은 서비스와 통합 가능
(데이터 저장, 검색, 삭제등 기본 CRUD 작업 수행)
- 객체 지향 API와 AWS 서비스에 대한 low-level/high-level access 제공

## boto3 특징
### resource API
- 두 가지 수준(Client, Resource)의 API 제공

#### Client(low-level) API
- Low-level 인터페이스
- service description에 의해서 만들어짐
- botocore 수준의 client를 공개(botocore는 AWS CLI와 boto3의 기초가 되는 라이브러리)
- AWS API와 1:1 매핑됨

#### Resource(high-level) API
- high-level 인터페이스
- resource description에 의해 만들어짐
- 식별자(identifier)와 속성(attribute)를 사용
- <b>자원에 대한 조작 위주</b>

#### Client API vs Resource API
- boto3.resource 는 boto3.client를 wrapping 한 high-level 인터페이스이지만 boto3.client 의 모든 기능을 wrapping 하지는 않기 때문에 둘 다 동시에 사용해서 작업해야 하는 경우가 생길 수 있음

#### 사용 example
~~~python
# client example 
import boto3

BUCKET_NAME = 'mybucket'
client = boto3.client('s3')
response = client.list_objects(Bucket=BUCKET_NAME)

for content in response['Contents']:
    obj_dict = client.get_object(Bucket=BUCKET_NAME, key=content['Key'])
    print(content['Key'], obj_dict['LastModified'])

# resource example
BUCKET_NAME = 'mybucket'
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)

for obj in bucket.objects.all():
    print(obj.key, obj.last_modified)
~~~


### 자원 접근을 통한 접근 증명 구조
- 자원에 대한 다음의 우선순위로 접근 증명
- '1. `client/resource/Session` 에 전달되는 자격 증명 정보
  - `client`, `resource` 함수에서 자격 증명 데이터를 매개변수로 전달함
  - 시스템 설정을 무시하고, 자격 증명 데이터를 직접 전달하는 경우에 해당
~~~python
import boto3

ACCESS_KEY = '...'
SECRET_KEY = '...'
SESSION_TOKEN = '...'

client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN
)

s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN
)
~~~  
- '2. 환경 변수
  - client, resource, Session에 자격 증명 정보가 인자로 전달되지 않으면 환경 변수 확인  
  - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` 의 변수 확인
- '3. `AWS_SHARED_CREDENTIALS_FILE`에 명시된 파일 또는 `~/aws/credentials`에 접근
  - 다음부터는 파일에 접근하기 시작함. 공유 자격 증명 파일의 기본 위치는 `~/aws/credentials`
  - `AWS_SHARED_CREDENTIALS_FILE` 환경 변수를 설정하여 위치 변경 가능
  - credentials은 `.ini` 형식의 파일이며, 각 섹션마다 자격 증명을 위한 세 가지 변수를 지정
  - 섹션 각각을 <b>profile</b>(아래 예시에서는 default, dev, prod)이라고 부름. session을 생성할 때 `AWS_PROFILE` 환경 변수를 설정하거나 `profile_name` 인자에 이름을 전달하여 어떤 profile 을 사용할 지 명시할 수 있음
~~~ini
[default]
aws_access_key_id=foo
aws_secret_access_key=bar

[dev]
aws_access_key_id=foo2
aws_secret_access_key=bar2

[prod]
aws_access_key_id=foo3
aws_secret_access_key=bar3
~~~
- 여기서 <b>session은 client나 resource를 생성할 수 있도록 자격 증명에 대한 '상태'를 저장하고 있는 객체 </b>
~~~python
import boto3

session = boto3.Session(profile_name='dev')
dev_d3_client = session.client('s3')
~~~
- 별도로 명시하지 않으면, `[default]` profile을 사용. 보통 이렇게 credential를 사용하는 방식을 쓰는 것 같음

- '4. AWS Config 파일
  - 기본 위치는 `~/.aws/config`이고, `AWS_CONFIG_FILE` 환경 변수를 설정하여 위치를 변경할 수 있음
  - config 파일은 credentials 파일과 동일하게 작성됨  
    차이점은 `[profile[name]]` 포맷으로 표현한다는 것임
~~~ini
[default]
aws_access_key_id=foo
aws_secret_access_key=bar

[profile dev]
aws_access_key_id=foo2
aws_secret_access_key=bar2

[profile prod]
aws_access_key_id=foo3
aws_secret_access_key=bar3
~~~
- `AWS_CONFIG_FILE` 환경 변수에 명시된 파일이나, `~/aws/config`에 접근하여 role에 대한 정보를 명시하여, boto3가 자동으로 AWS STS에 AssumeRole을 호출하도록 할 수 있음
- `role_arn`, `source_profile`, `session_name` 등의 파라미터 필요
~~~ini
[profile crossaccount]
role_arn=arn:aws:iam:...
source_profile=development
~~~
- '5. boto2 config 파일 
  - 그 후에는 boto2 config 파일에서 자격 증명 로드
  - `BOTO_CONFIG` 환경 변수가 나타내는 경로의 파일을 먼저 검사하고, 그렇지 않으면 `/etc/boto.cfg`와 `~/boto` 파일 검사. `[Credentials]` 섹션만 사용
~~~ini
[Credentials]
aws_access_key_id = foo
aws_secret_access_key = bar
~~~
- '6. IAM Role
  - 위의 방법들로 자격 증명을 찾지 못한 경우, boto3 는 EC2 인스턴스의 메타 데이터 서비스에서 자격 증명 로드
  - EC2 인스턴스를 시작할 때 사용할 IAM role만 지정하면, 별도의 명시적인 구성을 하지 않아도 boto3가 알아서 인스턴스의 자격 증명을 시도 
- EC2 인스턴스에서 boto3 를 사용하는 경우, `IAM role`을 사용하는 것이 좋고, 그렇지 않은 경우라면 공유 자격 증명 파일을 쓰는 것이 좋다고 함

## boto3 사용 가능한 resource 
- 대부분의 AWS 서비스들의 resource를 boto3 로 사용 가능함  
  작업 가능한 resoruce list는 boto3 documentation 참조
- cloudformation : AWS 리소스 자동 생성해주는 서비스
- cloudwatch : AWS 모니터링
- dynamodb: NoSQL DB
- ec2: 컴퓨팅 용량 제공 웹 서비스
- glacier: 데이터 보관 및 장기 백업 storage class
- iam: AWS 리소스에 대한 엑세스 제어 웹 서비스
- opsworks: Chef 및 Puppet의 관리형 인스턴스를 제공하는 구성 관리 서비스
- s3: Object storage
- sns: 메세지 전송 관리 서비스 
- sqs: simple queue 서비스
- ... 

## boto3 주요 함수
- `boto3.client`, `boto3.resource`
- `boto3.Session`: client & resource 서비스 생성을 위해 사용
- `boto3.Bucket` : S3에 저장된 특정 bucket에 접근하기 위해 사용
- `boto3.Object`: bucket에 저장된 객체에 접근하기 위해 사용
- `boto3.resource('s3').meta.cilent.upload_file` : file upload
- `boto3.resource('s3').meta.cilent.download_file` : file download

## boto3 Notice
- On 2021-01-15, deprecation for Python 2.7 was announced and support was dropped on 2021-07-15. 
- On 2022-05-30, we will be dropping support for Python 3.6. This follows the Python Software Foundation end of support for the runtime which occurred on 2021-12-23.


## boto3 관련 참고 블로그 
[Boto3 자격 증명 정보](https://planbs.tistory.com/entry/client%EB%82%98-resource%EC%97%90-access-key-id-secret-access-key%EB%A5%BC-%EC%A7%81%EC%A0%91-%EC%A0%84%EB%8B%AC%ED%95%98%EA%B8%B0)  
[Boto3 source code from git](https://github.com/boto/boto3)  
[Boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)  