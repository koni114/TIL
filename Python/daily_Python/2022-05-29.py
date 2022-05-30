"""
connection pool 객체 클래스 제작
- DB Source 에 따라 별도 connector 연결
- 연결 상태를 CURRUNNING, CURCLOSED, CONNCLOSED 로 나눠 설정
- list 자료구조에 여러개의 connection pool 관리.(_pools)
  즉, _pools list 에는 _conn 과 _curs 라는 list connection pool 을 관리함
  동시에 config 정보도 list 로 관리(_configs)
"""
import os
import threading
from cx_Oracle import connect as oconnect
from impala.dbapi import connect as iconnect  # impyla package 를 설치해야함
from psycopg2 import connect as pconnect

from cx_Oracle import makedsn


os.environ["NLS_LANG"] = "AL32UTF8"  # oracle 사용시, 한글 처리를 위한 환경변수 설정

CURRUNNING = "CURRUNNING"
CURCLOSED = "CURCLOSED"
CONNCLOSED = "CONNCLOSED"

class CursorBusy(Exception):
    def __init__(self):
        super().__init__("all connections is busy !")


class ConnectionPool:
    """
        config 가 동일한 Pool 존재 시, 기존에 생성된 Pool 을 반환
        신규 cursor 를 요청시, pool-size 보다 conn 수가 작으면 신규 conn 를 생성하여 반환
    """
    _configs = []
    _pools = []

    def __init__(self, connector, config: dict, pool_size= 2, pool_name=None, autocommit=True):
        """
            supported connectors
            - impala(impala)    ==> from impala.dbapi import connect
            - oracle(cx_oracle) ==> from cx_Oracle import connect as oconnect
            - epas(EDB Postgres Advanced Server) ==> psycopg2 import connect as pconnect

        :param connector: connector object or kind of connector string name
            ex) "oracle", "impala", "epas"
        :param config: db connection config
            ex) {
                'host': '172.28.62.112',
                'port': 5447,
                'database': 'localhost',
                'user': 'testuser',
                'pwd': 'testuser'
            }
        :param pool_size: max connection pool size
        :param pool_name: connection name
        :param autocommit: is auto-commit
        """
        if isinstance(connector, str):
            c_type = connector.lower()

            if c_type in ["oracle", "cx_oracle"]:
                connector = oconnect
            elif c_type in ["impala"]:
                connector = iconnect
            elif c_type in ["epas", "ppas", "psycopg2"]:
                connector = pconnect

        # config 정보에 해당하는 pool 존재 시, pool return
        if config in ConnectionPool._configs:
            idx = ConnectionPool._configs.index(config)
            pool = ConnectionPool._pools[idx]
            self.__dict__.update(pool.__dict__)

            if pool.pool_size < pool_size:
                print(f"increase pool size {self.pool_size} -> {pool_size} "
                      f"Connection Pool({self.pool_name})")

                self.pool_size = pool_size

            msg = f"already exists connection Pool ({self.connect.__module__}, name = {self.pool_name}"
            msg += f"ip = {self.config['host']}, pool_size = {self.pool_size}"
            print(msg)
        else:
            self.__lock = threading.Lock()
            self.pool_name = pool_name if pool_name else len(ConnectionPool._configs) + 1
            self.autocommit = autocommit
            self.connect = connector
            self.module_name = self.connect.__module__  # psycopg2, cx_Oracle, impala
            self.config = config
            self.pool_size = pool_size
            self.conns = []  # connection 객체
            self.curs = []  # cursor 객체
            ConnectionPool._configs.append(self.config)
            ConnectionPool._pools.append(self)
            msg = f"create new ConnectionPool ({self.connect.__module__}, {self.pool_name}, )"
            msg += f"ip = {self.config['host']} pool_size = {self.pool_size}"
            self.pool_log_level = "MORE"  # 원래는 logging -> MORE object 이어야함
            self.set_conn_logging_level()

    def set_conn_logging_level(self, level="WARNING"):
        """
            connector 의 logging level 변경

        :param level: INFO, WARNING, ERROR, MORE, DETAIL 중 하나 입력
        :return:
        """
        pass

    def set_pool_logging_level(self, level):
        """
            connection pool 의 logging level 변경

        :param level: logging level, DEBUG, MORE, DETAIL, INFO, WARNING ...
        :return:
        """
        self.pool_log_level = level

    def _close_conn(self, idx: int):
        """
            conn 객체의 커서를 close 하는 함수
        :param idx: conns list index
        """
        try:
            self.conns[idx].close()
        except Exception as e:
            print(f"{idx}th conn close failed")

    def _create_conn(self, idx=None):
        """
            conn 객체 생성해주는 함수
        :param idx: conns list index
        :return:
        """
        self._close_conn(idx)
        if self.module_name == "cx_Oracle":
            config = self.config
            dsn_tns = makedsn(config["host"], config["port"], service_name=config["database"])
            conn = self.connect(user=config["user"], password=config["pwd"], dsn=dsn_tns)
        else:
            conn = self.connect(** self.config)

        return conn

    def status_curs(self):
        """
            connection pool 의 cursor 의 상태를 반환해주는 함수
        :return:
            cursor 의 상태 반환
        """
        curs_size = len(self.curs)
        stats = [self._status_cur(idx) for idx in range(curs_size)]
        print(f"cursors status = ({curs_size}{stats})")
        return stats

    def __status_cur_psycopg2(self, idx):
        """
            psycopg2 상태 확인
        :param idx: conns list index
        :return:
            CONNCLOSED, CURCLOSED, CURRUNNING 중 하나 반환
        """
        if self.conns[idx].closed:
            return CONNCLOSED
        if self.curs[idx].closed:
            return CURCLOSED
        return CURRUNNING

    def __status_cur_oracle(self, idx):
        """
            Oracle 상태 확인
        :param idx: conns list index
        :return:
        """
        try:
            self.conns[idx].ping()
        except Exception as e:
            print(f"{idx}th conn ping failed | {e.__class__.__name__} | {e}")
        return CONNCLOSED

    def __status_cur_impala(self, idx):
        """
            impala 상태 확인(테스트 필요)
        :param idx:  conns list index
        :return:
            CONNCLOSED, CURCLOSED, CURRUNNING 중 하나 반환
        """
        cur = self.curs[idx]
        try:
            if cur._closed:
                cur.close()
                return CURCLOSED
            else:
                return CURRUNNING
        except Exception as e:
            print(f"{idx}th cursor | {e.__class__.__name__} | {e}")
        return CONNCLOSED

    def _status_cur(self, idx):
        """
            None, CURRUNNING, CURCLOSED, CONNCLOSED
        :param idx: conns list index
        :return:
            None, CURRUNNING, CURCLOSED, CONNCLOSED 중 하나 반환
        """
        if len(self.conns) < idx + 1:
            return None
        if self.module_name == "psycopg2":
            return self.__status_cur_psycopg2(idx)
        if self.module_name == "cx_Oracle":
            return self.__status_cur_oracle(idx)
        if self.module_name == "impala":
            return self.__status_cur_impala(idx)

    def __get_cursor(self):
        for idx in range(self.pool_size):
            stat = self._status_cur(idx)
            if stat is None:
                self.conns.append(self._create_conn())
                self.curs.append(self.conns[idx].cursor())
                return self.curs[idx]

            if stat == CONNCLOSED:
                self._create_conn(idx)

            if stat == CURCLOSED:
                self.curs[idx] = self.conns[idx].cursor()
                return self.curs[idx]
        raise CursorBusy

    def cursor(self):
        self.__lock.acquire()
        try:
            cur = self.__get_cursor()
            if self.module_name == "cx_Oracle":
                cur.arraysize = 5000
            self.__lock.release()
            return cur
        except Exception as e:
            print(f"failed get cursor {self.connect.__module__}/{self.pool_name} {self.status_curs()} | {e}")
            if self.__lock.locked():
                self.__lock.release()
            raise e

    def execute(self, query, fetch=False):
        try:
            with self.cursor() as cur:
                cur.execute(query)
                if fetch:
                    rslt = cur.fetchall()
                    return rslt
            return True
        except Exception as e:
            print(f"{e.__class__.__name__}")
            return False

    def close(self):
        """
            remove connection pool
        :return:
        """
        for idx in range(len(self.curs)):
            self._close_conn(idx)
            ConnectionPool._configs.remove(self.config)
            ConnectionPool._pools.remove(self)
















































