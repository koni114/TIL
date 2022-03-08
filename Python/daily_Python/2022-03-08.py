# 2022-03-08
# connection pool 제작

import pandas as pd
import psycopg2 as pg2
import numpy as np
from datetime import date, timedelta
import itertools
import cx_Oracle as cxo

pd.set_option("display.max_columns", 50)

# tb_m00s22_am_pred table 기반 생사 여부 판단 도출
# --> 해당 테이블의 sub_model_id, aggr_dt 를 group by 하여 count 가 1 이상인 경우 생으로 판단.
# --> ** 향후 고려 필요 사항: 예측 결과가 NaN으로 나오는 경우는 어떤 case 인지? 


