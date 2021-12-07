## flask 기반 모델 실행을 위한 script example
import time
import sys, os
import pandas as pd
import glob             # 해당 디렉토리 내 file list return
import pickle
import psutil           # 컴퓨터 CPU, 메모리, 하드디스크 정보를 위한 library
import psycopg2         # PostgreSQL library
import cx_Oracle        # oracle DB 연동을 위한 library
import json
import collections      #
import jaydebeapi as jp  # oracle, sqllite 를 위한 DB Connection library
import jpype             # Python 에서 JVM 을 띄운 뒤, 서로 통신을 라이브러리
from pandas.io.json import json_normalize # JSON data -> pandas dataFrame
from flask import Flask, render_template, request
from utils.flaskUtil import setting_log, get_working_path, get_X_test_from_DB, \
    make_response_json, preload_model, mk_temp_list
import joblib

init_done = False
app = Flask(__name__)

print(os.getcwd())

# row, col 생략 없이 출력

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

logger_n = setting_log()
working_path = os.getcwd()
model_id = 'K420004H'
model_full_path = os.path.join(working_path, 'mod/prodmod')
model_name_list = glob.glob(model_full_path + '/*.pkl')
for model_name in model_name_list:
    globals()[model_name.split("/")[-1].split(".")[0]] = joblib.load(model_name)

print(globals().keys())

logger_n.info("\n\n ====== hotRollMaterial ===== ")
start_time = time.time()
flask_cwd = os.getcwd()

pre_dir = "pre"
post_dir = "post"
utils_dir = "utils"

content = request.get_json()
print(content)

mgmt_id = content['model_id'][0]
working_path = "./"

request_json = eval(content['jsondata'][0])
dict_model_info = request_json['modelInfo']  # modelId, version
dict_req_info = request_json['reqInfo']      # respTp, serverUrl, topic, queryParam,reqId
dict_inputData = request_json['inputData']


