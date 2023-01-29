#!/usr/bin/env python
import os


def get_config_from_yaml(config_file_name: str="config.yaml") -> dict:
    """make dict type object from yaml file.
       Typically, user config.yam is under the 'PROJ_NAME/src' directory,
       and system config.yaml is under the PROJ_NAME directory.
       If the system yaml file exists,
       a config dict object that merges user and system yaml contents is created and returned.

    Args:
        config_file_name (str, optional): The name of the yaml file you want to convert into a config object
                                          Defaults to "config.yaml".

    Returns:
        _type_: dict
    """
    config = dict()
    user_config_file = os.path.join(get_src_home(), config_file_name)

    if os.path.isfile(user_config_file):
        config = read_file(file_name=user_config_file, data_type="yaml")

    system_config_file = os.path.join(os.path.sep.join(user_config_file.split(os.path.sep)[:-2]), config_file_name)

    if os.path.isfile(system_config_file):
        system_config = read_file(file_name=system_config_file, data_type="yaml")
        # merge user_config and system_config
        if isinstance(config, dict):
            config = add_update_dict(config, system_config)

    return config


def add_update_dict(dict_org: dict, _dict: dict) -> dict:
    """A function that updates '_dict' object to 'dict_org' dict object.
       - Add key-value that does not exist
       - The existing key is updated with a new value(**)
       - If value is a list, replace the existing list
    Args:
        dict_org (dict): standard dict
        _dict (dict): _  target dict

    Returns:
        dict: A dict object updated with two dict objects
    """
    if isinstance(_dict, dict):
        for key in _dict:
            if key in dict_org:
                item = _dict[key]
                if isinstance(item, dict):
                    dict_org[key] = add_update_dict(dict_org[key], item)
                else:
                    dict_org[key] = item
            else:
                dict_org[key] = _dict[key]
    return dict_org


def read_file(file_name: str, data_type: str="yaml") -> dict:
    """Read a file and return it in various formats
       format refers to the format of the input file.
       For example, string, JSON, YAML file formats
       Returns None if there is no file in that path.

    Args:
        file_name (str): The name of the file to read, and it must be a file name including full_path
        data_type (str, optional): Must be one of 'string', 'json', or 'yaml'

    Returns:
        dict: string or dictionary object
    """
    import json
    from decimal import Decimal

    import yaml

    if os.path.exists(file_name):
        with open(file_name, "r", encoding="UTF8") as f:
            if data_type == "yaml":
                return yaml.safe_load(f)
            elif data_type == "json":
                return json.loads(f.read(), parse_float=Decimal)
            elif data_type == "yaml":
                return yaml.safe_load(f)


def get_src_home() -> str:
    """A function that returns the location of the source where the function is executed

    Returns:
        str: location of the source where the function is executed
    """
    return os.path.dirname(os.path.realpath(__file__))


def set_env_minIO(conf: dict) -> None:
    """A function that sets the environment variables required for setting the minIO system.

    Args:
        conf (_type_): It is a config dict object,
                and minIO-related information must exist in a two-dimensional array in the corresponding dict.
                ex) conf['minIO']['aws_bucket_name']
    """
    for key, value in conf["minIO"].items():
        os.environ[key.upper()] = value

config = get_config_from_yaml()