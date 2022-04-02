import importlib
import os, sys
from argparse import ArgumentParser

from libs.util.gitInfo.git_info import get_git_info
from libs.util.io import read_file
from libs.util.common import AppInfo, host_name, dict2obj, delete_none
from libs.util.logger import create_logger, INFO, MORE, DETAIL, WARNING, ERROR, set_logging_level

app_info = AppInfo(app_dir=os.getcwd())

base_dir = app_info.app_dir()
app_name = app_info.app_name()
host_name_str = host_name()
default_prop_dir = os.path.join(base_dir, 'default_properties')  # 공통
default_conn_prop_file = os.path.join(default_prop_dir, "conn_properties.yaml")
default_app_prop_file = os.path.join(default_prop_dir, "app_properties.yaml")
default_app_args_file = os.path.join(default_prop_dir, "args_properties.yaml")

# prop_dir = os.path.join(base_dir, 'default_properties') # 개별 테스트 시
prop_dir = base_dir
conn_prop_file = os.path.join(prop_dir, "conn_properties.yaml")
app_prop_file = os.path.join(prop_dir, "app_properties.yaml")
app_args_file = os.path.join(prop_dir, "args_properties.yaml")

log_dir = os.path.join(base_dir, 'logs')
log_file = os.path.join(log_dir, f'{app_name}.log')
logger = create_logger(log_file)

EXECUTE_ENV = os.getenv("EXECUTE_ENV", 'prod')  # 실행 조건. dev, test, prod
APP_RUN_ENV = os.getenv("APP_RUN_ENV", None)  # 실행 환경. pp, pt, kp, kt, cp, ct

app_run_env_list = ['pp', 'pt', 'kp', 'kt', 'cp', 'ct']

if not APP_RUN_ENV in app_run_env_list:
    print(f"환경변수에 실행환경이 정의되지 않았습니다. APP_RUN_ENV --> {APP_RUN_ENV}")


def load_yaml(config_file):
    """
        config_file 위치의 yaml file 을 dict2obj object 로 return

    :param config_file:
                app_properties.yaml,
                args_properties.yaml,
                conn_properties.yaml
    :return:
    """
    properties = dict2obj({})
    if os.path.exists(config_file):
        logger.logc(MORE, f"load | {config_file}")
        dic = read_file(config_file, data_type="yaml")
        if dic is not None:
            properties = dict2obj(dic)
        else:
            logger.logc(INFO, f"skipped load | '{config_file}' does not exists")
        logger.logc(DETAIL, f"return items = {properties}")
        return properties


def _extend_args_conf(args_parser: ArgumentParser, args_conf):
    """
        dict 타입 args 값을 argument 에 추가
    """
    for arg_conf in args_conf:
        arg = arg_conf['arg']
        del arg_conf['arg']
        args_parser.add_argument(*arg, **arg_conf)


def input_args_parser(git_info):
    # conflict_handler --> 충돌하는 선택 사항 해결 전략. 같은 옵션 문자열 존재시 예전 인자로 대체(resolve)
    # ex) parser.add_argument('-f', '--foo', help='old foo help')
    # ex) parser.add_argument('--foo', help="new foo help")
    args_parser = ArgumentParser(conflict_handler="resolve")

    # input default app args
    logger.logc(INFO, f"load {repr(default_app_args_file)}")
    args_conf = read_file(default_app_args_file, data_type="yaml")
    _extend_args_conf(args_parser, args_conf)

    # input default test args
    if os.path.exists(app_args_file):
        try:
            logger.logc(INFO, f"load {repr(app_args_file)}")
            args_conf = read_file(app_args_file, data_type="yaml")
            _extend_args_conf(args_parser, args_conf)
        except Exception as e:
            if e.__class__.__name__ != "TypeError":
                logger.logc(WARNING, f"{repr(app_args_file)} | {e.__class__.__name__} | {e}")

    logger.logc(DETAIL, f"loaded items = {dict2obj(vars(args_parser.parse_known_args()[0]))}")
    args_parser.add_argument('--version', action='version', version=git_info.get("tagId"))  # git tagId 추출(version)

    args = dict2obj(vars(args_parser.parse_known_args()[0]))

    return args


class DefaultConfig(object):
    logger.log(INFO, "load default config ")
    GIT_INFO = get_git_info(base_dir)
    logger.log(INFO, f"application git info = {GIT_INFO}")

    # SECRET_KEY
    SECRET_KEY = os.getenv("SECRET_KEY", "ai_model_secret_key")

    # 기본 설정 가져오기
    __ALL_CONN_INFO_TMP = load_yaml(default_conn_prop_file)

    # 사용자 설정 가져오기
    __ALL_CONN_INFO_TMP.merge(load_yaml(conn_prop_file))

    ALL_CONN_INFO = __ALL_CONN_INFO_TMP['ai_conn_infos']
    logger.logc(DETAIL, f"ALL_CONN_INFO --> {repr(ALL_CONN_INFO)}")

    # app 설정 파일 로딩
    APP_PROPERTIES = load_yaml(default_app_prop_file)
    APP_PROPERTIES.merge(app_prop_file)

    # pytest 실행시, input_args_parser 미실행
    if sys.argv[0].endswith("pytest"):
        ARGS = dict2obj({})
    else:
        ARGS = input_args_parser(git_info=GIT_INFO)
        APP_PROPERTIES.merge(delete_none(ARGS))

    set_logging_level(logging_level=APP_PROPERTIES.logging_level)

    # os env 에 정보가 없으면 app 설정에서 읽음
    # app 설정에도 없으면 error 발생
    if APP_RUN_ENV not in ('pp', 'pt', 'kp', 'kt', 'cp', 'ct'):
        APP_RUN_ENV = APP_PROPERTIES.get("app_run_env", None)

    APP_PROPERTIES['app_run_env'] = APP_RUN_ENV
    APP_CONN_INFO = ALL_CONN_INFO[APP_RUN_ENV]

    logger.logc(MORE, f"conn properties --> {ALL_CONN_INFO}")
    logger.logc(MORE, f"app_args --> {ARGS}")
    logger.logc(MORE, f"app properties -->  {APP_PROPERTIES}")


class DevelopmentConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, "app_dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(DefaultConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, "app_test.db")
    PRESERVER_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(DefaultConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, "app_prod.db")
    SERVER_PORT = 7090


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

config = config_by_name[EXECUTE_ENV]  # 실행환경 기준의 config 값







