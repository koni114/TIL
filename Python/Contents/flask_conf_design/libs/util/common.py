
import os
import sys, threading, queue, copy, json, socket
from functools import wraps
from pytz import timezone
from libs.util.logger import getLogger, get_caller, INFO, WARNING, ERROR, MORE, DETAIL, DEBUG
import subprocess

logger = getLogger()

KST = timezone('Asia/Seoul')


def join_dir(*dirs):
    """
    :param dirs: join 하고자 하는 path
    :return: joined path
    """
    return os.path.join(*dirs)


class AppInfo:
    """
    현재 실행 중인 애플리케이션의 경로.
    애플리케이션 명을 관리하기 위한 클래스
    """
    __app_dir = None
    __app_fullname = None

    def __init__(self, app_dir=None, app_fullname=None):
        """
        :param app_dir: 애플리케이션 경로
        :param app_fullname: 애플리케이션 full 경로
        """
        self.app_dir(app_dir)
        self.app_full_name(app_fullname)

    @staticmethod
    def current_dir():
        return os.getcwd()

    def app_dir(self, app_dir=None):
        """
            application 을 실행하고자 하는 python script 를 기반으로
            해당 script 의 위치를 app_dir 로 setting.

        :return current_dir if pytest called or main.py script dir.
        """
        if app_dir:
            AppInfo.__app_dir = app_dir
        # app_dir 이 저장되어 있으면, 저장값 리턴
        # sys.argv[0] --> python script 를 싫행한 main.py 를 출력.
        elif AppInfo.__app_dir:
            return AppInfo.__app_dir
        elif sys.argv[0].endswith('pytest'):
            return self.current_dir()
        else:
            return os.path.abspath(os.path.dirname(sys.argv[0]))

    @staticmethod
    def app_full_name(app_fullname=None):
        """
        application name from argv[0]

        :param app_fullname:
        :return:
        """
        if app_fullname:
            AppInfo.__app_fullname = app_fullname
        elif AppInfo.__app_fullname:
            return AppInfo.__app_fullname
        else:
            return os.path.basename(sys.argv[0])

    def app_name(self):
        """
        application name from argv[0]
        ex) app.py -> app 추출
        :return: app_name by app_full_name
        """
        return self.app_full_name().split(".")[0]  # app.py -> app 추출


def host_name():
    """
    실행되는 host name 호출
    :return: socket.gethostname()
    """
    return socket.gethostname()


def to_list(obj):
    """
    str or list convert to list
    """
    if isinstance(obj, list):
        return obj
    elif obj is None:
        return []
    else:
        return [obj]


def delete_none(_dict):
    """
    dict 내부에서 value 가 None 인 것들은 key 를 제거
    :param _dict:
    :return: None 인 것들이 제거된 dict
    """
    if isinstance(_dict, dict):
        for key, value in list(_dict.items()):
            if isinstance(value, list):
                delete_none(value)
            elif value is None:
                _dict.pop(key)

        return _dict
    else:
        return {}


class dict2obj(dict):
    """
    다중 딕셔너리를 지원하는 object
    a = dict2obj()
    a.addkey('bb').addkey('cc')['dddd'] = 1
    a.addkey('bb').addkey('ccc').dddd = 1
    """
    def __init__(self, dict_=None):
        if dict_ is None:
            dict_ = {}
        super(dict2obj, self).__init__(dict_)
        for key in self:
            item = self[key]
            if isinstance(item, list):
                for idx, it in enumerate(item):
                    item[idx] = dict2obj(it)
            elif isinstance(item, dict):
                self[key] = dict2obj(item)

    def addkey(self, key):
        if key not in self:
            self.__setattr__(key, dict2obj())

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def merge(self, dict_):
        """
        dict 를 merge 하는 함수.
        - 기존에 없는 key-value 는 추가
        - 기존에 존재하는 key 는 value 를 새로 업데이트
        - value 가 list 인 경우는 기존 리스트 대체
          리스트의 값들 중, dict 인 값이 있으면 주의해야 함
        """
        self = _add_update_obj(self, dict_)


def _add_update_obj(dict_org, dict_):

    if isinstance(dict_, dict):
        for key in dict_:
            if key in dict_org:
                item = dict_[key]
                if isinstance(item, dict):
                    dict_org[key] = _add_update_obj(dict_org[item], item)
                else:
                    dict_org[key] = item
    return dict_org












def daemonize(func, *args, **kwargs):
    """
    daemon 생성기
    subprocess 생성 후, 입력받은 func 을 args, kwargs 를 입력받아 실행
    - 표준 입출력
    """
    try:
        # fork. --> 자식 프로세스를 만들기 위해 사용되는 프로세스 생성기.
        pid = os.fork()
        if pid > 0:  # 자식 프로세스를 생성한 부모 프로세스에서 코드가 실행되는 경우, pid > 0. --> 프로세스 종료
            logger.logc(INFO, f"forked to background run | PID = {pid}")
            sys.exit()  # --> process 종료
    except OSError as error:
        logger.logc(ERROR, f"Unable to fork. Error: {error.errno} ({error.strerror})")
        sys.exit()
    os.setsid()  # 새로운 세션을 생성

    sys.stdout.flush()
    sys.stderr.flush()

    # /dev/null: NULL 장치라 불리는 부분으로, 여기에 쓰여진 모든 값들을 버리지만
    #            OS 에서는 작업에

    si = open(os.devnull, 'r')   # r:  읽기 모드
    so = open(os.devnull, 'a+')  # a+: 읽기 또는 파일 추가모드. 파일이 없으면 만듬
    se = open(os.devnull, "a+")  # a+: 읽기 또는 파일 추가모드. 파일이 없으면 만듬

    # redirect stdout and stderr to the log file opened above
    # 표준 입출력 --> 파일 입출력으로 변경하기 위한 작업 수행

    # dup2 --> 열려진 file descriptor 를 다른 file descriptor 로 복사.
    #      --> 이를 통해 파일의 입출력의 방향을 변경할 수 있음
    # 일반적으로 알려진 file descriptor 로는 표준 입력(0), 표준 출력(1), 표준 오류(2) 가 있음
    # dup2 로 복사를 하면, 표준 입출력은 화면 입출력이 아닌 파일 입출력으로 바뀌게 됨.

    os.dup2(si.fileno(), sys.stdin.fileno())   # 표준 입력 -> si
    os.dup2(so.fileno(), sys.stdout.fileno())  # 표준 출력 -> so
    os.dup2(se.fileno(), sys.stderr.fileno())  # 오류 메세지 출력 -> se

    func(*args, **kwargs)


def pid_exists(pid):
    """
    check for the existence of unix pid.
    :param pid: process id
    :return:
      - True: process kill success
      - False: process not exists or OSError.
    """
    if pid == 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True



