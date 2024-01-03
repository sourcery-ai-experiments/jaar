from json import loads as json_loads, dumps as json_dumps


def get_empty_dict_if_none(x_dict: dict) -> dict:
    return {} if x_dict is None else x_dict


def return1ifnone(x_obj):
    return 1 if x_obj is None else x_obj


# class XFunc:
def x_is_json(json_x: str) -> bool:
    try:
        json_loads(json_x)
    except ValueError as e:
        return False
    return True


def x_get_json(dict_x: dict) -> str:
    return json_dumps(obj=dict_x)


def x_get_dict(json_x: str) -> dict:
    return json_loads(json_x)
