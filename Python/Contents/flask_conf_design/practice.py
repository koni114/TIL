import os
import sys
from libs.util.common import AppInfo
import time
import datetime

app_info = AppInfo()
app_info.app_dir()
app_info.app_full_name()
app_info.app_name()

for i in range(10):
    print(i)
    time.sleep(1)

