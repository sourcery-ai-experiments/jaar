from json import loads as json_loads, dumps as json_dumps


def get_empty_dict_if_none(x_dict: dict) -> dict:
    return {} if x_dict is None else x_dict


def get_1_if_None(x_obj):
    return 1 if x_obj is None else x_obj


def get_0_if_None(x_obj=None):
    return 0 if x_obj is None else x_obj


def add_dict_if_missing(x_dict: dict, x_key: any):
    if x_dict.get(x_key) is None:
        x_dict[x_key] = {}


def x_is_json(json_x: str) -> bool:
    try:
        x_get_dict(json_x)
    except ValueError as e:
        return False
    return True


def x_get_json(dict_x: dict) -> str:
    return json_dumps(obj=dict_x)


def x_get_dict(json_x: str) -> dict[str:]:
    return json_loads(json_x)
