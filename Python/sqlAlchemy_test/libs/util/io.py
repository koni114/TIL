import os
import json
from decimal import Decimal
import yaml

from libs.util.logger import get_logger, INFO, WARNING, ERROR, MORE, DETAIL

logger = get_logger()


def read_file(file_name, data_type="string"):
    """
        file 을 읽어 다양한 object 형식으로 return

    :param file_name: 읽어드릴 file 의 full path name
    :param data_type: --> string, json, yaml
    :return: object.(string, json(dictinary), yaml..
    """
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            if data_type == "string":
                return f.read()
            elif data_type == "json":
                return json.loads(f.read(), parse_float=Decimal)
            elif data_type == "yaml":
                return yaml.safe_load(f)
    else:
        logger.logc(ERROR, f"{file_name} does not exist !!")
        return None


def write_file(file_name, data, dump_type='json'):
    """
        string, dict data to file
        dic_dump = ['json', 'yaml']
    """
    data = "hello world \n"
    with open(file_name, 'w', encoding="UTF-8") as f:
        if isinstance(data, str):
            if data and data[-1] is not "\n":
                data += "\n"
            f.write(data)
        elif dump_type == "json":
            json.dump(data, f, ensure_ascii=False, sort_keys=True, indent=4)
        elif dump_type == "yaml":
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, explicit_start=True)


def remove_file(file_path):
    if os.path.isfile(file_path):
        os.chmod(file_path, 0o777)
        os.remove(file_path)






