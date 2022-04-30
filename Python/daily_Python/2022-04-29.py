# 2022-04-29.py
# datetime 라이브러리 활용 정리
import datetime
import pytz


# 1. 현재 날짜와 시간 출력하기
datetime_object = datetime.datetime.now()  # datetime.datetime

# datetime 객체를 print 하면 %Y-%m-%d %H:%M:%S.%ms
print(datetime_object)
print(f"datetime_object type --> {type(datetime_object)}")
datetime_object.strftime("%Y-%m-%d")

# 2. 현재 날짜(%Y-%m-%d) 출력하기
date_object = datetime.date.today()
print(f"date_object type --> {type(date_object)}")
print(date_object)

# 3. datetime 내부 class 알아보기
print(dir(datetime))

# datetime 모듈 내에 공통 클래스
# - date Class
# - time Class
# - datetime Class
# - timedelta Class

# 3.1 date Class
# date class 에서 date object 를 인스턴스화 할 수 있음.
d = datetime.date(2022, 4, 29)
print(d)

# 3.2 현재 날짜 추출
today = datetime.date.today()
print(f"Current date = {today}")

# 3.3 timestamp 로부터 date 추출
timestamp = datetime.date.fromtimestamp(1326244364)
print(f"Date = {timestamp}")

# 3.4 year, month, day 추출
print(f"Current year: {today.year}")
print(f"Current month: {today.month}")
print(f"Current day: {today.day}")

# 4.1  time Class
# time class 를 사용해서 객체를 인스턴스화 할 수 있음
a = datetime.time()
print(f"a = {a}")

b = datetime.time(11, 34, 56)
print(f"b = {b}")

c = datetime.time(hour=11, minute=34, second=56)
print(f"c = {c}")

d = datetime.time(hour=11, minute=34, second=56, microsecond=234566)
print(f"d = {d}")

# 5.1 datetime Class
# datetime class 를 사용해서 객체를 인스턴스화 할 수 있음

# 5.2 datetime(year, month, day)
a = datetime.datetime(2018, 11, 28)
print(a)

# 5.3 datetime(year, month, day, hour, minute, second, microsecond)
b = datetime.datetime(2017, 11, 28, 23, 55, 59, 342380)
print(b)

# 5.4 year, month, hour, minute and timestamp
a = datetime.datetime(2022, 4, 29, 23, 55, 59, 342380)
print(f"Current year: {a.year}")
print(f"Current month: {a.month}")
print(f"Current hour: {a.hour}")
print(f"Current minute: {a.minute}")
print(f"Current timestamp: {a.timestamp()}")

# 6. datetime.timedelta
# - 두 date/times 의 차이를 계산하기 위한 class

# 6.1 두 date/times 사이이 차이 계산
t1 = datetime.date(year=2022, month=4, day=10)
t2 = datetime.date(year=2022, month=3, day=23)

t3 = t1 - t2
print(f"t3 = {t3}")
print(f"type of t3 = {type(t3)}")  # datetime.timedelta type 임을 확인

# 6.2 두 timedelta 객체의 차이를 계산
t1 = datetime.timedelta(weeks=2, days=5, hours=1, seconds=33)
t2 = datetime.timedelta(days=4, hours=11, minutes=4, seconds=54)
t3 = t1 - t2
print(f"t3 = {t3}")

# 6.3 timedelta 객체의 negative 출력.
t4 = t2 - t1
print(f"t4 = {t4}")

# 6.4 seconds 내 Time duration
t = datetime.timedelta(days=5, hours=1, seconds=33, microseconds=233423)
print(f"total seconds = {t.total_seconds()}")

# + 연산자를 사용하여 두 날짜와 시간의 합을 찾을 수도 있음.
# 또한 timedelta 객체를 정수와 부동 소수점으로 곱하고 나눌 수 있음.

# 7. format datetime
# -->  strftime(), strptime() 를 통해 날짜 형식 변경 가능
# strftime() : datetime -> 문자형으로 변경
# strptime() : 문자형     -> datetime 으로 변경
# - 미국은 보통 mm/dd/yyyy
# - 영국은 보통 dd/mm/yyyy
# - 한국은 보통 yyyy-mm-dd

# strftime() : datetime -> 문자형으로 변경
now = datetime.datetime.now()
t = now.strftime("%H:%M:%S")
print(f"time : {t}")

s1 = now.strftime("%m/%d/%Y, %H:%M:%S")
print(f"s1 : {s1}")

s2 = now.strftime("%d/%m/%Y, %H:%M:%S")
print("s2:", s2)

# strptime() : 문자형     -> datetime 으로 변경
# strptime() 메소드는 2개의 argument 가 있음
# - 날짜와 시간을 나타내는 문자열
# - 첫 번째 인수와 동일한 형식 코드
date_string = "21 June, 2018"
print("date_string =", date_string)

date_object = datetime.datetime.strptime(date_string, "%d %B, %Y")
print(f"date_object = {date_object}")

# 8. Handling timezone
local = datetime.datetime.now()
print(f"Local: {local.strftime('%m/%d/%Y, ')}")

# 8.1 America/New_York
tz_NY = pytz.timezone("America/New_York")
datetime_NY = datetime.datetime.now(tz_NY)
print(f"NY: {datetime_NY.strftime('%m/%d/%Y, %H:%M:%S')}")
