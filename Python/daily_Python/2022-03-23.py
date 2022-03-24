# 2022-03-23.py
# pandas read_sql function 응용
"""
pandas 의 read_sql 함수를 사용하면 query + conn object 객체를 통해 dataFrame 을 만들어 낼 수 있음
이 때, 다음과 같이 format string + params 를 통해 query binding 을 수행하여 쿼리 수행이 가능

pd.read_sql(query, con, params)

"""
import configparser
import os
import psycopg2 as pg

def get_db_config_path():
    base_dir = os.getcwd()

    start_position = base_dir.find("m00s22")
    config_path = base_dir[:start_position] + "configs"
    config_path_with_filename = config_path + "/wb_db_config.ini"
    return config_path_with_filename, config_path


def get_pool(section=None):
    config = configparser.ConfigParser()
    db_config_path_with_file, _ = get_db_config_path()

    try:
        with open(db_config_path_with_file, encoding="utf-8") as f:
            config.read(f)
    except IOError:
        raise Exception("config File does not exist")

    config = config[section]
    database, user, host, port = config["database"], config["user"], config["host"], config["port"]
    password, pool_min_conn, pool_max_conn = config["password"], config["pool_min_conn"], config["pool_max_conn"]

    pg_pool = pg.pool.SimpleConnectionPool(pool_min_conn=pool_min_conn,
                                           pool_max_conn=pool_max_conn,
                                           host=host,
                                           database=database,
                                           user=user,
                                           password=password,
                                           port=port)

    return pg_pool

def select_by_args(db_conn, query, args: dict):
    import pandas as pd

    try:
        args_tmp = args.copy()

        for key, value in args.items():
            if isinstance(value, list):
                query = query.replace(f"%({key})s", ", ".join([f"%({test})s" for test in value]))
                args_tmp[key].pop()
                args_tmp.update({v: v for v in value})
        args = args_tmp

        if not args:
            with db_conn.getconn() as db_conn:
                df = pd.read_sql(sql=query, con=db_conn)
        else:
            with db_conn.getconn() as db_conn:
                df = pd.read_sql(sql=query, con=db_conn, params=args)

        return df

    except Exception as e:
        print(e)
        raise e

"""
파이썬의 문자열 형식화(String format)
- 문자열을 형식화하는 방법은 % 기호를 사용한 방식과 format 메서드를 사용한 방식
- 그리고 f 문자열을 사용하는 방식이 있음
"""

# % 기호를 사용한 문자열 형식화
# 문자열 뒤에 % 기호를 붙이고 그 뒤에 다른 값을 붙이면 뒤에 붙은 값이 문자열 안으로 들어감

print("내 이름은 %s 입니다." % "홍길동")
print("나는 %d 살 입니다." % 12)

print("원주율의 값은 %f 입니다." % 3.141592)

print("%d 곱하기 %d는 %d 이다." % (2, 3, 6))

#  name 과 age 라는 변수에 각각 이름과 나이를 넣고 다음과 같이 출력하는 코드를 만들어라

print("%s is %d years old" % ("Tom", 13))

value = "test"
print("{value} is test".format(value=value))
print("{a} 점수:, {x} 점, {b} 점수: {y} 점".format(a="영어", b="수학", x=100, y=10))

