# 수동으로 직접 dataFrame 제작하기
import pandas as pd
df = pd.DataFrame([['2017-01-01', 'x', 1], ['2017-01-02', 'y', 2]])
print(df)

# 웹 사이트의 엑세스 로그를 정규식으로 파상히기.
import re
import pandas as pd

pattern = re.compile("^\S+ \S+ \S+ \[(.*)\] \"(.*)\" (\S+) (\S+)$")

# 일치하지 않는 행은 그냥 버림
def parse_access_log(path):
    for line in open(path):
        for m in pattern.finditer(line):
            yield m.groups()


columns = ['time', 'request', 'status', 'bytes']
pd.DataFrame(parse_access_log('access.log'), columns=columns)

df.time = pd.to_datetime(df.time, format='%d/%b/%Y/:%X', exact=True)
df.head(2)

# 파일을 csv 로 내보내기
df.to_csv('access_log.csv', index=False)
# !head -3 access_log.csv

# csv file load
import pandas as pd
df1 = pd.read_csv('access_log.csv', parse_dates=['time']) # 시간을 인덱스로 저장
df2 = df1.set_index('time')          # 시간을 인덱스로 저장
df3 = df2['1995-07-01':'1995-07-03'] # 인덱스에 의한 시간 필터링
df3.resample('1d').size()




