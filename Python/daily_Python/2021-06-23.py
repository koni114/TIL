# datetime 완전 정복하기
#- 이 라이브러리를 활용하여 현재 시간을 구하거나, 특정 시간 포맷의 문자열 반환 가능
#- 다음의 내용을 알아보자

#- 1. 현재 날짜 및 시간
#- 2. 현재 날짜
#- 3. date, datetime 객체 생성
#- 4. Timestamp 로 date, datetime 객체 생성
#- 5. date 객체의 year, month, day
#- 6. time 객체 생성
#- 7. timedelta
#- 8. 특정 시간 형식으로 반환
#- 9. 문자열을 datetime 객체로 반환

#- 1. 현재 날짜 및 시간
#- now()는 현재 날짜, 시간 정보를 갖고 있는 datetime 객체를 생성
import datetime
datetime_object = datetime.datetime.now()
print(datetime_object)
print(type(datetime_object))

#- 2. 현재 날짜
#- today()는 현재 날짜 정보를 갖고 있는 date 객체 생성
date_object = datetime.date.today()
print(date_object)
print(type(date_object))

#- 3. date, datetime 객체 생성
#- 특정 날짜 정보를 갖고 있는 datetime 객체를 직접 생성할 수도 있음
d = datetime.datetime(2021, 6, 23, 11, 9, 30)
print(d)

a = datetime.date(2019, 1, 1)
print(a)

#- 4. Timestamp 로 date, datetime 객체 생성
#- Timestamp 는 1970/01/01(UTC)로부터 어떤 시간까지의 초를 계산 한 것
#- fromtimestamp 의 인자로 timestamp 를 전달하면 이것에 해당하는 date, datetime 객체가 생성됨

from datetime import date
from datetime import datetime

date_obj = date.fromtimestamp(1602374400)
print("Current Date =", date_obj)

datetime_obj = datetime.fromtimestamp(1602374400)
print("Current datetime =", datetime_obj)

#- 5. date 객체의 year, month, day
#- 다음과 같이 date 객체에서 year, month, day 값을 가져올 수 있음
from datetime import date
today = date.today()
print("year:", today.year)
print("month:", today.month)
print("day:", today.day)

#- 6. time 객체 생성
#- time()은 인자로 전달된 값으로 time 객체를 생성함
from datetime import time
a = time()
print("a =", a)
print(type(a))

b = time(15, 25, 30)
print("b = ", b)

c = time(hour=11, minute=21, second=30)
print("c = ", c)

d = time(15, 25, 30, 123456)
print("d = ", d)

from datetime import time

a = time(15, 25, 30)

print("time =", a)
print("hour =", a.hour)
print("minute =", a.minute)
print("second =", a.second)
print("microsecond =", a.microsecond)

#- 7. timedelta
#- 두 개의 시간 차이를 나타냄
from datetime import datetime, date
time1 = date(year=2020, month=10, day=11)
time2 = date(year=2018, month=11, day=22)
time_delta = time1 - time2
print("time_delta :", time_delta)

#- 8. 특정 시간 형식으로 반환
#- strftime 는 datetime 객체를 원하는 시간 형식으로 변환하고, 그 결과를 문자열로 리턴
from datetime import datetime
now = datetime.now()

format_time = now.strftime("%H:%M:%S")
print("time : ", format_time)

format_time = now.strftime("%m/%d/%Y, %H:%M:%S")
print("time : ", format_time)

# 9. 문자열을 datetime 객체로 반환
# strptime 은 문자열로 표현된 시간을 datetime 객체로 반환
from datetime import datetime

date_str = "11 October, 2020"
datetime_obj = datetime.strptime(date_str, "%d %B, %Y")
print("date = ", datetime_obj)
print(type(datetime_obj))

pd.read_csv('./test_data/sampledata/')


##
