import os, signal, time
from ai_model_app import create_app
from libs.util.common import AppInfo, daemonize, pid_exists
# from libs.util.config import config
# from libs.util.io import readFile, writeFile, removeFile

from libs.util.logger import getLogger, INFO, MORE, DETAIL, ERROR
logger = getLogger()



