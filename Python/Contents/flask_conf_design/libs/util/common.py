import os, sys, threading, queue, copy, json, socket
from functools import wraps
from pytz import timezone
from .logger import getLogger, get_caller, INFO, WARNING, ERROR, MORE, DETAIL, DEBUG
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
        main python file's location
        * return current_dir if pytest called
        """
        if app_dir:
            AppInfo.__app_dir = app_dir
        # app_dir 이 저장되어 있으면, 저장값 리턴
        elif AppInfo.__app_dir:
            return AppInfo.__app_dir
        elif sys.argv[0].endswith('pytest'):
            return self.current_dir()
        else:
            return os.path.abspath(os.path.dirname(sys.argv[0]))

    def app_full_name(self, app_fullname=None):
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
        :return:
        """
        return self.app_full_name().split(".")[0]


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
    if isinstance(obj, list): return obj
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
    pass


def daemonize(func, *args, **kwargs):
    try:
        # fork. --> 자식 프로세스를 만들기 위해 사용되는 프로세스 생성기.
        #       -->
        pid = os.fork()
        if pid > 0:
            logger.logc(INFO, f"forked to background run | PID = {pid}")
            sys.exit()  # --> process 종료
    except OSError as error:
        logger.logc(ERROR, f"Unable to fork. Error: {error.errno} ({error.strerror})")
        sys.exit()
    os.setsid()

    sys.stdout.flush()
    sys.stderr.flush()

    # /dev/null: NULL 장치라 불리는 부분으로, 여기에 쓰여진 모든 값들을 버리지만
    #            OS 에서는 작업에

    si = open(os.devnull, 'r')
    so = open(os.devnull, 'a+')
    se = open(os.devnull, "a+")
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

    func(*args, **kwargs)







