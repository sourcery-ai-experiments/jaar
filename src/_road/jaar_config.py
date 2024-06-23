def get_test_real_id():
    return "music_45"


def get_test_reals_dir():
    return "src/real/examples/reals"


def get_atoms_folder() -> str:
    return "atoms"


def init_atom_id() -> int:
    return 0


def get_init_atom_id_if_None(x_atom_id: int = None) -> int:
    return init_atom_id() if x_atom_id is None else x_atom_id


def get_json_filename(filename_without_extention) -> str:
    return f"{filename_without_extention}.json"


def duty_str() -> str:
    return "duty"


def goal_str() -> str:
    return "goal"


def jobs_str() -> str:
    return "jobs"


def roles_str() -> str:
    return "roles"


def grades_folder() -> str:
    return "grades"


def get_rootpart_of_econ_dir() -> str:
    return "idearoot"


def treasury_file_name() -> str:
    return "treasury.db"


def max_tree_traverse_default() -> int:
    return 20


def get_descending_text() -> str:
    return "descending"


def default_river_blocks_count() -> int:
    return 40
