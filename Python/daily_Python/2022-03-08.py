# 2022-03-08
# connection pool 제작

import pandas as pd
import psycopg2 as pg2
import psycopg2
import numpy as np
from datetime import date, timedelta
import itertools
import cx_Oracle as cxo

pd.set_option("display.max_columns", 50)

# tb_m00s22_am_pred table 기반 생사 여부 판단 도출
# --> 해당 테이블의 sub_model_id, aggr_dt 를 group by 하여 count 가 1 이상인 경우 생으로 판단.
# --> ** 향후 고려 필요 사항: 예측 결과가 NaN으로 나오는 경우는 어떤 case 인지?
#        해당 case 를 판단하여 생,사 여부를 판단해야함.

# 1. mk connection pool obj
database_name = "pphmn"
user = "posrwlb"
host = "172.18.47.51"
port = "5630"
password = "hmnopen"
pool_min_conn = 1
pool_max_conn = 100

# query text
am_pred_query = """
    SELECT am_model_id, sub_model_id, TO_CHAR(pred_date, 'YYYY-MM-DD') AS date_format, COUNT(pred_value)
    FROM poswork.tb_m00s22_am_pred
    GROUP BY am_model_id, sub_model_id, date_format
    WHERE date_format BETWEEN TO_CHAR(SYS_DATE, 'YYYY-MM-DD') AND 
"""

# query_tp = 1 인 애들이 예측. 2가 실적
am_exec_hist_sql_query = """
    SELECT A.am_model_id, A.sub_model_id, A.query_tp, A.query_text
           A.source_db_type, A.source_db_id, A.source_db1, A.source_db2
           B.ip, B.port, B.database_name
    FROM poswork.tb_m00s22_am_exec_hist_sql as A 
    LEFT OUTER JOIN poswork.tb_m00s22_cm_server as B ON
    A.source_db_id = B.serv_id
    WHERE query = 1;
"""

pg_pool = pg2.pool.SimpleConnectionPool(pool_min_conn, pool_max_conn,
                                        host=host,
                                        database=database_name,
                                        user=user,
                                        password=password,
                                        port=port)

pg_connection = pg_pool.getconn()

# 2. execute query and select data to dataFrame.
try:
    with pg_connection.cursor() as cursor:
        cursor.execute(am_pred_query)
        column_names = [desc[0] for desc in cursor.description] # cursor.description 으로 column 명 가져옴

        # fetchall : 모든 데이터를 한꺼번에 클라이언트로 가져올 때 사용
        # fetchone : 한번 호출에 하나의 Row 만 가져옴
        records = cursor.fetchall()
        am_pred_df = pd.DataFrame(records, columns=column_names)

        cursor.execute(am_exec_hist_sql_query)
        column_names = [desc[0] for desc in cursor.description]

        records = cursor.fetchall()
        am_exec_hist_sql_df = pd.DataFrame(records, columns=column_names)

    cursor.close()
    pg_pool.putconn(pg_connection)

except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    if pg_connection:
        print(pg_pool.closeall)

# 3. submd_stat 에 저장하기 위한 전처리 작업 수행
am_submd_stat_df = pd.DataFrame()
am_pred_df["date_format"] = pd.to_datetime(am_pred_df["date_format"], format="%Y-%m-%d")

# 최근 한달만 filtering.
today = date.today()
today_before_month = today - timedelta(days=30)

current_day = today.strftime("%Y-%m-%d")
current_day_before_month = today_before_month.strftime("%Y-%m-%d")

# 최근 30일치 filter
am_pred_df_cur_months = am_pred_df[am_pred_df["date_format"] > current_day_before_month]
am_pred_df_cur_months.sort_values(["sub_model_id", "date_format"], inplace=True)
print(am_pred_df_cur_months)

# submd_stat table 에 insert 하기 위한 result_submd_stat 계산
am_pred_df_cur_months_distinct_by_model_id = am_pred_df_cur_months[['am_model_id', 'sub_model_id', 'date_format']] \
    .drop_duplicates()

uniq_sub_model_id = pd.unique(am_pred_df_cur_months_distinct_by_model_id.sub_model_id)
date_range = np.array(pd.date_range(start=current_day_before_month, end=current_day))

result_submd_stat = pd.DataFrame(list(itertools.product(uniq_sub_model_id, date_range)),
                                 columns=["sub_model_id", "date_format"])

result_submd_stat = pd.merge(result_submd_stat,
                             am_pred_df_cur_months_distinct_by_model_id[['am_model_id', "sub_model_id"]],
                             how="left")

result_submd_stat = pd.merge(result_submd_stat, am_pred_df_cur_months, how='left')
result_submd_stat['op_live'] = np.where(np.isnan(result_submd_stat['count'], 0, 1))

result_submd_stat.rename(columns={"date_format": "aggr_dt"}, inplace=True)
result_submd_stat["works_code"] = "P"

# save result_submd_stat.csv
result_submd_stat.to_csv("result_submd_stat.csv", sep=",")



