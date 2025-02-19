from src.econ.econ import econunit_shop, EconUnit
from src.econ.examples.econ_env_kit import (
    get_temp_env_world_id,
    get_test_econ_dir,
    env_dir_setup_cleanup,
)
from src.instrument.sqlite import get_db_tables, get_db_columns
from src.instrument.file import open_file
from src.instrument.python import get_nested_value, get_dict_from_json


def check_table_column_existence(tables_dict: dict, x_econ: EconUnit) -> bool:
    with x_econ.get_treasury_conn() as treasury_conn:
        db_tables = get_db_tables(treasury_conn)
        db_tables_columns = get_db_columns(treasury_conn)

    for table_name, table_dict in tables_dict.items():
        print(f"Table: {table_name}")
        if db_tables.get(table_name) is None:
            return False

        db_columns = set(db_tables_columns.get(table_name).keys())
        config_columns = set(table_dict.get("columns").keys())
        diff_columns = db_columns.symmetric_difference(config_columns)
        print(f"Table: {table_name} Column differences: {diff_columns}")

        if diff_columns:
            return False

    return True


def test_EconUnit_set_econ_dirs_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # GIVEN create econ
    x_econ = econunit_shop(get_temp_env_world_id(), get_test_econ_dir())

    # WHEN
    x_econ.set_econ_dirs(in_memory_treasury=True)

    # THEN
    # grab config.json
    config_text = open_file(dest_dir="src/econ", file_name="treasury_db_config.json")
    config_dict = get_dict_from_json(config_text)
    tables_dict = get_nested_value(config_dict, ["tables"])

    assert check_table_column_existence(tables_dict, x_econ)
