import os, signal, time
from ai_model_app import create_app
from libs.util.common import AppInfo, daemonize, pid_exists
from libs.util.config import config
from libs.util.io import read_file, write_file, remove_file

from libs.util.logger import getLogger, INFO, MORE, DETAIL, ERROR
logger = getLogger()

appInfo = AppInfo()


def launcher(app_name, pid_file):
    """
        app start !
    """
    my_pid = os.getpid()

    write_file(pid_file, str(my_pid))  # pid 파일 생성
    app = create_app(app_name, config)
    app.config["JSON_SORT_KEYS"] = False
    logger.logc(DETAIL, app.config)

    port = app.config["APP_PROPERTIES"]["server_port"]
    debug_flag = app.config["APP_PROPERTIES"]['debug']
    execute_env = app.config["APP_PROPERTIES"]["execute_env"]
    prod_threads = app.config["APP_PROPERTIES"]["prod_threads"]

    logger.logc(INFO, f"start {app_name}, execute_env = {execute_env}")

    if execute_env == "prod":
        from waitress import serve
        serve(app, host="0.0.0.0", port=port, threads=prod_threads)
    else:
        app.run(host="0.0.0.0", port=port, debug=debug_flag)
    remove_file(pid_file)
    logger.logc(INFO, f"end {app_name}")


def starter(app_name):
    """
        pid 기반 시작, 재시작, 정지, foreground, background 실행 가능
    """
    os.chdir(appInfo.app_dir())
    pid_file = os.sep.join((appInfo.app_dir(), f"{app_name}.pid"))
    logger.log(MORE, f"pid file --> {pid_file}")
    my_pid = os.getpid()

    if os.path.exists(pid_file):
        old_pid = int(read_file(pid_file).strip())
        if not pid_exists(old_pid):  # 프로세스가 없으면 pid 파일 삭제
            os.remove(pid_file)
            old_pid = None
    else:
        old_pid = None

    run = config.APP_PROPERTIES.run

    if old_pid:
        if run in ['restart', 'stop']:
            os.kill(old_pid, signal.SIGINT)
            wait_count = 50

            while wait_count:
                time.sleep(0.1)
                if pid_exists(old_pid):
                    wait_count -= 1
                    if not wait_count: # 5초가 지난 경우..
                        logger.logc(INFO, f"{app_name}({old_pid}) is still running ..")
                        exit()
                else:
                    break

            remove_file(pid_file)  # pid 파일 삭제
            logger.logc(INFO, f"{app_name} stop (pid = {old_pid})")
        elif not config.APP_PROPERTIES.debug:
            logger.logc(INFO, f"{app_name}({old_pid}) already executed ..Exit")
            exit()
        else:
            logger.logc(INFO, f"{app_name}({old_pid} does not executed ...)")

        if run == 'stop':
            exit()
        if run == 'restart':
            logger.logc(INFO, f"{app_name}({old_pid} --> {my_pid} restart")
        else:
            logger.logc(INFO, f"{app_name}({my_pid} start | pid_file = {pid_file}")

        if config.APP_PROPERTIES.run_mode.lower() == 'background':
            daemonize(launcher, app_name, pid_file)
        else:
            launcher(app_name, pid_file)


def check_confirmed():
    """
        configuration check.
        --> yes, y 입력시 실행, 그렇지 않으면 종료
    """
    if not config.APP_PROPERTIES.without_confirmed:
        print(f" ---- application config ---- \n {config.APP_PROPERTIES}")
        key_in = input("Enter yes to run with this setting")
        if key_in is not 'yes' and key_in is not 'y':
            print(f"input {key_in} exit! bye~")
            exit()
    else:
        print("wait for 3sec ... if you want stop press (ctrl + c)")
        time.sleep(3)


def main():
    try:
        if config.APP_PROPERTIES.run != 'stop':
            check_confirmed()

        starter(appInfo.app_name())
    except Exception as e:
        print(f"{e.__class__.__name__} | {e}")
        print(f"{appInfo.app_name()} does not exists. Exit \n")













