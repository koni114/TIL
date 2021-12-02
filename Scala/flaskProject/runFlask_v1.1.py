# 2021-12-01.py
# Flask script

import time
import sys, os
import traceback

import pandas as pd
import glob
import pickle
import psutil     # 파이썬을 위해 실행 중인 프로세스 및 시스템 리소스
import psycopg2   # Python 과 PostgreSQL 을 연결
import cx_Oracle  # Oracle.. 등
import json
import collections
import jaydebeapi   # jdbc Database 접근
from pandas.io.json import json_normalize
from flask import Flask, render_template, request
from utils.flaskUtil import get_working_path, get_X_test_from_DB, make_response_json

init_done = False
app = Flask(__name__)


@app.route("/hotRollMaterial", methods=['POST', 'GET'])
def hotRollMaterial():

    logger_n.info(' ===== hotRollMaterial ===== ')
    start_time = time.time()
    flask_cwd = os.getcwd()

    try:
        content = request.get_json()
        print(content)
        logger_n.debug(f"Passed Argument : {str(content.keys())}")

        # (1) 모델 경로 호출(working_path)
        mgmt_id = content['model_id'][0]
        working_path = get_working_path(mgmt_id) # return working_path

        logger_n.debug(f"mgmt_id : {mgmt_id}, working_path: {working_path}")

        # (2) Handling Request JSON
        request_json = eval(content['jsonData'][0])
        dict_modelInfo = request_json['modelInfo']   # modelId, version
        dict_reqInfo = request_json['reqInfo']       # respTp, serverUrl, topic, queryParam, reqId
        dict_inputData = request_json['inputData']   # {'df1': df, 'df2': df}

        # (3) 사용자 Script 넘겨질 args dict
        df_dict = {'model_id': mgmt_id,
                   'working_path': working_path,
                   'bind_var': dict_reqInfo['queryParam'],
                   'data': {}}

        # (4) Handling queryParam : 해석계를 쿼리
        bind_var_value = dict_reqInfo['queryParam']
        if len(bind_var_value) > 0:
            logger_n.debug('Passed queryParam :' + str(bind_var_value))
            sql_df_dict = get_X_test_from_DB(mgmt_id, bind_var_value)

            for k, v in sql_df_dict.items():
                logger_n.debug(f'%s.shape : {k}, {str(v.shape)}')

            df_dict['data'].update(sql_df_dict) # dict 에 key-value 형태 값 updates

        # (5) Handling inputData : inputData 를 {DF, DF, ...}로
        if len(dict_inputData) > 0:
            logger_n.debug('Passed inputData keys() :' + str(dict_inputData.keys()))
            df_dict['data'].update(dict_inputData)

        sys.path.append(working_path) # 경로 이름을 추가할 수 있으며, 해당 디렉터리에 있는 파이썬 모듈 사용 가능
        os.chdir(working_path)
        logger_n.debug('CWD has been changed.')

        # (6) 전처리 스크립트를 불러와서 실행
        pre = "pre"
        if os.path.join(working_path, pre, 'preprocessCustom.py') in glob.glob(os.path.join(working_path, pre) + '/*.py'):
            import pre.preprocessCustom
            logger_n.debug('----- preprocessCustom -----')
            df_dict = preprocessCustom.preprocessCustom(df_dict)






    except Exception as e:
        err_msg = traceback.format_exc()
        logger_n.info(err_msg)
        dict_rtn = {'Error': err_msg}


def hello_world():
    return 'Hello_World!'


def preload_hotRollMaterial():
    '''
    모델 preload function
    '''

    pass


def setting_log():
    import logging
    import logging.handlers
    flask_log = logging.getLogger('runFlask_v1.1')
    form_matter = logging.Formatter('%(asctime)s:%(module)s:%(levelname)s:%(message)s', '%Y-%m-%d %H:%M:%S')
    file_max_byte = 1024 * 1024 * 10
    log_file_name = os.path.join('/Users/heojaehun/gitRepo/TIL/Scala/flaskProject/log/runFlask_1.1.log')

    file_handler = logging.handlers.RotatingFileHandler(filename=log_file_name,
                                                        maxBytes=file_max_byte,
                                                        backupCount=5)

    file_handler.setFormatter(form_matter)
    flask_log.addHandler(file_handler)
    flask_log.setLevel(level=logging.DEBUG)
    return flask_log


if __name__ == '__main__':
    logger_n = setting_log()
    # preload_hotRollMaterial()
    app.run(host='0.0.0.0', port=8002, debug=True)




import os
os.getcwd()


