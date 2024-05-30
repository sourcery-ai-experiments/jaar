def get_test_real_id():
    return "music_45"


def get_test_reals_dir():
    return "src/real/examples/reals"


def get_changes_folder() -> str:
    return "changes"


def init_change_id() -> int:
    return 0


def get_init_change_id_if_None(x_change_id: int = None) -> int:
    return init_change_id() if x_change_id is None else x_change_id


def get_json_filename(filename_without_extention) -> str:
    return f"{filename_without_extention}.json"


def duty_str() -> str:
    return "duty"


def work_str() -> str:
    return "work"


def get_rootpart_of_econ_dir() -> str:
    return "idearoot"
