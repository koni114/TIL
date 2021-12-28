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


@app.route("/hotRollMaterial", methods=['POST', 'GET'])
def hot_roll_material():
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
    mod_dir = 'mod'
    post_dir = "post"
    utils_dir = "utils"

    content = request.get_json()
    print(content)

    mgmt_id = content['model_id'][0]
    working_path = "./"

    # (2) Handling Request JSON
    request_json = eval(content['jsondata'][0])
    dict_model_info = request_json['modelInfo']  # modelId, version
    dict_req_info = request_json['reqInfo']      # respTp, serverUrl, topic, queryParam, reqId, transactionCode, resultTp
    dict_inputData = request_json['inputData']   # dict_inputData --> {'df1':df, 'df2':df, ...}

    # (3) 사용자 Script 에 넘겨질 args dict
    df_dict = {'model_id': mgmt_id,
               'working_path': working_path,
               'bind_var': dict_req_info['queryParam'],
               'data': {}}

    # (4) handling queryParam : 해석계 data 추출을 위한 쿼리 바인딩
    bind_var_value = dict_req_info['queryParam']             # dict
    if len(bind_var_value) > 0:
        logger_n.debug('Passed queryParam : ' + str(bind_var_value))  # bind_var_value 출력
        sql_df_dict = get_X_test_from_DB(mgmt_id, bind_var_value)
        for k, v in sql_df_dict.items():
            logger_n.debug(f"{k}.shape : {v.shape}")
        df_dict['data'].update(sql_df_dict)

    # (5) Handling inputData : inputData 를 (DF, DF, ...) 로
    if len(dict_inputData) > 0:
        logger_n.debug(f'Passed inputData.keys() : {str(dict_inputData.keys())}')
        df_dict['data'].update(dict_inputData)

    # (6) 모델 실행 directory 로 변경
    if os.path.join(working_path, pre_dir, 'preprocessing.py') in glob.glob(os.path.join(working_path, pre_dir) + '/*.py'):
        import pre.preprocessing
        logger_n.debug(" ===== preprocessing ===== ")
        df_dict = pre.preprocessing.preprocessing(df_dict)

    if os.path.join(working_path, mod_dir, 'model_load_and_predict.py') in glob.glob(os.path.join(working_path, pre_dir) + '/*.py'):
        import mod.model_load_and_predict
        logger_n.debug(" ===== model_load_and_predict ===== ")
        df_dict = mod.model_load_and_predict.model_load_and_predict(df_dict)

    if os.path.join(working_path, post_dir, 'postprocessing.py') in glob.glob(os.path.join(working_path, post_dir) + '/*.py'):
        import post.postprocessing
        logger_n.debug(" ===== postprocessing ===== ")
        df_dict = post.postprocessing.postprocessing(df_dict, dict_req_info)

    dict_rtn = {'Success': df_dict}
    os.chdir(flask_cwd)
    response_json = make_response_json(dict_rtn, dict_model_info, dict_req_info)
    process = psutil.Process(os.getpid())

    logger_n.info(f"   * elapsed %.3f {time.time()} - {start_time}")
    logger_n.info(f" VIRT: {process.memory_info().vms}, RES: {process.memory_info().rss}")

    # 리턴값 정리
    dumped = json.dumps(response_json, ensure_ascii=False)
    logger_n.debug("RETURN >>> \n" + dumped)

    return dumped


if __name__ == '__main__':
    logger_n = setting_log(os.getcwd())
    preload_model(working_path=os.getcwd(), model_id='k420004H',
                  model_name='', model_type='S')
    app.run(host='0.0.0.0', port=8002, debug=True)







