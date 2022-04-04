import os
import sys
from libs.util.common import AppInfo
import time
import datetime
from dateutil.parser import parse

date = "2022-04-01 10:20:30"
parsing_date = parse(date)

print(parsing_date)

datetime.datetime.now()