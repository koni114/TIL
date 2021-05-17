import os,time
os.environ['TZ'] = 'KST-09' # -는 본초자오선 동쪽을 뜻함
time.tzset()

import time

now = 159823184
local_tuple = time.localtime(now)
time_format = '%Y-%m-%d %H:%M:%S'

#- strftime --> UTC time -> current time
time_str = time.strftime(time_format, local_tuple)
print(time_str)

#- strftime --> current time -> UTC time
time_tuple = time.strptime(time_str, time_format)
utc_now = time.mktime(time_tuple)
print(utc_now)

import os
parse_format = '%Y-%m-%d %H:%M:%S %Z'  # %Z는 시간대를 뜻함
depart_icn = '2020-08-27 19:13:04 KST'
time_tuple = time.strptime(depart_icn, parse_format)
time_str = time.strftime(time_format, time_tuple)
print(time_str)

arrival_sfo = '2020-08-28 04:13:04 PDT'
time_tuple = time.strptime(arrival_sfo, time_format)