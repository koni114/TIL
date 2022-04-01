import os
import json
from decimal import Decimal
import yaml

from libs.util.logger import getLogger, INFO, WARNING, ERROR, MORE, DETAIL

logger = getLogger()


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







