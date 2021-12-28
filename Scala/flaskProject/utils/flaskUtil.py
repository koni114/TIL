import os


def preload_model(working_path=os.getcwd(), model_id='k420004H', model_name='', model_type='S'):
    pass


def get_working_path(mgmt_id):
    pass


def get_X_test_from_DB(mgmt_id, bind_var_value):
    pass


def make_response_json(dict_rtn, dict_model_info, dict_req_info):
    pass


def preload_model():
    pass


def mk_temp_list():
    pass


def setting_log(path='.'):
    import logging
    import logging.handlers
    flask_log = logging.getLogger('runFlask_v1.1')
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
    file_max_byte = 1024 * 1024 * 10
    log_file_name = os.path.join(path, 'runFlask_1.1.log')

    file_handler = logging.handlers.RotatingFileHandler(filename=log_file_name, maxBytes=file_max_byte, backupCount=5)
    file_handler.setFormatter(formatter)
    flask_log.addHandler(file_handler)
    flask_log.setLevel(level=logging.DEBUG)
    return flask_log

